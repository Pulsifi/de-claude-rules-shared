# Semantic Release

Manage automated versioning and releases using conventional commits.

## Trigger

Use this skill when the user asks to:
- Write commit messages
- Create a release
- Understand version bumps
- Fix commit message format

## Commit Message Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

### Type → Version Bump

| Type | Version Bump | Example |
|------|--------------|---------|
| `feat` | MINOR (1.0.0 → 1.1.0) | `feat(api): add user endpoint` |
| `fix` | PATCH (1.0.0 → 1.0.1) | `fix(auth): correct token expiry` |
| `perf` | PATCH (1.0.0 → 1.0.1) | `perf(query): optimize lookup` |
| `!` or `BREAKING CHANGE:` | MAJOR (1.0.0 → 2.0.0) | `feat!: remove v1 api` |
| `docs`, `style`, `refactor`, `test`, `build`, `ci`, `chore` | None | `docs: update readme` |

### Subject Rules

- Use imperative mood: "add" not "added" or "adds"
- Don't capitalize first letter: "add feature" not "Add feature"
- No period at the end
- Maximum 72 characters
- Be descriptive, not vague

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

### Breaking Change
```
feat(settings)!: migrate to pydantic v2 settings

BREAKING CHANGE: Settings class now uses Pydantic v2 API.
Update all code using `Config` inner class to use `model_config`.
```

### Simple Changes (No Body)
```
docs: update installation guide
ci: add type checking workflow
chore: update dependencies
```

## Branch Naming

```
<type>/<ticket-id>-<brief-description>
```

Examples:
```
feat/DA-687-migrate-to-uv
fix/DA-701-sentry-integration
docs/DA-688-update-readme
```

## How Releases Work

1. Commits pushed to `main` branch
2. Semantic release analyzes commit messages
3. Version bump determined from commit types
4. CHANGELOG.md generated
5. Git tag created (e.g., v1.2.3)
6. GitHub release published

## Configuration

In workspace root `pyproject.toml`:

```toml
[tool.semantic_release]
version_variable = ["pyproject.toml:project.version"]
version_toml = ["pyproject.toml:project.version"]
branch = "main"
upload_to_pypi = false
upload_to_release = true
```

## Manual Release (Rare)

```bash
# Dry run
semantic-release --noop version --print

# Actual release
semantic-release version
semantic-release publish
```

## Pull Request Conventions

PR titles follow the same format as commit messages:

```
<type>(<scope>): <description>
```

**PR Description Template:**
```markdown
## Summary
Brief description of what this PR does.

## Changes
- Bullet point list of changes

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass

## Related Issues
Closes #123
```

## Helpful Git Commands

```bash
# View commit history
git log --oneline --decorate

# View commits since last tag
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# Amend last commit message
git commit --amend

# Interactive rebase to fix commit messages
git rebase -i HEAD~3
```

## Common Mistakes

See [common-mistakes.md](references/common-mistakes.md) for examples.
