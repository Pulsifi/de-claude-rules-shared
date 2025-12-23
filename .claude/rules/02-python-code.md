# Python Code Style and Formatting Rules

## 1. General Principles
- **Style Guide:** All Python code MUST adhere to the [PEP 8](https://peps.python.org/pep-0008/) style guide.
- **Automation:** We use the `ruff` formatter for consistent styling. All generated code should be compliant with `ruff`'s default settings.
- **Clarity:** Code should be written to be as clear and readable as possible.
- **Type Hints:** All functions, methods, and class attributes MUST include type annotations.

## 2. Formatting Rules
- **Indentation:** Use 4 spaces per indentation level. Do not use tabs.
- **Line Length:** Each line must be a maximum of 88 characters long. It can wrap to multiple lines if needed.
- **Line Breaks:** When wrapping long lines, prefer breaking after an opening parenthesis/bracket or before a binary operator to improve readability.
- **Whitespace:**
    - Use a single space around most operators (`=`, `+=`, `==`, `<`, `>`).
    - Use a single space after commas in lists, dictionaries, and function arguments.
    - Avoid extraneous whitespace immediately inside parentheses, brackets, or braces.
- **Blank Lines:**
    - Use two blank lines to separate top-level functions and class definitions.
    - Use one blank line to separate method definitions inside a class.

## 3. Naming Conventions
- **Modules:** `lowercase_snake_case` (e.g., `api_client.py`).
- **Functions:** `lowercase_snake_case` (e.g., `propagate_description`, `propagate_constraint`).
- **Variables:** `lowercase_snake_case` (e.g., `request_data`, `message_data`).
- **Classes:** `CamelCase` (e.g., `DatabaseConnection`, `BigQueryWriteFn`).
- **Constants:** `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`, `DEFAULT_TIMEOUT`).

## 4. Imports
- **Ordering:** Imports must be grouped in the following order, with a blank line separating each group:
    1.  Standard library imports (e.g., `os`, `sys`, `math`, `datetime`).
    2.  Third-party library imports (e.g., `requests`, `pandas`, `numpy`).
    3.  Local application/library specific imports (e.g., `from my_project import utils`).
<!-- - **Style:** Use absolute imports (`from my_project.utils import helper`) instead of relative imports where possible. -->

## 5. Settings Management with Pydantic

All settings/configuration classes MUST use `pydantic_settings.BaseSettings` for type-safe environment variable management.

### Required Pattern

Settings classes MUST be placed in `components/{namespace}/settings/core.py` and follow this structure:

```python
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Base settings class with common configuration.

    All settings are loaded from environment variables.
    """
    model_config = ConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="ignore"
    )  # pyright: ignore

    # Project metadata
    ENVIRONMENT: str
    VERSION: str

    # GCP configuration
    GCP_PROJECT_ID: str
    GCP_REGION: str
    GCP_REGION_ABBREV: str
    GCP_REGION_SUFFIX: str

    # JIRA metadata
    EPIC: str
    COMPONENT: str
```

### Inheritance Pattern

For project-specific settings, inherit from the base `Settings` class:

```python
class MyServiceSettings(Settings):
    """Settings specific to MyService.

    Inherits common settings and adds service-specific configuration.
    """
    SLACK_BOT_TOKEN: str
    DATABASE_URL: str
    API_KEY: str
```

### Multiple Settings Classes

Projects with different components can have multiple settings classes:

```python
class LangfuseSettings(Settings):
    """Settings for Langfuse integration."""
    LANGFUSE_PUBLIC_KEY: str
    LANGFUSE_SECRET_KEY: str
    LANGFUSE_HOST: str


class Slack2AgentSettings(LangfuseSettings):
    """Settings for Slack to Agent integration.

    Inherits Langfuse settings and adds Slack-specific configuration.
    """
    SLACK_SIGNING_SECRET: str
    SLACK_BOT_TOKEN: str
    AGENT_ENGINE_BUCKET: str
    FIRESTORE_DATABASE: str
    FIRESTORE_COLLECTION: str
    AGENT_ENGINE_REGION: str
```

### Default Values

Use Python's default value syntax for optional settings:

```python
class SessionManagementSettings(Settings):
    """Settings for session management."""
    AGENT_ENGINES: set[str] = {
        "product_knowledge_agent_gpt_5_mini",
    }
    AGENT_ENGINE_REGION: str
    SESSION_INACTIVE_DAYS: int = 7
    SLACK_URL: str = "https://hooks.slack.com/services/..."
```

### Usage Pattern

```python
from components.my_namespace.settings import MyServiceSettings

settings = MyServiceSettings()
print(settings.GCP_PROJECT_ID)
print(settings.API_KEY)
```

### Key Requirements

1. **Always use `BaseSettings`:** Never use plain dataclasses or dictionaries for settings
2. **Type annotations:** All fields MUST have type annotations
3. **model_config:** Always include `ConfigDict` with `case_sensitive=True`, `env_file=".env"`, `extra="ignore"`
4. **Inheritance:** Use inheritance to avoid repeating common settings
5. **Docstrings:** Include class docstrings explaining the purpose
6. **Upper case:** Environment variable names MUST be UPPER_CASE

## 6. Example of Well-Formatted Code
Here is an example of a Python module that follows all the style guidelines:
```python
import os
import sys
from collections import namedtuple

import requests

from my_project.utils import custom_formatter

MAX_RETRIES = 3
API_ENDPOINT = "https://api.example.com/data"


class DataProcessor:
    """Process data fetched from a remote source.

    This class handles the retrieval and formatting of data from a specified
    API endpoint.

    Attributes:
        api_key (str): The API key used for authentication with the remote source.
    """

    def __init__(self, api_key: str):
        """Initialize the DataProcessor with an API key.

        Args:
            api_key (str): The API key for authenticating with the data source.
        """
        self.api_key = api_key

    def fetch_and_format_data(self, item_id: int) -> str | None:
        """Fetch and format a specific item's data from the API.

        Sends a GET request to the configured API endpoint with the given item ID,
        parses the JSON response, and formats the data using a custom formatter.

        Note:
        - This function performs a network request and may raise exceptions
          related to network connectivity or API response issues.

        Args:
            item_id (int): The unique identifier of the item to fetch.

        Returns:
            str | None: The formatted data as a string, or None if an error occurs
                during the request or data processing.

        Raises:
            requests.exceptions.RequestException: If a network error or an
                unsuccessful HTTP status code is encountered during the API call.
        """
        try:
            response = requests.get(
                f"{API_ENDPOINT}/{item_id}",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}", file=sys.stderr)
            return None

        formatted_data = custom_formatter.format(data)
        return formatted_data


def get_system_load(default_value: float = 0.0) -> float:
    """Get the current system load average over 1 minute.

    Retrieves the 1-minute load average of the system. If the operating system
    does not support `os.getloadavg`, a default value is returned.

    Args:
        default_value (float, optional): The value to return if `os.getloadavg`
            is not available. Defaults to 0.0.

    Returns:
        float: The 1-minute system load average, or the `default_value` if
            not supported.
    """
    if hasattr(os, "getloadavg"):
        return os.getloadavg()[0]
    return default_value
```
