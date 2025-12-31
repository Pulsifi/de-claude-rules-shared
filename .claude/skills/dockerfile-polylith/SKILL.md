---
name: dockerfile-polylith
description: Create Dockerfiles for Polylith projects with proper brick copying and uv setup. Use when containerizing applications, deploying to Cloud Run, ECS, Kubernetes, or creating Docker images.
allowed-tools: Read, Write, Edit, Glob
---

# Dockerfile for Polylith Projects

Create Dockerfiles for containerized Polylith deployments.

## Build Context

Docker builds execute from **workspace root** to access all bricks:

```bash
# From workspace root
docker build -f projects/my_app/Dockerfile -t my-app:latest .
```

## Standard Dockerfile Template

```dockerfile
FROM python:3.13-slim@sha256:a93b51c5acbd72f9d28fd811a230c67ed59bcd727ac08774dee4bbf64b7630c7

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends ca-certificates curl

# Install uv with specific version for reproducibility
ADD https://astral.sh/uv/0.7.8/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

# Copy project configuration and lock file (layer caching)
COPY projects/{project_name}/pyproject.toml ./
COPY uv.lock ./

# Install dependencies without installing the project itself
RUN uv sync --frozen --no-default-groups --no-install-project

# Copy only the Polylith bricks this project needs
COPY components/{namespace}/{component1} {namespace}/{component1}
COPY components/{namespace}/{component2} {namespace}/{component2}
COPY bases/{namespace}/{base_name} {namespace}/{base_name}

# Move base entry point to main.py
RUN mv {namespace}/{base_name}/core.py main.py

# Ensure virtual environment is in PATH
ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "main.py"]
```

## Multi-Stage Build Template

For smaller production images:

```dockerfile
# Build stage
FROM python:3.13-slim AS builder

ADD https://astral.sh/uv/0.7.8/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

COPY projects/{project_name}/pyproject.toml ./
COPY uv.lock ./

RUN uv sync --frozen --no-default-groups --no-install-project

# Runtime stage
FROM python:3.13-slim

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy Polylith bricks
COPY components/{namespace}/{component1} {namespace}/{component1}
COPY components/{namespace}/{component2} {namespace}/{component2}
COPY bases/{namespace}/{base_name} {namespace}/{base_name}

RUN mv {namespace}/{base_name}/core.py main.py

ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "main.py"]
```

## Key Principles

1. **Pin uv version** - Use exact version (0.7.8) for reproducibility
2. **Pin base image with digest** - Ensures exact image version
3. **Copy pyproject.toml first** - Leverage Docker layer caching
4. **Use --frozen flag** - Deterministic builds from lock file
5. **Use --no-default-groups** - Exclude dev/test dependencies
6. **Use --no-install-project** - We copy bricks manually
7. **Copy only needed bricks** - Check project's `[tool.polylith.bricks]`
8. **Maintain namespace structure** - Keep `{namespace}/` directory layout

## Flags Explained

```bash
uv sync --frozen --no-default-groups --no-install-project
```

- `--frozen`: Use exact versions from lock file
- `--no-default-groups`: Skip dev, test, release dependencies
- `--no-install-project`: Don't install project as editable package

## Troubleshooting

**"Module not found" error:**
- Verify COPY commands match brick references in pyproject.toml
- Check namespace directory structure in COPY commands
- Ensure COPY commands run from workspace root context

**Large image size:**
- Use multi-stage builds
- Use `--no-default-groups` flag
- Only copy required bricks

## Reference

See [05-deployment.md](../../rules/05-deployment.md#3-docker-container-deployment) for complete guidelines.
