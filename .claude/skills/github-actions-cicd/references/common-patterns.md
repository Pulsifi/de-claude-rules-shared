# Common Workflow Patterns

## Docker Build with Caching

**Sandbox (with cache):**
```yaml
- uses: docker/setup-buildx-action@v3

- uses: docker/build-push-action@v5
  with:
    context: .
    file: ./projects/{name}/Dockerfile
    push: true
    tags: ${{ vars.IMAGE_URL }}:${{ env.VERSION }}
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

**Production (no cache):**
```yaml
- uses: docker/build-push-action@v5
  with:
    context: .
    file: ./projects/{name}/Dockerfile
    push: true
    tags: ${{ vars.IMAGE_URL }}:${{ env.VERSION }}
    # No cache for production - fresh build
```

## GCP Authentication

```yaml
- name: "Authenticate to Google Cloud"
  uses: google-github-actions/auth@v3
  with:
    token_format: "access_token"
    workload_identity_provider: "projects/${{ secrets.GCP_PROJECT_NUMBER }}/locations/global/workloadIdentityPools/gha-${{ vars.ENVIRONMENT }}/providers/pulsifi-github-${{ vars.ENVIRONMENT }}"
    service_account: "github-actions@${{ vars.GCP_PROJECT_ID }}.iam.gserviceaccount.com"
```

## Descriptive Logging

Always echo values before setting outputs:

```yaml
- name: "Configure version tag"
  id: configure-version-tag
  run: |
    TIMESTAMP=$(date -u +%Y%m%d-%H%M%S)
    BRANCH=${GITHUB_REF_NAME//[\/-]/_}
    VERSION=${BRANCH}-${TIMESTAMP}

    echo "Generated sandbox version: ${VERSION}"
    echo "VERSION=${VERSION}" >> $GITHUB_OUTPUT
```

## Environment-Based Logic

```yaml
- name: "Determine stack and version"
  id: determine-stack-version
  run: |
    if [[ "${{ github.event_name }}" == "workflow_dispatch" ]]; then
      STACK="production"
      VERSION=$(echo "${{ github.ref }}" | sed 's|refs/tags/v||')
      echo "Using version from selected tag: ${VERSION}"
    else
      STACK="sandbox"
      TIMESTAMP=$(date -u +%Y%m%d-%H%M%S)
      BRANCH=${GITHUB_REF_NAME//[\/-]/_}
      VERSION=${BRANCH}-${TIMESTAMP}
      echo "Generated sandbox version: ${VERSION}"
    fi

    echo "Deploying to stack: ${STACK} with version: ${VERSION}"
    echo "STACK=${STACK}" >> $GITHUB_OUTPUT
    echo "VERSION=${VERSION}" >> $GITHUB_OUTPUT
```

## Conditional Job Execution

```yaml
jobs:
  provision:
    if: |
      github.event_name == 'workflow_dispatch' ||
      (github.event_name == 'pull_request' && github.event.label.name == 'provision infrastructure')
```

## Permissions

```yaml
permissions:
  id-token: write       # OIDC token for GCP auth
  contents: read        # Read repository
  pull-requests: write  # Comment on PRs
```

## Prohibited Patterns

```yaml
# DON'T hardcode Python version
python-version: "3.13"  # ❌

# DO use version file
python-version-file: "pyproject.toml"  # ✅

# DON'T use latest uv
version: "latest"  # ❌

# DO pin exact version
version: "0.7.8"  # ✅

# DON'T sync without frozen
uv sync  # ❌

# DO use frozen
uv sync --frozen  # ✅

# DON'T cache uv
uses: actions/cache@v4  # ❌ for uv deps
```
