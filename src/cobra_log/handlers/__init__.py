# src/cobra_log/handlers.py
# -*- coding: utf-8 -*-
# Python version: 3.9
# @TianZhen
"""
Log handlers for :pkg:`cobra_log` package.

Functions
---------
- :func:`console_handler`: Build a `console handler` with `cobra rich formatter`.
- :func:`file_handler`: Build a `rotating file handler` with `common formatter`.
- :func:`stream_handler`: Build a `stream handler` with `common formatter`.
Classes
-------
- :class:`ConsoleHandler`: Handler for logging to the console, that works well with progress bars from `tqdm` and `rich` consoles.
- :class:`CobraRichFormatter`: Formatter for logging with rich text, formatted exception trace and dynamic output control.
"""

from ._build import (console_handler, file_handler, stream_handler)
from ._cobra_handlers import ConsoleHandler
from ._cobra_formatters import CobraRichFormatter


__all__ = [
    "console_handler",
    "file_handler",
    "stream_handler",
    "ConsoleHandler",
    "CobraRichFormatter"
]
