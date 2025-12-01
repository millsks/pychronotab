"""
Basic usage examples for pychronotab.
"""

from datetime import datetime, timezone
from pychronotab import CronExpression

# Example 1: Every 5 minutes
print("Example 1: Every 5 minutes")
expr = CronExpression("*/5 * * * *", tz=timezone.utc)
now = datetime.now(timezone.utc)
print(f"Current time: {now}")
print(f"Next run: {expr.next(now)}")
print(f"Next after that: {expr.next(expr.next(now))}")
print()

# Example 2: Every 30 seconds (6-field cron)
print("Example 2: Every 30 seconds")
expr_seconds = CronExpression("*/30 * * * * *", tz=timezone.utc)
print(f"Next run: {expr_seconds.next(now)}")
print()

# Example 3: Daily at midnight
print("Example 3: Daily at midnight")
expr_daily = CronExpression("0 0 * * *", tz=timezone.utc)
print(f"Next midnight: {expr_daily.next(now)}")
print()

# Example 4: Business hours on weekdays
print("Example 4: Every 15 minutes during business hours (9-5) on weekdays")
expr_business = CronExpression("0 */15 9-17 * * MON-FRI", tz=timezone.utc)
next_run = expr_business.next(now)
print(f"Next business hour run: {next_run}")
print()

# Example 5: Iterate over next 5 occurrences
print("Example 5: Next 5 occurrences of '*/10 * * * *'")
expr_iter = CronExpression("*/10 * * * *", tz=timezone.utc)
iterator = expr_iter.iter(now, direction="forward")
for i in range(5):
    print(f"  {i+1}. {next(iterator)}")
