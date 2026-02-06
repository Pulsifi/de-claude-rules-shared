# Dockerfile Template for Cloud Run Jobs

## Standard Template

```dockerfile
FROM python:3.13-slim@sha256:{digest}

# Install uv from official image
COPY --from=ghcr.io/astral-sh/uv:0.7.8 /uv /uvx /usr/local/bin/

WORKDIR /app

# Copy dependencies first for layer caching
COPY projects/{job_name}/pyproject.toml ./pyproject.toml
COPY uv.lock ./uv.lock

# Install dependencies without the project itself
RUN uv sync --frozen --no-default-groups --no-install-project

# Copy only the Polylith bricks this project needs
COPY components/{namespace}/logging/ ./{namespace}/logging/
COPY components/{namespace}/settings/ ./{namespace}/settings/
COPY bases/{namespace}/{base_name}/ ./{namespace}/{base_name}/

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
7. **Use trailing slashes on directory COPYs** - Ensures Docker treats destination as directory

## Build Command

Always run from workspace root:

```bash
docker build -f projects/{job_name}/Dockerfile -t {image} .
```
