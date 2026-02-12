# src/cobra_log/handlers.py
# -*- coding: utf-8 -*-
# Python version: 3.9
# @TianZhen
"""
Log handlers for :pkg:`cobra_log` package.

Functions
---------
- :func:`file_handler`: Create a file handler for logging.
- :func:`stream_handler`: Create a stream handler for logging.
"""

from __future__ import annotations
import logging
import os
from logging.handlers import RotatingFileHandler

from .types import (T_LogLevelName, T_PathType)

_LOG_FMT = r"%(asctime)s - <%(levelname)s> - <%(filename)s(%(funcName)s)-%(lineno)d> - %(message)s"
_DATE_FMT = r"%y-%m-%d %H:%M:%S"


def _name_to_level(level: T_LogLevelName, /):
    r"""Get the logging level value from the logging level name."""
    level = str(level).upper()
    return logging._nameToLevel.get(level, logging.NOTSET)


def file_handler(
    save_path: T_PathType,
    /,
    level: T_LogLevelName = "debug",
    log_fmt: str = _LOG_FMT,
    date_fmt: str = _DATE_FMT,
    backup_count: int = 0,
    max_bytes: int = 100*1024
):
    r"""
    Create a rotating file handler for logging. Open the specified file and use it as the stream for logging.

    NOTE: Name of the file handler is :param:`save_path`.

    Parameters
    ----------
        save_path : T_PathType
            The log file storage address.

        level : T_LogLevelName, default to `"debug"`
            The lowest level of log file storage.

        log_fmt : str, default to LOG_FMT
            The log storage format.
            :attr:`_LOG_FMT` is defined as `r"%(asctime)s - <%(levelname)s> - <%(filename)s(%(funcName)s)-%(lineno)d> - %(message)s"`.
            Includes:
            - `%(levelno)s`: log level value;
            - `%(levelname)s`: log level name;
            - `%(pathname)s`: the path of the current executable program, i.e., sys.argv[0];
            - `%(filename)s`: the name of the current executable program;
            - `%(funcName)s`: the current function of the log;
            - `%(lineno)d`: the current line number of the log;
            - `%(asctime)s`: the time of the log;
            - `%(thread)d`: thread ID;
            - `%(threadName)s`: thread name;
            - `%(process)d`: process ID;
            - `%(message)s`: log information;
            - `%(name)s`: log handler name, default to root.

        date_fmt : _type_, default to DATE_FMT
            The time storage format in the log.
            :attr:`_DATE_FMT` is defined as `r"%y-%m-%d %H:%M:%S"`.

        backup_count : int, default to `0`
            The number of log file backups.
            - `>0`: rolling log;
            - `<=0`: no backup, all logs are stored in one file.

        max_bytes : int, default to `100*1024`
            The maximum size of the log file in bytes.
            - `>0`: rolling log when the log file exceeds the specified size;
            - `<=0`: no size limit, all logs are stored in one file.

    Returns
    -------
        logging.RotatingFileHandler
            The file handler for logging.
    """
    # check save_path
    _save_path = os.fspath(save_path)

    handler = RotatingFileHandler(
        filename=_save_path,
        mode="a",
        backupCount=backup_count,
        maxBytes=max_bytes,
        delay=True
    )
    # add formatter
    handler.setFormatter(logging.Formatter(
        fmt=log_fmt,
        datefmt=date_fmt
    ))
    # add level
    handler.setLevel(_name_to_level(level))
    # set name
    handler.set_name(_save_path)

    return handler


def stream_handler(
    level: T_LogLevelName = "warning",
    log_fmt: str = r"(%(name)s)[%(levelname)s]: %(message)s",
    date_fmt: str = _DATE_FMT,
):
    r"""
    Create a stream handler for logging.

    NOTE: Name of the stream handler is `"stdout"`.

    Parameters
    ----------
        level : T_LogLevelName, default to `"warning"`
            The lowest level of log output to the stream.

        log_fmt : str, default to `r"(%(name)s)[%(levelname)s]: %(message)s"`
            The log output format for the stream handler.
            See also :param:`log_fmt` in :meth:`file_handler`.

        date_fmt : _type_, default to DATE_FMT
            The time storage format in the log.

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
    handler.setLevel(_name_to_level(level))
    # set name
    handler.set_name("stdout")

    return handler
