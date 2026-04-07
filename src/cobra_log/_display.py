# -*- coding: utf-8 -*-
# Python version: 3.9
# @TianZhen

import warnings
from typing import Any

from .exceptions import NoColorWarning

try:
    from cobra_color import (cstr as t_cstr, safe_print as t_safe_print)  # type: ignore
    _COLOR_AVAIL = True
except ImportError:
    warnings.warn(
        "Missing dependency `cobra-color`, terminal color display unavailable for `cobra-log`. Install it via: pip install cobra-log[color]",
        category=NoColorWarning,
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
    """
    Enable or disable colored terminal display. Requires :pkg:`cobra-color`.
    """
    global _USE_COLOR
    _USE_COLOR = flag and _COLOR_AVAIL
