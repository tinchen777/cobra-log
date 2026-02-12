# -*- coding: utf-8 -*-
# Python version: 3.9
# @TianZhen

from __future__ import annotations
import logging
import warnings
import os
from typing import (Any, Optional, Tuple, List, Dict, Union)

from .handlers import (_name_to_level, file_handler, stream_handler)
from .exceptions import InvalidHandlerWarning
from .types import (T_LogLevelName, T_Handler)


# === cstr & smart_print ===
try:
    from cobra_color import (cstr as t_cstr, safe_print as t_safe_print)  # type: ignore
    _COLOR_AVAIL = True
except ImportError:
    warnings.warn(
        "Missing color library `cobra-color`, terminal color display unavailable for `cobra-log`.",
        category=ImportWarning,
        stacklevel=3
    )
    _COLOR_AVAIL = False

_USE_COLOR: bool = _COLOR_AVAIL


def cstr(*objects: Any, sep: str = "", **kwargs):
    if _USE_COLOR:
        return t_cstr(*objects, sep=sep, **kwargs)
    return sep.join(objects)


def display(*args, **kwargs):
    if _COLOR_AVAIL:
        return t_safe_print(*args, **kwargs)
    print(*args, **kwargs)


def enable_color(flag: bool = True, /):
    r"""
    Enable or disable colored terminal display. Requires :pkg:`cobra-color`.
    """
    global _USE_COLOR
    _USE_COLOR = flag and _COLOR_AVAIL


# === trace display ===
_TRACE_CONFIG = {
    "with_border": True,
    "exc_mode": "context",
    "exc_depth": -1,
    "tb_depth": -1,
    "exc_args_limit": -1,
    "min_width": 50
}


def set_trace(**kwargs: Any):
    r"""
    Set the global trace display configuration.

    Parameters
    ----------
        **kwargs : Any
            The trace display configuration to be updated. Including:
            - `with_border`: bool
            - `exc_mode`: Literal["cause", "context"]
            - `exc_depth`: int
            - `tb_depth`: Optional[int]
            - `exc_args_limit`: int
    """
    global _TRACE_CONFIG
    _TRACE_CONFIG.update(kwargs)


# === log ===
_ACTIVATED_LOGGER: logging.Logger = None


def add_handler(
    logger: logging.Logger,
    handler: T_Handler,
    /,
    level: Optional[T_LogLevelName] = None,
    conflict: Union[bool, Dict[str, logging.Handler]] = False
):
    r"""
    Add a log handler to the specified logger.

    Parameters
    ----------
        logger : logging.Logger
            The logger to add the handler.

        handler : T_Handler
            The log handler to be added.
            - _logging.Handler_: The log handler instance to be added;
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
        # set name
        if isinstance(handler, logging.FileHandler):
            _file_path = handler.baseFilename
            handler.set_name(_file_path)
        elif isinstance(handler, logging.StreamHandler):
            handler.set_name("stdout")
        # add level
        if level is not None:
            handler.setLevel(_name_to_level(level))
        _handler = handler
    elif handler == "stdout":
        # stream handler
        _handler = stream_handler(level=level or "warning")
    else:
        try:
            _file_path = handler
            _handler = file_handler(_file_path, level=level or "debug")
        except Exception as e:
            raise ValueError(f"Log handler must be a `logging.Handler` instance, `'stdout'` or a valid log file path, got {handler!r}.") from e
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
    overwrite_handler: bool = False,
    level: T_LogLevelName = "debug",
    propagate: bool = False
):
    r"""
    Activate a logger with the specified name, creating it if necessary, and add handlers to it.

    NOTE: Until another logger is activated, all exceptions are processed by the currently active logger.

    Parameters
    ----------
        name : str
            The name of the logger.

        *handlers : Union[Tuple[T_Handler, ...], T_Handler]
            The log handlers to be added to the logger. Each handler can be specified in the following formats:
            - _T_Handler_: The log handler to be added. See also :param:`handler` in :meth:`add_handler`;
            - Tuple[T_Handler, T_LogLevelName]: The log handler to be added with the log level for this handler. See also :param:`handler` in :meth:`add_handler`.

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
    global _ACTIVATED_LOGGER
    # register (if necessary) and activate logger
    _ACTIVATED_LOGGER = logging.getLogger(name)
    # logger level
    _new_level = _name_to_level(level)
    if _ACTIVATED_LOGGER.level != _new_level:
        _ACTIVATED_LOGGER.setLevel(_new_level)
    # propagate
    _ACTIVATED_LOGGER.propagate = bool(propagate)
    # conflict
    _conflict = overwrite_handler
    if _conflict is True:
        _conflict = {h.get_name(): h for h in _ACTIVATED_LOGGER.handlers}
    # add handlers
    for handler in handlers:
        if not handler:
            continue
        _handler = handler
        _handler_level = None
        if isinstance(handler, (Tuple, List)):
            _handler = handler[0]
            if len(handler) > 1:
                _handler_level = handler[1]
        # add handler
        try:
            add_handler(_ACTIVATED_LOGGER, _handler, level=_handler_level, conflict=_conflict)
        except ValueError as e:
            warnings.warn(
                f"Failed to add handler {_handler} to logger '{name}': {e}",
                category=InvalidHandlerWarning,
                stacklevel=3
            )

    return _ACTIVATED_LOGGER


use_logger("default")
