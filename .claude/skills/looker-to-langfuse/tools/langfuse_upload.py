"""
Langfuse upload tool for Claude skill.
Reads data files from disk — never routes raw data through the LLM.
"""

import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from langfuse import Langfuse

load_dotenv()  # searches from cwd upward

DATA_DIR = Path.cwd() / "data"


def _client():
    return Langfuse(
        public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
        secret_key=os.environ["LANGFUSE_SECRET_KEY"],
        host=os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com"),
    )


def list_existing_datasets() -> dict:
    """Returns existing Langfuse datasets so Kelsey can choose to append or create new."""
    host = os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com")
    public_key = os.environ["LANGFUSE_PUBLIC_KEY"]
    secret_key = os.environ["LANGFUSE_SECRET_KEY"]
    auth = (public_key, secret_key)

    response = requests.get(f"{host}/api/public/v2/datasets", auth=auth)
    response.raise_for_status()
    datasets = response.json().get("data", [])

    result = []
    for d in datasets:
        count_resp = requests.get(
            f"{host}/api/public/dataset-items",
            params={"datasetName": d["name"], "limit": 1},
            auth=auth,
        )
        count_resp.raise_for_status()
        total = count_resp.json().get("meta", {}).get("totalItems", "?")
        result.append({"name": d["name"], "item_count": total})

    return {"datasets": result}


def upload_to_langfuse(
    run_files: list[str],
    dataset_name: str,
    truncate_tables_to: int = None,
) -> dict:
    """
    Reads run JSON files from disk and uploads each as a dataset item.
    Each run file = one dataset item (one filter combination).

    run_files: list of file paths returned by fetch_dashboard_data / fetch_all_combinations
    dataset_name: Langfuse dataset name (created if not exists)
    truncate_tables_to: if set, truncate table rows to this number per chart
    """
    lf = _client()

    # Create or get dataset (Langfuse create_dataset is idempotent)
    lf.create_dataset(name=dataset_name)

    uploaded = 0
    skipped = 0
    warnings = []

    for file_path in run_files:
        path = Path(file_path)
        if not path.exists():
            skipped += 1
            warnings.append(f"File not found: {file_path}")
            continue

        run = json.loads(path.read_text())
        filters = run.get("filters", {})
        charts = run.get("charts", {})

        # Build the dataset item input
        item_input = {}
        for key, chart in charts.items():
            if "error" in chart:
                item_input[key] = {"error": chart["error"]}
                continue

            rows = chart.get("rows", [])

            if len(rows) == 1:
                # Scorecard — store as single value if single field
                values = list(rows[0].values())
                item_input[key] = values[0] if len(values) == 1 else rows[0]
            else:
                # Table — optionally truncate
                if truncate_tables_to and len(rows) > truncate_tables_to:
                    warnings.append(
                        f"{key}: truncated from {len(rows)} to {truncate_tables_to} rows"
                    )
                    rows = rows[:truncate_tables_to]
                item_input[key] = rows

        lf.create_dataset_item(
            dataset_name=dataset_name,
            input=item_input,
            metadata={"filters_applied": filters, "source_file": path.name},
        )
        uploaded += 1

    return {
        "dataset_name": dataset_name,
        "uploaded": uploaded,
        "skipped": skipped,
        "warnings": warnings,
    }


if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"

    if cmd == "list":
        print(json.dumps(list_existing_datasets(), indent=2))
    elif cmd == "upload" and len(sys.argv) >= 4:
        files = sys.argv[2:-1]
        dataset = sys.argv[-1]
        result = upload_to_langfuse(files, dataset)
        print(json.dumps(result, indent=2))
    else:
        print("Usage:")
        print("  python langfuse_upload.py list")
        print("  python langfuse_upload.py upload <file1> <file2> ... <dataset_name>")
