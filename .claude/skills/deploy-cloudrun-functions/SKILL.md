# Deploy Cloud Run Functions

Deploy Polylith projects to Google Cloud Functions.

## Trigger

Use this skill when the user asks to:
- Deploy to Cloud Functions
- Set up a Cloud Function project
- Create copy.sh script for deployment
- Generate requirements.txt for Cloud Functions

## Project Structure

```
projects/{project_name}/
├── pyproject.toml      # Project dependencies and brick references
├── main.py             # Entry point shim (committed)
├── copy.sh             # Brick copy script (committed)
├── .gitignore          # Ignore generated files
├── {namespace}/        # Generated - copied bricks (NOT committed)
└── requirements.txt    # Generated - dependencies (NOT committed)
```

## Procedure: Setting Up New Cloud Function Project

### Step 1: Create Entry Point Shim

Create `main.py` that imports from the base:

```python
# projects/{project_name}/main.py
"""Cloud Function entry point for {service description}."""

from {namespace}.{base_name}.core import {function_name}

__all__ = ["{function_name}"]
```

**Example:**
```python
"""Cloud Function entry point for IP geolocation service."""

from asset.data_transformation.core import get_ip_geo_info

__all__ = ["get_ip_geo_info"]
```

### Step 2: Create copy.sh Script

Create script to copy Polylith bricks:

```bash
#!/bin/bash

# Copy Polylith bricks to project directory for Cloud Functions deployment

namespace="{namespace}"
project="{project_name}"

# Create namespace directory
mkdir -p ${namespace}

# Copy base
echo "Copying base: ${project}..."
cp -r ../../bases/${namespace}/${project} ${namespace}/

# Copy components (only what this project needs)
echo "Copying component: logging..."
cp -r ../../components/${namespace}/logging ${namespace}/

echo "Copying component: settings..."
cp -r ../../components/${namespace}/settings ${namespace}/

echo "Polylith bricks copied successfully to projects/${project}/"
```

### Step 3: Configure .gitignore

Add generated files to `.gitignore`:

```gitignore
# Cloud Functions deployment artifacts
{namespace}/
requirements.txt
```

### Step 4: Add Required Dependencies

Ensure `pyproject.toml` includes `functions-framework`:

```toml
[project]
dependencies = [
    "functions-framework>=3.10.0",
    # ... other dependencies
]
```

## Procedure: Deployment (CI/CD)

### Step 1: Copy Bricks

```bash
cd projects/{project_name}
./copy.sh
```

### Step 2: Generate requirements.txt

```bash
uv export --format requirements-txt --no-hashes --no-emit-project -o requirements.txt
```

**Flag explanations:**
- `--no-hashes`: Cloud Functions doesn't require hash verification
- `--no-emit-project`: Exclude `-e .` editable install reference

### Step 3: Deploy

```bash
gcloud functions deploy {function_name} \
  --gen2 \
  --runtime=python313 \
  --region=asia-southeast1 \
  --source=. \
  --entry-point={function_name} \
  --trigger-http
```

## Key Principles

- **Shim pattern**: `main.py` imports from base's `core.py`
- **Copy only needed bricks**: Match project's `[tool.polylith.bricks]`
- **Don't commit generated files**: `{namespace}/` and `requirements.txt`
- **Namespace structure preserved**: Copied bricks maintain import paths

## Troubleshooting

### "Module not found" error

- Verify `copy.sh` was executed
- Check namespace directory structure matches imports
- Ensure all required bricks are copied

### "editable requirement" error

Use correct `uv export` flags:
```bash
uv export --format requirements-txt --no-hashes --no-emit-project -o requirements.txt
```
