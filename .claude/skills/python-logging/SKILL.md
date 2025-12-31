---
name: python-logging
description: Create structured logging statements with proper format. Use when adding logging, creating log messages, handling errors with logging, or asking about logging standards.
allowed-tools: Read, Write, Edit
---

# Python Structured Logging

Create structured logging statements following project standards.

## Logging Format Requirements

All logs MUST use structured dictionary format with the `msg` parameter.

### Key Fields

- **event** (required) - Past-tense verb + object describing what happened
- **payload** (optional) - Contextual data relevant to the event
- **traceback** (error logs only) - Exception traceback for debugging

### Event Naming Convention

- **Start with verb in past tense** followed by object
- Correct: `"Fetched user data"`, `"Published message"`, `"Started pipeline"`
- Wrong: `"User data fetched"`, `"Message published"`, `"Pipeline started"`

## Templates

### Info Log

```python
import logging

logging.info(
    msg={
        "event": "Fetched user profile",
        "payload": {
            "user_id": user_id,
            "profile_data": profile_data,
        },
    }
)
```

### Error Log (with traceback)

```python
import logging
import traceback

try:
    result = risky_operation()
except Exception as e:
    logging.error(
        msg={
            "event": str(e),
            "payload": {
                "traceback": traceback.format_exc(),
                "operation": "risky_operation",
            },
        }
    )
```

### Warning Log

```python
logging.warning(
    msg={
        "event": "Retried failed request",
        "payload": {
            "attempt": retry_count,
            "max_retries": MAX_RETRIES,
            "endpoint": endpoint,
        },
    }
)
```

### Debug Log

```python
logging.debug(
    msg={
        "event": "Processed batch item",
        "payload": {
            "item_id": item_id,
            "batch_index": index,
        },
    }
)
```

## DO and DON'T

### DO:
- Use structured dictionary format
- Start event with past-tense verb
- Include relevant context in payload
- Include traceback in error logs
- Keep payloads concise

### DON'T:
- Log plain strings: `logging.info("User logged in")`
- Use present tense: `"Fetching user data"`
- Include sensitive data (passwords, tokens, PII)
- Include full request/response bodies (unless necessary)
- Concatenate messages: `logging.info(f"User {user_id} logged in")`

## Complete Example

```python
import logging
import traceback
from typing import Any


def process_data(data: list[dict[str, Any]]) -> dict[str, Any]:
    """Process data items and return results."""
    logging.info(
        msg={
            "event": "Started data processing",
            "payload": {"item_count": len(data)},
        }
    )

    try:
        results = []
        for item in data:
            processed = transform_item(item)
            results.append(processed)

        logging.info(
            msg={
                "event": "Completed data processing",
                "payload": {
                    "input_count": len(data),
                    "output_count": len(results),
                },
            }
        )

        return {"status": "success", "results": results}

    except Exception as e:
        logging.error(
            msg={
                "event": str(e),
                "payload": {
                    "traceback": traceback.format_exc(),
                    "operation": "process_data",
                    "item_count": len(data),
                },
            }
        )
        raise
```

## Reference

See [02-development.md](../../rules/02-development.md#7-logging-standards) for complete guidelines.
