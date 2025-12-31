---
name: github-workflow
description: Create GitHub Actions workflows with uv package manager and project standards. Use when creating CI/CD pipelines, setting up GitHub Actions, configuring test/deploy workflows, or automating builds.
allowed-tools: Read, Write, Edit, Glob
---

# GitHub Actions Workflow

Create GitHub Actions workflows following project standards.

## Standard Setup Steps

Every workflow requiring Python MUST include these steps:

```yaml
steps:
  - name: "Check out GitHub repository"
    uses: actions/checkout@v4

  - name: "Set up Python"
    uses: actions/setup-python@v5
    with:
      python-version-file: "pyproject.toml"

  - name: "Set up uv"
    uses: astral-sh/setup-uv@v5
    with:
      version: "0.7.8"

  - name: "Install dependencies"
    run: |
      uv sync --frozen

  - name: "Activate virtualenv"
    run: echo "$PWD/.venv/bin" >> $GITHUB_PATH
```

## Key Rules

### Python Version
- **Always use `python-version-file`** - Never hardcode Python version
- References version from `pyproject.toml`

### uv Version
- **Always pin exact version** - Currently `0.7.8`
- **Never use `latest`** or version ranges

### Dependencies
- **Always use `--frozen`** - Ensures deterministic builds
- **Use `--group`** for specific dependency groups

### Caching
- **NEVER cache uv dependencies** - uv is fast enough (<5 seconds)
- Remove all `actions/cache` for Python dependencies

## Workflow Templates

### Type Check Workflow

```yaml
name: Type Check

on:
  pull_request:
    branches: [main]

jobs:
  type-check:
    runs-on: ubuntu-latest
    steps:
      - name: "Check out GitHub repository"
        uses: actions/checkout@v4

      - name: "Set up Python"
        uses: actions/setup-python@v5
        with:
          python-version-file: "pyproject.toml"

      - name: "Set up uv"
        uses: astral-sh/setup-uv@v5
        with:
          version: "0.7.8"

      - name: "Install dependencies"
        run: uv sync --frozen

      - name: "Activate virtualenv"
        run: echo "$PWD/.venv/bin" >> $GITHUB_PATH

      - name: "Execute type check via pyright"
        uses: jakebailey/pyright-action@v2
```

### Test Workflow

```yaml
name: Test

on:
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: "Check out GitHub repository"
        uses: actions/checkout@v4

      - name: "Set up Python"
        uses: actions/setup-python@v5
        with:
          python-version-file: "pyproject.toml"

      - name: "Set up uv"
        uses: astral-sh/setup-uv@v5
        with:
          version: "0.7.8"

      - name: "Install dependencies"
        run: uv sync --frozen

      - name: "Activate virtualenv"
        run: echo "$PWD/.venv/bin" >> $GITHUB_PATH

      - name: "Execute pytest"
        run: |
          uv run pytest test/ \
            --junitxml=pytest.xml \
            --cov-report=xml:coverage.xml \
            --cov=components/
```

### Release Workflow

```yaml
name: Release

on:
  push:
    branches: [main]

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - name: "Check out GitHub repository"
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: "Set up Python"
        uses: actions/setup-python@v5
        with:
          python-version-file: "pyproject.toml"

      - name: "Set up uv"
        uses: astral-sh/setup-uv@v5
        with:
          version: "0.7.8"

      - name: "Install release dependencies"
        run: uv sync --frozen --group release

      - name: "Activate virtualenv"
        run: echo "$PWD/.venv/bin" >> $GITHUB_PATH

      - name: "Run semantic release"
        run: semantic-release publish
```

## Prohibited Patterns

```yaml
# DON'T hardcode Python version
python-version: "3.13"  # Use python-version-file instead

# DON'T use version ranges for uv
version: "latest"  # Pin exact version

# DON'T sync without --frozen
run: uv sync  # Always use --frozen

# DON'T add caching for uv
uses: actions/cache@v4  # uv is fast enough
```

## Naming Conventions

### Workflow name and run-name

```yaml
name: Infrastructure Provision
run-name: Provision ${{ github.event_name == 'workflow_dispatch' && 'production' || 'sandbox' }} infrastructure
```

### Step IDs

- Use `id:` when step sets output variables
- Format: `verb-subject` in kebab-case
- Examples: `determine-stack-version`, `configure-version-tag`

## Reference

See [06-automation.md](../../rules/06-automation.md#part-1-cicd-workflows) for complete guidelines.
