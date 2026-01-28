# pyproject.toml Templates

## Workspace Root Template

```toml
[build-system]
requires = ["hatchling", "hatch-polylith-bricks"]
build-backend = "hatchling.build"

[project]
name = "workspace-name"
version = "1.0.0"
description = "Workspace description"
readme = "README.md"
requires-python = "~=3.13.0"
authors = [
    { name = "Data Engineering Team", email = "de-team@pulsifi.me" }
]
dependencies = [
    # ALL runtime dependencies used by any project
    "Flask>=3.1.2",
    "google-cloud-bigquery>=3.30.0",
    "google-cloud-logging>=3.13.0",
    "pydantic-settings>=2.12.0",
]

[dependency-groups]
dev = [
    "polylith-cli>=1.40.0",
    "pre-commit>=4.5.0",
    "pyright>=1.1.407",
    "ruff>=0.14.8",
]
test = [
    "pytest>=9.0.2",
    "pytest-cov>=7.0.0",
    "pytest-env>=1.2.0",
]
release = [
    "pulumi>=3.213.0",
    "pulumi-gcp>=9.6.0",
    "python-semantic-release==10.4.0",
]

[tool.hatch.build]
dev-mode-dirs = ["components", "bases", "development", "."]

[tool.hatch.build.targets.wheel]
packages = []

[tool.hatch.build.hooks.polylith-bricks]
enabled = true

[tool.hatch.metadata]
allow-direct-references = true

[tool.polylith.bricks]
# Bases
"bases/{namespace}/base_name" = "{namespace}/base_name"
# Components
"components/{namespace}/component_name" = "{namespace}/component_name"

[tool.uv]
default-groups = "all"

[tool.uv.workspace]
members = ["projects/*"]

[tool.ruff]
line-length = 88
target-version = "py313"

[tool.ruff.format]
quote-style = "double"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.pyright]
pythonVersion = "3.13"
typeCheckingMode = "standard"
include = [
    "bases",
    "components",
    "development",
    "projects",
]

[tool.pytest.ini_options]
addopts = "--tb=short -v"
testpaths = ["test"]
required_plugins = ["pytest-cov", "pytest-env"]
```

## Project Template

```toml
[build-system]
requires = ["hatchling", "hatch-polylith-bricks"]
build-backend = "hatchling.build"

[project]
name = "project-name"
version = "1.0.0"
description = "Project description"
requires-python = "~=3.13.0"
authors = [
    { name = "Data Engineering Team", email = "de-team@pulsifi.me" }
]
dependencies = [
    # SUBSET of workspace root dependencies only
    "google-cloud-bigquery>=3.30.0",
    "google-cloud-logging>=3.13.0",
]

[tool.polylith.bricks]
# Relative paths from project directory
"../../bases/{namespace}/base_name" = "{namespace}/base_name"
"../../components/{namespace}/component_name" = "{namespace}/component_name"
```

## Workspace vs Project Comparison

| Section                    | Workspace Root | Project Files |
| -------------------------- | -------------- | ------------- |
| `[build-system]`           | Required       | Required      |
| `[project]`                | Required       | Required      |
| `[project] readme`         | Required       | NEVER         |
| `[dependency-groups]`      | Required       | NEVER         |
| `[tool.uv.workspace]`      | Required       | NEVER         |
| `[tool.uv]`                | Required       | NEVER         |
| `[tool.ruff]`              | Required       | NEVER         |
| `[tool.pyright]`           | Required       | NEVER         |
| `[tool.hatch.build]`       | Required       | NEVER         |
| `[tool.polylith.bricks]`   | Required       | Required      |
| `[tool.pytest.ini_options]`| Required       | NEVER         |

## Critical Rules

### Subset Rule

Project dependencies MUST be a subset of workspace root dependencies:

```toml
# Workspace root - has ALL dependencies
dependencies = [
    "Flask>=3.1.2",
    "google-cloud-bigquery>=3.30.0",
    "google-cloud-logging>=3.13.0",
]

# Project - only what it needs (subset)
dependencies = [
    "google-cloud-bigquery>=3.30.0",
    # Flask not included - this project doesn't use it
]
```

If a project needs a new dependency, add to workspace root FIRST:
```bash
uv add {package_name}
```

### Brick Path Format

Workspace root uses paths from workspace root:
```toml
"components/{namespace}/logging" = "{namespace}/logging"
```

Projects use relative paths from project directory:
```toml
"../../components/{namespace}/logging" = "{namespace}/logging"
```
