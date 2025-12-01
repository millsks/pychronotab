# pychronotab Project Structure

This document explains the organization of the pychronotab project.

## Directory Structure

```
pychronotab/
├── .github/
│   └── workflows/
│       ├── ci.yml              # CI/CD pipeline
│       └── publish.yml         # PyPI publishing workflow
├── docs/
│   ├── setup_guide.md          # Installation and setup guide
│   └── migration_guide.md      # Migration from croniter
├── examples/
│   ├── basic_usage.py          # Basic usage examples
│   └── croniter_compat.py      # croniter compatibility examples
├── src/
│   └── pychronotab/
│       ├── __init__.py         # Package exports
│       ├── core.py             # CronExpression implementation
│       ├── fields.py           # Cron field parsing
│       ├── compat_croniter.py  # croniter API compatibility
│       └── exceptions.py       # Exception classes
├── tests/
│   ├── __init__.py
│   ├── test_core.py            # CronExpression tests
│   ├── test_fields.py          # Field parsing tests
│   └── test_compat_croniter.py # croniter API tests
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── MANIFEST.in
├── pytest.ini
├── pyproject.toml              # Project configuration
└── README.md                   # Main documentation
```

## Key Files

### Source Code (`src/pychronotab/`)

- **`__init__.py`**: Package entry point, exports public API
- **`core.py`**: Main `CronExpression` class with modern API
- **`fields.py`**: Cron field parsing logic (handles `*`, ranges, steps, etc.)
- **`compat_croniter.py`**: `croniter` class for backward compatibility
- **`exceptions.py`**: Custom exception classes

### Tests (`tests/`)

- **`test_core.py`**: Tests for `CronExpression` functionality
- **`test_fields.py`**: Tests for cron field parsing
- **`test_compat_croniter.py`**: Tests for croniter API compatibility

### Configuration

- **`pyproject.toml`**: Modern Python project configuration (PEP 621)
- **`pytest.ini`**: pytest configuration
- **`MANIFEST.in`**: Specifies files to include in distribution

### Documentation

- **`README.md`**: Main project documentation
- **`docs/setup_guide.md`**: Detailed setup and usage guide
- **`docs/migration_guide.md`**: Guide for migrating from croniter
- **`CONTRIBUTING.md`**: Contribution guidelines
- **`CHANGELOG.md`**: Version history

### Examples

- **`examples/basic_usage.py`**: Examples using modern API
- **`examples/croniter_compat.py`**: Examples using croniter-compatible API

## Development Workflow

### 1. Setup Development Environment

```bash
# Clone repository
git clone https://github.com/yourusername/pychronotab.git
cd pychronotab

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
pip install pytest pytest-cov
```

### 2. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pychronotab --cov-report=html

# Run specific test file
pytest tests/test_core.py

# Run specific test
pytest tests/test_core.py::TestCronExpression::test_every_5_minutes
```

### 3. Build Package

```bash
# Install build tools
pip install build

# Build distribution
python -m build

# This creates:
# - dist/pychronotab-0.1.0.tar.gz (source distribution)
# - dist/pychronotab-0.1.0-py3-none-any.whl (wheel)
```

### 4. Publish to PyPI

```bash
# Install twine
pip install twine

# Upload to TestPyPI first
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ pychronotab

# Upload to PyPI
twine upload dist/*
```

## Architecture Overview

### Core Components

1. **Field Parsing** (`fields.py`)
   - Parses individual cron fields (second, minute, hour, etc.)
   - Handles wildcards, ranges, steps, lists
   - Provides next/prev value lookups

2. **Expression Evaluation** (`core.py`)
   - Combines field constraints
   - Iterates through time to find matches
   - Handles timezone conversions and DST

3. **Compatibility Layer** (`compat_croniter.py`)
   - Wraps `CronExpression` with croniter API
   - Maintains state for iteration
   - Supports multiple return types

### Design Principles

- **Zero external dependencies**: Uses only Python stdlib
- **Timezone-aware by default**: Uses `zoneinfo` (Python 3.9+)
- **Immutable expressions**: `CronExpression` objects are immutable
- **Efficient iteration**: Skips impossible times instead of checking every second
- **Comprehensive testing**: High test coverage with edge cases

## Adding New Features

### Example: Adding a new method to CronExpression

1. **Add method to `core.py`**:
```python
def matches(self, dt: datetime) -> bool:
    """Check if datetime matches the cron expression."""
    return self._matches(dt)
```

2. **Add tests to `tests/test_core.py`**:
```python
def test_matches(self):
    expr = CronExpression("*/5 * * * *", tz=timezone.utc)
    dt_match = datetime(2024, 1, 1, 12, 5, 0, tzinfo=timezone.utc)
    dt_no_match = datetime(2024, 1, 1, 12, 3, 0, tzinfo=timezone.utc)

    assert expr.matches(dt_match)
    assert not expr.matches(dt_no_match)
```

3. **Update documentation** in `README.md` and `docs/setup_guide.md`

4. **Add to `__all__` in `__init__.py`** if it's part of public API

## Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md` with changes
3. Commit changes: `git commit -m "Release v0.2.0"`
4. Tag release: `git tag v0.2.0`
5. Push: `git push && git push --tags`
6. GitHub Actions will automatically publish to PyPI

## Getting Help

- Read the documentation in `docs/`
- Check examples in `examples/`
- Run tests to see expected behavior
- Open an issue on GitHub
