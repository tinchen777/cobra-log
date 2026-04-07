# src/cobra_log/types.py
"""
Type definitions for :pkg:`cobra_log` package.
"""

from __future__ import annotations
import logging
from os import PathLike
from typing import (Literal, Union)


PathType = Union[str, PathLike[str]]

LogLevelName = Literal["debug", "info", "warning", "error", "critical"]

HandlerType = Union[logging.Handler, PathType, Literal["stdout", "console"]]
