# Project Context
This is a Python project using Polylith architecture.

## Documentation Structure

This project uses a **hybrid approach** with condensed rules (always-loaded guidelines) and skills (on-demand templates and workflows):

- **Rules** (`.claude/rules/`): Condensed reference guidelines always available in context
- **Skills** (`.claude/skills/`): Interactive templates and step-by-step workflows invoked on demand

---

## Rules (Quick Reference)

Condensed guidelines in `.claude/rules/`. Each rule file points to relevant skills for templates.

| File | Purpose | Related Skills |
|------|---------|----------------|
| [01-setup.md](.claude/rules/01-setup.md) | Architecture & tool config | `polylith-component`, `polylith-base`, `polylith-project`, `polylith-explain` |
| [02-development.md](.claude/rules/02-development.md) | Python coding standards | `python-docstring`, `python-logging`, `python-code-review` |
| [03-dependencies.md](.claude/rules/03-dependencies.md) | uv & pyproject.toml | `uv-dependency`, `pyproject-config` |
| [04-testing.md](.claude/rules/04-testing.md) | Testing standards | *(placeholder - to be expanded)* |
| [05-deployment.md](.claude/rules/05-deployment.md) | Deployment patterns | `cloud-function-deploy`, `dockerfile-polylith`, `kustomize-cloudrun` |
| [06-automation.md](.claude/rules/06-automation.md) | CI/CD & git workflow | `github-workflow`, `conventional-commit`, `pr-description` |

---

## Skills (On-Demand)

Invoke skills for templates, examples, and step-by-step guidance.

### Polylith Architecture
| Skill | Purpose |
|-------|---------|
| `polylith-component` | Create new Polylith components with proper structure |
| `polylith-base` | Create new Polylith bases (entry points) |
| `polylith-project` | Create deployable projects |
| `polylith-explain` | Explain Polylith architecture concepts |

### Python Development
| Skill | Purpose |
|-------|---------|
| `python-docstring` | Generate Google-style docstrings |
| `python-logging` | Create structured logging statements |
| `python-code-review` | Review code for style compliance |

### Dependencies & Configuration
| Skill | Purpose |
|-------|---------|
| `uv-dependency` | uv commands for dependency management |
| `pyproject-config` | pyproject.toml configuration templates |

### Deployment
| Skill | Purpose |
|-------|---------|
| `cloud-function-deploy` | Cloud Functions deployment setup |
| `dockerfile-polylith` | Dockerfile templates for Polylith projects |
| `kustomize-cloudrun` | Kustomize/Cloud Run configuration |

### Automation & Git
| Skill | Purpose |
|-------|---------|
| `github-workflow` | GitHub Actions workflow templates |
| `conventional-commit` | Conventional commit message examples |
| `pr-description` | Pull request description templates |

---

## Quick Navigation

**Creating new code**: Use `polylith-component` or `polylith-base` skills
**Writing docstrings**: Use `python-docstring` skill
**Adding dependencies**: Use `uv-dependency` skill
**Setting up deployment**: Use `cloud-function-deploy` or `dockerfile-polylith` skills
**Writing commits/PRs**: Use `conventional-commit` or `pr-description` skills

---

## Glossary & Key Concepts

Quick definitions of Polylith and architecture-specific terms.

### Polylith Architecture

- **Workspace** - The top-level monorepo directory containing all Polylith bricks, projects, and configuration files
- **Brick** - Fundamental unit of code in Polylith (either a component or base), acting like LEGO bricks you can compose
- **Component** - Reusable, stateless building block encapsulating specific functionality (e.g., `logging`, `settings`, `pubsub`)
- **Base** - Entry point for applications or services that compose components (e.g., `api_server`, `data_transformation`, `cli_tool`)
- **Project** - Deployable unit that specifies which components and bases to include (e.g., microservice, web app, CLI tool)
- **Namespace** - Python package namespace grouping related bricks (e.g., `de_backoffice`, `asset`, `pipeline`)

### Infrastructure & Deployment

- **2-Stack Pattern** - Architectural pattern separating infrastructure foundation (Stack 1) from application deployment (Stack 2)
- **Stack 1: Infrastructure Foundation** - Rarely-changing foundational resources provisioned by Pulumi (service accounts, buckets, IAM, Artifact Registry)
- **Stack 2: Application Deployment** - Frequently-changing application code and deployment configs (Docker images, Cloud Run manifests, Cloud Functions)
- **Kustomize** - Kubernetes-native configuration management tool used for environment-specific Cloud Run manifests
- **Overlay** - Environment-specific configuration patches in Kustomize (e.g., `sandbox`, `production`)

### Tools & Workflows

- **uv** - Fast Python package manager (v0.7.8) replacing pip/poetry for dependency management
- **Pulumi** - Infrastructure as Code tool for provisioning GCP resources declaratively
- **Polylith CLI** - Command-line tool for creating and managing Polylith bricks (`poly create component`)
- **Conventional Commits** - Standardized commit message format enabling automated semantic versioning

### Repository Specifics

- **de_backoffice** - The actual namespace used in this repository (documentation examples may use `asset` or `example`)
- **console-cr** - Cloud Run service name for the Streamlit backoffice console application
- **infrastructure/** - Directory containing all infrastructure definitions (pulumi, cloudrun, cloudfunction)
- **projects/** - Directory containing deployable applications with their own `pyproject.toml`
