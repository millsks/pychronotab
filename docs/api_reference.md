# API Reference

Complete API documentation for pychronotab.

## Table of Contents

- [CronExpression](#cronexpression) - Modern API
- [croniter](#croniter) - Compatibility API
- [Exceptions](#exceptions)
- [Field Parsing](#field-parsing)

---

## CronExpression

Modern, timezone-aware cron expression iterator.

### Constructor

```python
CronExpression(expr: str, tz: timezone | ZoneInfo | None = None)
```

**Parameters:**
- `expr` (str): Cron expression (5 or 6 fields)
- `tz` (timezone | ZoneInfo, optional): Timezone for interpretation (default: UTC)

**Example:**
```python
from datetime import timezone
from pychronotab import CronExpression

expr = CronExpression("*/5 * * * *", tz=timezone.utc)
```

### Methods

#### `next(base=None, *, inclusive=False)`

Get the next occurrence after (or at, if inclusive) base.

**Parameters:**
- `base` (datetime, optional): Starting datetime (default: now in self.tz)
- `inclusive` (bool): If True and base matches, return base (default: False)

**Returns:** datetime - Next matching datetime

**Example:**
```python
from datetime import datetime, timezone

expr = CronExpression("*/5 * * * *", tz=timezone.utc)
now = datetime.now(timezone.utc)
next_run = expr.next(now)
```

#### `prev(base=None, *, inclusive=False)`

Get the previous occurrence before (or at, if inclusive) base.

**Parameters:**
- `base` (datetime, optional): Starting datetime (default: now in self.tz)
- `inclusive` (bool): If True and base matches, return base (default: False)

**Returns:** datetime - Previous matching datetime

**Example:**
```python
prev_run = expr.prev(now)
```

#### `iter(start=None, *, direction='forward', inclusive=False)`

Iterate over occurrences.

**Parameters:**
- `start` (datetime, optional): Starting datetime (default: now)
- `direction` (str): "forward" or "backward" (default: "forward")
- `inclusive` (bool): Include start if it matches (default: False)

**Yields:** datetime - Matching datetimes

**Example:**
```python
for run_time in expr.iter(now, direction="forward"):
    print(run_time)
    if some_condition:
        break
```

---

## croniter

croniter-compatible API for backward compatibility.

### Constructor

```python
croniter(
    expr_format: str,
    start_time: datetime | None = None,
    day_or: bool = True,
    max_years_between_matches: int | None = None,
    **kwargs
)
```

**Parameters:**
- `expr_format` (str): Cron expression (5 or 6 fields)
- `start_time` (datetime, optional): Starting datetime (default: now)
- `day_or` (bool): If True, day_of_month and day_of_week are OR'd (default: True)
- `max_years_between_matches` (int, optional): Not used (for API compatibility)
- `**kwargs`: Additional args for compatibility (ignored)

**Example:**
```python
from datetime import datetime
from pychronotab import croniter

it = croniter("*/5 * * * *", datetime.now())
```

### Methods

#### `get_next(ret_type=datetime)`

Get the next occurrence.

**Parameters:**
- `ret_type` (Type): Return type - `datetime`, `float`, or `int` (default: datetime)

**Returns:** datetime | float | int - Next occurrence

**Example:**
```python
# Get as datetime
next_dt = it.get_next(datetime)

# Get as timestamp
next_ts = it.get_next(float)
```

#### `get_prev(ret_type=datetime)`

Get the previous occurrence.

**Parameters:**
- `ret_type` (Type): Return type - `datetime`, `float`, or `int` (default: datetime)

**Returns:** datetime | float | int - Previous occurrence

**Example:**
```python
prev_dt = it.get_prev(datetime)
```

#### `get_current(ret_type=datetime)`

Get the current occurrence (last returned by get_next/get_prev).

**Parameters:**
- `ret_type` (Type): Return type - `datetime`, `float`, or `int` (default: datetime)

**Returns:** datetime | float | int - Current occurrence

**Raises:** CroniterBadDateError - If get_next/get_prev hasn't been called yet

**Example:**
```python
it.get_next(datetime)
current = it.get_current(datetime)
```

#### `all_next(ret_type=datetime)`

Iterate over all future occurrences.

**Parameters:**
- `ret_type` (Type): Return type - `datetime`, `float`, or `int` (default: datetime)

**Yields:** datetime | float | int - Future occurrences

**Example:**
```python
for dt in it.all_next(datetime):
    print(dt)
    if some_condition:
        break
```

#### `all_prev(ret_type=datetime)`

Iterate over all past occurrences.

**Parameters:**
- `ret_type` (Type): Return type - `datetime`, `float`, or `int` (default: datetime)

**Yields:** datetime | float | int - Past occurrences

**Example:**
```python
for dt in it.all_prev(datetime):
    print(dt)
    if some_condition:
        break
```

#### `set_current(dt)`

Set the current position.

**Parameters:**
- `dt` (datetime): New current datetime

**Example:**
```python
from datetime import datetime, timezone

it.set_current(datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc))
```

#### `get_schedule(ret_type=datetime)`

Alias for `get_current()` for compatibility.

**Parameters:**
- `ret_type` (Type): Return type

**Returns:** datetime | float | int - Current occurrence

### Properties

#### `cur`

Current position as timestamp (for compatibility).

**Returns:** float | None - Current timestamp or None

**Example:**
```python
timestamp = it.cur
```

### Iterator Protocol

The `croniter` class supports Python's iterator protocol:

```python
it = croniter("*/5 * * * *", datetime.now())

for dt in it:
    print(dt)
    if some_condition:
        break
```

---

## Exceptions

### CroniterError

Base exception for all pychronotab errors.

```python
from pychronotab import CroniterError

try:
    # ... code ...
except CroniterError as e:
    print(f"Cron error: {e}")
```

### CroniterBadCronError

Raised when a cron expression is invalid.

```python
from pychronotab import CroniterBadCronError, CronExpression

try:
    expr = CronExpression("invalid cron")
except CroniterBadCronError as e:
    print(f"Invalid cron expression: {e}")
```

### CroniterBadDateError

Raised when a date/time value is invalid.

```python
from pychronotab import CroniterBadDateError
```

---

## Field Parsing

### Supported Syntax

#### Wildcards
- `*` - Any value

#### Specific Values
- `5` - Specific value
- `1,3,5` - List of values

#### Ranges
- `1-5` - Range of values (inclusive)
- `MON-FRI` - Named ranges (for days/months)

#### Steps
- `*/5` - Every 5 units
- `0-30/5` - Every 5 units in range
- `1-10/2` - Every 2 units in range (1, 3, 5, 7, 9)

#### Named Values
- Months: `JAN`, `FEB`, `MAR`, `APR`, `MAY`, `JUN`, `JUL`, `AUG`, `SEP`, `OCT`, `NOV`, `DEC`
- Days: `SUN`, `MON`, `TUE`, `WED`, `THU`, `FRI`, `SAT`

### Field Ranges

| Field | Range | Special Values |
|-------|-------|----------------|
| Second | 0-59 | - |
| Minute | 0-59 | - |
| Hour | 0-23 | - |
| Day of Month | 1-31 | - |
| Month | 1-12 | JAN-DEC |
| Day of Week | 0-6 | SUN-SAT (0=Sunday) |

### Examples

```python
# Every 5 minutes
"*/5 * * * *"

# Every hour at 30 minutes past
"30 * * * *"

# Every day at midnight
"0 0 * * *"

# Every Monday at 9 AM
"0 9 * * MON"

# Every 30 seconds (6-field)
"*/30 * * * * *"

# Business hours on weekdays
"0 9-17 * * MON-FRI"

# First and 15th of month
"0 0 1,15 * *"

# Every quarter
"0 0 1 JAN,APR,JUL,OCT *"

# Complex: Every 15 minutes during business hours on weekdays
"0 */15 9-17 * * MON-FRI"
```

---

## Type Hints

pychronotab includes comprehensive type hints:

```python
from datetime import datetime, timezone
from typing import Iterator
from pychronotab import CronExpression

def schedule_task(expr_str: str) -> datetime:
    expr: CronExpression = CronExpression(expr_str, tz=timezone.utc)
    next_run: datetime = expr.next()
    return next_run

def get_next_runs(expr_str: str, count: int) -> list[datetime]:
    expr: CronExpression = CronExpression(expr_str, tz=timezone.utc)
    iterator: Iterator[datetime] = expr.iter(datetime.now(timezone.utc))
    return [next(iterator) for _ in range(count)]
```

---

## Thread Safety

`CronExpression` objects are immutable and thread-safe. Multiple threads can safely call methods on the same instance.

`croniter` objects maintain internal state and are **not** thread-safe. Each thread should create its own instance.

```python
# ✅ Thread-safe
expr = CronExpression("*/5 * * * *")
# Multiple threads can call expr.next() safely

# ❌ Not thread-safe
it = croniter("*/5 * * * *", datetime.now())
# Each thread needs its own croniter instance
```

---

## Performance Considerations

- Field parsing happens once during construction
- `next()` and `prev()` use efficient value lookups
- Iteration skips impossible times (e.g., Feb 31)
- Maximum search window is 1 year to prevent infinite loops

For high-frequency scheduling (sub-second), consider:
- Pre-computing schedules
- Caching `CronExpression` instances
- Using 6-field cron with seconds field
