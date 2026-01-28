# Polylith New Brick

Create new Polylith bricks (components, bases) and projects following workspace conventions.

## Trigger

Use this skill when the user asks to:
- Create a new component or base
- Add a new project to the workspace
- Set up a new Polylith brick

## Prerequisites

Before creating any brick:
1. Confirm the **brick type**: component, base, or project
2. Confirm the **brick name** (e.g., `logging`, `data_processor`)

The namespace is defined in `workspace.toml` and used automatically by the CLI.

## Procedure: Creating Components or Bases

### Step 1: Create Brick with Polylith CLI

```bash
# Create a component
uv run poly create component --name {brick_name}

# Create a base
uv run poly create base --name {brick_name}
```

The CLI automatically:
- Creates directory at `components/{namespace}/{brick_name}/` or `bases/{namespace}/{brick_name}/`
- Adds `__init__.py` at brick level (NOT at namespace level - namespace packages don't need it)
- Creates `core.py` for implementation
- Registers brick in workspace root `pyproject.toml` under `[tool.polylith.bricks]`
- Creates test directory `test/components/{namespace}/{brick_name}/test_core.py` (when `[tool.polylith.test] enabled = true`)

### Step 2: Add Dependencies (If Needed)

If the brick needs new dependencies not in workspace root:

1. **Add to workspace root first:**
   ```bash
   uv add {package_name}
   ```

2. **Sync to install:**
   ```bash
   uv sync
   ```

### Step 3: Implement the Brick

Edit `{brick_type}s/{namespace}/{brick_name}/core.py` following Python code standards.

## Procedure: Creating Projects

### Step 1: Create Project with Polylith CLI

```bash
uv run poly create project --name {project_name}
```

### Step 2: Configure Project pyproject.toml

Edit `projects/{project_name}/pyproject.toml` following the template in [pyproject-templates.md](references/pyproject-templates.md).

Key requirements:
- `[build-system]` at the top
- No `readme` field (workspace root only)
- No `[dependency-groups]` (inherited from workspace)
- No `[tool.ruff]` or `[tool.pyright]` (workspace-wide config)
- Dependencies must be a **subset** of workspace root
- `[tool.polylith.bricks]` uses relative paths (`../../bases/...`, `../../components/...`)

### Step 3: Add Project-Specific Dependencies

Only add dependencies that are already in workspace root:
```toml
[project]
dependencies = [
    # Must be subset of workspace root dependencies
    "google-cloud-bigquery>=3.30.0",
]
```

If new dependency needed, add to workspace root first with `uv add`.

### Step 4: Sync and Verify

```bash
uv sync
uv run poly info
```

## Directory Structure Reference

See [directory-structure.md](references/directory-structure.md) for complete examples.

## pyproject.toml Templates

See [pyproject-templates.md](references/pyproject-templates.md) for workspace and project templates.

## Namespace Package Rule

- **Namespace level** (`{namespace}/`): NO `__init__.py` - Python auto-treats as namespace package
- **Brick level** (`{namespace}/logging/`): HAS `__init__.py` - created by Polylith CLI

## Code Sharing Principles

**Component-first Thinking**
- Prioritize creating new functionality as components
- Design components to be independent and reusable
- Ask: "Will another project need this?"

**Avoid Duplication**
- Actively seek to reuse existing components
- Don't copy-paste logic between projects
- Extract common patterns into shared components

**Clear Boundaries**
- Components should have well-defined responsibilities
- Minimize implicit dependencies between components
- Use explicit interfaces (function signatures, type hints)

## Quick Start Checklist

New component or base:
1. `uv run poly create component --name {name}` or `uv run poly create base --name {name}`
2. Add dependencies to workspace root if needed: `uv add {package}`
3. Implement in `core.py`
4. Write tests in `test/{brick_type}s/{namespace}/{name}/test_core.py`
5. Run `uv run pytest` to verify

New project:
1. `uv run poly create project --name {name}`
2. Edit `projects/{name}/pyproject.toml` (subset deps, relative brick paths)
3. Add deployment files (`Dockerfile`, `copy.sh`, or `main.py`)
4. Run `uv sync` to verify

## Common Mistakes to Avoid

- Adding `__init__.py` at namespace level
- Adding dependencies to project that aren't in workspace root
- Including `readme` field in project pyproject.toml
- Duplicating `[dependency-groups]` in project files
- Using absolute paths in project's `[tool.polylith.bricks]`
