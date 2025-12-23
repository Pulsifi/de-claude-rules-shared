# Python Logging Rules

## 1. Logging Format

* **Structured Format:** All logs must use structured dictionary format passed to the `msg` parameter.
* **Key Fields:**

  * `event`: A short, descriptive message summarizing what happened.

    * Must start with a **verb in past tense** followed by the **object**.

      * ✅ *Example:*  `"Started stream query"`, `"Fetched user profile"`, `"Sent Slack message"`.  
      * ❌ Avoid reversed order or passive forms such as `"Stream query started"` or `"User profile fetched"`.
  * `payload`: Contains contextual or supplementary information.
  * `traceback`: Included only in error logs to capture exception details.
* **Style Consistency:** Keep keys in lowercase with underscores only if necessary (e.g., `response_data`).


## 2. Logging Levels and Usage

### Info Logs

* Use `logging.info()` for successful or expected operations.
* Structure:

  ```python
  logging.info(
      msg={
          "event": "Posted Slack message result.",
          "payload": {
              "response_data": response_data,
          },
      }
  )
  ```
* The `"event"` field describes the completed action in past tense.
* The `"payload"` field should contain contextual data relevant to the event.

### Error Logs

* Use `logging.error()` for errors, exceptions, or unexpected failures.
* Must include traceback information for debugging.
* Import the traceback module at the top of the file:

  ```python
  import traceback
  ```
* Structure:

  ```python
  logging.error(
      msg={
          "event": str(e),
          "payload":{
            "traceback": traceback.format_exc(),
          }
      }
  )
  ```

## 3. GCP Cloud Logging Integration

For GCP-deployed services (Cloud Functions, Cloud Run, etc.), use Google Cloud Logging for proper log aggregation and monitoring.

### Required Pattern

GCP logging setup MUST be placed in `components/{namespace}/gcp/logging.py`:

```python
"""GCP Cloud Logging integration."""

import google.auth
import google.auth.exceptions
import google.cloud.logging
from google.auth.credentials import AnonymousCredentials
from google.cloud.logging_v2.handlers import StructuredLogHandler, setup_logging


def attach_gcp_logger(
    version: str,
    epic: str,
    component: str,
    subcomponent: str,
) -> None:
    """Set up a google-cloud-logging handler and attach it to the Python root logger.

    Automatically detects if running in GCP (with valid credentials) or locally
    (falls back to anonymous credentials for local development).

    Args:
        version (str): Semantic release version (e.g., "1.2.3").
        epic (str): Jira epic identifier.
        component (str): Jira component name.
        subcomponent (str): The subfolder name within the workspace or service name.
    """
    try:
        google.auth.default()
        client = google.cloud.logging.Client()
    except google.auth.exceptions.DefaultCredentialsError:
        # Local development: use anonymous credentials
        client = google.cloud.logging.Client(
            project="data-local-warehouse",
            credentials=AnonymousCredentials()
        )

    handler = StructuredLogHandler(
        project_id=client.project,
        labels={
            "version": version,
            "epic": epic,
            "component": component,
            "subcomponent": subcomponent,
        },
    )
    setup_logging(handler)
```

### Usage in Cloud Functions

Call `attach_gcp_logger()` at the start of your Cloud Function handler:

```python
from components.my_namespace.gcp.logging import attach_gcp_logger
from components.my_namespace.settings import get_settings

def handler(request):
    settings = get_settings()
    attach_gcp_logger(
        version=settings.VERSION,
        epic=settings.EPIC,
        component=settings.COMPONENT,
        subcomponent="my_service"
    )

    # Now all logging.info() calls will go to GCP Cloud Logging
    logging.info("Started processing request")
```

### Key Features

1. **Automatic credential detection:** Works in both GCP and local environments
2. **Structured labels:** All logs are tagged with version, epic, component, and subcomponent
3. **Root logger attachment:** All Python logging calls automatically route to GCP
4. **Local development:** Falls back to anonymous credentials for testing locally

## 4. General Rules

* **No Plain String Logs:** Do not log raw strings or concatenated messages. Always use structured dictionaries.
* **Verb Style:** The `"event"` message must always begin with a verb in **past tense** (e.g., *Fetched data.*, *Processed request.*, *Posted message.*).
* **Payload Data:** Keep payloads concise. Avoid including large or sensitive data (e.g., full request bodies or tokens).
* **Consistency:** Use the same structure across all modules and services to simplify downstream log parsing.
