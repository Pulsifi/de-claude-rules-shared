---
name: polylith-component
description: Create a new Polylith component with proper structure, __init__.py, and core.py files. Use when creating components, adding reusable functionality, or setting up shared libraries in the monorepo.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Polylith Component Creator

Create new Polylith components following the project's architecture standards.

## Instructions

When the user wants to create a new component:

1. **Gather information:**
   - Component name (lowercase_snake_case)
   - Namespace (check existing components in `components/` directory)
   - Optional: grouping subdirectory (e.g., `gcp/`, `aws/`)

2. **Determine the correct path:**
   ```
   components/{namespace}/{optional_grouping}/{component_name}/
   ```

3. **Create the component structure:**

   **`__init__.py`:**
   ```python
   """Package initialization for {component_name} component."""
   ```

   **`core.py`:**
   ```python
   """{Component description} component.

   This component provides {functionality description}.
   """

   # Standard library imports
   from typing import Any

   # Third-party imports (if needed)

   # Local imports (if needed)


   def {main_function}() -> {return_type}:
       """Function description.

       Args:
           param: Description of parameter

       Returns:
           Description of return value
       """
       pass
   ```

4. **Create corresponding test file:**
   ```
   test/components/{namespace}/{optional_grouping}/{component_name}/test_core.py
   ```

   **Test file template:**
   ```python
   """Tests for {component_name} component."""

   import pytest

   from {namespace}.{component_name}.core import {main_function}


   class TestComponentName:
       """Test suite for {component_name} component."""

       def test_main_function(self) -> None:
           """Test {main_function} functionality."""
           # Arrange
           # Act
           # Assert
           pass
   ```

5. **Register the component in workspace root `pyproject.toml`:**
   - Add to `[tool.polylith.bricks]` section
   - Format: `"components/{namespace}/{component_name}" = "{namespace}/{component_name}"`

## Component Design Principles

From [01-setup.md](../../rules/01-setup.md):

- **Single responsibility:** Each component should do one thing well
- **Stateless:** Components should not maintain global state
- **Pure functions:** Prefer pure functions for testability
- **Hide implementation:** Expose only necessary interfaces
- **Reusable:** Design for potential use across multiple projects

## Example

Creating a `validation` component in the `pipeline` namespace:

```
components/pipeline/validation/
├── __init__.py
└── core.py

test/components/pipeline/validation/
└── test_core.py
```

## Reference

See [01-setup.md](../../rules/01-setup.md#2-understanding-polylith-core-concepts) for complete component guidelines.
See [02-development.md](../../rules/02-development.md) for Python coding standards.
