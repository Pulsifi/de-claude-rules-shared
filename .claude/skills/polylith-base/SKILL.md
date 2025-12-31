---
name: polylith-base
description: Create a new Polylith base (entry point) with proper structure. Use when creating API servers, CLI tools, serverless functions, or any application entry point that composes components.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Polylith Base Creator

Create new Polylith bases following the project's architecture standards.

## What is a Base?

Bases are **entry points** for applications or services. They:
- Compose components to deliver specific functionality
- Act as thin layers (minimal business logic)
- Define how the application is exposed (HTTP, CLI, event-driven)

## Instructions

When the user wants to create a new base:

1. **Gather information:**
   - Base name (lowercase_snake_case)
   - Namespace (check existing bases in `bases/` directory)
   - Base type: API server, CLI tool, Cloud Function, data processor, etc.

2. **Determine the correct path:**
   ```
   bases/{namespace}/{base_name}/
   ```

3. **Create the base structure:**

   **`__init__.py`:**
   ```python
   """Package initialization for {base_name} base."""
   ```

   **`core.py`:**
   ```python
   """{Base description}.

   This base serves as the entry point for {functionality description}.
   It composes the following components:
   - {component_1}: {purpose}
   - {component_2}: {purpose}
   """

   # Standard library imports
   import logging
   from typing import Any

   # Third-party imports
   # (e.g., Flask, functions-framework, click)

   # Local imports - components this base uses
   from {namespace}.{component_name}.core import {function}


   def main() -> None:
       """Application entry point."""
       pass
   ```

4. **Create corresponding test file:**
   ```
   test/bases/{namespace}/{base_name}/test_core.py
   ```

   **Test file template:**
   ```python
   """Integration tests for {base_name} base."""

   import pytest

   from {namespace}.{base_name}.core import main


   class TestBaseName:
       """Integration test suite for {base_name} base."""

       def test_main_function(self) -> None:
           """Test main entry point."""
           # Arrange
           # Act
           # Assert
           pass
   ```

5. **Register the base in workspace root `pyproject.toml`:**
   - Add to `[tool.polylith.bricks]` section
   - Format: `"bases/{namespace}/{base_name}" = "{namespace}/{base_name}"`

## Base Types and Patterns

### Cloud Function Base
```python
"""Cloud Function for {description}."""

import functions_framework
from flask import Request

from {namespace}.logging.core import log_event
from {namespace}.settings.core import Settings


@functions_framework.http
def handle_request(request: Request) -> tuple[dict, int]:
    """HTTP Cloud Function entry point.

    Args:
        request: Flask request object

    Returns:
        Tuple of response body and status code
    """
    settings = Settings()
    log_event("Received request", {"path": request.path})

    # Business logic using composed components
    return {"status": "ok"}, 200
```

### CLI Tool Base
```python
"""CLI tool for {description}."""

import click

from {namespace}.{component}.core import process_data


@click.command()
@click.option("--input", "-i", required=True, help="Input file path")
@click.option("--output", "-o", required=True, help="Output file path")
def main(input: str, output: str) -> None:
    """Process data from input to output."""
    result = process_data(input)
    # Write result to output
```

### API Server Base
```python
"""FastAPI server for {description}."""

from fastapi import FastAPI

from {namespace}.{component}.core import get_data

app = FastAPI(title="{Service Name}")


@app.get("/health")
async def health() -> dict:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/data/{item_id}")
async def get_item(item_id: str) -> dict:
    """Get item by ID."""
    return get_data(item_id)
```

## Base Design Principles

From [01-setup.md](../../rules/01-setup.md):

- **Thin layer:** Keep business logic in components, not bases
- **Compose components:** Bases orchestrate component functionality
- **Single entry point:** Each base should have one clear purpose
- **Environment-aware:** Handle configuration via settings component

## Reference

See [01-setup.md](../../rules/01-setup.md#2-understanding-polylith-core-concepts) for complete base guidelines.
See [02-development.md](../../rules/02-development.md) for Python coding standards.
See [05-deployment.md](../../rules/05-deployment.md) for deployment patterns.
