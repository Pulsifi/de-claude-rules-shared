---
name: pyproject-config
description: Configure pyproject.toml files for workspace root and projects. Use when creating pyproject.toml, configuring build system, setting up Polylith bricks, or understanding workspace vs project configuration.
allowed-tools: Read, Write, Edit, Glob
---

# pyproject.toml Configuration

Configure pyproject.toml files following project standards.

## Workspace vs Project Configuration

### Workspace Root ONLY

These sections appear ONLY in workspace root `pyproject.toml`:

```toml
# Workspace members
[tool.uv.workspace]
members = ["projects/*"]

# Dependency groups (inherited by projects)
[dependency-groups]
dev = ["ruff>=0.14.8", "pyright>=1.1.407"]
test = ["pytest>=9.0.2"]
release = ["pulumi>=3.213.0"]

# Default groups for local dev
[tool.uv]
default-groups = "all"

# Code quality tools
[tool.ruff]
line-length = 88
target-version = "py313"

[tool.pyright]
pythonVersion = "3.13"
typeCheckingMode = "standard"

# Hatch build config
[tool.hatch.build]
dev-mode-dirs = ["components", "bases", "development", "."]
```

### Both Workspace and Projects

```toml
# Build system (identical in both)
[build-system]
requires = ["hatchling", "hatch-polylith-bricks"]
build-backend = "hatchling.build"

# Project metadata (different content)
[project]
name = "project-name"
version = "1.0.0"
description = "Description"
requires-python = "~=3.13.0"

# Polylith bricks (different paths)
[tool.polylith.bricks]
```

### Projects NEVER Include

- `[tool.uv.workspace]`
- `[dependency-groups]`
- `[tool.uv]` default-groups
- `[tool.ruff]`
- `[tool.pyright]`
- `readme` field in `[project]`

## Templates

### Workspace Root pyproject.toml

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
    { name = "Data Engineering Team", email = "data_eng@pulsifi.me" }
]
dependencies = [
    # ALL runtime dependencies used by any project
    "Flask>=3.1.2",
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
]
release = [
    "pulumi>=3.213.0",
    "python-semantic-release==10.4.0",
]

[tool.hatch.build]
dev-mode-dirs = ["components", "bases", "development", "."]

[tool.hatch.build.targets.wheel]
packages = []

[tool.hatch.build.hooks.polylith-bricks]
enabled = true

[tool.polylith.bricks]
"bases/namespace/base_name" = "namespace/base_name"
"components/namespace/component_name" = "namespace/component_name"

[tool.uv]
default-groups = "all"

[tool.uv.workspace]
members = ["projects/*"]

[tool.ruff]
line-length = 88
target-version = "py313"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]

[tool.pyright]
pythonVersion = "3.13"
typeCheckingMode = "standard"
```

### Project pyproject.toml

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
    { name = "Data Engineering Team", email = "data_eng@pulsifi.me" }
]
dependencies = [
    # SUBSET of workspace root dependencies
    "Flask>=3.1.2",
    "google-cloud-logging>=3.13.0",
]

[tool.polylith.bricks]
"../../bases/namespace/base_name" = "namespace/base_name"
"../../components/namespace/component_name" = "namespace/component_name"
```

## Quick Reference Table

| Section | Workspace | Projects | Notes |
|---------|-----------|----------|-------|
| `[project]` | Required | Required | Different content |
| `[build-system]` | Required | Required | Identical |
| `[dependency-groups]` | Required | Never | Inherited |
| `[tool.uv.workspace]` | Required | Never | Defines workspace |
| `[tool.polylith.bricks]` | Required | Required | Different paths |
| `[tool.ruff]` | Required | Never | Workspace-wide |
| `readme` field | Yes | Never | Only in workspace |

## Common Mistakes

```toml
# WRONG - dependency not in workspace root
dependencies = ["new-package>=1.0.0"]  # Add to workspace first!

# WRONG - readme in project
readme = "README.md"  # Only in workspace root

# WRONG - dependency groups in project
[dependency-groups]
dev = ["ruff"]  # Inherited, don't duplicate

# WRONG - absolute brick paths in project
"bases/namespace/base" = "namespace/base"  # Use ../../
```

## Reference

See [03-dependencies.md](../../rules/03-dependencies.md#2-workspace-vs-project-configuration) for complete guidelines.
