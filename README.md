# de-claude-rule-shared

This repository contains shared Claude Code rules and configuration for data engineering projects built with:

- **🐍 Python 3.13** - Modern Python with type hints and best practices
- **📦 uv** - Fast, reliable Python package management
- **🧱 Polylith** - Modular architecture for scalable monorepos

Perfect for data engineers building pipelines, managing data assets, and deploying cloud-native applications.

## What's Included

- `.claude/rules/` - Lifecycle-organized rule files:
  - **01-setup.md** - Polylith architecture concepts, monorepo structure, tool versions
  - **02-development.md** - Python code style, docstrings, type hints, logging patterns
  - **03-dependencies.md** - uv package management, pyproject.toml configuration, subset rule
  - **04-testing.md** - Testing standards (🚧 placeholder for future expansion)
  - **05-deployment.md** - Cloud Functions & Docker deployment patterns
  - **06-automation.md** - GitHub Actions CI/CD workflows, git conventions, semantic versioning
- `CLAUDE.md` - Project context file with comprehensive rule index

## Using in Your Repository

### Initial Setup

1. **Add as submodule** (from your repository root):
   ```bash
   git submodule add https://github.com/pulsifi/de-claude-rules-shared.git .claude-shared
   ```

2. **Create symlinks** to make Claude Code find the rules:
   ```bash
   # Create symlink for rules directory
   ln -s .claude-shared/.claude .claude

   # Create symlink for CLAUDE.md
   ln -s .claude-shared/CLAUDE.md CLAUDE.md
   ```

3. **Commit the changes**:
   ```bash
   git add .gitmodules .claude CLAUDE.md
   git commit -m "feat: add shared Claude rules via submodule"
   git push
   ```

### Updating Rules

When rules are updated in the shared repository:

```bash
# Pull latest rules
git submodule update --remote .claude-shared

# Commit the update
git add .claude-shared
git commit -m "chore: update Claude rules to latest version"
git push
```

### Cloning Repository with Submodules

**For new clones:**
```bash
# Clone with submodules initialized
git clone --recurse-submodules <repository-url>
```

**If already cloned without submodules:**
```bash
# Initialize and update submodules
git submodule update --init --recursive
```

## Versioning

This repository uses semantic versioning. Check the [releases page](https://github.com/pulsifi/de-claude-rules-shared/releases) for version history.

### Pinning to Specific Version (Optional)

If you need stability, pin to a specific tag:

```bash
# In your repository
cd .claude-shared
git checkout v1.0.0
cd ..
git add .claude-shared
git commit -m "chore: pin Claude rules to v1.0.0"
```

## Making Changes

### Proposing Updates

1. Fork this repository
2. Create a feature branch: `git checkout -b feat/add-new-rule`
3. Make your changes
4. Submit a pull request with clear description
5. Once merged, all consuming repositories can update

### Testing Changes Locally

Before proposing changes, test in one repository:

```bash
# In consuming repository
cd .claude-shared
git checkout -b test-new-rule
# Make changes
cd ..

# Test with Claude Code
# If successful, push branch and create PR in claude-rules-shared
```

## Repository Structure

```
de-claude-rules-shared/
├── .claude/
│   └── rules/
│       ├── 01-setup.md                    # Polylith architecture & setup
│       ├── 02-development.md              # Python coding standards
│       ├── 03-dependencies.md             # uv & pyproject.toml
│       ├── 04-testing.md                  # Testing standards (placeholder)
│       ├── 05-deployment.md               # Cloud Functions & Docker
│       └── 06-automation.md               # CI/CD & git workflows
├── CLAUDE.md
└── README.md (this file)
```

## Current Tool Versions

See [01-setup.md](.claude/rules/01-setup.md#5-tool-versions) for current versions:
- Python: 3.13
- uv: 0.7.8
- hatchling: Latest compatible
- hatch-polylith-bricks: Latest compatible

## Troubleshooting

### Submodule shows as modified but no changes

This usually means the submodule pointer needs updating:
```bash
git submodule update --remote .claude-shared
```

### Symlinks not working on Windows

Windows requires admin privileges for symlinks. Alternatives:
1. Use Git Bash with developer mode enabled
2. Copy files instead of symlinking (but requires manual updates)

### Claude Code not finding rules

Ensure symlinks are created correctly:
```bash
ls -la | grep claude
# Should show:
# .claude -> .claude-shared/.claude
# CLAUDE.md -> .claude-shared/CLAUDE.md
```

## Support

For questions or issues:
- Create an issue in this repository
- Start a discussion for questions and ideas

## License

MIT License - Feel free to use and adapt for your data engineering projects

