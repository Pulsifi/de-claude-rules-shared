---
name: uv-dependency
description: Manage Python dependencies with uv package manager. Use when adding, removing, updating dependencies, syncing packages, or managing uv.lock file.
allowed-tools: Read, Write, Edit, Bash, Glob
---

# uv Dependency Management

Manage Python dependencies using uv package manager.

## Common Operations

### Adding Dependencies

```bash
# Add runtime dependency to workspace root
uv add <package_name>

# Add dependency to specific project
cd projects/my_service && uv add <package_name>

# Add development dependency
uv add <package_name> --group dev

# Add test dependency
uv add <package_name> --group test

# Add release dependency
uv add <package_name> --group release
```

### Removing Dependencies

```bash
# Remove runtime dependency
uv remove <package_name>

# Remove from specific project
cd projects/my_service && uv remove <package_name>

# Remove from dependency group
uv remove <package_name> --group dev
```

### Updating Dependencies

```bash
# Update all dependencies to latest compatible versions
uv lock --upgrade

# Update specific package
uv lock --upgrade-package <package_name>

# Install updated dependencies
uv sync
```

### Syncing Dependencies

```bash
# Local development (all groups)
uv sync

# CI/CD (frozen, deterministic)
uv sync --frozen

# Specific group only
uv sync --frozen --group release

# No default groups (minimal install)
uv sync --frozen --no-default-groups
```

## Key Rules

### Workspace-First Approach

1. **Add to workspace root first** - All dependencies go in root `pyproject.toml`
2. **Subset rule (CRITICAL)** - Project dependencies MUST be subset of workspace
3. **Never add new dependencies directly to projects** - Add to workspace first

### Version Constraints

- Use `>=` with locked versions from `uv.lock`
- Example: If lock has `google-cloud-pubsub==2.33.0`, use `>=2.33.0`

### Lock File Management

- **Always commit `uv.lock`** to version control
- **Use `--frozen` in CI/CD** to prevent lock file updates
- **Update deliberately** with `uv lock` or `uv lock --upgrade`

## Dependency Groups

Defined only in workspace root:

```toml
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
```

## Workflow: Adding a New Dependency

1. Add to workspace root: `uv add <package>`
2. Verify in `uv.lock`: Check resolved version
3. Update constraint: Use `>=` with locked version
4. Add to project: If project-specific, add same version to project `pyproject.toml`
5. Commit both files together

## Troubleshooting

**Lock file conflicts:**
- Use `uv sync --frozen` for daily work
- Only one person updates lock file at a time

**"Package not found" error:**
- Verify package name spelling
- Check if package exists on PyPI
- Try `uv add --index-url` for private packages

**Version conflicts:**
- Run `uv lock` to resolve
- Check for incompatible version constraints

## Reference

See [03-dependencies.md](../../rules/03-dependencies.md) for complete dependency management guidelines.
