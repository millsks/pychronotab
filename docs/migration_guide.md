# Migration Guide from croniter

This guide helps you migrate from the abandoned `croniter` library to `pychronotab`.

## Why Migrate?

- ✅ **Active maintenance** - pychronotab is actively maintained
- ✅ **No namespace conflicts** - works alongside `python-crontab` and other cron libraries
- ✅ **Modern Python** - uses `zoneinfo` instead of `pytz`
- ✅ **6-field cron support** - includes seconds field
- ✅ **Full API compatibility** - drop-in replacement for most use cases

## Quick Migration

### Step 1: Install pychronotab

```bash
pip install pychronotab
pip uninstall croniter  # optional
```

### Step 2: Update imports

**Before:**
```python
from croniter import croniter
```

**After:**
```python
from pychronotab import croniter
```

That's it! Your existing code should work without changes.

## API Compatibility

pychronotab provides full compatibility with croniter's public API:

### Supported Methods

✅ `__init__(expr_format, start_time, day_or, ...)`  
✅ `get_next(ret_type)`  
✅ `get_prev(ret_type)`  
✅ `get_current(ret_type)`  
✅ `all_next(ret_type)`  
✅ `all_prev(ret_type)`  
✅ `set_current(dt)`  
✅ `cur` property  
✅ Iterator protocol (`__iter__`)

### Return Types

Both `datetime` and `float` return types are supported:

```python
from datetime import datetime
from pychronotab import croniter

it = croniter("*/5 * * * *", datetime.now())

# Get datetime
dt = it.get_next(datetime)

# Get timestamp
ts = it.get_next(float)
```

## Code Examples

### Example 1: Basic Usage

**croniter:**
```python
from croniter import croniter
from datetime import datetime

base = datetime(2024, 1, 1, 12, 0)
it = croniter("*/5 * * * *", base)
print(it.get_next(datetime))
```

**pychronotab:**
```python
from pychronotab import croniter  # Only change
from datetime import datetime

base = datetime(2024, 1, 1, 12, 0)
it = croniter("*/5 * * * *", base)
print(it.get_next(datetime))
```

### Example 2: Iteration

**croniter:**
```python
from croniter import croniter
from datetime import datetime

it = croniter("*/10 * * * *", datetime.now())
for dt in it.all_next(datetime):
    print(dt)
    if some_condition:
        break
```

**pychronotab:**
```python
from pychronotab import croniter  # Only change
from datetime import datetime

it = croniter("*/10 * * * *", datetime.now())
for dt in it.all_next(datetime):
    print(dt)
    if some_condition:
        break
```

### Example 3: rq-scheduler Integration

**Before (with croniter):**
```python
from rq_scheduler import Scheduler
from croniter import croniter
from datetime import datetime

scheduler = Scheduler()
scheduler.cron(
    "*/5 * * * *",
    func=my_task,
    queue_name='default'
)
```

**After (with pychronotab):**
```python
from rq_scheduler import Scheduler
from pychronotab import croniter  # Only change
from datetime import datetime

scheduler = Scheduler()
scheduler.cron(
    "*/5 * * * *",
    func=my_task,
    queue_name='default'
)
```

## New Features in pychronotab

While maintaining full compatibility, pychronotab adds new features:

### 1. Modern API

```python
from pychronotab import CronExpression
from datetime import datetime, timezone

expr = CronExpression("*/5 * * * *", tz=timezone.utc)
next_run = expr.next(datetime.now(timezone.utc))
```

### 2. 6-field Cron (with seconds)

```python
from pychronotab import croniter

# Every 30 seconds
it = croniter("*/30 * * * * *", datetime.now())
print(it.get_next(datetime))
```

### 3. Better Timezone Support

```python
from pychronotab import CronExpression
from zoneinfo import ZoneInfo

tz = ZoneInfo("America/New_York")
expr = CronExpression("0 9 * * *", tz=tz)
```

## Troubleshooting

### Issue: Import Error

**Error:**
```
ImportError: cannot import name 'croniter' from 'pychronotab'
```

**Solution:**
Make sure you've installed pychronotab:
```bash
pip install pychronotab
```

### Issue: Timezone Differences

**Problem:** Results differ slightly from croniter when using timezones.

**Explanation:** pychronotab uses `zoneinfo` (Python 3.9+) instead of `pytz`. This provides more accurate DST handling.

**Solution:** If you need exact croniter behavior, ensure your datetimes are timezone-aware and use the same timezone throughout.

### Issue: Namespace Conflict

**Problem:** Still getting conflicts with `crontab` module.

**Explanation:** Make sure you're importing from `pychronotab`, not `croniter` or `crontab`:

```python
# ✅ Correct
from pychronotab import croniter

# ❌ Wrong
from croniter import croniter
from crontab import CronTab
```

## Getting Help

- GitHub Issues: https://github.com/yourusername/pychronotab/issues
- Documentation: https://github.com/yourusername/pychronotab
- Examples: See `examples/` directory in the repository

## Reporting Migration Issues

If you encounter issues during migration, please report them with:

1. Your croniter code (before)
2. Your pychronotab code (after)
3. Expected vs actual behavior
4. Python version and pychronotab version
