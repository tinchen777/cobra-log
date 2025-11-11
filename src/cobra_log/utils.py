# -*- coding: utf-8 -*-
# Python version: 3.9
# @TianZhen

import inspect
import os
import re
from cobra_color import (ctext, smart_print)
from typing import Any


TRACE_FMT = r"%(fileName)s->%(funcName)s(%(lineno)d)"


def trace_exc(__msg: Any, *exc: Exception):
    r"""
    Format a statement with message and an instance of raised exception. Just like:

    >>> message.
    >>>     1=> <type_except> exception1
    >>>     2=> <type_except> exception2
    >>>         2=> <type_except> exception21

    Parameters
    ----------
        __msg : Any
            Description message.

        *exc : Exception
            An instance of raised exception.

            NOTE: The first exception should be thrown later and the last exception should be thrown earlier.

    Returns
    -------
        str
            Formatted string.
    """
    # message
    msg = str(__msg)
    if not msg.endswith((".", "!", "?", "。", "！", "？")):
        msg += "."

    for idx, e in enumerate(exc):
        # exception string
        exc_str = str(e)
        if "\n" in exc_str and "=>" in exc_str:
            # exist traced exceptions
            exc_str = exc_str.replace("\n", "\n    ")
            exc_styles = ()
        else:
            # no traced exceptions
            if not exc_str.endswith((".", "!", "?")):
                exc_str += "."
            if idx == len(exc) - 1:
                exc_styles = {"bold", "seleted"}
            else:
                exc_styles = {"bold"}
        # arrow
        if len(exc) == 1:
            arrow = ctext("\n    ", styles={"disappear"}) + ctext(" => ", styles={"bold"})
        else:
            idx_str = str(len(exc) - idx)
            arrow = ctext("\n    ", styles={"disappear"}) + ctext(f" {idx_str}=> ", styles={"bold"})
            exc_str = re.sub(r"(\d?=>)", lambda m: idx_str + m.group(1), exc_str)

        # traceback
        tb = e.__traceback__
        tb_str = f": {os.path.basename(tb.tb_frame.f_code.co_filename)}({tb.tb_lineno})" if tb else ""
        tb_detail = ctext(f"<{e.__class__.__name__}{tb_str}> ", styles={"italic", *exc_styles})

        msg += f"{arrow}{tb_detail}{ctext(exc_str, styles=exc_styles)}"

    return msg


def stack_trace(fmt: str = TRACE_FMT, stack_level: int = 1):
    r"""
    Trace the stack information of the function call.

    Parameters
    ----------
        fmt : str, default to TRACE_FMT
            The format string, `TRACE_FMT` is defined as `r"%(fileName)s->%(funcName)s(%(lineno)d)"`.
            Includes:
            - `%(stackDepth)d`: stack depth;
            - `%(funcName)s`: function name;
            - `%(filePath)s`: file path;
            - `%(fileName)s`: file name;
            - `%(lineno)d`: line number;
            - `%(funcLineno)d`: function start line number.

        stack_level : int, default to `1`
            The stack level of the function call.
            - `0`: this function;
            - `1`: the caller of this function;
            - ...

    Returns
    -------
        str
            Formatted stack information.
    """
    text = ""
    try:
        total_stack = inspect.stack()
        frame_info = total_stack[stack_level][0]
        total_depth = len(total_stack)  # stack的总深度

        stackDepth = total_depth - stack_level  # stack深度
        funcName = frame_info.f_code.co_name  # 调用所在的函数名称
        filePath = frame_info.f_code.co_filename  # 调用所在文件绝对地址
        fileName = os.path.basename(filePath)  # 调用所在文件名称
        lineno = int(frame_info.f_lineno)  # 调用所在行号
        funcLineno = frame_info.f_code.co_firstlineno  # 调用所在的函数的起始行号

        text = fmt % {"stackDepth": stackDepth, "funcName": funcName, "filePath": filePath, "fileName": fileName, "lineno": lineno, "funcLineno": funcLineno}

    except KeyError as e:
        smart_print(ctext(f"ERROR: Can Not Match [{e}] In Stack Trace Format [{fmt}].", fore="d", styles={"bold"}, back="y"))
    except Exception as e:
        smart_print(ctext(f"ERROR: Get Stack Trace Error. <{e.__class__.__name__}> {e}", fore="d", styles={"bold"}, back="y"))

    return text
