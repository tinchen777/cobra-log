# src/cobra_log/types.py
"""
Type definitions for :pkg:`cobra_log` package.
"""

from __future__ import annotations
import logging
from os import PathLike
from typing import (Literal, Union)


T_PathType = Union[str, PathLike[str]]

T_LogLevelName = Literal["debug", "info", "warning", "error", "critical"]

T_Handler = Union[logging.Handler, T_PathType, Literal["stdout", "console"]]
