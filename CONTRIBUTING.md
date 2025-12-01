# Contributing to pychronotab

Thank you for your interest in contributing to pychronotab!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pychronotab.git
cd pychronotab
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install in development mode:
```bash
pip install -e .
pip install pytest pytest-cov
```

## Running Tests

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=pychronotab --cov-report=html
```

## Code Style

- Follow PEP 8
- Use type hints where appropriate
- Add docstrings to all public functions/classes
- Keep functions focused and testable

## Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Reporting Issues

When reporting issues, please include:

- Python version
- pychronotab version
- Minimal code to reproduce the issue
- Expected vs actual behavior

## Feature Requests

Feature requests are welcome! Please open an issue describing:

- The use case
- Why existing functionality doesn't cover it
- Proposed API (if applicable)

Thank you for contributing!
