# -*- coding: utf-8 -*-
# Python version: 3.9
# @TianZhen

import logging
from typing import (Any, List, Sequence)

from ._display import cstr
from .types import T_LogLevelName


_FRAME = {
    "light": {
        "top_left": "\u256D",
        "top_right": "\u256E",
        "bottom_left": "\u2570",
        "bottom_right": "\u256F",
        "horizontal": "\u2500",
        "vertical": "\u2502"
    },
    "double": {
        "top_left": "\u2554",
        "top_right": "\u2557",
        "bottom_left": "\u255A",
        "bottom_right": "\u255D",
        "horizontal": "\u2550",
        "vertical": "\u2551"
    },
    "heavy": {
        "top_left": "\u250F",
        "top_right": "\u2513",
        "bottom_left": "\u2517",
        "bottom_right": "\u251B",
        "horizontal": "\u2501",
        "vertical": "\u2503"
    }
}


def box_lines(
    lines: Sequence[str],
    /,
    top_indent: int = 0,
    rest_indent: int = 0,
    frame_style: str = "light",
    min_width: int = 50,
    **pattern: Any
) -> str:
    """
    Box the lines with a border.

    Parameters
    ----------
        lines : Sequence[str]
            The lines to be boxed.

        top_indent : int, default to `0`
            The number of spaces to indent for the top border line.

        rest_indent : int, default to `0`
            The number of spaces to indent for the rest lines.

        frame_style : str, default to `"light"`
            The border style name of :attr:`_FRAME`, including `"light"`, `"double"` and `"heavy"`.

        min_width : int, default to `50`
            The minimum width of the boxed lines, excluding the border and the rest lines indent.

        **pattern : Any
            The color pattern for the border, including `fg`, `bg` and `styles`.
            See also :func:`cobra_color.cstr` for details.

    Returns
    -------
        str
            The boxed lines as a string.
    """
    frame = _FRAME.get(frame_style, _FRAME["light"])
    rest_indent = max(0, rest_indent)
    top_indent = max(0, top_indent)
    # width
    width = max(len(line) for line in lines) + 1
    if width == 1:
        return ""
    width = max((min_width), width, top_indent)
    # top line
    top_line_items: List[str] = []
    if top_indent == 0:
        top_line_items.append(frame["top_left"])
    top_remain_len = width + rest_indent + 1 - top_indent
    if top_remain_len > 0:
        top_line_items.append(frame["horizontal"] * top_remain_len)
    if top_remain_len > -1:
        top_line_items.append(frame["top_right"])
    boxed_lines = [cstr(*top_line_items, **pattern)]
    # middle lines
    vert_line = cstr(frame["vertical"], **pattern)
    for line in lines:
        boxed_lines.append(cstr(" " * rest_indent, vert_line, line, " " * (width - len(line)), vert_line))
    # bottom line
    boxed_lines.append(cstr(
        " " * rest_indent,
        frame["bottom_left"],
        frame["horizontal"] * width,
        frame["bottom_right"],
        **pattern
    ))
    return cstr(*boxed_lines, sep="\n")


def get_log_level(level_name: T_LogLevelName, /):
    """
    Get the logging level value from the logging level name.

    Parameters
    ----------
        level_name : T_LogLevelName
            The logging level name.

    Returns
    -------
        int
            The logging level value.
    """
    level_name = str(level_name).upper()
    return logging._nameToLevel.get(level_name, logging.NOTSET)


def find_handler(
    logger: logging.Logger,
    handler_name: str,
    /,
    formatter_required: bool = False
):
    """
    Find a handler with the specified name in the logger.

    Parameters
    ----------
        logger : logging.Logger
            The logger to find the handler in.

        handler_name : str
            The name of the handler to be found.

        formatter_required : bool, default to `False`
            Control whether the handler must have a formatter to be considered valid.

    Returns
    -------
        logging.Handler
            The handler with the specified name if found, otherwise `None`.
    """
    for handler in logger.handlers:
        if handler.get_name() == handler_name:
            if formatter_required and handler.formatter is None:
                continue
            else:
                return handler
    return None
