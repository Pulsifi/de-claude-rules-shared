# Service Accounts with IAM

## Stack Configuration

```yaml
input:projects:
  my-project:
    service_account:
      account_id: cloud-run-my-project
      description: Service account for My Project Cloud Run Jobs
      display_name: Cloud Run Job My Project
    service_account_iam:
      account_id: cloud-run-my-project
      roles:
        - roles/bigquery.admin
        - roles/run.invoker
        - roles/logging.logWriter
        - roles/secretmanager.secretAccessor
```

## Python Implementation

Use dict spread (`**config`) to pass config directly to resource constructor:

```python
service_account_config = project_config["service_account"]

# Create service account using dict spread
service_account = gcp.serviceaccount.Account(
    resource_name=make_resource_name(
        "serviceaccount", service_account_config["account_id"]
    ),
    **service_account_config,  # Spreads account_id, description, display_name
)

# Bind IAM roles
for role in project_config["service_account_iam"]["roles"]:
    gcp.projects.IAMMember(
        resource_name=make_resource_name(
            "iammember", service_account_config["account_id"], role
        ),
        member=service_account.member,
        project=gcp_project,
        role=role,
    )
```

**Why dict spread:**
- YAML config keys match Pulumi resource parameters
- No need to map each property explicitly
- Easy to add new properties without code changes

## Common Roles

| Role | Purpose |
|------|---------|
| `roles/bigquery.admin` | Full BigQuery access |
| `roles/run.invoker` | Invoke Cloud Run services/jobs |
| `roles/logging.logWriter` | Write logs to Cloud Logging |
| `roles/secretmanager.secretAccessor` | Access secrets |
| `roles/storage.objectViewer` | Read Cloud Storage objects |
| `roles/pubsub.publisher` | Publish to Pub/Sub topics |
