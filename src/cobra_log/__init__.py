# src/cobra_log/__init__.py
"""
cobra-log
===========

A lightweight and easy-to-use logging library for Python.

Functions
---------
- :func:`log_init`: Initialize the logging system.
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
from cobra_log import (log_init, info, warning, error)

# Initialize the log system
log_init("log_save_path.log", use_color=True)

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
```
"""

from ._core import (log_init, enable_color, set_trace)
from ._log_levels import (critical, error, warning, info, debug)
from ._utils import trace_stack


__author__ = "Zhen Tian"
__version__ = "1.2.0"

__all__ = [
    "log_init",
    "enable_color",
    "set_trace",
    "critical",
    "error",
    "warning",
    "info",
    "debug",
    "trace_stack"
]
