"""
croniter API compatibility examples.
"""

from datetime import datetime, timezone
from pychronotab import croniter

# Example 1: Basic croniter usage
print("Example 1: Basic croniter API")
base = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
it = croniter("*/5 * * * *", base)

print(f"Starting from: {base}")
print(f"Next: {it.get_next(datetime)}")
print(f"Next: {it.get_next(datetime)}")
print(f"Next: {it.get_next(datetime)}")
print()

# Example 2: Get timestamps instead of datetime
print("Example 2: Get timestamps (float)")
it2 = croniter("*/10 * * * *", base)
print(f"Next (timestamp): {it2.get_next(float)}")
print(f"Next (timestamp): {it2.get_next(float)}")
print()

# Example 3: Iterate backward
print("Example 3: Iterate backward")
it3 = croniter("*/5 * * * *", base)
print(f"Previous: {it3.get_prev(datetime)}")
print(f"Previous: {it3.get_prev(datetime)}")
print()

# Example 4: Infinite iterator
print("Example 4: Infinite iterator (first 5)")
it4 = croniter("*/15 * * * *", base)
for i, dt in enumerate(it4.all_next(datetime)):
    print(f"  {i+1}. {dt}")
    if i >= 4:
        break
print()

# Example 5: 6-field cron with seconds
print("Example 5: 6-field cron (with seconds)")
it5 = croniter("*/30 * * * * *", base)
print(f"Next: {it5.get_next(datetime)}")
print(f"Next: {it5.get_next(datetime)}")
print(f"Next: {it5.get_next(datetime)}")
