# Setup: Polylith Architecture & Tool Configuration

**When to use this file:** Start here for architecture concepts and tool versions.

**Skills available:** Use `polylith-component`, `polylith-base`, `polylith-project`, or `polylith-explain` skills for step-by-step guidance.

---

## Quick Reference

### Tool Versions (Source of Truth)

| Tool | Version | Location |
|------|---------|----------|
| Python | 3.13 | `pyproject.toml` `requires-python` |
| uv | 0.7.8 | CI/CD workflows |
| hatchling | Latest | `[build-system]` |

### Directory Structure

```
workspace-root/
├── pyproject.toml          # Workspace config + ALL dependencies
├── uv.lock                 # Locked versions
├── workspace.toml          # Polylith metadata
├── infrastructure/         # Infrastructure definitions (SEPARATE)
│   ├── cloudrun/           # Kustomize manifests
│   ├── cloudfunction/      # Cloud Function configs
│   └── pulumi/             # IaC (service accounts, storage, IAM)
├── bases/{namespace}/      # Entry points
├── components/{namespace}/ # Reusable libraries
├── projects/               # Deployable applications
├── development/            # Notebooks, experiments
└── test/                   # Tests (mirrors bricks structure)
```

---

## 1. Infrastructure and Application Separation

### Core Principle

| Aspect | Infrastructure (Stack 1) | Application (Stack 2) |
|--------|--------------------------|----------------------|
| Location | `infrastructure/pulumi/` | `projects/` + `infrastructure/cloudrun/` |
| Change Frequency | Rare (weeks/months) | Frequent (daily) |
| Deployment | Manual, requires approval | Automated CI/CD |
| Examples | Service accounts, buckets, IAM | Business logic, APIs |

**Key Insight:** `infrastructure/cloudrun/` and `infrastructure/cloudfunction/` are part of Stack 2 (application), not Stack 1 (foundation).

### What Goes Where

**`infrastructure/` directory:**
- Cloud Run service manifests (Kustomize)
- Cloud Function deployment configs
- Pulumi IaC (service accounts, IAM, buckets)
- Pub/Sub topics, BigQuery datasets

**Polylith workspace (`bases/`, `components/`, `projects/`):**
- Business logic and domain code
- Data processing and transformations
- API routes and CLI commands
- Application configuration

---

## 2. Polylith Core Concepts

### Bricks

| Type | Purpose | Location | Examples |
|------|---------|----------|----------|
| **Component** | Reusable, stateless building blocks | `components/{namespace}/` | `logging`, `settings`, `pubsub` |
| **Base** | Entry points that compose components | `bases/{namespace}/` | `api_server`, `data_processor` |

### Projects

- Deployable units combining bases and components
- Located in `projects/`
- Each has own `pyproject.toml` with subset of workspace dependencies
- Contains deployment config (Dockerfile or copy.sh)

### Brick Relationships

```
Component ──► Component (can import)
Base ──────► Component (can import)
Base ───────✗ Base (cannot import)
Project ───► Base + Components (references in pyproject.toml)
```

---

## 3. Developer Workflow

### Daily Development

```bash
# Single virtual environment for entire monorepo
uv venv
uv sync

# Run commands
uv run pytest test/
uv run ruff check .
uv run pyright
```

### Key Principles

1. **Workspace-first:** Add dependencies to workspace root first, then projects
2. **Test in isolation:** Test components/bases before integrating
3. **Consistent tooling:** All config in workspace `pyproject.toml`

---

## 4. Quick Start Checklist

- [ ] Initialize workspace with `pyproject.toml` and `workspace.toml`
- [ ] Create virtual environment: `uv venv`
- [ ] Set up directory structure
- [ ] Configure workspace-level tools (ruff, pyright)
- [ ] Create `infrastructure/` directory

**For creating bricks and projects, use the Polylith skills.**
