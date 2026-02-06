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
└── overlays/              # Only create environments the project needs
    ├── sandbox/
    │   └── kustomization.yaml
    ├── staging/
    │   └── kustomization.yaml
    └── production/
        └── kustomization.yaml
```

## Procedure: Creating New Cloud Run Job

### Step 1: Create Dockerfile

Create `projects/{job_name}/Dockerfile`:

```dockerfile
FROM python:3.13-slim@sha256:{digest}

# Install uv from official image
COPY --from=ghcr.io/astral-sh/uv:0.7.8 /uv /uvx /usr/local/bin/

WORKDIR /app

# Copy project files for dependency resolution
COPY projects/{job_name}/pyproject.toml ./pyproject.toml
COPY uv.lock ./uv.lock

# Install dependencies
RUN uv sync --frozen --no-default-groups --no-install-project

# Copy Polylith bricks
COPY components/{namespace}/logging/ ./{namespace}/logging/
COPY components/{namespace}/settings/ ./{namespace}/settings/
COPY bases/{namespace}/{base_name}/ ./{namespace}/{base_name}/
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

### Step 4: Create Environment Overlays

Create overlays for each required environment. Common options are sandbox, staging, and production — not all projects need all three.

`infrastructure/cloudrunjob/{job_name}/overlays/{environment}/kustomization.yaml`:

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: data-{environment}-warehouse

resources:
  - ../../base

images:
  - name: IMAGE_URL
    newName: IMAGE_URL_PLACEHOLDER

patches:
  - patch: |-
      - op: add
        path: /spec/template/spec/template/spec/serviceAccountName
        value: {service_account}@data-{environment}-warehouse.iam.gserviceaccount.com
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

## Reference Files

- [dockerfile-template.md](references/dockerfile-template.md) - Full Dockerfile template
- [kustomize-patches.md](references/kustomize-patches.md) - Common Kustomize patches
