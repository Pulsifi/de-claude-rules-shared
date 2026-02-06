# GitHub Actions CI/CD

Create and maintain GitHub Actions workflows following project standards.

## Trigger

Use this skill when the user asks to:
- Create a GitHub Actions workflow
- Set up CI/CD for a project
- Fix workflow issues
- Add new workflow jobs

## Standard Setup Pattern

Every Python workflow MUST include these steps:

```yaml
steps:
  - name: "Check out GitHub repository"
    uses: actions/checkout@v4

  - name: "Set up Python"
    uses: actions/setup-python@v5
    with:
      python-version-file: "pyproject.toml"  # Never hardcode version

  - name: "Set up uv"
    uses: astral-sh/setup-uv@v5
    with:
      version: "0.7.8"  # Always pin exact version

  - name: "Install dependencies"
    run: uv sync --frozen  # Always use --frozen in CI/CD

  - name: "Activate virtualenv"
    run: echo "$PWD/.venv/bin" >> $GITHUB_PATH
```

## Workflow Templates

### Type Check

```yaml
name: Type Check

on:
  pull_request:
    branches: [main]

jobs:
  type-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version-file: "pyproject.toml"
      - uses: astral-sh/setup-uv@v5
        with:
          version: "0.7.8"
      - run: uv sync --frozen
      - run: echo "$PWD/.venv/bin" >> $GITHUB_PATH
      - uses: jakebailey/pyright-action@v2
```

### Test

```yaml
name: Test

on:
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version-file: "pyproject.toml"
      - uses: astral-sh/setup-uv@v5
        with:
          version: "0.7.8"
      - run: uv sync --frozen
      - run: echo "$PWD/.venv/bin" >> $GITHUB_PATH
      - run: |
          uv run pytest test/ \
            --junitxml=pytest.xml \
            --cov-report=xml:coverage.xml \
            --cov=components \
            --cov=bases
```

### Release

```yaml
name: Release

on:
  push:
    branches: [main]

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Required for semantic release
      - uses: actions/setup-python@v5
        with:
          python-version-file: "pyproject.toml"
      - uses: astral-sh/setup-uv@v5
        with:
          version: "0.7.8"
      - run: uv sync --frozen --group release
      - run: echo "$PWD/.venv/bin" >> $GITHUB_PATH
      - run: semantic-release publish
```

## Dependency Groups

| Group | Use Case | Command |
|-------|----------|---------|
| (default) | Standard dev | `uv sync --frozen` |
| release | CI/CD deployment | `uv sync --frozen --group release` |
| test | Test-only jobs | `uv sync --frozen --group test` |

## Workflow Naming

All workflows MUST have both `name` and `run-name`:

```yaml
name: Infrastructure Provision
run-name: Provision ${{ github.event_name == 'workflow_dispatch' && 'production' || 'sandbox' }} infrastructure
```

## Step ID Convention

Use `verb-subject` in kebab-case when steps have outputs:

```yaml
- name: "Determine stack and version"
  id: determine-stack-version
  run: |
    echo "VERSION=${VERSION}" >> $GITHUB_OUTPUT
```

## Reference Files

- [workflow-templates.md](references/workflow-templates.md) - Complete workflow examples
- [common-patterns.md](references/common-patterns.md) - Docker build, GCP auth patterns
