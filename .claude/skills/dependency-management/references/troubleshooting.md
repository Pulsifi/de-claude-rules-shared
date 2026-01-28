# Dependency Troubleshooting

## "Package not found" during build

**Cause:** Missing brick configuration or incorrect paths.

**Solution:** Verify `[tool.polylith.bricks]` paths match actual directory structure.

**Debug steps:**
```bash
# Check if brick paths exist
ls bases/{namespace}/{brick_name}
ls components/{namespace}/{brick_name}

# Verify relative paths from project directory
cd projects/{project_name}
ls ../../bases/{namespace}/{brick_name}
```

## Dependencies installed but imports fail

**Cause:** Virtual environment not activated or wrong Python interpreter.

**Solution:** Ensure `.venv/bin/python` is being used; check IDE interpreter settings.

**Debug steps:**
```bash
# Verify virtual environment
which python  # Should show .venv/bin/python

# Check installed packages
uv pip list

# Reinstall if needed
uv sync --frozen
```

## Lock file conflicts in git

**Cause:** Multiple developers running `uv lock` with different package indices.

**Solution:** Use `uv sync --frozen` in development; only update lock file deliberately.

**Best practice:**
- Designate one person to update lock file
- Use `uv sync --frozen` for daily work
- Only run `uv lock` when adding/updating dependencies

## "Requires python ~=3.13.0 but..." error

**Cause:** System Python version doesn't match project requirements.

**Fix with uv:**
```bash
# Install Python 3.13
uv python install 3.13

# Pin Python version (creates .python-version file)
uv python pin 3.13

# Create virtual environment and sync
uv venv
uv sync --frozen

# Verify
python --version  # Should show Python 3.13.x
```

## Cloud Functions deployment fails with "editable requirement" error

**Cause:** `uv export` included `-e .` in requirements.txt

**Correct command:**
```bash
uv export --format requirements-txt --no-hashes --no-emit-project -o requirements.txt
```

## Project can't import workspace dependencies

**Cause:** Project `pyproject.toml` missing dependencies that are only in workspace root.

**Solution:** Add required dependencies to project's `[project] dependencies` section.

**Why:** Projects don't automatically inherit workspace runtime dependencies, only dependency groups (dev, test, release).

## Version mismatch between workspace and project

**Cause:** Project specifies different version constraint than workspace root.

**Solution:** Ensure project uses exact same version constraint as workspace root:

```toml
# Workspace root
"google-cloud-bigquery>=3.30.0"

# Project (must match)
"google-cloud-bigquery>=3.30.0"  # ✅ Same constraint
"google-cloud-bigquery>=3.0.0"   # ❌ Different constraint
```
