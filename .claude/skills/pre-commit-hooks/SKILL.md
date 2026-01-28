# Pre-commit Hooks

Set up and manage pre-commit hooks for code quality enforcement.

## Trigger

Use this skill when the user asks to:
- Set up pre-commit hooks
- Configure code quality hooks
- Fix pre-commit hook issues
- Add commit message validation

## Standard Configuration

Create `.pre-commit-config.yaml` at workspace root:

```yaml
repos:
  - repo: local
    hooks:
      - id: ruff-format
        name: ruff-format
        entry: "uv run ruff format bases components projects"
        language: system
        always_run: true
        types: [python]

  - repo: local
    hooks:
      - id: ruff-linter
        name: ruff-linter
        entry: "uv run ruff check --fix bases components projects"
        language: system
        always_run: true
        types: [python]

  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: "uv run pytest"
        pass_filenames: false
        language: system
        always_run: true
        types: [python]
```

## Procedure: Initial Setup

### Step 1: Ensure pre-commit is installed

Pre-commit is included in the `dev` dependency group:
```bash
uv sync
```

### Step 2: Install git hooks

```bash
uv run pre-commit install
```

This installs hooks that run automatically before each `git commit`.

### Step 3: Verify setup

```bash
# Run hooks manually on all files
uv run pre-commit run --all-files
```

## Hook Descriptions

| Hook | Purpose | Behavior |
|------|---------|----------|
| **ruff-format** | Format Python code | Auto-fixes formatting issues |
| **ruff-linter** | Lint and fix code | Auto-fixes linting issues |
| **pytest** | Run test suite | Ensures tests pass before commit |

## Handling Hook Failures

### When hooks auto-fix files

The commit will fail but files are fixed. Stage changes and retry:

```bash
git add -u
git commit -m "your commit message"
```

### When tests fail

Fix the failing tests, then commit again:

```bash
# See which tests failed
uv run pytest -v

# Fix issues, then commit
git add -u
git commit -m "your commit message"
```

### Temporarily skip hooks (not recommended)

```bash
git commit --no-verify -m "message"
```

## Optional: Commit Message Validation

Add conventional commit validation:

```yaml
# Add to .pre-commit-config.yaml
  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v3.0.0
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]
```

Then install commit-msg hook:
```bash
uv run pre-commit install --hook-type commit-msg
```

## Useful Commands

```bash
# Run specific hook
uv run pre-commit run ruff-format --all-files

# Update hook versions
uv run pre-commit autoupdate

# Uninstall hooks
uv run pre-commit uninstall
```

## Troubleshooting

### "pre-commit: command not found"

Ensure you've synced dependencies:
```bash
uv sync
```

### Hooks not running on commit

Reinstall the hooks:
```bash
uv run pre-commit install
```

### Hook runs but misses files

Check the `entry` paths include all relevant directories (bases, components, projects).
