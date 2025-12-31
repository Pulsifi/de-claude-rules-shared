---
name: cloud-function-deploy
description: Set up Cloud Functions deployment with copy.sh scripts and main.py entry points. Use when deploying to Cloud Functions, creating copy.sh scripts, setting up serverless functions, or generating requirements.txt.
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Cloud Functions Deployment

Set up Google Cloud Functions deployment for Polylith projects.

## Required Files

For Cloud Functions deployment, projects need:

1. `pyproject.toml` - Project dependencies and brick references
2. `main.py` - Entry point shim
3. `copy.sh` - Script to copy Polylith bricks
4. `.gitignore` - Exclude generated files

## Templates

### copy.sh Script

```bash
#!/bin/bash

# Copy Polylith bricks to project directory for Cloud Functions deployment

# Define the namespace
namespace="{namespace}"

# Define the project name
project="{project_name}"

# Create namespace directory structure
mkdir -p ${namespace}

# Copy only the specific base this project needs
echo "Copying base: {base_name}..."
cp -r ../../bases/${namespace}/{base_name} ${namespace}/

# Copy only the components this project needs
echo "Copying component: logging..."
cp -r ../../components/${namespace}/logging ${namespace}/

echo "Copying component: settings..."
cp -r ../../components/${namespace}/settings ${namespace}/

echo "Polylith bricks copied successfully to projects/${project}/"
```

### main.py Entry Point Shim

```python
"""Cloud Function entry point for {service description}."""

from {namespace}.{base_name}.core import {function_name}

__all__ = ["{function_name}"]
```

### .gitignore

```gitignore
# Cloud Functions deployment artifacts
{namespace}/
requirements.txt
```

### pyproject.toml Dependencies

```toml
[project]
dependencies = [
    "functions-framework>=3.10.0",  # Required for Cloud Functions
    # ... other dependencies
]
```

## Generating requirements.txt

Use `uv export` with specific flags:

```bash
uv export --format requirements-txt --no-hashes --no-emit-project -o requirements.txt
```

**Flags:**
- `--format requirements-txt`: pip-compatible format
- `--no-hashes`: Cloud Functions doesn't need hash verification
- `--no-emit-project`: Exclude `-e .` editable install reference
- `-o requirements.txt`: Output file name

## Deployment Workflow

1. Run `copy.sh` to copy bricks into project directory
2. Run `uv export` to generate requirements.txt
3. Deploy with `gcloud functions deploy`

### Example CI/CD Steps

```yaml
- name: "Copy Polylith bricks"
  working-directory: projects/my_function
  run: ./copy.sh

- name: "Generate requirements.txt"
  working-directory: projects/my_function
  run: |
    uv export --format requirements-txt --no-hashes --no-emit-project -o requirements.txt

- name: "Deploy Cloud Function"
  run: |
    gcloud functions deploy my-function \
      --gen2 \
      --runtime python313 \
      --region asia-southeast1 \
      --source projects/my_function \
      --entry-point function_name \
      --trigger-http
```

## Key Principles

1. **Copy only required bricks** - Check project's `[tool.polylith.bricks]`
2. **Maintain namespace structure** - Keep `{namespace}/` directory layout
3. **Use --no-emit-project** - Prevent editable install errors
4. **Add generated files to .gitignore** - Don't commit `{namespace}/` or `requirements.txt`
5. **Keep shim simple** - Just import and re-export, no logic

## Troubleshooting

**"Module not found" error:**
- Ensure `copy.sh` was executed
- Verify namespace directory exists
- Check brick paths match imports

**"editable requirement" error:**
- Use `--no-emit-project` flag with `uv export`

## Reference

See [05-deployment.md](../../rules/05-deployment.md#2-cloud-functions-deployment) for complete guidelines.
