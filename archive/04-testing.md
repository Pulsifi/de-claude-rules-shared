# Testing: Quality Assurance Standards

**When to use this file:** Reference this for testing strategies, test structure, coverage requirements, and data validation patterns.

**Related documentation:**
- For Polylith testing strategy overview, see [01-setup.md](01-setup.md#4-testing-strategy)
- For Python code standards, see [02-development.md](02-development.md)
- For CI/CD test automation, see [06-automation.md](06-automation.md)

---

## Table of Contents

1. [Testing Philosophy](#1-testing-philosophy)
2. [Test Structure and Organization](#2-test-structure-and-organization)
3. [Unit Testing](#3-unit-testing)
4. [Integration Testing](#4-integration-testing)
5. [End-to-End Testing](#5-end-to-end-testing)
6. [Test Coverage Requirements](#6-test-coverage-requirements)
7. [Mocking and Fixtures](#7-mocking-and-fixtures)
8. [Data Testing](#8-data-testing)
9. [Performance Testing](#9-performance-testing)
10. [Best Practices](#10-best-practices)

---

## 1. Testing Philosophy

> **Note:** This section is a placeholder for future comprehensive testing guidelines.

### Test Pyramid

Component tests (unit) → Base tests (integration) → Project tests (E2E)

### Key Principles

- **Test at the right level:** Unit tests for components, integration tests for bases
- **Fast feedback:** Tests should run quickly to enable rapid development
- **Isolated tests:** Each test should be independent and not rely on other tests
- **Readable tests:** Tests serve as documentation - make them clear and descriptive

---

## 2. Test Structure and Organization

> **Note:** Detailed guidelines to be added.

### Directory Structure

```
components/pipeline/logging/
├── __init__.py
├── core.py
└── test/
    ├── __init__.py
    └── test_core.py

bases/pipeline/cdc_processor/
├── __init__.py
├── core.py
└── test/
    ├── __init__.py
    └── test_core.py

projects/cdc_pipeline/
└── test/
    ├── __init__.py
    └── test_integration.py
```

### pytest Configuration

All pytest configuration MUST be defined in the workspace root `pyproject.toml` file under `[tool.pytest.ini_options]`.

**Standard configuration:**
```toml
[tool.pytest.ini_options]
addopts = "--tb=short -v"
testpaths = ["test"]
required_plugins = ["pytest-cov", "pytest-env"]
```

**Configuration options:**
- **addopts:** Default command-line arguments
  - `--tb=short` - Short traceback format for cleaner output
  - `-v` - Verbose mode showing individual test names
- **testpaths:** Directories to search for tests (workspace root `test/` directory)
- **required_plugins:** Ensure critical pytest plugins are installed

**Additional common options:**
```toml
[tool.pytest.ini_options]
addopts = "--tb=short -v"
testpaths = ["test"]
required_plugins = ["pytest-cov", "pytest-env"]
env = [
    "ENVIRONMENT=test",
    "GCP_PROJECT_ID=test-project",
    # Additional test environment variables
]
```

**Key points:**
- Configuration lives in workspace root, not project files
- All projects inherit the same pytest configuration
- Use `pytest-env` plugin for test-specific environment variables
- Keep test paths relative to workspace root

---

## 3. Unit Testing

> **Note:** Component-level testing guidelines to be added.

Topics to cover:
- pytest fixtures and parametrize
- Mocking external dependencies
- Testing pure functions
- Exception testing
- Parametrized tests

---

## 4. Integration Testing

> **Note:** Base-level testing guidelines to be added.

Topics to cover:
- Testing component composition
- API endpoint testing
- Database integration testing
- Message queue testing

---

## 5. End-to-End Testing

> **Note:** Project-level testing guidelines to be added.

Topics to cover:
- Full pipeline testing
- Docker compose for test environments
- Test data management
- Cleanup strategies

---

## 6. Test Coverage Requirements

> **Note:** Coverage standards to be defined.

Placeholder requirements:
- Components: Minimum 80% coverage
- Bases: Minimum 70% coverage
- Critical paths: 100% coverage

---

## 7. Mocking and Fixtures

> **Note:** Mocking patterns to be added.

Topics to cover:
- pytest fixtures
- Mock patterns for external services
- Fixture scope (function, module, session)
- Shared fixtures

---

## 8. Data Testing

> **Note:** Data quality testing to be added.

Topics to cover:
- Schema validation
- Data quality checks
- Great Expectations integration
- dbt test patterns

---

## 9. Performance Testing

> **Note:** Performance testing guidelines to be added.

Topics to cover:
- Load testing
- Stress testing
- Benchmark testing
- Performance regression detection

---

## 10. Best Practices

> **Note:** Testing best practices to be compiled.

### General Guidelines

**DO:**
- Write tests before or alongside production code
- Keep tests simple and focused
- Use descriptive test names
- Test edge cases and error conditions
- Clean up test data and resources

**DON'T:**
- Write tests that depend on execution order
- Hard-code test data that could change
- Test implementation details instead of behavior
- Skip writing tests for "simple" code
- Ignore flaky tests

---

## Contributing to This Document

This is a placeholder document for future testing standards. When expanding this guide, consider including:

1. **pytest configuration** - How to configure pytest in pyproject.toml
2. **Test naming conventions** - Standard patterns for test function names
3. **Assertion patterns** - Recommended assertion styles
4. **Test data management** - Where to store and how to manage test data
5. **CI/CD integration** - Running tests in GitHub Actions
6. **Coverage reporting** - Tools and thresholds for coverage
7. **Test documentation** - Documenting complex test scenarios
8. **Debugging tests** - Strategies for debugging failing tests
9. **Data pipeline testing** - Specific patterns for ETL/ELT testing
10. **Database testing** - Patterns for testing database operations

---

## Quick Reference

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=components --cov=bases

# Run specific test file
uv run pytest test/test_core.py

# Run tests matching pattern
uv run pytest -k "test_user"

# Run with verbose output
uv run pytest -v

# Run failed tests only
uv run pytest --lf
```

### Common pytest Flags

- `-v, --verbose` - Verbose output
- `-k EXPRESSION` - Run tests matching expression
- `--lf, --last-failed` - Run only failed tests
- `--ff, --failed-first` - Run failed tests first
- `-x, --exitfirst` - Exit on first failure
- `--cov=PATH` - Measure coverage for PATH
- `--cov-report=html` - Generate HTML coverage report

---

**Status:** 🚧 Placeholder - Comprehensive guidelines to be added

**Last Updated:** 2024-12-25
