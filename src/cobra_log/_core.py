# -*- coding: utf-8 -*-
# Python version: 3.9
# @TianZhen

from __future__ import annotations
import logging
import warnings
import os
from typing import (Optional, Tuple, List, Dict, Union)

from .handlers import (
    console_handler,
    file_handler,
    stream_handler,
    ConsoleHandler
)
from ._utils import get_log_level
from .exceptions import InvalidHandlerWarning
from .types import (T_LogLevelName, T_Handler)


_LOGGER: logging.Logger = None
_DEBUG_CONSOLE_HANDLER = console_handler()


def add_handler(
    logger: logging.Logger,
    handler: T_Handler,
    /,
    level: Optional[T_LogLevelName] = None,
    conflict: Union[bool, Dict[str, logging.Handler]] = False
):
    """
    Add a log handler to the specified logger.

    Parameters
    ----------
        logger : logging.Logger
            The logger to add the handler.

        handler : T_Handler
            The log handler to be added.
            - _logging.Handler_: The log handler instance to be added;
            - `"console"`: A console handler with the name `"cobra-console"`;
            - `"stdout"`: A stream handler with the name `"stdout"`;
            - _T_PathType_: A file handler with the name of the save path.

        level : Optional[T_LogLevelName], default to `None`
            The lowest level of log output to the handler.
            - _T_LogLevelName_: Set the logging level of this handler;
            - `None`: Keep the handler level unchanged.

        conflict : Union[bool, Dict[str, logging.Handler]], default to `False`
            Control how to handle the conflict when there is an existing handler with the same name as the new handler.
            - `True`: Remove an existing handler with the same name before adding the new handler;
            - _Dict[str,logging.Handler]_: Remove an existing handler in conflict with the same name before adding the new handler;
            - `False`: Keep the existing handler unchanged and add the new handler, which may cause duplicated handler.

    Raises
    ------
        ValueError
            If the :param:`handler` is not a :class:`logging.Handler` instance, `"stdout"` or a valid log file path.
    """
    # get handler instance
    _file_path = None
    if isinstance(handler, logging.Handler):
        # logging.Handler instance
        # set name for handler if not set
        if isinstance(handler, logging.FileHandler):
            _file_path = handler.baseFilename
            if handler.get_name() is None:
                handler.set_name(_file_path)
        elif handler.get_name() is None:
            if isinstance(handler, logging.StreamHandler):
                handler.set_name("stdout")
            elif isinstance(handler, ConsoleHandler):
                handler.set_name("cobra-console")
        # add level
        if level is not None:
            handler.setLevel(get_log_level(level))
        _handler = handler
    elif handler == "console":
        # console handler
        if level is None or level == "debug":
            _handler = _DEBUG_CONSOLE_HANDLER
        else:
            _handler = console_handler(level=level)
    elif handler == "stdout":
        # stream handler
        _handler = stream_handler(level=level or "warning")
    else:
        try:
            _file_path = handler
            _handler = file_handler(_file_path, level=level or "debug")
        except Exception as e:
            raise ValueError(f"Log handler must be a `logging.Handler` instance, `'console'`, `'stdout'` or a valid log file path, got {handler!r}.") from e
    # create log directory
    if _file_path is not None:
        log_dir = os.path.dirname(_file_path)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
    # check conflict
    handler_name = _handler.get_name()
    if conflict is True:
        for h in logger.handlers:
            if h.get_name() == handler_name:
                logger.removeHandler(h)
                break  # only remove the first matched handler
    elif isinstance(conflict, Dict):
        _conflict_handler = conflict.get(handler_name)
        if isinstance(_conflict_handler, logging.Handler):
            logger.removeHandler(_conflict_handler)
    # add handler
    logger.addHandler(_handler)


def use_logger(
    name: str,
    /,
    *handlers: Union[Tuple[T_Handler, ...], T_Handler],
    default_handler: Optional[T_Handler] = "console",
    overwrite_handler: bool = False,
    level: T_LogLevelName = "debug",
    propagate: bool = False
):
    """
    Activate a logger with the specified name, creating it if necessary, and add handlers to it.

    NOTE: Until another logger is activated, all exceptions are processed by the currently active logger.

    Parameters
    ----------
        name : str
            The name of the logger.

        *handlers : Union[Tuple[T_Handler, ...], T_Handler]
            The log handlers to be added to the logger. Each handler can be specified in the following formats:
            - _T_Handler_: The log handler to be added. See also :param:`handler` in :func:`add_handler`;
            - Tuple[T_Handler, T_LogLevelName]: The log handler to be added with the log level for this handler. See also :param:`handler` in :func:`add_handler`.

        default_handler : Optional[T_Handler], default to `"console"`
            The default log handler to be added when there is no handler in the current logger after adding the specified handlers. See also :param:`handler` in :func:`add_handler`.

        overwrite_handler : bool, default to `False`
            Control whether to overwrite an existing handler with the same name for each handler.

            NOTE: It does not affect the handler in the current :param:`handlers`.

        level : T_LogLevelName, default to `"debug"`
            The lowest level of the logger.

        propagate : bool, default to `False`
            Control whether to propagate messages to ancestor loggers.

    Returns
    -------
        logging.Logger
            The logger with the specified name.
    """
    global _LOGGER
    # register (if necessary) and activate logger
    _LOGGER = logging.getLogger(name)
    # logger level
    _new_level = get_log_level(level)
    if _LOGGER.level != _new_level:
        _LOGGER.setLevel(_new_level)
    # propagate
    _LOGGER.propagate = bool(propagate)
    # conflict
    if overwrite_handler and _LOGGER.hasHandlers():
        _conflict = {h.get_name(): h for h in _LOGGER.handlers}
    else:
        _conflict = False
    # add handlers
    for handler in handlers:
        if not handler:
            continue
        _handler = handler
        _handler_level = None
        if isinstance(handler, (Tuple, List)):
            # handler with level
            _handler = handler[0]
            if len(handler) > 1:
                _handler_level = handler[1]
        # add handler
        try:
            add_handler(_LOGGER, _handler, level=_handler_level, conflict=_conflict)
        except ValueError as e:
            warnings.warn(
                f"Failed to add handler {_handler!r} to logger {name!r}: {e}",
                category=InvalidHandlerWarning,
                stacklevel=2
            )
    # add default handler if there is no handler
    if not _LOGGER.hasHandlers() and default_handler is not None:
        try:
            add_handler(_LOGGER, default_handler)
        except ValueError as e:
            warnings.warn(
                f"Failed to add default handler {default_handler!r} to logger {name!r}: {e}",
                category=InvalidHandlerWarning,
                stacklevel=2
            )

    return _LOGGER


use_logger("default")
