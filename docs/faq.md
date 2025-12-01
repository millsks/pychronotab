# Frequently Asked Questions (FAQ)

## General Questions

### What is pychronotab?

pychronotab is a modern Python library for parsing and iterating cron expressions. It provides full compatibility with the abandoned croniter library while adding new features like 6-field cron support (with seconds) and improved timezone handling.

### Why was pychronotab created?

pychronotab was created to solve two main problems:

1. **Namespace conflicts**: When using multiple task schedulers (like django-celery-beat and rq-scheduler), the underlying `crontab` packages would conflict.
2. **Abandoned croniter**: The original croniter library is no longer maintained, but many projects depend on it.

### Is pychronotab a drop-in replacement for croniter?

Yes! Simply change your import:

```python
# Old
from croniter import croniter

# New
from pychronotab import croniter
```

Everything else stays the same.

## Installation & Setup

### What Python versions are supported?

Python 3.9 and higher. We use `zoneinfo` from the standard library, which was introduced in Python 3.9.

### Does pychronotab have any dependencies?

No! pychronotab uses only Python's standard library. No external dependencies required.

### How do I install pychronotab?

```bash
pip install pychronotab
```

### Can I use pychronotab alongside python-crontab?

Yes! That's one of the main reasons pychronotab was created. All imports are under the `pychronotab` namespace, so there are no conflicts with `python-crontab` or other cron libraries.

## Cron Expressions

### What cron formats are supported?

pychronotab supports:

- **5-field cron** (standard Unix cron): `minute hour day month day_of_week`
- **6-field cron** (with seconds): `second minute hour day month day_of_week`

### How do I use the seconds field?

Use a 6-field cron expression:

```python
from pychronotab import CronExpression

# Every 30 seconds
expr = CronExpression("*/30 * * * * *")
```

### What operators are supported?

- `*` - Any value
- `5` - Specific value
- `1-5` - Range
- `*/5` - Step (every 5)
- `1,3,5` - List
- `1-5/2` - Range with step
- `JAN-DEC` - Month names
- `SUN-SAT` - Day names

### Can I use month and day names?

Yes! Both are supported:

```python
# Months
"0 0 1 JAN,APR,JUL,OCT *"  # Quarterly

# Days
"0 9 * * MON-FRI"  # Weekdays
```

### How does day_of_month and day_of_week interaction work?

By default, they are OR'd together (standard cron behavior). If either matches, the expression matches.

```python
# Runs on the 1st of the month OR on Mondays
"0 0 1 * MON"
```

## Timezone Handling

### How do I specify a timezone?

```python
from datetime import timezone
from zoneinfo import ZoneInfo
from pychronotab import CronExpression

# Using UTC
expr = CronExpression("0 9 * * *", tz=timezone.utc)

# Using named timezone
expr = CronExpression("0 9 * * *", tz=ZoneInfo("America/New_York"))
```

### What happens with naive datetimes?

Naive datetimes are interpreted in the expression's timezone:

```python
from datetime import datetime, timezone
from pychronotab import CronExpression

expr = CronExpression("0 9 * * *", tz=timezone.utc)
naive_dt = datetime(2024, 1, 1, 12, 0)  # No timezone

# Will be treated as 2024-01-01 12:00 UTC
next_run = expr.next(naive_dt)
```

### How are DST transitions handled?

pychronotab correctly handles Daylight Saving Time:

- **Spring forward** (missing hour): Skips to the next valid time
- **Fall back** (repeated hour): Uses the first occurrence

```python
from zoneinfo import ZoneInfo
from pychronotab import CronExpression

tz = ZoneInfo("America/New_York")
expr = CronExpression("0 2 * * *", tz=tz)

# During spring forward, 2 AM doesn't exist
# Will return 3 AM instead
```

### Should I use pytz or zoneinfo?

Use `zoneinfo` (Python 3.9+). It's part of the standard library and provides better DST handling.

```python
# ✅ Recommended
from zoneinfo import ZoneInfo
tz = ZoneInfo("America/New_York")

# ❌ Avoid (deprecated)
import pytz
tz = pytz.timezone("America/New_York")
```

## API Usage

### What's the difference between CronExpression and croniter?

- **CronExpression**: Modern, clean API with timezone support
- **croniter**: Backward-compatible API matching the original croniter library

Use `CronExpression` for new code, `croniter` for compatibility.

### How do I get the next N occurrences?

```python
from pychronotab import CronExpression
from datetime import datetime, timezone

expr = CronExpression("*/5 * * * *", tz=timezone.utc)
now = datetime.now(timezone.utc)

# Method 1: Using iter()
iterator = expr.iter(now)
next_5 = [next(iterator) for _ in range(5)]

# Method 2: Using next() repeatedly
occurrences = []
current = now
for _ in range(5):
    current = expr.next(current)
    occurrences.append(current)
```

### How do I check if a datetime matches a cron expression?

Use the internal `_matches()` method (or we can expose it):

```python
from pychronotab import CronExpression
from datetime import datetime, timezone

expr = CronExpression("*/5 * * * *", tz=timezone.utc)
dt = datetime(2024, 1, 1, 12, 5, 0, tzinfo=timezone.utc)

# Check if it matches
matches = expr._matches(dt)  # True
```

### Can I iterate backward in time?

Yes!

```python
# CronExpression API
for dt in expr.iter(now, direction="backward"):
    print(dt)
    if some_condition:
        break

# croniter API
it = croniter("*/5 * * * *", now)
for dt in it.all_prev(datetime):
    print(dt)
    if some_condition:
        break
```

### How do I get timestamps instead of datetime objects?

Use the croniter API with `float` return type:

```python
from pychronotab import croniter
from datetime import datetime

it = croniter("*/5 * * * *", datetime.now())
timestamp = it.get_next(float)  # Returns Unix timestamp
```

## Integration

### How do I use pychronotab with rq-scheduler?

```python
from rq_scheduler import Scheduler
from redis import Redis

# Create scheduler
redis_conn = Redis()
scheduler = Scheduler(connection=redis_conn)

# Schedule with cron
scheduler.cron(
    "*/5 * * * *",  # Every 5 minutes
    func=my_task,
    queue_name='default'
)
```

rq-scheduler will use pychronotab if you've replaced croniter.

### How do I use pychronotab with Celery?

Celery has its own cron implementation, but you can use pychronotab to calculate next run times:

```python
from pychronotab import CronExpression
from datetime import datetime, timezone

expr = CronExpression("*/5 * * * *", tz=timezone.utc)
next_run = expr.next(datetime.now(timezone.utc))

# Use next_run to schedule a task
```

### Can I use pychronotab with Django?

Yes! It works great with django-rq:

```python
# settings.py
RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    },
}

# tasks.py
from pychronotab import CronExpression
from datetime import datetime, timezone

def get_next_run():
    expr = CronExpression("0 0 * * *", tz=timezone.utc)
    return expr.next(datetime.now(timezone.utc))
```

## Performance

### Is pychronotab fast?

Yes! Key optimizations:

- Cron expressions are parsed once during construction
- Field lookups use binary search on sorted values
- Impossible times are skipped (e.g., Feb 31)
- No external dependencies to load

### Can I cache CronExpression instances?

Yes! `CronExpression` objects are immutable and thread-safe:

```python
# Cache at module level
HOURLY_EXPR = CronExpression("0 * * * *")

def get_next_hourly_run():
    return HOURLY_EXPR.next()
```

### What's the performance for sub-second scheduling?

For sub-second scheduling, use 6-field cron:

```python
# Every 100ms would require external scheduling
# But every second works great:
expr = CronExpression("* * * * * *")  # Every second
```

## Troubleshooting

### Why am I getting "No valid values in field" error?

This means your cron expression has an invalid field. Check:

- Field ranges (minute: 0-59, hour: 0-23, etc.)
- Syntax (no spaces in ranges: `1-5` not `1 - 5`)
- Step values are positive

```python
# ❌ Invalid
"0 0 32 * *"  # Day 32 doesn't exist

# ✅ Valid
"0 0 1-31 * *"
```

### Why is my expression not matching expected times?

Common issues:

1. **Timezone mismatch**: Ensure your datetime and expression use the same timezone
2. **Day of week**: Remember 0=Sunday, 6=Saturday
3. **Inclusive flag**: By default, `next()` excludes the base time

```python
# If base is 12:05 and expr is "*/5 * * * *"
expr.next(base, inclusive=False)  # Returns 12:10
expr.next(base, inclusive=True)   # Returns 12:05
```

### Why am I getting different results than croniter?

Possible reasons:

1. **Timezone handling**: pychronotab uses `zoneinfo`, croniter uses `pytz`
2. **DST transitions**: Different handling of ambiguous times
3. **Bug fixes**: pychronotab may have fixed bugs present in croniter

If you find a genuine incompatibility, please report it!

### How do I debug cron expressions?

```python
from pychronotab import CronExpression
from datetime import datetime, timezone

expr = CronExpression("*/5 * * * *", tz=timezone.utc)

# Check the parsed fields
print(expr.minute_field.values)  # [0, 5, 10, 15, ...]
print(expr.hour_field.values)    # [0, 1, 2, ..., 23]

# Test with specific datetime
now = datetime.now(timezone.utc)
print(f"Next: {expr.next(now)}")
print(f"Prev: {expr.prev(now)}")
```

## Contributing

### How can I contribute?

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines. We welcome:

- Bug reports
- Feature requests
- Documentation improvements
- Code contributions

### How do I report a bug?

Open an issue on GitHub with:

1. Python version
2. pychronotab version
3. Minimal code to reproduce
4. Expected vs actual behavior

### Can I add new features?

Yes! Please open an issue first to discuss the feature before implementing it.

## License & Legal

### What license is pychronotab under?

MIT License - free for commercial and personal use.

### Can I use pychronotab in commercial projects?

Yes! The MIT license allows commercial use.

### Is pychronotab affiliated with croniter?

No. pychronotab is an independent project inspired by croniter's API, but not affiliated with or endorsed by the original croniter project.
