# pychronotab AI Coding Agent Instructions

## Project Overview
**pychronotab** is a modern cron expression iterator designed as a drop-in replacement for the abandoned `croniter` library. Core purpose: solve namespace conflicts when using multiple task schedulers (e.g., `django-celery-beat` + `rq-scheduler`) by providing a clean `pychronotab` namespace.

**Unique features:**
- Dual API: Modern `CronExpression` class + backward-compatible `croniter` wrapper
- 5-field (standard) AND 6-field (with seconds) cron support
- Timezone-aware using Python 3.9+ `zoneinfo` (not `pytz`)
- All imports under `pychronotab` namespace (no conflicts with `python-crontab`)

## Architecture

### Three-Layer Design
1. **`fields.py`**: Parses cron fields into sorted lists of allowed values
   - `CronField` class handles `*`, ranges (`1-5`), steps (`*/5`), lists (`1,3,5`), and name aliases (`JAN-DEC`, `SUN-SAT`)
   - Provides `next_value()` and `prev_value()` for efficient iteration
   
2. **`core.py`**: Modern `CronExpression` API (primary implementation)
   - Uses 6 `CronField` instances (second, minute, hour, day, month, dow)
   - `_advance_to_next_candidate()` optimizes by skipping impossible times (e.g., jumps to next month when day doesn't match)
   - Normalizes all datetimes to `self.tz` (converts or attaches timezone)
   
3. **`compat_croniter.py`**: Stateful wrapper providing full `croniter` API compatibility
   - Tracks `_current` position for `get_next()`/`get_prev()` calls
   - Delegates all logic to `CronExpression` internally

### Field Detection Logic
- 5 fields → assumes `minute hour day month dow` (standard cron)
- 6 fields → assumes `second minute hour day month dow` (extended)
- No explicit format parameter; count determines interpretation

## Development Workflows

### Setup & Testing
```bash
pixi install              # Install all dependencies
pixi run -e test test             # pytest
pixi run -e test test-cov         # pytest with coverage report
pixi run -e lint lint             # ruff check
pixi run -e lint type-check       # mypy
pixi run -e lint check            # Run both lint and type-check
pixi run -e dev ci                # Run complete CI suite (check + test-cov + build)
```

**Note:** Pixi uses feature-based environments. Tasks are defined in features and must be run with the `-e` flag to specify the environment:
- `-e test` for test tasks (pytest, test-cov)
- `-e lint` for lint tasks (lint, type-check, check)
- `-e dev` for dev tasks (build, publish, ci)
- Default environment includes all dev features

**CI runs on:** Python 3.10, 3.11, 3.12, 3.13 × ubuntu/windows/macos

### Key Test Patterns
- Always test with **timezone-aware datetimes** (`tzinfo=timezone.utc`)
- Test boundary conditions: month/year wrap, DST transitions
- Test both `inclusive=True/False` for edge cases
- See `tests/test_core.py` for canonical examples

## Code Conventions

### Type Hints & Imports
- Use `from __future__ import annotations` in all modules
- Type timezone parameters as `Optional[timezone | ZoneInfo]`
- Never use `pytz`—project requires Python 3.9+ for `zoneinfo`

### Exception Handling
- All exceptions inherit from `CroniterError` (for croniter compatibility)
- Raise `CroniterBadCronError` for parsing failures
- Raise `CroniterBadDateError` when iteration exceeds limits (1 year max)

### Timezone Normalization
**Critical:** All datetimes MUST be normalized via `_normalize_datetime()`:
- Naive datetime → attach `self.tz`
- Different timezone → convert to `self.tz` with `astimezone()`
- Example in `core.py` line 53-65

### Day-of-Week Conversion
Python's `datetime.weekday()` returns Mon=0...Sun=6, but cron uses Sun=0...Sat=6. Convert:
```python
cron_dow = (dt.weekday() + 1) % 7
```

## Critical Implementation Details

### Iteration Limits
`_advance_to_next_candidate()` has a 1-year iteration cap to prevent infinite loops on impossible expressions (e.g., `0 0 31 2 *` — Feb 31st never exists).

### Step Value Parsing
In `fields.py`, step syntax `*/5` or `1-10/2` MUST:
1. Validate step > 0
2. Apply step from range start, not global min
3. Include end value if divisible by step

### Return Type Conversion (croniter API)
`croniter.get_next(ret_type)` supports:
- `datetime` → return datetime object
- `float` → return `.timestamp()`
See `compat_croniter.py` lines 68-85 for implementation

## When Adding Features

1. **Add to `CronExpression` first** (`core.py`) — it's the source of truth
2. **Add compatibility wrapper in `croniter`** if needed for backward compatibility
3. **Test both APIs** in separate test files (`test_core.py` vs `test_compat_croniter.py`)
4. Update README examples for both APIs

## Build & Distribution

- Uses **hatchling** with **hatch-vcs** for dynamic versioning from git tags
- Version automatically derived from git tags (no manual version bumping)
- Package is `src/pychronotab/` (src layout prevents import issues)
- `pixi run build` creates wheel + sdist in `dist/`
- Version file auto-generated at `src/pychronotab/_version.py` (gitignored)

## Known Gotchas

- **Don't modify microseconds** except to zero them (cron has second precision max)
- **Always pass `tz` to `CronExpression`** even if using UTC (explicit > implicit)
- **Month/day names are case-insensitive** but stored as uppercase in `fields.py`
- **croniter API is stateful**—calling `get_next()` twice advances twice (unlike `CronExpression.next()` which is pure)
