# -*- coding: utf-8 -*-
# Python version: 3.9
# @TianZhen

from __future__ import annotations
import sys
import inspect
from typing import (Any, Optional, Union, Literal)

from . import _core
from ._exceptions import (
    CriticalErrorException,
    ErrorException,
    WarningException
)
from ._utils import (trace_exc, trace_stack, box_lines, _fmt_msg)


_EXC_FMT = r" [%(fileName)s->%(funcName)s(%(lineno)d)]"
_FRAME_GAP = 2


def _fmt_main(prefix: str, msg: str = "", /, loc: Union[bool, int] = True, indent: int = 0, **pattern: Any):
    r"""Format the main message."""
    _msg = _fmt_msg(msg)
    # location information
    if loc is False:
        loc_info = ""
    else:
        loc_level = 0 if loc is True else max(0, int(loc))
        loc_info = trace_stack(loc_level + 3, fmt=_EXC_FMT)
    # main message
    main_msg = _core.cstr(f"{prefix}{loc_info}: {_msg}", **pattern)
    # indent
    if indent > 0:
        main_msg = _core.cstr(" " * indent, main_msg)

    return main_msg, _msg


def _fmt_exc(exc: Any, /, top_indent: int, frame_style: str, indent: int = 0, **pattern: Any):
    r"""Format the exception trace."""
    # exception
    if exc is None:
        exc = sys.exc_info()[1]  # try to get the current exception
    if not exc:
        return "", None

    with_border = bool(_core._TRACE_CONFIG.get("with_border", True))
    # exception message
    exc_msg = trace_exc(
        exc,
        mode=_core._TRACE_CONFIG.get("exc_mode", "context"),
        exc_depth=_core._TRACE_CONFIG.get("exc_depth", -1),
        tb_depth=_core._TRACE_CONFIG.get("tb_depth", -1),
        exc_args_limit=_core._TRACE_CONFIG.get("exc_args_limit", -1),
        indent=3 if with_border else 4
    )
    # box lines
    if with_border:
        exc_msg = box_lines(
            exc_msg.splitlines()[1:],
            top_indent=top_indent + _FRAME_GAP,
            rest_indent=indent,
            frame_style=frame_style,
            **pattern
        )

    return exc_msg, exc


def critical(
    msg: str = "",
    /,
    exc: Optional[Any] = None,
    throw: Union[Optional[Exception], Literal["fatal"]] = "fatal",
    loc: Union[bool, int] = True,
    display: bool = True
):
    r"""
    `CRITICAL-ERROR` or `FATAL-ERROR` level with `log` record (requires :func:`log_init`).

    NOTE: Used when the overall program is not running.

    Parameters
    ----------
        msg : str, default to `""`
            Description message.

        exc : Optional[Any], default to `None`
            An instance of exception.
            - _Exception_: Record the exception traceback and message;
            - `None`: Try to catch the exception in the current context. If no exception is caught, no exception information will be recorded;
            - `""`: No exception information will be recorded.

        throw : Union[Optional[Exception], Literal["fatal"]], default to `"fatal"`
            The type of exception to be output after logging, use `raise` to throw the exception.
            - `"fatal"`: Return a :class:`SystemExit` exception with the formatted message, which will cause the program to `exit` immediately;
            - _Exception_: Return the specified exception with the description message;
            - `None`: Return :class:`CriticalErrorException` exception with the description message.

        loc : Union[bool, int], default to `True`
            Control whether to display file function location information.
            - `True`: Display `CRITICAL` location as stack level `1`;
            - _int_: Display `CRITICAL` location according to stack level. i.e.: `0`: the location where the `CRITICAL` is called; `1`: the location of the parent function that calls the `CRITICAL`.; ...

        display : bool, default to `True`
            Control whether to display the formatted message.

    Returns
    -------
        SystemExit
            :param:`throw` is `"fatal"`.
        Exception
            :param:`throw` is an Exception class.
        CriticalErrorException
            :param:`throw` is `None`.
    """
    # main message
    prefix = "{FATAL-ERROR}" if throw == "fatal" else "CRITICAL-ERROR"
    main_msg, _msg = _fmt_main(prefix, msg, loc=loc, fg="w", bg="lr", styles={"bold"})
    # exception message
    exc_msg, exc = _fmt_exc(exc, top_indent=len(main_msg), frame_style="double", fg="lr", styles={"bold", "blink"})
    # log
    if _core._FILE_HANDLER:
        _core._LOGGER.critical(str(_msg), exc_info=exc, stack_info=True, stacklevel=2)
    # combine
        final_msg = _core.cstr(main_msg, " " * _FRAME_GAP, exc_msg)
    # display
    if display:
        _core.display(final_msg)
    # throw
    if throw == "fatal":
        return SystemExit(final_msg)
    elif inspect.isclass(throw) and issubclass(throw, Exception):
        return throw(_msg)
    else:
        return CriticalErrorException(_msg)


def error(
    msg: str = "",
    /,
    exc: Optional[Any] = None,
    throw: Optional[Exception] = None,
    loc: Union[bool, int] = True,
    display: bool = True
):
    r"""
    `ERROR` level with `log` record (requires :func:`log_init`).

    NOTE: Used when some functions are not running.

    Parameters
    ----------
        msg : str, default to `""`
            Description message.

        exc : Optional[Any], default to `None`
            An instance of exception.
            - _Exception_: Record the exception traceback and message;
            - `None`: Try to catch the exception in the current context. If no exception is caught, no exception information will be recorded;
            - `""`: No exception information will be recorded.

        throw : Optional[Exception], default to `None`
            The type of exception to be output after logging.
            - _Exception_: Return the specified exception with the description message;
            - `None`: Return :class:`ErrorException` exception with the description message.

        loc : Union[bool, int], default to `True`
            Control whether to display file function location information.
            - `True`: Display `ERROR` location as stack level `1`;
            - _int_: Display `ERROR` location according to stack level. i.e.: `0`: the location where the `ERROR` is called; `1`: the location of the parent function that calls the `ERROR`.; ...

        display : bool, default to `True`
            Control whether to display the formatted message.

    Returns
    -------
        Exception
            :param:`throw` is an Exception class.
        ErrorException
            :param:`throw` is `None`.
    """
    # main message
    main_msg, _msg = _fmt_main("ERROR", msg, loc=loc, fg="d", bg="y", styles={"bold"})
    # exception message
    exc_msg, exc = _fmt_exc(exc, top_indent=len(main_msg), frame_style="double", fg="y", styles={"bold", "blink"})
    # log
    if _core._FILE_HANDLER:
        _core._LOGGER.error(str(_msg), exc_info=exc, stack_info=True, stacklevel=2)
    # display
    if display:
        # combine
        final_msg = _core.cstr(main_msg, " " * _FRAME_GAP, exc_msg)
        _core.display(final_msg)
    # throw
    if inspect.isclass(throw) and issubclass(throw, Exception):
        return throw(_msg)
    else:
        return ErrorException(_msg)


def warning(
    msg: str = "",
    /,
    exc: Optional[Any] = None,
    throw: Optional[Exception] = None,
    loc: Union[bool, int] = True,
    dim: bool = False,
    display: bool = True
):
    r"""
    `WARNING` level with `log` record (requires :func:`log_init`).

    NOTE: Used when unexpected events occur, and the program can still run normally.

    Parameters
    ----------
        msg : str, default to `""`
            Description message.

        exc : Optional[Any], default to `None`
            An instance of exception.
            - _Exception_: Record the exception traceback and message;
            - `None`: Try to catch the exception in the current context. If no exception is caught, no exception information will be recorded;
            - `""`: No exception information will be recorded.

        throw : Optional[Exception], default to `None`
            The type of exception to be output after logging.
            - _Exception_: Return the specified exception with the description message;
            - `None`: Return :class:`WarningException` exception with the description message.

        loc : bool, default to `True`
            Control whether to display file function location information.
            - `True`: Display `WARNING` location as stack level `1`;
            - _int_: Display `WARNING` location according to stack level. i.e.: `0`: the location where the `WARNING` is called; `1`: the location of the parent function that calls the `WARNING`.; ...

        dim : bool, default to `False`
            Control whether to dim the `WARNING` message.

        display : bool, default to `True`
            Control whether to display the formatted message.

    Returns
    -------
        Exception
            :param:`throw` is an Exception class.
        WarningException
            :param:`throw` is `None`.
    """
    # main message
    main_msg, _msg = _fmt_main("WARNING", msg, loc=loc, fg="y", styles=None if dim else {"bold"})
    # exception message
    exc_msg, exc = _fmt_exc(exc, top_indent=len(main_msg), frame_style="light", fg="y", styles={"dim"} if dim else {"bold"})
    # log
    if _core._FILE_HANDLER:
        _core._LOGGER.warning(str(_msg), exc_info=exc, stack_info=True, stacklevel=2)
    # display
    if display:
        # combine
        final_msg = _core.cstr(main_msg, " " * _FRAME_GAP, exc_msg)
        _core.display(final_msg)
    # throw
    if inspect.isclass(throw) and issubclass(throw, Exception):
        return throw(_msg)
    else:
        return WarningException(_msg)


def info(
    msg: str = "",
    /,
    exc: Optional[Any] = "",
    indent: int = 0,
    loc: Union[bool, int] = False,
    outline: bool = False,
    display: bool = True
):
    r"""
    `INFO` level with `log` record (requires :func:`log_init`).

    NOTE: Used to record key node information.

    Parameters
    ----------
        msg : str, default to `""`
            Description message.

        exc : Optional[Any], default to `""`
            An instance of exception.
            - _Exception_: Record the exception traceback and message;
            - `None`: Try to catch the exception in the current context. If no exception is caught, no exception information will be recorded;
            - `""`: No exception information will be recorded.

        indent : int, default to `0`
            The indentation of the `INFO`.

        loc : bool, default to `True`
            Control whether to display file function location information.
            - `True`: Display `INFO` location as stack level `1`;
            - _int_: Display `INFO` location according to stack level. i.e.: `0`: the location where the `INFO` is called; `1`: the location of the parent function that calls the `INFO`.; ...

        outline : bool, default to `False`
            Control whether to highlight the `INFO` message.

        display : bool, default to `True`
            Control whether to display the formatted message.

    Returns
    -------
        str
            Formatted message.
    """
    # main message
    if outline:
        main_msg, _msg = _fmt_main("KEY-INFO", msg, loc=loc, indent=indent, fg="lb", styles={"bold"})
    else:
        main_msg, _msg = _fmt_main("INFO", msg, loc=loc, indent=indent, fg="lg", styles={"bold"})
    # exception message
    exc_msg, exc = _fmt_exc(exc, top_indent=len(main_msg), indent=indent, frame_style="light", fg="lb" if outline else "g", styles={"bold"} if outline else None)
    # log
    if _core._FILE_HANDLER:
        _core._LOGGER.info(str(_msg), exc_info=exc, stack_info=False, stacklevel=2)
    # combine
    final_msg = _core.cstr(main_msg, " " * _FRAME_GAP, exc_msg)
    # display
    if display:
        _core.display(final_msg)

    return final_msg


def debug(*args: Any, **kwargs: Any):
    r"""
    `DEBUG` level with `log` record (requires :func:`log_init`).

    NOTE: Used for debugging.
    """
    msg = ""
    for arg in args:
        msg += f"\n{arg}"
    for arg_name, arg_val in kwargs.items():
        msg += f"\n[{arg_name}]: {arg_val}"
    # log
    if _core._FILE_HANDLER and msg:
        _core._LOGGER.debug(msg, stack_info=True, stacklevel=2)
