# Common Commit Message Mistakes

## Wrong Commit Type

```
# Wrong
update: add new feature

# Correct
feat: add new feature
```

## Missing Type

```
# Wrong
added CDC event deduplication

# Correct
feat(pipeline): add CDC event deduplication
```

## Past Tense

```
# Wrong
feat(pipeline): added event deduplication

# Correct
feat(pipeline): add event deduplication
```

## Capitalized Subject

```
# Wrong
feat(pipeline): Add event deduplication

# Correct
feat(pipeline): add event deduplication
```

## Period at End

```
# Wrong
feat(pipeline): add event deduplication.

# Correct
feat(pipeline): add event deduplication
```

## Too Vague

```
# Wrong
fix: update code

# Correct
fix(logging): correct sentry DSN configuration for production
```

## Multiple Changes in One Commit

```
# Wrong - combines unrelated changes
feat: add user auth and fix logging bug

# Correct - separate commits
feat(auth): add user authentication
fix(logging): correct sentry DSN configuration
```

## Wrong Breaking Change Format

```
# Wrong - breaking change not properly indicated
feat(api): remove deprecated endpoint

# Correct - use ! or BREAKING CHANGE footer
feat(api)!: remove deprecated endpoint

# Or with footer
feat(api): remove deprecated endpoint

BREAKING CHANGE: The /v1/users endpoint has been removed.
Use /v2/users instead.
```
