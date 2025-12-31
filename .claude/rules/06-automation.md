# Automation: CI/CD Workflows & Version Control

**When to use this file:** Reference for CI/CD rules and commit conventions.

**Skills available:** Use `github-workflow`, `conventional-commit`, or `pr-description` skills for templates.

---

## Part 1: CI/CD Workflows

### Required Setup Steps

Every GitHub Actions workflow with Python MUST include:

```yaml
- uses: actions/setup-python@v5
  with:
    python-version-file: "pyproject.toml"  # Never hardcode version

- uses: astral-sh/setup-uv@v5
  with:
    version: "0.7.8"  # Always pin exact version

- run: uv sync --frozen  # Always use --frozen

- run: echo "$PWD/.venv/bin" >> $GITHUB_PATH  # Activate venv
```

### Key Rules

| Rule | Requirement |
|------|-------------|
| Python version | Use `python-version-file`, never hardcode |
| uv version | Pin exact version (0.7.8), never use `latest` |
| Dependency install | Always use `--frozen` flag |
| Caching | NEVER cache uv dependencies |

### Prohibited Patterns

```yaml
# ✗ Wrong
python-version: "3.13"      # Hardcoded
version: "latest"           # Not pinned
run: uv sync                # Missing --frozen
uses: actions/cache@v4      # Don't cache uv
```

**For workflow templates, use the `github-workflow` skill.**

---

## Part 2: Conventional Commits

### Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

### Commit Types and Version Bumps

| Type | Version Bump | Description |
|------|--------------|-------------|
| `feat` | MINOR (1.0.0 → 1.1.0) | New feature |
| `fix` | PATCH (1.0.0 → 1.0.1) | Bug fix |
| `perf` | PATCH (1.0.0 → 1.0.1) | Performance improvement |
| `docs` | None | Documentation only |
| `style` | None | Formatting, whitespace |
| `refactor` | None | Code change (no fix or feature) |
| `test` | None | Tests |
| `build` | None | Build system or dependencies |
| `ci` | None | CI/CD configuration |
| `chore` | None | Other maintenance |

### Breaking Changes

Breaking changes trigger MAJOR bump (1.0.0 → 2.0.0):

```
feat(api)!: remove deprecated endpoints

# Or use footer:
BREAKING CHANGE: Configuration format changed to YAML.
```

### Subject Rules

- **Imperative mood:** "add feature" not "added feature"
- **No capitalization:** "add feature" not "Add feature"
- **No period at end**
- **Max 72 characters**

### Common Scopes

`pipeline`, `cdc`, `gcp`, `settings`, `logging`, `ci`, `docker`

**For examples and templates, use the `conventional-commit` skill.**

---

## Part 3: Branch and PR Conventions

### Branch Naming

```
<type>/<ticket-id>-<brief-description>
```

Examples:
- `feat/DA-687-migrate-to-uv`
- `fix/DA-701-sentry-integration`

### PR Title Format

Same as commit messages:

```
<type>(<scope>): <description>
```

**For PR templates, use the `pr-description` skill.**

---

## Part 4: Semantic Release

### How It Works

1. Analyzes commits since last release
2. Determines version bump from commit types
3. Generates changelog
4. Creates git tag and GitHub release

### Configuration

```toml
[tool.semantic_release]
version_toml = ["pyproject.toml:project.version"]
branch = "main"
upload_to_pypi = false
upload_to_release = true
```

### Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| No version bump | No `feat:` or `fix:` commits | Use correct commit types |
| Wrong version bump | Wrong commit type | Fix with interactive rebase before merge |
| Release failed | Format error or permissions | Check commit format; verify GH_TOKEN |
