# Development: Python Coding Standards

**When to use this file:** Reference for Python style guidelines that apply to ALL code.

**Skills available:** Use `python-docstring`, `python-logging`, or `python-code-review` skills for templates and detailed guidance.

---

## 1. Code Style

### Formatting Rules

| Rule | Standard |
|------|----------|
| Indentation | 4 spaces (no tabs) |
| Line length | 88 characters max |
| Blank lines | 2 between top-level, 1 between methods |
| Quotes | Double quotes for strings |

### Spacing

```python
# Correct
x = 5
items = [1, 2, 3]
config = {"host": "localhost", "port": 8080}

# Wrong
x=5
items = [1,2,3]
config = {"host":"localhost","port":8080}
```

---

## 2. Naming Conventions

| Element | Style | Example |
|---------|-------|---------|
| Modules | `lowercase_snake_case` | `api_client.py` |
| Functions | `lowercase_snake_case` | `calculate_total()` |
| Variables | `lowercase_snake_case` | `user_count` |
| Classes | `CamelCase` | `DataProcessor` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRIES` |
| Private | `_leading_underscore` | `_internal_helper()` |

---

## 3. Import Organization

Imports MUST be in three groups with blank lines:

```python
# 1. Standard library
import os
import sys
from typing import Any

# 2. Third-party
import requests
from google.cloud import pubsub_v1

# 3. Local
from my_workspace.components.logging.core import log_event
```

---

## 4. Type Hints

**Required for:**
- All function parameters and return values
- All class attributes

**Use modern syntax:**
```python
# Correct (Python 3.13)
def fetch_user(user_id: int) -> dict[str, Any] | None:
    ...

# Wrong (old syntax)
from typing import Dict, Optional
def fetch_user(user_id: int) -> Optional[Dict[str, Any]]:
    ...
```

---

## 5. Docstrings

**Format:** Google Python Style Guide

**Required sections:**
1. Summary (imperative mood)
2. Args (if parameters)
3. Returns (if returns value)
4. Raises (if raises exceptions)

```python
def fetch_data(endpoint: str, timeout: int = 10) -> dict[str, Any]:
    """Fetch data from API endpoint.

    Args:
        endpoint: The API endpoint URL
        timeout: Request timeout in seconds. Defaults to 10.

    Returns:
        dict[str, Any]: Response data from the API

    Raises:
        requests.RequestException: For connection errors
    """
```

**For templates, use the `python-docstring` skill.**

---

## 6. Logging

**Format:** Structured dictionary with `msg` parameter

**Required fields:**
- `event`: Past-tense verb + object (e.g., "Fetched user data")
- `payload`: Contextual data
- `traceback`: Required for error logs

```python
# Info log
logging.info(msg={"event": "Fetched user profile", "payload": {"user_id": user_id}})

# Error log (must include traceback)
logging.error(msg={"event": str(e), "payload": {"traceback": traceback.format_exc()}})
```

**DO NOT:**
- Log plain strings: `logging.info("User logged in")`
- Use present tense: `"Fetching user data"`
- Include sensitive data (passwords, tokens, PII)

**For templates, use the `python-logging` skill.**

---

## 7. Code Quality Tools

| Tool | Purpose | Config Location |
|------|---------|-----------------|
| ruff | Linter + formatter | Workspace `pyproject.toml` |
| pyright | Type checker | Workspace `pyproject.toml` |
| pre-commit | Git hooks | `.pre-commit-config.yaml` |

```bash
uv run ruff check .
uv run ruff format .
uv run pyright
```
