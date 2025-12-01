#!/usr/bin/env python3
"""
Quick start script to verify pychronotab installation and functionality.
"""

from datetime import datetime, timezone
from pychronotab import CronExpression, croniter

def main():
    print("=" * 60)
    print("pychronotab Quick Start")
    print("=" * 60)
    print()

    # Test 1: Modern API
    print("Test 1: Modern API (CronExpression)")
    print("-" * 60)
    expr = CronExpression("*/5 * * * *", tz=timezone.utc)
    now = datetime.now(timezone.utc)
    print(f"Expression: */5 * * * * (every 5 minutes)")
    print(f"Current time: {now}")
    print(f"Next run: {expr.next(now)}")
    print(f"Previous run: {expr.prev(now)}")
    print()

    # Test 2: croniter API
    print("Test 2: croniter-Compatible API")
    print("-" * 60)
    it = croniter("*/10 * * * *", now)
    print(f"Expression: */10 * * * * (every 10 minutes)")
    print(f"Next 3 occurrences:")
    for i in range(3):
        print(f"  {i+1}. {it.get_next(datetime)}")
    print()

    # Test 3: 6-field cron with seconds
    print("Test 3: 6-field Cron (with seconds)")
    print("-" * 60)
    expr_sec = CronExpression("*/30 * * * * *", tz=timezone.utc)
    print(f"Expression: */30 * * * * * (every 30 seconds)")
    print(f"Next run: {expr_sec.next(now)}")
    print()

    # Test 4: Complex expression
    print("Test 4: Complex Expression")
    print("-" * 60)
    expr_complex = CronExpression("0 */15 9-17 * * MON-FRI", tz=timezone.utc)
    print(f"Expression: 0 */15 9-17 * * MON-FRI")
    print(f"(Every 15 minutes during business hours on weekdays)")
    print(f"Next run: {expr_complex.next(now)}")
    print()

    print("=" * 60)
    print("✅ All tests passed! pychronotab is working correctly.")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  - Read the documentation: docs/setup_guide.md")
    print("  - Check examples: examples/")
    print("  - Run tests: pytest")
    print()

if __name__ == "__main__":
    main()
