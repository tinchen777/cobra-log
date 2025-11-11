# -*- coding: utf-8 -*-
# Python version: 3.9
# @TianZhen

from __future__ import annotations
import logging
from logging.handlers import RotatingFileHandler
import os
from typing import (Any, Optional, Type)

from .types import LogLevelName


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
FILE_HANDLER = None

LOG_FMT = r"%(asctime)s - <%(levelname)s> - <%(filename)s(%(funcName)s)-%(lineno)d> - %(message)s"
DATE_FMT = r"%y-%m-%d %H:%M:%S"


def log_init(
    log_save_path: Optional[str] = None,
    log_level: LogLevelName = "debug",
    log_fmt: str = LOG_FMT,
    date_fmt: str = DATE_FMT,
    cover: bool = True,
    backup_count: int = 0
):
    r"""
    Initialize the log storage configuration.

    NOTE: The log storage configuration can be set multiple times, and only the latest log storage configuration instance is retained.

    Parameters
    ----------
        log_save_path : Optional[str], default to `None`
            The log file storage address. If invalid, no log file output stream is created.

        log_level : LogLevelName, default to `"debug"`
            The lowest level of log file storage, `LogLevelName` includes `"debug"`, `"info"`, `"warning"`, `"error"` and `"critical"`.

        log_fmt : str, default to LOG_FMT
            The log storage format, `LOG_FMT` is defined as `r"%(asctime)s - <%(levelname)s> - <%(filename)s(%(funcName)s)-%(lineno)d> - %(message)s"`.
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
            The time storage format in the log, `DATE_FMT` is defined as `r"%y-%m-%d %H:%M:%S"`.

        cover : bool, default to `True`
            Control whether to cover the latest storage configuration instance.

        backup_count : int, default to `0`
            The number of log file backups.
            - `>0`: rolling log;
            - `<=0`: no backup, all logs are stored in one file.
    """
    # log level
    if log_level == "critical":
        level = logging.CRITICAL
    elif log_level == "error":
        level = logging.ERROR
    elif log_level == "warning":
        level = logging.WARNING
    elif log_level == "info":
        level = logging.INFO
    else:
        level = logging.DEBUG

    global FILE_HANDLER
    if FILE_HANDLER and cover:
        LOGGER.removeHandler(FILE_HANDLER)

    if log_save_path is not None and log_save_path.endswith(".log"):
        # create log directory
        log_dir = os.path.dirname(log_save_path)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        # file handler
        FILE_HANDLER = RotatingFileHandler(
            filename=log_save_path,
            mode="a",
            backupCount=backup_count,
            maxBytes=100*1024,
            delay=True
        )
        LOGGER.addHandler(FILE_HANDLER)
        FILE_HANDLER.setFormatter(logging.Formatter(
            fmt=log_fmt,
            datefmt=date_fmt
        ))
        FILE_HANDLER.setLevel(level)


def exception(exctype: Type[BaseException], val: BaseException, traceback: Optional[Any], stack_level: int = 1):
    r"""
    General exception and `log` record. Stored as `log` requires `log_init()`.

    Parameters
    ----------
        exctype : type[BaseException]
            The type of exception.

        val : BaseException
            The exception statement.

        traceback : Optional[Any]
            The exception trace.

        stack_level : int, default to `1`
            The stack level of the function call.
            - `0`: this function;
            - `1`: the caller of this function;
            - ...
    """
    if FILE_HANDLER:
        LOGGER.critical(
            f"[{exctype.__name__}] - {val}",
            exc_info=(exctype, val, traceback),
            stacklevel=1 + stack_level
        )
