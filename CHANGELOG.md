# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-12-01

### Added
- Initial release
- Full croniter API compatibility
- Support for 5-field (standard) cron expressions
- Support for 6-field cron expressions (with seconds)
- Modern timezone handling with `zoneinfo`
- DST-aware datetime iteration
- `CronExpression` class for modern API
- `croniter` class for backward compatibility
- Comprehensive test suite
- Examples and documentation

### Features
- Zero namespace conflicts with `crontab`/`python-crontab`
- Active maintenance (not abandoned)
- Python 3.9+ support
- Type hints throughout

[0.1.0]: https://github.com/yourusername/pychronotab/releases/tag/v0.1.0
