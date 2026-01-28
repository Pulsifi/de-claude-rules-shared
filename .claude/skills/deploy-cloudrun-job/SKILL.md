# Deploy Cloud Run Job

Deploy containerized batch jobs to Cloud Run using Docker and Kustomize.

## Trigger

Use this skill when the user asks to:
- Deploy a Cloud Run Job
- Create a batch processing job
- Set up Kustomize for Cloud Run Job
- Create Dockerfile for Cloud Run Job

## Project Structure

```
projects/{job_name}/
├── pyproject.toml      # Dependencies and brick references
├── Dockerfile          # Container definition
└── main.py             # Entry point (optional)

infrastructure/cloudrunjob/{job_name}/
├── base/
│   ├── job.yaml           # Base job definition
│   └── kustomization.yaml
└── overlays/
    └── production/
        └── kustomization.yaml  # Production patches
```

## Procedure: Creating New Cloud Run Job

### Step 1: Create Dockerfile

Create `projects/{job_name}/Dockerfile`:

```dockerfile
FROM python:3.13-slim@sha256:{digest}

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends ca-certificates curl

# Install uv
ADD https://astral.sh/uv/0.7.8/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

# Copy dependencies first (layer caching)
COPY projects/{job_name}/pyproject.toml ./
COPY uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-default-groups --no-install-project

# Copy Polylith bricks
COPY components/{namespace}/logging {namespace}/logging
COPY components/{namespace}/settings {namespace}/settings
COPY bases/{namespace}/{base_name} {namespace}/{base_name}

# Set up entry point
RUN mv {namespace}/{base_name}/core.py main.py

ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "main.py"]
```

### Step 2: Create Base Job Manifest

Create `infrastructure/cloudrunjob/{job_name}/base/job.yaml`:

```yaml
apiVersion: run.googleapis.com/v1
kind: Job
metadata:
  name: {job_name}
  labels:
    component: data-pipeline
  annotations:
    run.googleapis.com/launch-stage: BETA
spec:
  template:
    metadata:
      annotations:
        run.googleapis.com/execution-environment: gen2
    spec:
      taskCount: 1
      template:
        spec:
          maxRetries: 3
          timeoutSeconds: 600
          containers:
          - name: worker
            image: IMAGE_URL
            env:
            - name: COMPONENT
              value: data-pipeline
            resources:
              limits:
                cpu: "1"
                memory: 512Mi
```

### Step 3: Create Base Kustomization

Create `infrastructure/cloudrunjob/{job_name}/base/kustomization.yaml`:

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - job.yaml
```

### Step 4: Create Production Overlay

Create `infrastructure/cloudrunjob/{job_name}/overlays/production/kustomization.yaml`:

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: {gcp_project_id}

resources:
  - ../../base

images:
  - name: IMAGE_URL
    newName: IMAGE_URL_PLACEHOLDER

patches:
  - patch: |-
      - op: add
        path: /spec/template/spec/template/spec/serviceAccountName
        value: {service_account}@{gcp_project_id}.iam.gserviceaccount.com
    target:
      kind: Job
      name: {job_name}
```

## Procedure: Deployment

### Step 1: Build and Push Image

```bash
docker build -f projects/{job_name}/Dockerfile -t {image_url}:{version} .
docker push {image_url}:{version}
```

### Step 2: Update Image in Kustomize

```bash
cd infrastructure/cloudrunjob/{job_name}/overlays/production
kustomize edit set image IMAGE_URL={image_url}:{version}
```

### Step 3: Build and Deploy Manifest

```bash
kustomize build . | sed "s|VERSION_PLACEHOLDER|{version}|g" > /tmp/job.yaml
gcloud run jobs replace /tmp/job.yaml --region=asia-southeast1
```

## Key Differences from Services

| Aspect | Cloud Run Job | Cloud Run Service |
|--------|---------------|-------------------|
| API Version | `run.googleapis.com/v1` | `serving.knative.dev/v1` |
| Kind | `Job` | `Service` |
| Use Case | Batch tasks | HTTP servers |
| Ports | None | Required |
| Health Probes | None | Required |
| Deploy Command | `gcloud run jobs replace` | `gcloud run services replace` |

## Reference Files

- [dockerfile-template.md](references/dockerfile-template.md) - Full Dockerfile template
- [kustomize-patches.md](references/kustomize-patches.md) - Common Kustomize patches
