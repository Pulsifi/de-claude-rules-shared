---
name: python-code-review
description: Review Python code for style, naming, imports, type hints, and project standards compliance. Use when reviewing code, checking style, fixing formatting issues, or asking about Python conventions.
allowed-tools: Read, Glob, Grep
---

# Python Code Style Review

Review Python code against project coding standards.

## Review Checklist

### 1. Code Style and Formatting

- [ ] 4 spaces for indentation (no tabs)
- [ ] Max 88 characters per line
- [ ] Proper spacing around operators (`x = 5`, not `x=5`)
- [ ] Space after commas (`[1, 2, 3]`, not `[1,2,3]`)
- [ ] Two blank lines between top-level definitions
- [ ] One blank line between class methods

### 2. Naming Conventions

| Element | Style | Example |
|---------|-------|---------|
| Modules | `lowercase_snake_case` | `api_client.py` |
| Functions | `lowercase_snake_case` | `calculate_total()` |
| Variables | `lowercase_snake_case` | `user_count` |
| Classes | `CamelCase` | `DataProcessor` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRIES` |
| Private | `_leading_underscore` | `_internal_helper()` |

### 3. Import Organization

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

### 4. Type Hints

- All functions MUST have type hints
- All class attributes MUST have type hints
- Use modern Python 3.13 syntax: `list[str]` not `List[str]`
- Use union syntax: `str | None` not `Optional[str]`

```python
# Good
def fetch_user(user_id: int) -> dict[str, Any] | None:
    ...

# Bad
def fetch_user(user_id):
    ...
```

### 5. Docstrings

- All public functions MUST have docstrings
- Use Google-style format
- Include Args, Returns, Raises sections

### 6. Logging

- Use structured dictionary format
- Past-tense event names
- Include traceback in error logs

## Common Issues to Flag

### Style Issues

```python
# Wrong - missing spaces
x=5
items=[1,2,3]

# Correct
x = 5
items = [1, 2, 3]
```

### Import Issues

```python
# Wrong - mixed groups, unsorted
import requests
import os
from local import thing
import sys

# Correct - grouped and sorted
import os
import sys

import requests

from local import thing
```

### Type Hint Issues

```python
# Wrong - missing hints, old syntax
from typing import List, Optional

def process(items):
    ...

def get_name() -> Optional[str]:
    ...

# Correct - modern syntax
def process(items: list[dict]) -> list[str]:
    ...

def get_name() -> str | None:
    ...
```

### Naming Issues

```python
# Wrong
class data_processor:  # Should be CamelCase
    def ProcessData(self):  # Should be snake_case
        maxRetries = 3  # Should be snake_case

# Correct
class DataProcessor:
    def process_data(self):
        max_retries = 3
```

## Tools

- **ruff**: Linter and formatter (configured in workspace `pyproject.toml`)
- **pyright**: Type checker
- **pre-commit**: Git hooks for automatic checks

```bash
# Run linter
uv run ruff check .

# Run formatter
uv run ruff format .

# Run type checker
uv run pyright
```

## Reference

See [02-development.md](../../rules/02-development.md) for complete Python coding standards.
