---
name: kustomize-cloudrun
description: Configure Cloud Run services with Kustomize base and overlays. Use when setting up Cloud Run deployments, managing environment-specific configs, or creating Kustomize manifests.
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Cloud Run Configuration with Kustomize

Configure Cloud Run services using Kustomize for environment management.

## Directory Structure

```
infrastructure/cloudrun/
├── base/
│   ├── service.yaml        # Base Cloud Run service definition
│   └── kustomization.yaml  # Base kustomization config
└── overlays/
    ├── sandbox/
    │   └── kustomization.yaml  # Sandbox-specific patches
    └── production/
        └── kustomization.yaml  # Production-specific patches
```

## Templates

### base/service.yaml

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: {service-name}
spec:
  template:
    metadata:
      labels:
        version: VERSION_PLACEHOLDER
    spec:
      serviceAccountName: {service-account}@{project-id}.iam.gserviceaccount.com
      containers:
      - name: {service-name}
        image: IMAGE_URL
        ports:
        - containerPort: 8080
        resources:
          limits:
            cpu: "1"
            memory: 2Gi
        env:
        - name: ENVIRONMENT
          value: "base"
        startupProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
          failureThreshold: 3
```

### base/kustomization.yaml

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - service.yaml
```

### overlays/sandbox/kustomization.yaml

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - ../../base

patches:
  - target:
      kind: Service
      name: {service-name}
    patch: |-
      - op: replace
        path: /spec/template/spec/containers/0/env
        value:
          - name: ENVIRONMENT
            value: sandbox
          - name: GCP_PROJECT_ID
            value: {project-id-sandbox}
```

### overlays/production/kustomization.yaml

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - ../../base

patches:
  - target:
      kind: Service
      name: {service-name}
    patch: |-
      - op: replace
        path: /spec/template/spec/containers/0/env
        value:
          - name: ENVIRONMENT
            value: production
          - name: GCP_PROJECT_ID
            value: {project-id-production}
      - op: replace
        path: /spec/template/spec/containers/0/resources/limits/cpu
        value: "2"
      - op: replace
        path: /spec/template/spec/containers/0/resources/limits/memory
        value: 4Gi
```

## Deployment Commands

```bash
# Update image reference
cd infrastructure/cloudrun/overlays/${ENVIRONMENT}
kustomize edit set image \
  IMAGE_URL=asia-southeast1-docker.pkg.dev/${PROJECT}/repo/${SERVICE}:${VERSION}

# Generate final manifest
kustomize build . | sed "s|VERSION_PLACEHOLDER|${VERSION}|g" > /tmp/service.yaml

# Deploy to Cloud Run
gcloud run services replace /tmp/service.yaml --region=asia-southeast1

# Make publicly accessible (if needed)
gcloud run services add-iam-policy-binding ${SERVICE} \
  --region=asia-southeast1 \
  --member=allUsers \
  --role=roles/run.invoker
```

## Preview Configuration

```bash
# Preview sandbox configuration
cd infrastructure/cloudrun/overlays/sandbox
kustomize build .

# Preview production configuration
cd infrastructure/cloudrun/overlays/production
kustomize build .
```

## Common Patterns

### Adding Environment Variables

```yaml
patches:
  - target:
      kind: Service
      name: my-service
    patch: |-
      - op: add
        path: /spec/template/spec/containers/0/env/-
        value:
          name: NEW_VAR
          value: "new-value"
```

### Updating Resource Limits

```yaml
patches:
  - target:
      kind: Service
      name: my-service
    patch: |-
      - op: replace
        path: /spec/template/spec/containers/0/resources/limits/cpu
        value: "4"
      - op: replace
        path: /spec/template/spec/containers/0/resources/limits/memory
        value: 8Gi
```

### Adding Secret Reference

```yaml
patches:
  - target:
      kind: Service
      name: my-service
    patch: |-
      - op: add
        path: /spec/template/spec/containers/0/env/-
        value:
          name: API_KEY
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: api-key
```

## Key Benefits

1. **Separation of Concerns** - App code vs service config
2. **Environment Management** - Base + overlays pattern
3. **Version Control** - All configs tracked in git
4. **Deployment Flexibility** - Build once, configure per environment

## Reference

See [05-deployment.md](../../rules/05-deployment.md#4-cloud-run-service-configuration-kustomize) for complete guidelines.
