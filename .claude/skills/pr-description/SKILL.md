---
name: pr-description
description: Create pull request descriptions with proper format and sections. Use when creating PRs, writing PR descriptions, or asking about PR conventions.
allowed-tools: Read, Bash, Glob
---

# Pull Request Description

Create pull request descriptions following project conventions.

## PR Title Format

PR titles follow the same format as commits:

```
<type>(<scope>): <description>
```

Examples:
- `feat(pipeline): add CDC event deduplication`
- `fix(logging): correct sentry integration`
- `docs: update installation guide`

## PR Description Template

```markdown
## Summary
Brief description of what this PR does.

## Changes
- Bullet point list of changes
- Another change
- Yet another change

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Related Issues
Closes #123
Relates to #456

## Breaking Changes
(If applicable) Describe breaking changes and migration steps.

## Screenshots
(If applicable) Add screenshots for UI changes.
```

## Section Guidelines

### Summary
- 1-2 sentences describing the PR purpose
- Focus on "what" and "why", not "how"

### Changes
- Bullet points for each logical change
- Group related changes together
- Be specific but concise

### Testing
- Mark completed items with [x]
- List all testing done
- Include manual testing steps if needed

### Related Issues
- Use `Closes #123` for issues this PR fixes
- Use `Relates to #456` for related issues
- GitHub will auto-link and close issues

### Breaking Changes
- Clearly describe what breaks
- Provide migration steps
- List affected components/APIs

## Examples

### Feature PR

```markdown
## Summary
Add event deduplication to prevent duplicate CDC events from being
published to Pub/Sub.

## Changes
- Add LRU cache for tracking processed LSN positions
- Implement deduplication check before publish
- Add metrics for duplicate event count
- Update unit tests for deduplication logic

## Testing
- [x] Unit tests added for deduplication logic
- [x] Integration tests pass
- [x] Manual testing with duplicate events

## Related Issues
Closes #142
```

### Bug Fix PR

```markdown
## Summary
Fix incorrect Sentry DSN configuration causing production errors to
be sent to staging project.

## Changes
- Read DSN from SENTRY_DSN environment variable
- Add validation for DSN format
- Update configuration documentation

## Testing
- [x] Unit tests updated
- [x] Verified correct project in Sentry dashboard
- [x] Manual testing in staging environment

## Related Issues
Fixes #156
```

### Breaking Change PR

```markdown
## Summary
Migrate Settings class to Pydantic v2 API for better performance
and type safety.

## Changes
- Replace `class Config:` with `model_config = SettingsConfigDict()`
- Update all settings imports
- Update type hints for v2 compatibility

## Testing
- [x] Unit tests updated for new API
- [x] Integration tests pass
- [x] Manual testing of all settings

## Related Issues
Closes #200

## Breaking Changes
Settings class now uses Pydantic v2 API:

**Before:**
```python
class Settings(BaseSettings):
    class Config:
        env_prefix = "APP_"
```

**After:**
```python
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_")
```

Migration steps:
1. Update all `class Config:` to `model_config = SettingsConfigDict()`
2. Update `env_prefix` to use new format
```

## Reference

See [06-automation.md](../../rules/06-automation.md#14-pull-request-conventions) for complete guidelines.
