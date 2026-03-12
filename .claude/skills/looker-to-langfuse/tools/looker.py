"""
Looker tools for Claude skill.
LLM never sees raw data — only summaries. Data is written to disk.
"""

import json
import re
import os
import sys
from datetime import datetime
from pathlib import Path

import looker_sdk

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)


def _client():
    # looker.ini must be in the skill root folder
    ini_path = Path(__file__).parent.parent / "looker.ini"
    return looker_sdk.init40(config_file=str(ini_path))


def _snake(text: str) -> str:
    """Convert chart title to snake_case key."""
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def get_dashboard_metadata(dashboard_id: str) -> dict:
    """
    Returns dashboard filters and chart tile summaries.
    LLM uses this to understand what's available before fetching data.
    """
    sdk = _client()
    dashboard = sdk.dashboard(dashboard_id)

    filters = []
    for f in (dashboard.dashboard_filters or []):
        filters.append({
            "name": f.name,
            "title": f.title,
            "type": f.type,
            "default_value": f.default_value,
        })

    tiles = []
    for el in (dashboard.dashboard_elements or []):
        title = el.title or el.note_text or "(untitled)"
        tile_type = "unknown"
        if el.type == "vis":
            vis_type = (el.result_maker and el.result_maker.vis_config or {})
            vis_type = vis_type.get("type", "unknown") if isinstance(vis_type, dict) else "unknown"
            tile_type = "scorecard" if vis_type == "single_value" else "table_or_chart"
        tiles.append({
            "id": el.id,
            "title": title,
            "key": _snake(title),
            "type": tile_type,
        })

    return {
        "dashboard_id": dashboard_id,
        "title": dashboard.title,
        "filters": filters,
        "tiles": tiles,
        "tile_count": len(tiles),
    }


def fetch_dashboard_data(dashboard_id: str, filters: dict, combo_label: str = None) -> dict:
    """
    Fetches all tile data for a given filter combination.
    Writes full data to disk. Returns only a summary to the LLM.

    combo_label: optional label like "combo_01" to identify this run
    """
    sdk = _client()
    dashboard = sdk.dashboard(dashboard_id)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    label = combo_label or timestamp
    out_file = DATA_DIR / f"run_{label}.json"

    payload = {
        "filters": filters,
        "combo_label": label,
        "charts": {}
    }
    summary = []

    for el in (dashboard.dashboard_elements or []):
        title = el.title or "(untitled)"
        key = _snake(title)

        # Get the query from the tile
        query = None
        if el.result_maker and el.result_maker.query:
            query = el.result_maker.query
        elif el.query_id:
            query = sdk.query(el.query_id)

        if not query:
            summary.append({"key": key, "title": title, "status": "no_query"})
            continue

        try:
            # Build inline query with filter overrides
            inline = looker_sdk.models40.WriteQuery(
                model=query.model,
                view=query.view,
                fields=query.fields,
                filters={**(query.filters or {}), **filters},
                sorts=query.sorts,
                limit=str(query.limit or "500"),
            )
            result_raw = sdk.run_inline_query("json", inline)
            rows = json.loads(result_raw)

            payload["charts"][key] = {
                "title": title,
                "rows": rows,
            }
            summary.append({
                "key": key,
                "title": title,
                "row_count": len(rows),
                "status": "ok",
            })
        except Exception as e:
            payload["charts"][key] = {"title": title, "error": str(e)}
            summary.append({"key": key, "title": title, "status": "error", "error": str(e)})

    # Write full data to disk
    out_file.write_text(json.dumps(payload, indent=2, default=str))

    return {
        "saved_to": str(out_file),
        "combo_label": label,
        "filters": filters,
        "chart_summary": summary,
    }


def fetch_all_combinations(dashboard_id: str, filter_combos: list[dict]) -> dict:
    """
    Fetches data for all filter combinations. Saves each to disk.
    Returns only a summary of all runs — no raw data passed to LLM.

    filter_combos: list of dicts, e.g. [{"date": "2025-01", "region": "US"}, ...]
    """
    results = []
    for i, combo in enumerate(filter_combos):
        label = f"combo_{i+1:02d}"
        print(f"Fetching {label} with filters {combo}...", file=sys.stderr)
        summary = fetch_dashboard_data(dashboard_id, combo, combo_label=label)
        results.append(summary)

    all_ok = all(
        all(c["status"] == "ok" for c in r["chart_summary"])
        for r in results
    )

    return {
        "total_combos": len(results),
        "all_ok": all_ok,
        "runs": [
            {
                "combo_label": r["combo_label"],
                "filters": r["filters"],
                "saved_to": r["saved_to"],
                "chart_summary": r["chart_summary"],
            }
            for r in results
        ],
    }


if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "metadata"
    dashboard_id = sys.argv[2] if len(sys.argv) > 2 else None

    if cmd == "metadata" and dashboard_id:
        result = get_dashboard_metadata(dashboard_id)
        print(json.dumps(result, indent=2))
    else:
        print("Usage: python looker.py metadata <dashboard_id>")
