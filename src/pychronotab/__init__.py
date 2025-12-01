"""
pychronotab - A modern cron expression iterator with croniter API compatibility.

Supports both 5-field (standard) and 6-field (with seconds) cron expressions.
Designed to avoid namespace conflicts with crontab/python-crontab packages.
"""

from .core import CronExpression
from .compat_croniter import croniter
from .exceptions import CroniterError, CroniterBadCronError, CroniterBadDateError

try:
    from ._version import __version__
except ImportError:
    __version__ = "0.0.0+unknown"

__all__ = ["CronExpression", "croniter", "CroniterError", "CroniterBadCronError", "CroniterBadDateError"]
