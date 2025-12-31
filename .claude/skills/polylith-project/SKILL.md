---
name: polylith-project
description: Create a new deployable Polylith project with pyproject.toml, Dockerfile or copy.sh, and proper brick references. Use when setting up new microservices, Cloud Functions, Cloud Run services, or CLI applications.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Polylith Project Creator

Create new deployable Polylith projects following the project's architecture standards.

## What is a Project?

Projects are **deployable units** that:
- Combine bases and components into a complete application
- Have their own `pyproject.toml` with specific dependencies
- Include deployment configuration (Dockerfile, copy.sh)
- Reference only the bricks they actually need

## Instructions

When the user wants to create a new project:

1. **Gather information:**
   - Project name (lowercase with hyphens for pyproject.toml name)
   - Deployment target: Cloud Functions, Cloud Run/Docker, CLI
   - Which base(s) does it use?
   - Which components does it need?

2. **Create the project directory:**
   ```
   projects/{project_name}/
   ```

3. **Create pyproject.toml:**

   ```toml
   [build-system]
   requires = ["hatchling", "hatch-polylith-bricks"]
   build-backend = "hatchling.build"

   [project]
   name = "{project-name}"
   version = "1.0.0"
   description = "{Project description}"
   requires-python = "~=3.13.0"
   authors = [
       { name = "Data Engineering Team", email = "data_eng@pulsifi.me" }
   ]
   dependencies = [
       # Only include dependencies this project needs
       # MUST be subset of workspace root dependencies
   ]

   [tool.polylith.bricks]
   # Relative paths from project directory to bricks
   "../../bases/{namespace}/{base_name}" = "{namespace}/{base_name}"
   "../../components/{namespace}/{component_name}" = "{namespace}/{component_name}"
   ```

4. **Create deployment files based on target:**

## Cloud Functions Project

**Required files:**
- `pyproject.toml`
- `main.py` (entry point shim)
- `copy.sh` (brick copy script)

**main.py:**
```python
"""Cloud Function entry point for {description}."""

from {namespace}.{base_name}.core import {function_name}

__all__ = ["{function_name}"]
```

**copy.sh:**
```bash
#!/bin/bash

# Copy Polylith bricks to project directory for Cloud Functions deployment

namespace="{namespace}"
project="{project_name}"

mkdir -p ${namespace}

echo "Copying base: {base_name}..."
cp -r ../../bases/${namespace}/{base_name} ${namespace}/

echo "Copying component: {component_name}..."
cp -r ../../components/${namespace}/{component_name} ${namespace}/

echo "Polylith bricks copied successfully to projects/${project}/"
```

**.gitignore (add to project):**
```gitignore
# Cloud Functions deployment artifacts
{namespace}/
requirements.txt
```

## Docker/Cloud Run Project

**Required files:**
- `pyproject.toml`
- `Dockerfile`

**Dockerfile:**
```dockerfile
FROM python:3.13-slim

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends ca-certificates curl

# Install uv with specific version for reproducibility
ADD https://astral.sh/uv/0.7.8/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

# Copy project configuration and lock file
COPY projects/{project_name}/pyproject.toml ./
COPY uv.lock ./

# Install dependencies without installing the project itself
RUN uv sync --frozen --no-default-groups --no-install-project

# Copy only the Polylith bricks this project needs
COPY components/{namespace}/{component_name} {namespace}/{component_name}
COPY bases/{namespace}/{base_name} {namespace}/{base_name}

# Move base entry point to main.py
RUN mv {namespace}/{base_name}/core.py main.py

# Ensure virtual environment is in PATH
ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "main.py"]
```

## Key Rules (from 03-dependencies.md)

1. **Subset Rule (CRITICAL):** Project dependencies MUST be a subset of workspace root dependencies
2. **No readme field:** Only workspace root has `readme` field
3. **No dependency-groups:** Projects inherit from workspace
4. **No tool.uv:** Projects inherit from workspace
5. **Relative brick paths:** Use `../../` for brick paths

## Checklist After Creation

- [ ] Add base to workspace root `[tool.polylith.bricks]`
- [ ] Add components to workspace root `[tool.polylith.bricks]`
- [ ] Verify all dependencies exist in workspace root `pyproject.toml`
- [ ] Create infrastructure config if needed (e.g., `infrastructure/cloudrun/`)
- [ ] Update CI/CD workflows if needed

## Reference

See [01-setup.md](../../rules/01-setup.md#3-monorepo-structure-and-organization) for project structure.
See [03-dependencies.md](../../rules/03-dependencies.md) for dependency configuration.
See [05-deployment.md](../../rules/05-deployment.md) for deployment patterns.
