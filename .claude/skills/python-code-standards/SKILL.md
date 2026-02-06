# Python Code Standards

Python code quality standards and conventions for this workspace.

## Trigger

Use this skill when the user asks to:
- Review code style or formatting
- Add docstrings or type hints
- Understand naming conventions
- Fix linting or type errors

## Quality Tools

- **PEP 8** compliance enforced via `ruff` (line length: 88)
- **Type hints** required on all functions, methods, class attributes
- **Docstrings** in Google style for all public APIs
- **Type checking** via `pyright` (standard mode)

## Google Style Docstrings

```python
def fetch_data(url: str, timeout: int = 30) -> dict[str, Any]:
    """Fetch data from the specified URL.

    Args:
        url: The endpoint URL to fetch from.
        timeout: Request timeout in seconds.

    Returns:
        Parsed JSON response as dictionary.

    Raises:
        ConnectionError: If the request fails.
    """
```

## Code Formatting

| Rule | Standard |
|------|----------|
| Indentation | 4 spaces (never tabs) |
| Line length | 88 characters max |
| Blank lines | 2 between top-level definitions, 1 between methods |
| Whitespace | Space around operators (`=`, `+`), after commas, none inside brackets |

**Line wrapping**: Break after opening parenthesis or before binary operators.

## Naming Conventions

| Element | Style | Example |
|---------|-------|---------|
| Modules | `lowercase_snake_case` | `api_client.py` |
| Functions/Variables | `lowercase_snake_case` | `fetch_data`, `user_count` |
| Classes | `CamelCase` | `DataProcessor` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRIES` |
| Private | `_leading_underscore` | `_internal_helper` |

## Import Order

Three groups separated by blank lines:
1. Standard library
2. Third-party
3. Local (from workspace)

## Structured Logging

```python
logging.info(msg={"event": "Past-tense verb + object", "payload": {...}})
logging.error(msg={"event": str(e), "payload": {"traceback": traceback.format_exc()}})
```

- **event**: Past tense ("Fetched data", NOT "Fetching data")
- **payload**: Contextual data (no secrets/PII)
- **traceback**: Required in error logs
