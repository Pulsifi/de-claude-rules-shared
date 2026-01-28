# Directory Structure Reference

## Workspace Root Structure

```
workspace-root/
├── pyproject.toml          # Workspace-level config and all dependencies
├── uv.lock                 # Locked dependency versions
├── workspace.toml          # Polylith workspace metadata
├── bases/
│   └── {namespace}/        # Namespace directory (NO __init__.py)
│       ├── api_server/     # Base for API service
│       ├── cli_tool/       # Base for CLI application
│       └── data_processor/ # Base for data pipeline
├── components/
│   └── {namespace}/        # Namespace directory (NO __init__.py)
│       ├── logging/        # Logging component
│       ├── settings/       # Configuration component
│       └── gcp_bigquery/   # BigQuery operations
├── development/            # REPL-driven development, notebooks
│   └── {namespace}/
├── projects/
│   ├── api_service/        # Deployable API project
│   │   ├── pyproject.toml
│   │   ├── main.py         # Entry point shim
│   │   └── Dockerfile      # For containerized deployment
│   └── data_pipeline/      # Deployable pipeline project
│       ├── pyproject.toml
│       ├── main.py
│       └── copy.sh         # For Cloud Functions deployment
├── infrastructure/         # Infrastructure definitions (separate from app code)
│   ├── pyproject.toml      # Infrastructure dependencies (Pulumi, providers)
│   ├── cloudrun/           # Cloud Run Kustomize manifests
│   ├── cloudrunjob/        # Cloud Run Job Kustomize manifests
│   ├── cloudfunction/      # Cloud Function deployment configs
│   └── pulumi/             # Pulumi IaC stacks
└── test/                   # Tests at workspace root
    ├── conftest.py         # Workspace-wide pytest fixtures
    ├── components/         # Component tests mirror components/
    │   └── {namespace}/
    │       └── logging/
    │           └── test_core.py
    └── bases/              # Base tests mirror bases/
        └── {namespace}/
            └── api_server/
                └── test_core.py
```

## Component Directory

```
components/{namespace}/{component_name}/
├── __init__.py    # Created by Polylith CLI (makes it a package)
└── core.py        # Main implementation
```

## Base Directory

```
bases/{namespace}/{base_name}/
├── __init__.py    # Created by Polylith CLI (makes it a package)
└── core.py        # Entry point implementation
```

## Project Directory

```
projects/{project_name}/
├── pyproject.toml   # Project dependencies and brick references
├── main.py          # Entry point shim (optional)
├── copy.sh          # Deployment script (Cloud Functions)
└── Dockerfile       # Docker configuration (Cloud Run/containerized)
```

## Test Directory

```
test/
├── conftest.py              # Workspace-wide pytest fixtures
├── fixtures/                # Shared test data
├── components/
│   └── {namespace}/
│       └── {component_name}/
│           └── test_core.py  # Component unit tests
└── bases/
    └── {namespace}/
        └── {base_name}/
            └── test_core.py  # Base integration tests
```

## Namespace Package Rule

```
components/
└── data_integration/       # NO __init__.py (namespace package)
    └── logging/            # HAS __init__.py (regular package)
        ├── __init__.py
        └── core.py
```

Why this matters:
- Namespace packages (PEP 420) allow splitting a namespace across directories
- `from data_integration.logging.core import log_event` works because:
  - `data_integration` is a namespace package (no `__init__.py`)
  - `logging` is a regular package (has `__init__.py`)
