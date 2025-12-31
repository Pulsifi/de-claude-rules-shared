---
name: python-docstring
description: Generate Google-style docstrings for Python functions, classes, and modules. Use when writing docstrings, documenting code, adding function documentation, or when asked about docstring format.
allowed-tools: Read, Write, Edit
---

# Python Docstring Generator

Generate Google-style docstrings following project standards.

## Docstring Format Requirements

- **Style:** Google Python Style Guide
- **Quotes:** Always use triple double quotes (`"""`)
- **Line length:** Maximum 88 characters per line
- **Structure:** Summary line, blank line, detailed description, sections

## Docstring Sections (in order)

1. **Summary** (required) - One-line description in imperative mood
2. **Extended description** (optional) - Detailed explanation
3. **Note** (optional) - Important considerations, side effects
4. **Args** (required if parameters exist) - Parameter descriptions
5. **Returns** (required if returns value) - Return value description
6. **Yields** (required if generator) - Yielded value description
7. **Raises** (required if raises exceptions) - Exception descriptions

## Templates

### Function Docstring

```python
def fetch_and_process_data(
    endpoint: str,
    timeout: int = 10,
    retries: int = 3
) -> list[dict[str, Any]]:
    """Fetch and process data from API endpoint.

    Send GET request to specified endpoint, parse JSON response,
    and return processed data items.

    Note:
    - This function loads all data into memory
    - Retries automatically on network errors

    Args:
        endpoint: The API endpoint URL to fetch data from
        timeout: Request timeout in seconds. Defaults to 10.
        retries: Number of retry attempts on failure. Defaults to 3.

    Returns:
        list[dict[str, Any]]: Processed data items from the API

    Raises:
        requests.exceptions.RequestException: For connection errors
        ValueError: If response is not valid JSON
    """
```

### Class Docstring

```python
class DataProcessor:
    """Process and transform data from multiple sources.

    This class handles fetching, transforming, and loading data
    from various API endpoints into a standardized format.

    Attributes:
        api_key: Authentication key for API access
        timeout: Default request timeout in seconds
        retry_count: Number of automatic retries on failure
    """

    def __init__(self, api_key: str, timeout: int = 30):
        """Initialize the DataProcessor.

        Args:
            api_key: Authentication key for API access
            timeout: Request timeout in seconds. Defaults to 30.
        """
```

### Generator Docstring

```python
def read_large_file(file_path: str) -> Iterator[str]:
    """Read large file line by line.

    Efficiently process large files by yielding one line at a time
    instead of loading entire file into memory.

    Args:
        file_path: Path to the file to read

    Yields:
        str: Each line from the file, with trailing newline removed

    Raises:
        FileNotFoundError: If file doesn't exist
        PermissionError: If file can't be read
    """
```

### Module Docstring

```python
"""Data fetching module for external API integration.

This module provides utilities for fetching and processing data
from external APIs with retry logic and error handling.
"""
```

## Checklist

- [ ] Triple double quotes (`"""`)
- [ ] Imperative mood summary ("Fetch data" not "Fetches data")
- [ ] Args section with types and descriptions
- [ ] Returns section with type
- [ ] Raises section if applicable
- [ ] Note section for important details
- [ ] Max 88 characters per line

## Reference

See [02-development.md](../../rules/02-development.md#6-docstring-standards) for complete guidelines.
