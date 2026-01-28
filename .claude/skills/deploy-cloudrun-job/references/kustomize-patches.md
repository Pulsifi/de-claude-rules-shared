# Common Kustomize Patches for Cloud Run Jobs

## Service Account

```yaml
patches:
  - patch: |-
      - op: add
        path: /spec/template/spec/template/spec/serviceAccountName
        value: my-sa@my-project.iam.gserviceaccount.com
    target:
      kind: Job
      name: my-job
```

## Secrets Annotation

Note: Use `~1` to escape `/` in annotation keys:

```yaml
patches:
  - patch: |-
      - op: add
        path: /spec/template/metadata/annotations/run.googleapis.com~1secrets
        value: "API_TOKEN:projects/my-project/secrets/MY_API_TOKEN"
    target:
      kind: Job
      name: my-job
```

## Environment Variables

```yaml
patches:
  - patch: |-
      - op: add
        path: /spec/template/spec/template/spec/containers/0/env/-
        value:
          name: ENVIRONMENT
          value: production
      - op: add
        path: /spec/template/spec/template/spec/containers/0/env/-
        value:
          name: VERSION
          value: VERSION_PLACEHOLDER
      - op: add
        path: /spec/template/spec/template/spec/containers/0/env/-
        value:
          name: GCP_PROJECT_ID
          value: my-project
    target:
      kind: Job
      name: my-job
```

## Secret as Environment Variable

```yaml
patches:
  - patch: |-
      - op: add
        path: /spec/template/spec/template/spec/containers/0/env/-
        value:
          name: API_TOKEN
          valueFrom:
            secretKeyRef:
              name: API_TOKEN
              key: latest
    target:
      kind: Job
      name: my-job
```

## Resource Limits

```yaml
patches:
  - patch: |-
      - op: replace
        path: /spec/template/spec/template/spec/containers/0/resources/limits/cpu
        value: "2"
      - op: replace
        path: /spec/template/spec/template/spec/containers/0/resources/limits/memory
        value: 1Gi
    target:
      kind: Job
      name: my-job
```

## JSON Patch Escaping

| Character | Escape |
|-----------|--------|
| `/` | `~1` |
| `~` | `~0` |

Example: `run.googleapis.com/secrets` → `run.googleapis.com~1secrets`

## Debugging

Preview final manifest:
```bash
cd infrastructure/cloudrunjob/my-job/overlays/production
kustomize build .
```
