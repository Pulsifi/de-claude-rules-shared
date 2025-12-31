---
name: polylith-explain
description: Explain Polylith architecture concepts, monorepo structure, infrastructure separation, and the 2-stack pattern. Use when developers ask about architecture, directory structure, bricks, workspaces, or how components/bases/projects relate.
allowed-tools: Read, Glob, Grep
---

# Polylith Architecture Explainer

Help developers understand the Polylith architecture and project organization.

## Core Concepts

### Workspace
The top-level monorepo directory containing all Polylith building blocks:
- Defined in `workspace.toml` at the workspace root
- Contains all bricks, projects, and configuration
- Single virtual environment for the entire monorepo

### Bricks
Fundamental units of code, like LEGO bricks:

| Type | Purpose | Location | Example |
|------|---------|----------|---------|
| **Component** | Reusable, stateless building blocks | `components/{namespace}/` | `logging`, `settings`, `pubsub` |
| **Base** | Entry points that compose components | `bases/{namespace}/` | `api_server`, `data_processor` |

### Projects
Deployable units that combine bricks:
- Located in `projects/`
- Each has its own `pyproject.toml`
- Specifies which bricks to include
- Contains deployment configuration (Dockerfile, copy.sh)

## Directory Structure

```
workspace-root/
├── pyproject.toml          # Workspace config + ALL dependencies
├── uv.lock                 # Locked dependency versions
├── workspace.toml          # Polylith metadata
├── infrastructure/         # Infrastructure definitions (SEPARATE)
│   ├── cloudrun/           # Cloud Run Kustomize manifests
│   ├── cloudfunction/      # Cloud Function configs
│   └── pulumi/             # IaC for GCP resources
├── bases/
│   └── {namespace}/        # Entry points
├── components/
│   └── {namespace}/        # Reusable libraries
├── projects/               # Deployable applications
├── development/            # Notebooks, experiments
└── test/                   # Tests (mirrors bricks structure)
```

## The 2-Stack Pattern

### Stack 1: Infrastructure Foundation
- **Location:** `infrastructure/pulumi/`
- **Content:** Service accounts, buckets, IAM, Artifact Registry
- **Change frequency:** Rare (weeks/months)
- **Deployment:** Manual, requires approval

### Stack 2: Application
- **Location:** `projects/` + `infrastructure/cloudrun/` or `cloudfunction/`
- **Content:** Application code + deployment configuration
- **Change frequency:** Frequent (multiple times/day)
- **Deployment:** Automated via CI/CD

### Why Separate?
- Fast application deployments (2-3 min vs 15-20 min)
- Independent rollbacks
- Clear ownership boundaries
- Reduced blast radius

## Common Questions

### "Where should I put this code?"

| Code Type | Location |
|-----------|----------|
| Reusable logic (logging, settings, API clients) | `components/` |
| Application entry points (HTTP handlers, CLI) | `bases/` |
| Deployment configuration | `projects/` |
| Infrastructure (service accounts, buckets) | `infrastructure/pulumi/` |
| Cloud Run service config | `infrastructure/cloudrun/` |
| Tests | `test/components/` or `test/bases/` |

### "How do bricks relate to each other?"

```
Component ──► Component (can import)
Base ──────► Component (can import)
Base ───────X Base (cannot import)
Project ───► Base + Components (references in pyproject.toml)
```

### "What's the difference between component and base?"

| Aspect | Component | Base |
|--------|-----------|------|
| Purpose | Reusable library | Application entry point |
| State | Stateless | May handle requests |
| Dependencies | Other components only | Components |
| Deployment | Never deployed alone | Part of project |
| Examples | `logging`, `settings` | `api_server`, `etl_runner` |

## When to Use This Skill

This skill helps when developers ask:
- "What is Polylith?"
- "Where does this code belong?"
- "How do I organize my monorepo?"
- "What's the difference between components and bases?"
- "Why is infrastructure separate?"
- "What's the 2-stack pattern?"

## Reference

For complete details, see:
- [01-setup.md](../../rules/01-setup.md) - Architecture and structure
- [03-dependencies.md](../../rules/03-dependencies.md) - Dependency management
- [05-deployment.md](../../rules/05-deployment.md) - Deployment patterns
