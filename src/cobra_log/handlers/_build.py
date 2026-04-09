# -*- coding: utf-8 -*-
# Python version: 3.9
# @TianZhen

from __future__ import annotations
import logging
import os
from logging.handlers import RotatingFileHandler
from typing import (Optional, Literal, TYPE_CHECKING)

from ._cobra_handlers import ConsoleHandler
from ._cobra_formatters import CobraRichFormatter
from .._utils import get_log_level

if TYPE_CHECKING:
    from ..types import (LogLevelName, PathType)

_CONSOLE_FMT = r"(%(name)s)%(prefix)s %(stack)s: %(message)s"
_FILE_FMT = r"%(asctime)s - (%(name)s)<%(levelname)s> - %(pathname)s(%(lineno)d) - %(message)s"
_STDOUT_FMT = r"(%(name)s)[%(levelname)s]: %(message)s"
_DATE_FMT = r"%y-%m-%d %H:%M:%S"


def console_handler(
    *,
    level: LogLevelName = "debug",
    log_fmt: str = _CONSOLE_FMT,
    date_fmt: str = _DATE_FMT,
    stackfmt: Optional[str] = None,
    with_border: bool = True,
    min_width: int = 50,
    exc_mode: Literal["cause", "context"] = "context",
    exc_depth: int = -1,
    tb_depth: Optional[int] = -1,
    exc_args_limit: int = -1
) -> ConsoleHandler:
    """
    Create a `console handler` with `cobra rich formatter`.

    NOTE: Name of the console handler is `"cobra-console"`.

    Parameters
    ----------
        level : LogLevelName, default to `"warning"`
            The lowest level of log output to the stream.

        other parameters
            See also :class:`CobraRichFormatter` for details.

    Returns
    -------
        ConsoleHandler
            The console handler for logging.
    """
    handler = ConsoleHandler()
    # add formatter
    handler.setFormatter(CobraRichFormatter(
        fmt=log_fmt,
        datefmt=date_fmt,
        stackfmt=stackfmt,
        with_border=with_border,
        min_width=min_width,
        exc_mode=exc_mode,
        exc_depth=exc_depth,
        tb_depth=tb_depth,
        exc_args_limit=exc_args_limit
    ))
    # add level
    handler.setLevel(get_log_level(level))
    # set name
    handler.set_name("cobra-console")

    return handler


def file_handler(
    save_path: PathType,
    /, *,
    level: LogLevelName = "debug",
    log_fmt: str = _FILE_FMT,
    date_fmt: str = _DATE_FMT,
    mode: str = "a",
    backup_count: int = 0,
    max_bytes: int = 100*1024,
    delay: bool = True
) -> RotatingFileHandler:
    """
    Create a `rotating file handler` with `common formatter`. Open the specified file and use it as the stream for logging.

    NOTE: Name of the file handler is string of :param:`save_path`.

    Parameters
    ----------
        save_path : PathType
            The log file storage address.

        level : LogLevelName, default to `"debug"`
            The lowest level of log file storage.

        log_fmt : str
            The log storage format, default to :attr:`_FILE_FMT`.
            See also :class:`logging.Formatter`.

        date_fmt : str
            The time storage format in the log, default to :attr:`_DATE_FMT`.
            See also :class:`logging.Formatter`.

        mode : str, default to `"a"`
            The file opening mode, including `"a"` for append and `"w"` for overwrite.

        backup_count : int, default to `0`
            The number of log file backups.
            - `>0`: rolling log;
            - `<=0`: no backup, all logs are stored in one file.

        max_bytes : int, default to `100*1024`
            The maximum size of the log file in bytes.
            - `>0`: rolling log when the log file exceeds the specified size;
            - `<=0`: no size limit, all logs are stored in one file.

        delay : bool, default to `True`
            Whether to delay file opening until the first log is emitted.

    Returns
    -------
        logging.RotatingFileHandler
            The file handler for logging.
    """
    # check save_path
    _save_path = os.fspath(save_path)

    handler = RotatingFileHandler(
        filename=_save_path,
        mode=mode,
        backupCount=backup_count,
        maxBytes=max_bytes,
        delay=delay
    )
    # add formatter
    handler.setFormatter(logging.Formatter(
        fmt=log_fmt,
        datefmt=date_fmt
    ))
    # add level
    handler.setLevel(get_log_level(level))
    # set name
    handler.set_name(_save_path)

    return handler


def stream_handler(
    *,
    level: LogLevelName = "warning",
    log_fmt: str = _STDOUT_FMT,
    date_fmt: str = _DATE_FMT,
) -> logging.StreamHandler:
    """
    Create a `stream handler` with `common formatter`.

    NOTE: Name of the stream handler is `"stdout"`.

    Parameters
    ----------
        level : LogLevelName, default to `"warning"`
            The lowest level of log output to the stream.

        log_fmt : str
            The log output format for the stream handler, default to :attr:`_STDOUT_FMT`.
            See also :class:`logging.Formatter`.

        date_fmt : str
            The time storage format in the log, default to :attr:`_DATE_FMT`.
            See also :class:`logging.Formatter`.

    Returns
    -------
        logging.StreamHandler
            The stream handler for logging.
    """
    handler = logging.StreamHandler()
    # add formatter
    handler.setFormatter(logging.Formatter(
        fmt=log_fmt,
        datefmt=date_fmt
    ))
    # add level
    handler.setLevel(get_log_level(level))
    # set name
    handler.set_name("stdout")

    return handler
