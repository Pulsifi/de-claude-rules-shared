# Dockerfile Template for Cloud Run Jobs

## Standard Template

```dockerfile
FROM python:3.13-slim@sha256:{digest}

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends ca-certificates curl

# Install uv with pinned version
ADD https://astral.sh/uv/0.7.8/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

# Copy dependencies first for layer caching
COPY projects/{job_name}/pyproject.toml ./
COPY uv.lock ./

# Install dependencies without the project itself
RUN uv sync --frozen --no-default-groups --no-install-project

# Copy only the Polylith bricks this project needs
COPY components/{namespace}/logging {namespace}/logging
COPY components/{namespace}/settings {namespace}/settings
COPY components/{namespace}/gcp_bigquery {namespace}/gcp_bigquery
COPY bases/{namespace}/{base_name} {namespace}/{base_name}

# Set up entry point
RUN mv {namespace}/{base_name}/core.py main.py

# Ensure virtual environment is in PATH
ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "main.py"]
```

## Key Principles

1. **Pin base image with digest** - Reproducible builds
2. **Copy pyproject.toml and uv.lock first** - Docker layer caching
3. **Use `--no-install-project`** - We copy bricks manually
4. **Use `--no-default-groups`** - Exclude dev/test dependencies
5. **Copy only needed bricks** - Match project's `[tool.polylith.bricks]`
6. **Build from workspace root** - Access all bricks

## Build Command

Always run from workspace root:

```bash
docker build -f projects/{job_name}/Dockerfile -t {image} .
```

## Multi-stage Build (Optional)

For smaller images:

```dockerfile
# Build stage
FROM python:3.13-slim AS builder
ADD https://astral.sh/uv/0.7.8/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"
WORKDIR /app
COPY projects/{job_name}/pyproject.toml ./
COPY uv.lock ./
RUN uv sync --frozen --no-default-groups --no-install-project

# Runtime stage
FROM python:3.13-slim
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY components/{namespace}/... {namespace}/...
COPY bases/{namespace}/... {namespace}/...
RUN mv {namespace}/{base_name}/core.py main.py
ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "main.py"]
```
