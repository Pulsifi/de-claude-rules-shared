---
name: conventional-commit
description: Write conventional commit messages for semantic versioning. Use when creating commits, writing commit messages, understanding commit format, or asking about version bumps.
allowed-tools: Read, Bash
---

# Conventional Commit Messages

Write commit messages following Conventional Commits specification.

## Commit Message Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

## Commit Types

| Type | Version Bump | Description |
|------|--------------|-------------|
| `feat` | MINOR (1.0.0 → 1.1.0) | New feature |
| `fix` | PATCH (1.0.0 → 1.0.1) | Bug fix |
| `perf` | PATCH (1.0.0 → 1.0.1) | Performance improvement |
| `docs` | None | Documentation only |
| `style` | None | Formatting, whitespace |
| `refactor` | None | Code changes (no bug fix or feature) |
| `test` | None | Adding or updating tests |
| `build` | None | Build system or dependencies |
| `ci` | None | CI/CD configuration |
| `chore` | None | Other maintenance |

## Breaking Changes

Breaking changes trigger MAJOR bump (1.0.0 → 2.0.0):

```
# Method 1: Add ! after type/scope
feat(api)!: remove deprecated endpoints

# Method 2: BREAKING CHANGE footer
feat(settings): change configuration format

BREAKING CHANGE: Configuration now uses YAML instead of JSON.
```

## Subject Rules

- **Imperative mood:** "add feature" not "added feature"
- **No capitalization:** "add feature" not "Add feature"
- **No period:** "add feature" not "add feature."
- **Max 72 characters**
- **Be descriptive:** Explain what changed

## Common Scopes

- `pipeline` - Data pipeline logic
- `cdc` - Change Data Capture
- `gcp` - GCP-related components
- `settings` - Configuration
- `logging` - Logging infrastructure
- `ci` - CI/CD workflows
- `docker` - Dockerfile changes

## Examples

### Feature

```
feat(pipeline): add CDC event deduplication

Implement deduplication logic to prevent duplicate CDC events from
being published to Pub/Sub. Uses in-memory cache with LRU eviction.

Closes #142
```

### Bug Fix

```
fix(logging): correct sentry DSN configuration

Previously used wrong DSN for production environment.

Fixes #156
```

### Documentation

```
docs: add comprehensive docstrings to core modules
```

### CI/CD

```
ci: migrate deploy workflow to uv

Replace Poetry with uv for faster dependency installation.
```

### Breaking Change

```
feat(settings)!: migrate to pydantic v2 settings

BREAKING CHANGE: Settings class now uses Pydantic v2 API.
Update all code using `Config` inner class to use `model_config`.
```

## Common Mistakes

```
# WRONG - past tense
feat(pipeline): added event deduplication

# CORRECT - imperative
feat(pipeline): add event deduplication

# WRONG - capitalized
feat(pipeline): Add event deduplication

# CORRECT - lowercase
feat(pipeline): add event deduplication

# WRONG - period at end
feat(pipeline): add event deduplication.

# CORRECT - no period
feat(pipeline): add event deduplication

# WRONG - too vague
fix: update code

# CORRECT - descriptive
fix(logging): correct sentry DSN for production
```

## Branch Naming

```
<type>/<ticket-id>-<brief-description>
```

Examples:
- `feat/DA-687-migrate-to-uv`
- `fix/DA-701-sentry-integration`
- `docs/DA-688-update-readme`

## Semantic Release

Commits on `main` branch are analyzed:
1. `feat:` → MINOR bump
2. `fix:` or `perf:` → PATCH bump
3. `BREAKING CHANGE:` or `!` → MAJOR bump
4. Other types → No bump

## Reference

See [06-automation.md](../../rules/06-automation.md#10-commit-message-format) for complete guidelines.
