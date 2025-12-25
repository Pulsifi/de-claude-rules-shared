# Project Context
This is a Python project using Polylith architecture.

## Rules

See the detailed rules in `.claude/rules/` for comprehensive guidelines. Below is a quick reference:

| File | Purpose | Key Topics |
|------|---------|-----------|
| [01-setup.md](.claude/rules/01-setup.md) | Monorepo architecture & tool configuration | Polylith concepts (workspace, bricks, components, bases), tool versions (Python 3.13, uv 0.7.8), developer workflow |
| [02-development.md](.claude/rules/02-development.md) | Python coding standards | PEP 8 compliance, ruff formatting, naming conventions, type hints, import ordering, docstrings, logging |
| [03-dependencies.md](.claude/rules/03-dependencies.md) | Dependency & deployment configuration | Workspace vs project config, subset rule (CRITICAL), Cloud Functions copy.sh, Docker COPY patterns, dependency groups |
| [04-testing.md](.claude/rules/04-testing.md) | Testing standards 🚧 | Placeholder for pytest patterns, coverage requirements, data testing (to be expanded) |
| [05-deployment.md](.claude/rules/05-deployment.md) | Deployment patterns | Cloud Functions deployment, Docker containers, deployment strategy decision tree |
| [06-automation.md](.claude/rules/06-automation.md) | CI/CD workflows & version control | GitHub Actions setup, uv installation (0.7.8), `uv sync --frozen`, conventional commits, semantic versioning, PR conventions |

### Quick Navigation

**For architecture questions**: Start with `01-setup.md`
**For code style questions**: See `02-development.md` (comprehensive guide covering code, docstrings, and logging)
**For dependency management**: See `03-dependencies.md` (most comprehensive)
**For testing standards**: See `04-testing.md` (🚧 placeholder - to be expanded)
**For deployment**: See `05-deployment.md`
**For CI/CD & git workflow**: See `06-automation.md`
