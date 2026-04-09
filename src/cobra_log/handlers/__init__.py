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

Examples
--------
- Basic handler creation::

    from logging import getLogger
    from cobra_log.handlers import console_handler, file_handler

    # Create a logger
    logger = getLogger("my_app")

    # Add console handler with cobra rich formatter
    console = console_handler(level="info")
    logger.addHandler(console)

    # Add file handler for persistent logging
    file = file_handler("logs/app.log", level="debug")
    logger.addHandler(file)

- Logging with rich formatting (formatted for readable terminal output)::

    from logging import getLogger
    from cobra_log.handlers import console_handler

    logger = getLogger("data_processor")
    console = console_handler(
        level="info",
        with_border=True,
        min_width=60
    )
    logger.addHandler(console)
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
