# -*- coding: utf-8 -*-
# Python version: 3.9
# @TianZhen

from __future__ import annotations
import inspect
from typing import (Any, Optional, Union, Literal, Callable)

from . import _core
from ._utils import find_handler
from .exceptions import (
    CriticalErrorException,
    ErrorException,
    WarningException
)


def _parse_stack(stack: Union[bool, int], /, default_level: int = 0):
    """Parse the `stack` parameter to get `stack_info` and `stacklevel`."""
    default_level = max(0, default_level)
    if isinstance(stack, bool):
        return stack, default_level + 3
    elif isinstance(stack, int):
        return True, max(0, stack) + 3
    else:
        raise TypeError(f"`stack` parameter must be `bool` or `int`, got {type(stack).__name__!r}.")


def _log(func: Callable, msg: str, exc: Optional[Any], stack: Union[bool, int], **extra: Any):
    """Log the message with the specified log function and parameters, and return the `fmt_text` and `fmt_msg` attributes from the console handler's formatter if available."""
    if _core._LOGGER.hasHandlers():
        stack_info, stacklevel = _parse_stack(stack)
        func(msg, exc_info=exc, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
        # rich results
        console_handler = find_handler(_core._LOGGER, "cobra-console", formatter_required=True)
        if console_handler is not None and console_handler.formatter is not None:
            fmt_text = getattr(console_handler.formatter, "fmt_text", msg)
            fmt_msg = getattr(console_handler.formatter, "fmt_msg", msg)
            return fmt_text, fmt_msg
    return msg, msg


def critical(
    msg: str = "",
    /,
    exc: Optional[Any] = True,
    *,
    throw: Union[Optional[type[Exception]], Literal["fatal"]] = "fatal",
    stack: Union[bool, int] = True,
    indent: int = 0,
    display: bool = True
):
    """
    `CRITICAL-ERROR` or `FATAL-ERROR` level with `log` record (requires :func:`use_logger`).

    NOTE: Used when the overall program is not running.

    Parameters
    ----------
        msg : str, default to `""`
            Description message.

        exc : Optional[Any], default to `True`
            An instance of exception.
            - _Exception_: Record the exception traceback and message;
            - `True`: Try to catch the exception in the current context. If no exception is caught, no exception information will be recorded;
            - `None`: No exception information will be recorded.

        throw : Union[Optional[type[Exception]], Literal["fatal"]], default to `"fatal"`
            The type of exception to be output after logging, use `raise` to throw the exception.
            - `"fatal"`: Return a :class:`SystemExit` exception with the formatted message, which will cause the program to `exit` immediately;
            - _Exception_: Return the specified exception with the description message;
            - _others_: Return :class:`CriticalErrorException` exception with the description message.

        stack : Union[bool, int], default to `True`
            Control whether to display file function stack information.
            - `True`: Display `CRITICAL` location as stack level `0`;
            - _int_: Display `CRITICAL` location according to stack level. i.e.: `0`: the location where the `CRITICAL` is called; `1`: the location of the parent function that calls the `CRITICAL`.; ...

        indent : int, default to `0`
            The indentation of the `CRITICAL` message of the console handler.

        display : bool, default to `True`
            Control whether to display the formatted message via the console handler.

    Returns
    -------
        SystemExit
            :param:`throw` is `"fatal"`.
        Exception
            :param:`throw` is an Exception class.
        CriticalErrorException
            :param:`throw` not an Exception class and not `"fatal"`.
    """
    fmt_text, fmt_msg = _log(
        _core._LOGGER.critical, msg, exc, stack,
        prefix="{FATAL-ERROR}" if throw == "fatal" else "CRITICAL-ERROR",
        pattern=dict(fg="w", bg="lr", styles={"bold"}),
        border_pattern=dict(frame_style="double", fg="lr", styles={"bold", "blink"}),
        indent=indent,
        display=display
    )
    # throw
    if throw == "fatal":
        return SystemExit(fmt_text)
    elif inspect.isclass(throw) and issubclass(throw, Exception):
        return throw(fmt_msg)
    else:
        return CriticalErrorException(fmt_msg)


def error(
    msg: str = "",
    /,
    exc: Optional[Any] = True,
    *,
    throw: Optional[type[Exception]] = None,
    stack: Union[bool, int] = True,
    indent: int = 0,
    display: bool = True
):
    """
    `ERROR` level with `log` record (requires :func:`use_logger`).

    NOTE: Used when some functions are not running.

    Parameters
    ----------
        msg : str, default to `""`
            Description message.

        exc : Optional[Any], default to `True`
            An instance of exception.
            - _Exception_: Record the exception traceback and message;
            - `True`: Try to catch the exception in the current context. If no exception is caught, no exception information will be recorded;
            - `None`: No exception information will be recorded.

        throw : Optional[type[Exception]], default to `None`
            The type of exception to be output after logging, use `raise` to throw the exception.
            - _Exception_: Return the specified exception with the description message;
            - _others_: Return :class:`ErrorException` exception with the description message.

        stack : Union[bool, int], default to `True`
            Control whether to display file function stack information.
            - `True`: Display `ERROR` location as stack level `0`;
            - _int_: Display `ERROR` location according to stack level. i.e.: `0`: the location where the `ERROR` is called; `1`: the location of the parent function that calls the `ERROR`.; ...

        indent : int, default to `0`
            The indentation of the `ERROR` message of the console handler.

        display : bool, default to `True`
            Control whether to display the formatted message via the console handler.

    Returns
    -------
        Exception
            :param:`throw` is an Exception class.
        ErrorException
            :param:`throw` not an Exception class.
    """
    _, fmt_msg = _log(
        _core._LOGGER.error, msg, exc, stack,
        prefix="ERROR",
        pattern=dict(fg="d", bg="y", styles={"bold"}),
        border_pattern=dict(frame_style="double", fg="y", styles={"bold", "blink"}),
        indent=indent,
        display=display
    )
    # throw
    if inspect.isclass(throw) and issubclass(throw, Exception):
        return throw(fmt_msg)
    else:
        return ErrorException(fmt_msg)


def warning(
    msg: str = "",
    /,
    exc: Optional[Any] = True,
    *,
    throw: Optional[type[Exception]] = None,
    stack: Union[bool, int] = True,
    dim: bool = False,
    indent: int = 0,
    display: bool = True
):
    """
    `WARNING` level with `log` record (requires :func:`use_logger`).

    NOTE: Used when unexpected events occur, and the program can still run normally.

    Parameters
    ----------
        msg : str, default to `""`
            Description message.

        exc : Optional[Any], default to `True`
            An instance of exception.
            - _Exception_: Record the exception traceback and message;
            - `True`: Try to catch the exception in the current context. If no exception is caught, no exception information will be recorded;
            - `None`: No exception information will be recorded.

        throw : Optional[type[Exception]], default to `None`
            The type of exception to be output after logging, use `raise` to throw the exception.
            - _Exception_: Return the specified exception with the description message;
            - _others_: Return :class:`WarningException` exception with the description message.

        stack : bool, default to `True`
            Control whether to display file function stack information.
            - `True`: Display `WARNING` location as stack level `0`;
            - _int_: Display `WARNING` location according to stack level. i.e.: `0`: the location where the `WARNING` is called; `1`: the location of the parent function that calls the `WARNING`.; ...

        dim : bool, default to `False`
            Control whether to dim the `WARNING` message of the console handler.

        indent : int, default to `0`
            The indentation of the `WARNING` message of the console handler.

        display : bool, default to `True`
            Control whether to display the formatted message via the console handler.

    Returns
    -------
        Exception
            :param:`throw` is an Exception class.
        WarningException
            :param:`throw` not an Exception class.
    """
    _, fmt_msg = _log(
        _core._LOGGER.warning, msg, exc, stack,
        prefix="WARNING",
        pattern=dict(fg="y", styles=None if dim else {"bold"}),
        border_pattern=dict(frame_style="light", fg="y", styles={"dim"} if dim else {"bold"}),
        indent=indent,
        display=display
    )
    # throw
    if inspect.isclass(throw) and issubclass(throw, Exception):
        return throw(fmt_msg)
    else:
        return WarningException(fmt_msg)


def info(
    msg: str = "",
    /,
    exc: Optional[Any] = None,
    *,
    stack: Union[bool, int] = False,
    outline: bool = False,
    indent: int = 0,
    display: bool = True
):
    """
    `INFO` level with `log` record (requires :func:`use_logger`).

    NOTE: Used to record key node information.

    Parameters
    ----------
        msg : str, default to `""`
            Description message.

        exc : Optional[Any], default to `None`
            An instance of exception.
            - _Exception_: Record the exception traceback and message;
            - `True`: Try to catch the exception in the current context. If no exception is caught, no exception information will be recorded;
            - `None`: No exception information will be recorded.

        stack : bool, default to `True`
            Control whether to display file function stack information.
            - `True`: Display `INFO` location as stack level `0`;
            - _int_: Display `INFO` location according to stack level. i.e.: `0`: the location where the `INFO` is called; `1`: the location of the parent function that calls the `INFO`.; ...

        outline : bool, default to `False`
            Control whether to highlight the `INFO` message of the console handler.

        indent : int, default to `0`
            The indentation of the `INFO` message of the console handler.

        display : bool, default to `True`
            Control whether to display the formatted message via the console handler.
    """
    _log(
        _core._LOGGER.info, msg, exc, stack,
        prefix="KEY-INFO" if outline else "INFO",
        pattern=dict(fg="lb" if outline else "lg", styles={"bold"}),
        border_pattern=dict(frame_style="light", fg="lb" if outline else "g", styles={"bold"} if outline else None),
        indent=indent,
        display=display
    )


def debug(*args: Any, **kwargs: Any):
    """
    `DEBUG` level with `log` record (requires :func:`use_logger`).

    NOTE: Used for debugging.
    """
    msg = ""
    for arg in args:
        msg += f"\n{arg}"
    for arg_name, arg_val in kwargs.items():
        msg += f"\n[{arg_name}]: {arg_val}"
    # log
    if _core._LOGGER.hasHandlers() and msg:
        stack_info, stacklevel = _parse_stack(True)
        _core._LOGGER.debug(msg, stack_info=stack_info, stacklevel=stacklevel)
