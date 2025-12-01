# Setup and Installation Guide

## Installation

### From PyPI (recommended)

```bash
pip install pychronotab
```

### From source

```bash
git clone https://github.com/yourusername/pychronotab.git
cd pychronotab
pip install -e .
```

## Requirements

- Python 3.9 or higher
- No external dependencies (uses stdlib only)

## Quick Start

### Modern API

```python
from datetime import datetime, timezone
from pychronotab import CronExpression

# Create a cron expression
expr = CronExpression("*/5 * * * *", tz=timezone.utc)

# Get next occurrence
now = datetime.now(timezone.utc)
next_run = expr.next(now)
print(f"Next run: {next_run}")

# Get previous occurrence
prev_run = expr.prev(now)
print(f"Previous run: {prev_run}")

# Iterate over occurrences
for run_time in expr.iter(now):
    print(run_time)
    # Break after 5 iterations
    if run_time > now + timedelta(minutes=25):
        break
```

### croniter-Compatible API

```python
from datetime import datetime
from pychronotab import croniter

# Create iterator
it = croniter("*/5 * * * *", datetime.now())

# Get next occurrences
print(it.get_next(datetime))
print(it.get_next(datetime))
print(it.get_next(datetime))
```

## Cron Expression Syntax

### 5-field format (standard)
```
* * * * *
│ │ │ │ │
│ │ │ │ └─── day of week (0-6, SUN-SAT)
│ │ │ └───── month (1-12, JAN-DEC)
│ │ └─────── day of month (1-31)
│ └───────── hour (0-23)
└─────────── minute (0-59)
```

### 6-field format (with seconds)
```
* * * * * *
│ │ │ │ │ │
│ │ │ │ │ └─── day of week (0-6, SUN-SAT)
│ │ │ │ └───── month (1-12, JAN-DEC)
│ │ │ └─────── day of month (1-31)
│ │ └───────── hour (0-23)
│ └─────────── minute (0-59)
└───────────── second (0-59)
```

### Supported operators

- `*` - any value
- `5` - specific value
- `1-5` - range
- `*/5` - step (every 5)
- `1,3,5` - list
- `1-5/2` - range with step
- `JAN-DEC` - month names
- `SUN-SAT` - day names

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

# Every 30 seconds
"*/30 * * * * *"

# Business hours (9-5) on weekdays, every 15 minutes
"0 */15 9-17 * * MON-FRI"

# First day of every month at midnight
"0 0 1 * *"

# Every quarter (Jan, Apr, Jul, Oct) on the 1st at noon
"0 12 1 JAN,APR,JUL,OCT *"
```

## Timezone Handling

pychronotab uses Python's `zoneinfo` module for timezone support:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pychronotab import CronExpression

# Use specific timezone
tz = ZoneInfo("America/New_York")
expr = CronExpression("0 9 * * *", tz=tz)

# Naive datetimes will be interpreted in the expression's timezone
now = datetime.now()  # naive
next_run = expr.next(now)  # will be timezone-aware

# Timezone-aware datetimes will be converted if needed
utc_now = datetime.now(ZoneInfo("UTC"))
next_run = expr.next(utc_now)  # converted to America/New_York
```

## DST Handling

pychronotab correctly handles Daylight Saving Time transitions:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pychronotab import CronExpression

# During DST transition, times are adjusted appropriately
tz = ZoneInfo("America/New_York")
expr = CronExpression("0 2 * * *", tz=tz)

# Will correctly handle the "missing hour" during spring forward
# and the "repeated hour" during fall back
```
