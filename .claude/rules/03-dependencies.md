# Dependencies: uv Package Management

**When to use this file:** Reference for dependency rules and constraints.

**Skills available:** Use `uv-dependency` or `pyproject-config` skills for commands and templates.

---

## 1. Critical Rules

### Subset Rule (MUST FOLLOW)

Project dependencies MUST be a **subset** of workspace root dependencies.

```
Workspace root: [Flask, requests, google-cloud-logging, ipinfo]
Project A:      [Flask, google-cloud-logging]           ✓ Valid (subset)
Project B:      [Flask, pandas]                         ✗ Invalid (pandas not in workspace)
```

**Workflow:**
1. Add new dependency to workspace root first
2. Then add to project's `pyproject.toml`

### Lock File Rules

- **Always commit `uv.lock`** to version control
- **Always use `--frozen` in CI/CD**: `uv sync --frozen`
- **Never update lock file in CI/CD**

### Version Constraints

- Use `>=` with locked versions from `uv.lock`
- Example: If lock has `google-cloud-pubsub==2.33.0`, use `>=2.33.0`

---

## 2. Workspace vs Project Configuration

### Workspace Root ONLY

| Section | Purpose |
|---------|---------|
| `[tool.uv.workspace]` | Defines workspace members |
| `[dependency-groups]` | dev, test, release groups |
| `[tool.uv]` default-groups | Local dev settings |
| `[tool.ruff]` | Linter config |
| `[tool.pyright]` | Type checker config |
| `[tool.hatch.build]` | Build config |
| `readme` field | Only in workspace root |

### Both Workspace and Projects

| Section | Notes |
|---------|-------|
| `[build-system]` | Identical in both |
| `[project]` | Different content |
| `[tool.polylith.bricks]` | Different paths |

### Projects NEVER Include

- `[dependency-groups]` - inherited
- `[tool.uv]` - inherited
- `[tool.ruff]` - workspace-wide
- `[tool.pyright]` - workspace-wide
- `readme` field - workspace only

---

## 3. Quick Reference Table

| Section | Workspace | Projects |
|---------|-----------|----------|
| `[project]` | ✓ Required | ✓ Required |
| `[build-system]` | ✓ Required | ✓ Required |
| `[dependency-groups]` | ✓ Required | ✗ Never |
| `[tool.uv.workspace]` | ✓ Required | ✗ Never |
| `[tool.polylith.bricks]` | ✓ Required | ✓ Required |
| `[tool.ruff]` | ✓ Required | ✗ Never |
| `readme` | ✓ Yes | ✗ Never |

---

## 4. Dependency Groups

Defined ONLY in workspace root:

```toml
[dependency-groups]
dev = ["polylith-cli>=1.40.0", "ruff>=0.14.8", "pyright>=1.1.407"]
test = ["pytest>=9.0.2", "pytest-cov>=7.0.0"]
release = ["pulumi>=3.213.0", "python-semantic-release==10.4.0"]
```

---

## 5. Build System

**Required in both workspace and projects:**

```toml
[build-system]
requires = ["hatchling", "hatch-polylith-bricks"]
build-backend = "hatchling.build"
```

---

## 6. Polylith Bricks

**Workspace root** (paths from workspace root):
```toml
[tool.polylith.bricks]
"bases/asset/data_transformation" = "asset/data_transformation"
"components/asset/logging" = "asset/logging"
```

**Project** (relative paths with `../../`):
```toml
[tool.polylith.bricks]
"../../bases/asset/data_transformation" = "asset/data_transformation"
"../../components/asset/logging" = "asset/logging"
```

---

## 7. Prohibited Patterns

```toml
# ✗ Wrong - old format
[project.optional-dependencies]

# ✗ Wrong - missing version
dependencies = ["requests"]

# ✗ Wrong - poetry backend
[build-system]
requires = ["poetry-core"]

# ✗ Wrong - hardcoded Python
requires-python = "3.13.0"

# ✗ Wrong - readme in project
[project]
readme = "README.md"  # Only in workspace root
```

---

## 8. Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| "Package not found" during build | Wrong brick paths | Verify `[tool.polylith.bricks]` paths |
| Imports fail | Wrong Python interpreter | Use `.venv/bin/python` |
| Lock file conflicts | Multiple developers updating | Use `uv sync --frozen` for daily work |
| "editable requirement" error | `uv export` included `-e .` | Use `--no-emit-project` flag |

**For commands and templates, use the `uv-dependency` or `pyproject-config` skills.**
