# src/cobra_log/__init__.py
"""
cobra-log
===========

A lightweight and easy-to-use logging library for Python.

Modules
-------
- :mod:`cobra_log.handlers`: Logger handlers.
Functions
---------
- :func:`use_logger`: Activate a logger with the specified name and configuration.
- :func:`add_handler`: Add a log handler to the specified logger.
- :func:`enable_color`: Enable or disable colored output (need :pkg:`cobra-color`).
- :func:`set_trace`: Configure global trace display settings.
- :func:`critical`: Log a critical error message and raise an exception.
- :func:`error`: Log an error message.
- :func:`warning`: Log a warning message.
- :func:`info`: Log an informational message.
- :func:`debug`: Log a debug message.
- :func:`trace_stack`: Trace the stack information of the function call.

Examples
--------

```python
from cobra_log import (use_logger, info, warning, error)

# initialize and activate loggers
use_logger("my_logger_1", "stdout")
use_logger("my_logger_2", "log_save_path.log", "stdout")
# use my_logger_2
try:
    try:
        try:
            1 / 0
        except Exception as e:
            raise error("An error occurred.", throw=None) from e
    except Exception as ee:
        raise error(
            "An error(TimeoutError) occurred.",
            throw=TimeoutError
        ) from ee
except Exception:
    critical("A critical error occurred.", throw=None)
# activate my_logger_1
use_logger("my_logger_1")
# use my_logger_1
warning("A warning occurred.")
info("An info occurred.")
```
"""

from ._core import (enable_color, set_trace, use_logger, add_handler)
from ._log_levels import (critical, error, warning, info, debug)
from ._utils import trace_stack


__author__ = "Zhen Tian"
__version__ = "1.3.0"

__all__ = [
    "use_logger",
    "add_handler",
    "enable_color",
    "set_trace",
    "critical",
    "error",
    "warning",
    "info",
    "debug",
    "trace_stack"
]
