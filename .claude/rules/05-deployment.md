# Deployment: Cloud Functions & Docker Patterns

**When to use this file:** Reference for deployment strategy decisions.

**Skills available:** Use `cloud-function-deploy`, `dockerfile-polylith`, or `kustomize-cloudrun` skills for templates and step-by-step guidance.

---

## 1. Deployment Strategy Decision Tree

### When to Use Each Strategy

| Strategy | Use When |
|----------|----------|
| **copy.sh + requirements.txt** | Deploying to Cloud Functions |
| **Dockerfile COPY** | Cloud Run, ECS, Kubernetes, Docker |
| **hatchling auto-assembly** | PyPI distribution, local development |

---

## 2. Cloud Functions Deployment

### Required Files

```
projects/{project_name}/
├── pyproject.toml    # Dependencies and brick references
├── main.py           # Entry point shim (committed)
├── copy.sh           # Brick copy script (committed)
└── .gitignore        # Exclude generated files
```

### Key Principles

1. **copy.sh copies bricks** before deployment
2. **main.py is a shim** that imports from base's `core.py`
3. **requirements.txt generated** with `uv export --no-emit-project`
4. **Add to .gitignore:** `{namespace}/` and `requirements.txt`

### Requirements.txt Generation

```bash
uv export --format requirements-txt --no-hashes --no-emit-project -o requirements.txt
```

**For templates, use the `cloud-function-deploy` skill.**

---

## 3. Docker Container Deployment

### Build Context

Docker builds execute from **workspace root**:

```bash
docker build -f projects/my_app/Dockerfile -t my-app:latest .
```

### Key Principles

1. **Pin uv version** (0.7.8) for reproducibility
2. **Copy pyproject.toml first** for layer caching
3. **Use `--frozen --no-default-groups --no-install-project`**
4. **Copy only needed bricks** from `components/` and `bases/`
5. **Maintain namespace structure** in COPY commands

**For templates, use the `dockerfile-polylith` skill.**

---

## 4. Cloud Run with Kustomize

### Directory Structure

```
infrastructure/cloudrun/
├── base/
│   ├── service.yaml
│   └── kustomization.yaml
└── overlays/
    ├── sandbox/
    │   └── kustomization.yaml
    └── production/
        └── kustomization.yaml
```

### Deployment Flow

1. Build and push Docker image
2. Update image reference: `kustomize edit set image`
3. Generate manifest: `kustomize build .`
4. Deploy: `gcloud run services replace`

**For templates, use the `kustomize-cloudrun` skill.**

---

## 5. Strategy Comparison

| Aspect | Cloud Functions | Docker |
|--------|----------------|--------|
| Brick copying | `copy.sh` script | Dockerfile COPY |
| Dependencies | `uv export` → requirements.txt | `uv sync --frozen` |
| Generated files | `{namespace}/`, `requirements.txt` | In image layers |
| .gitignore | Yes (exclude generated) | Not needed |

---

## 6. Best Practices

### For All Strategies

- Only copy bricks listed in project's `[tool.polylith.bricks]`
- Maintain namespace directory structure
- Pin uv version (0.7.8)
- Use `--frozen` flag for deterministic builds

### Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| "Module not found" in Cloud Functions | copy.sh not run | Run copy.sh before deployment |
| "Module not found" in Docker | Wrong COPY paths | Verify paths match brick references |
| Large deployment size | Too many dependencies | Use `--no-default-groups` |
| "editable requirement" error | Missing flag | Use `--no-emit-project` |
