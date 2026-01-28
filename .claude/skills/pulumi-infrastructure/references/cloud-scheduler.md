# Cloud Scheduler to Cloud Run Jobs

## Stack Configuration

```yaml
input:projects:
  my-project:
    cloud_scheduler:
      - name: my-job-daily
        target_job: my-job-api2bq
        region: asia-southeast1
        description: Daily data extraction job
        schedule: "0 4 * * *"
        time_zone: Asia/Kuala_Lumpur
```

## Python Implementation

Use `copy()` and `pop()` for custom parameters like `target_job`:

```python
scheduler_configs = project_config.get("cloud_scheduler", [])

for scheduler_config in scheduler_configs:
    # Copy to avoid mutating original
    scheduler = scheduler_config.copy()

    # Pop custom parameters not in Pulumi resource args
    target_job = scheduler.pop("target_job")

    # Build Cloud Run Job URL
    job_url = (
        f"https://{scheduler['region']}-run.googleapis.com"
        f"/apis/run.googleapis.com/v1/namespaces/{gcp_project}/jobs/{target_job}:run"
    )

    gcp.cloudscheduler.Job(
        resource_name=make_resource_name("scheduler", scheduler["name"]),
        **scheduler,  # Spreads name, region, description, schedule, time_zone
        http_target=gcp.cloudscheduler.JobHttpTargetArgs(
            uri=job_url,
            http_method="POST",
            oauth_token=gcp.cloudscheduler.JobHttpTargetOauthTokenArgs(
                service_account_email=service_accounts[project_name].email,
            ),
        ),
    )
```

**Why copy() + pop():**
- `target_job` is custom - used to build URL, not a Pulumi arg
- After popping, remaining keys spread directly to resource

## Common Schedules

| Schedule | Meaning |
|----------|---------|
| `0 4 * * *` | Daily at 4:00 AM |
| `0 */6 * * *` | Every 6 hours |
| `0 0 * * 0` | Weekly on Sunday midnight |
| `0 0 1 * *` | Monthly on 1st at midnight |

## Time Zones

Use IANA time zone names:
- `Asia/Kuala_Lumpur`
- `Asia/Singapore`
- `UTC`
