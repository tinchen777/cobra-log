# src/cobra_log/__init__.py
"""
cobra-log
----

A lightweight Python package for terminal display enhancements.


```
"""
from . import exceptions

from .core import (log_init, exception)
from .log_levels import (critical, error, warning, info, debug)
from .utils import (trace_exc, stack_trace)


__author__ = "Zhen Tian"
__version__ = "0.1.0"

__all__ = [
    "exceptions",
    "log_init",
    "exception",
    "critical",
    "error",
    "warning",
    "info",
    "debug",
    "trace_exc",
    "stack_trace"
]
