# Looker to Langfuse Dataset

Generate Langfuse evaluation datasets from Looker dashboards.

## Trigger

Use this skill when the user asks to:
- Pull data from a Looker dashboard into Langfuse
- Create or update a Langfuse dataset from Looker
- Generate filter combinations from a Looker dashboard
- Build an eval dataset for Langfuse Playground

## Setup (One-time)

Kelsey needs two credential files in her working directory:

**`looker.ini`** — Looker SDK credentials (provided by DE team):
```ini
[Looker]
base_url=https://your-instance.looker.com
client_id=xxx
client_secret=xxx
```

**`.env`** — Langfuse credentials:
```ini
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

Install dependencies:
```bash
pip install looker-sdk langfuse python-dotenv
```

Copy tools from skill directory to working directory:
```bash
cp -r .claude/skills/looker-to-langfuse/tools ./tools
```

## Procedure

### Step 1: Understand the Dashboard

Run metadata to see available filters and charts:

```bash
python tools/looker.py metadata <dashboard_id>
```

Show Kelsey:
- Available filters (name, type, default value)
- List of charts (title, key, type: scorecard or table_or_chart)

### Step 2: Show Available Filter Options

Run filter-options to show Kelsey what values are selectable for each filter:

```bash
python tools/looker.py filter-options <dashboard_id>
```

This returns:
- **enumeration** filters: fixed list of allowed values (e.g. `day`, `month`, `year`)
- **string** filters: all distinct values currently in Looker (e.g. Company IDs)
- **date_range** filters: reminder to use Looker date syntax (e.g. `90 days`, `2025-01-01 to 2025-03-31`)

### Step 3: Define Filter Combinations

Ask Kelsey how many combinations she wants and which filters to vary.
Generate and confirm the full list before fetching.

Example output to confirm with Kelsey:
```
Combo 01: { "date_filter": "2025-01", "region": "MY" }
Combo 02: { "date_filter": "2025-01", "region": "SG" }
Combo 03: { "date_filter": "2025-02", "region": "MY" }
...
```

### Step 4: Fetch All Combinations

Call `fetch_all_combinations` via Python:

```python
from tools.looker import fetch_all_combinations

result = fetch_all_combinations(
    dashboard_id="123",
    filter_combos=[
        {"date_filter": "2025-01", "region": "MY"},
        {"date_filter": "2025-01", "region": "SG"},
        # ...
    ]
)
print(result)  # Summary only — row counts, statuses
```

Each combination is saved to `data/run_combo_XX.json`. Raw data never enters LLM context.

Review the summary with Kelsey. If any chart has many rows (>100), ask:
> "Chart `<key>` returned N rows. Keep all or truncate to a smaller number?"

### Step 5: Choose Dataset

Check existing Langfuse datasets:

```bash
python tools/langfuse_upload.py list
```

Ask Kelsey:
> "Do you want to create a new dataset, or append to an existing one?"

### Step 6: Upload to Langfuse

```python
from tools.langfuse_upload import upload_to_langfuse
from pathlib import Path

run_files = sorted(Path("data").glob("run_combo_*.json"))

result = upload_to_langfuse(
    run_files=[str(f) for f in run_files],
    dataset_name="my-dataset-name",
    truncate_tables_to=50,  # or None to keep all rows
)
print(result)
```

Confirm with Kelsey: items uploaded, warnings, dataset name.

## Dataset Item Shape

Each item = one filter combination:

```json
{
  "input": {
    "chart_title_snake_case": 42,              // scorecard: single value
    "another_chart_title": [                   // table: array of rows
      {"col_a": "val", "col_b": 10},
      ...
    ]
  },
  "metadata": {
    "filters_applied": {"date_filter": "2025-01", "region": "MY"},
    "source_file": "run_combo_01.json"
  }
}
```

## Key Principles

- **Never read `data/*.json` files into context** — they can be very large. Use summaries only.
- **Raw data lives on disk** — tools write to `data/`, LLM only sees row counts and chart names.
- **Truncation is Kelsey's decision** — always ask before truncating, never silently truncate.
- **`create_dataset` is idempotent** — safe to re-run; items are always appended.

## Troubleshooting

### Credentials missing
```
KeyError: LANGFUSE_PUBLIC_KEY
```
Check that `.env` exists and is filled in. Run `cat .env` to verify (never share keys).

### Tile has no query
Some tiles (text boxes, embedded content) have no underlying query — they are skipped with status `no_query`. This is expected.

### Tile fetch error
One tile failing does not abort the run. Review the summary — if a critical chart errors, check filters are valid for that tile's model/view.

### Module not found
Ensure tools were copied to the working directory:
```bash
ls tools/looker.py tools/langfuse_upload.py
```
