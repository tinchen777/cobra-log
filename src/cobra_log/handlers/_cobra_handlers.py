# -*- coding: utf-8 -*-
# Python version: 3.9
# @TianZhen

from __future__ import annotations
import logging

from .._display import display


class ConsoleHandler(logging.Handler):
    """
    Handler for logging to the console, that works well with progress bars from `tqdm` and `rich` consoles.
    """
    def __init__(self, level: int = logging.NOTSET):
        super().__init__(level)

    def emit(self, record: logging.LogRecord):
        try:
            msg = self.format(record)
            if getattr(record, "display", True):
                display(msg)
        except Exception:
            self.handleError(record)
