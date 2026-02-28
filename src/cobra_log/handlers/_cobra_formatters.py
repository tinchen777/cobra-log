# -*- coding: utf-8 -*-
# Python version: 3.9
# @TianZhen

from __future__ import annotations
import logging
import traceback
from typing import (Optional, Literal, Any, Tuple, List)

from .._display import cstr
from .._utils import box_lines


_STACK_FMT = r"[%(filename)s->%(funcName)s(%(lineno)d)]"
_FRAME_GAP = 2

_END_SYMBOLS = (".", "!", "?", "。", "！", "？")
_FINAL_STYLES = {"bold", "selected"}

_TB_STR = "traceback"
_EXC_ARROW_STR = cstr("\u25B6 ", styles={"bold"})
_CAUSE_LINE = {"vertical": "\u2502", "horizontal": "\u2500", "corner": "\u2514"}
# traceback braces
_BRACE = {"upper": "\u250E", "middle": "\u2520", "lower": "\u2516"}
_SHORT_LINE = "\u2574"


def _add_indent(indent: int, /, nowrap: bool = False) -> str:
    """Create indentation."""
    return cstr(("" if nowrap else "\n") + " " * indent, styles={"disappear"})


def _fmt_msg(msg: Any, /, limit: Optional[int] = None) -> str:
    """Format message."""
    msg = msg if isinstance(msg, str) else str(msg)
    if limit is not None and len(msg) > limit:
        msg = msg[:limit] + ".."
    if msg and not msg.endswith(_END_SYMBOLS):
        msg += "."
    return msg


class CobraRichFormatter(logging.Formatter):
    """
    Formatter for logging with rich text, formatted exception trace and dynamic output control.

    Formatter instances are used to convert a LogRecord to text.

    The Formatter can be initialized with a format string which makes use of knowledge of the LogRecord attributes - e.g. the default value mentioned above makes use of the fact that the user's message and arguments are pre-formatted into a LogRecord's message attribute. Currently, the useful attributes in a LogRecord are described by:

    - `%(prefix)s`        Custom prefix for the log message, passed by :param:`extra` in logging method
    - `%(stack)s`         Formatted stack information, generated when :param:`stack_info` is set to `True` in logging method

    - %(name)s            Name of the logger (logging channel)
    - %(levelno)s         Numeric logging level for the message (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`)
    - %(levelname)s       Text logging level for the message (`"DEBUG"`, `"INFO"`, `"WARNING"`, `"ERROR"`, `"CRITICAL"`)
    - %(pathname)s        Full pathname of the source file where the logging call was issued (if available)
    - %(filename)s        Filename portion of pathname
    - %(module)s          Module (name portion of filename)
    - %(lineno)d          Source line number where the logging call was issued (if available)
    - %(funcName)s        Function name
    - %(created)f         Time when the LogRecord was created (time.time() return value)
    - %(asctime)s         Textual time when the LogRecord was created
    - %(msecs)d           Millisecond portion of the creation time
    - %(relativeCreated)d Time in milliseconds when the LogRecord was created, relative to the time the logging module was loaded (typically at application startup time)
    - %(thread)d          Thread ID (if available)
    - %(threadName)s      Thread name (if available)
    - %(process)d         Process ID (if available)
    - %(message)s         The result of record.getMessage(), computed just as the record is emitted
    """
    def __init__(
        self,
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        stackfmt: Optional[str] = None,
        with_border: bool = True,
        min_width: int = 50,
        exc_mode: Literal["cause", "context"] = "context",
        exc_depth: int = -1,
        tb_depth: Optional[int] = -1,
        exc_args_limit: int = -1
    ):
        """
        Initialize the formatter with specified format strings.

        Parameters
        ----------
            fmt : Optional[str], default to `None`
                The format string for the log message.
                - `None`: Use the default format string `%(message)s`.

            datefmt : Optional[str], default to `None`
                The format string for the log record's creation time, as accepted by :func:`time.strftime`.
                - `None`: Use the default format string `"%Y-%m-%d %H:%M:%S"`.

            stackfmt : Optional[str], default to `None`
                The format string for the stack information, which is generated when `stack_info` is set to `True` in logging method.
                - `None`: Use the default format string ` [%(filename)s->%(funcName)s(%(lineno)d)]`.

            with_border : bool, default to `True`
                Whether to display the border for exception trace.

            min_width : int, default to `50`
                The minimum width of the border for exception trace.

            exc_mode : Literal["cause", "context"], default to `"context"`
                The trace mode for exception chain.
                - `"cause"`: Trace the cause exception chain, i.e., the exceptions linked by `__cause__` attribute. This chain is formed when exceptions are raised with `from` keyword.
                - `"context"`: Trace the context exception chain, i.e., the exceptions linked by `__context__` attribute. This chain is formed when an exception is raised in an except block and not handled, regardless of whether `from` keyword is used.

            exc_depth : int, default to `-1`
                The maximum depth of exception chain to trace.
                - `< 1`: Trace all exceptions in the chain;
                - `>= 1`: Trace the last :param:`exc_depth` exceptions in the chain, omitting earlier exceptions.

            tb_depth : Optional[int], default to `-1`
                The maximum depth of stack traceback frames to trace for each exception.
                - `None`: Without traceback frames;
                - `< 1`: Trace all traceback frames;
                - `>= 1`: Trace the last :param:`tb_depth` traceback frames, omitting earlier frames.

            exc_args_limit : int, default to `-1`
                The maximum number of exception arguments to display for each exception.
                - `< 1`: Display all exception arguments;
                - `>= 1`: Display the first :param:`exc_args_limit` exception arguments, omitting later arguments.
        """
        super().__init__(fmt=fmt, datefmt=datefmt)

        self._stackfmt = str(stackfmt) if stackfmt else _STACK_FMT
        self._with_border = with_border

        self._exc_mode = exc_mode
        self._exc_depth = exc_depth
        self._tb_depth = tb_depth
        self._exc_args_limit = exc_args_limit
        self._min_width = min_width

    def formatException(self, exception: Any, /, indent: int) -> str:
        """
        Trace the exception chain and format it as a string.

        Parameters
        ----------
            exception : Any
                The exception instance to trace.

            indent : int
                The number of spaces to indent for the exception chain.

        Returns
        -------
            str
                Formatted string.
        """
        indent = int(indent)
        _base_indent = _add_indent(indent)

        # === non-exception type ===
        if not isinstance(exception, Exception):
            # non-exception type
            return _base_indent + _EXC_ARROW_STR +\
                cstr(_fmt_msg(exception), styles=_FINAL_STYLES)

        # === exception type ===
        trace_lines: List[str] = []
        # 1. build exception chain
        exc_lists: List[List[Any]] = [[]]
        exc = exception
        _exc_list = exc_lists[-1]
        exc_count = 0
        while exc is not None:
            _exc_list.append((exc_count, exc))
            exc_count += 1
            # check next exception in chain
            if exc.__cause__ is not None:
                exc = exc.__cause__
            else:
                if self._exc_mode == "cause":
                    # cause
                    break
                else:
                    # context
                    exc_lists.append([])
                    _exc_list = exc_lists[-1]
                    exc = exc.__context__

        if self._exc_mode == "cause":
            trace_lines.extend([
                _base_indent,
                cstr("    for cause exception(s) only", styles={"dim"})
            ])
        if 0 < self._exc_depth < exc_count:
            _e_omit_num = _rest_omit_num = exc_count - self._exc_depth
            while _rest_omit_num > 0:
                if _rest_omit_num >= len(exc_lists[0]):
                    _rest_omit_num -= len(exc_lists[0])
                    exc_lists.pop(0)
                else:
                    exc_lists[0] = exc_lists[0][_rest_omit_num:]
                    _rest_omit_num = 0
            trace_lines.extend([
                _base_indent,
                cstr(f"... omitted {_e_omit_num} exception(s) ...", styles={"dim"})
            ])
        # 2. format exception chain
        for _exc_list in exc_lists:
            trace_lines.extend(self._compile_exc(
                _exc_list,
                indent=indent,
                total_exc=exc_count
            ))

        return cstr(*trace_lines)

    def formatMessage(self, record: logging.LogRecord) -> str:
        """
        Format the message for a log record.
        """
        # main message
        main_msg = cstr(self._style.format(record), **record.pattern)
        # indent
        if record.indent > 0:
            main_msg = cstr(" " * record.indent, main_msg)

        return main_msg

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the specified record as text.

        The record's attribute dictionary is used as the operand to a
        string formatting operation which yields the returned string.
        Before formatting the dictionary, a couple of preparatory steps
        are carried out. The message attribute of the record is computed
        using LogRecord.getMessage(). If the formatting string uses the
        time (as determined by a call to usesTime(), formatTime() is
        called to format the event time. If there is exception information,
        it is formatted using formatException() and appended to the message.
        """
        # add & format message
        record.message = self.fmt_msg = _fmt_msg(record.getMessage())
        # add asctime
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        # add stack
        if "%(stack)" in self._style._fmt and record.stack_info:
            try:
                record.stack = self._stackfmt % record.__dict__
            except Exception:
                record.stack = ""
        else:
            record.stack = ""
        # add indent
        record.indent = getattr(record, "indent", 0)
        # add pattern
        record.pattern = getattr(record, "pattern", {})
        record.border_pattern = getattr(record, "border_pattern", {})

        result = self.formatMessage(record)
        # format exception
        if record.exc_info and record.exc_info[1] and not hasattr(record, "exc_traced"):
            # Cache the exception traceback to avoid converting it multiple times (it's constant anyway)
            record.exc_traced = self.formatException(
                record.exc_info[1],
                indent=3 if self._with_border else 4
            )
            if self._with_border:
                record.exc_traced = box_lines(
                    record.exc_traced.splitlines()[1:],
                    top_indent=len(result) + _FRAME_GAP,
                    rest_indent=record.indent,
                    min_width=self._min_width,
                    **record.border_pattern
                )
        if getattr(record, "exc_traced", None):
            result = cstr(result, " " * _FRAME_GAP, record.exc_traced)
        self.fmt_text = result

        return result

    def _compile_exc(
        self,
        exc_cause_list: List[Tuple[int, Exception]],
        /,
        indent: int,
        total_exc: int
    ):
        """Compile a cause exception chain into trace lines."""
        trace_lines: List[str] = []

        for idx, (exc_idx, exc) in enumerate(exc_cause_list):
            # for exception chain
            _base_indent = _add_indent(indent)
            is_final = exc_idx == total_exc - 1
            # actual exception
            if len(exc_cause_list) > 1 and idx > 0:
                # non-first exception in chain with multiple exceptions
                indent_arrow = cstr(
                    _add_indent(indent-3),
                    _CAUSE_LINE["corner"] + "<" + _CAUSE_LINE["horizontal"],
                    f"({total_exc - exc_idx})",
                    _EXC_ARROW_STR
                )
            else:
                indent_arrow = cstr(_base_indent, f"({total_exc - exc_idx})", _EXC_ARROW_STR)
            trace_lines.append(indent_arrow)
            # exception name
            exc_name = cstr(
                exc.__class__.__name__,
                fg=None if is_final else "c",
                bg="lr" if is_final else None,
                styles={"dim"} if is_final else {"bold"}
            )
            # 1. stack traceback
            if len(exc_cause_list) > 1 and idx < len(exc_cause_list) - 1:
                # non-final exception in chain with multiple exceptions
                _tb_indent = cstr(_base_indent, f" {_CAUSE_LINE['vertical']}   ")
            else:
                _tb_indent = _add_indent(len(indent_arrow) - 1)
            tb_stack = list(traceback.extract_tb(exc.__traceback__))
            if not self._tb_depth or len(tb_stack) == 1:
                # only one traceback frame
                tb_stack = tb_stack[-1:]
                _name_width = len(exc_name)
            else:
                if 0 < self._tb_depth < len(tb_stack):
                    _tb_omit_num = len(tb_stack) - self._tb_depth
                    tb_stack = tb_stack[-self._tb_depth:]
                    _tb_len = len(tb_stack)
                    tb_stack.insert(0, cstr(f"... omitted {_tb_omit_num} traceback frame(s) ...", styles={"dim"}))
                _tb_len = len(tb_stack)
                tb_idx_width = len(str(_tb_len))
                _name_width = max(len(_TB_STR) + tb_idx_width + 1, len(exc_name))
            for tb_idx, tb in enumerate(tb_stack):
                # for each traceback frame
                if isinstance(tb, str):
                    # omitted traceback frames
                    trace_lines.extend([f"{_BRACE['upper']} ", tb])
                    continue
                # traceback detail
                _tb_detail = cstr(f"{tb.filename}({tb.lineno})", styles={"udl"})
                if tb_idx == len(tb_stack) - 1:
                    # final traceback (exception raised here)
                    tb_prefix = _BRACE["lower"] if len(tb_stack) > 1 else ""
                    _tb_name = exc_name
                    _tb_styles = _FINAL_STYLES if is_final else set()
                    # 2. exception args
                    _e_args = self._fmt_exc_args(exc.args, is_final)
                    if 0 < self._exc_args_limit < len(_e_args):
                        _arg_omit_num = len(_e_args) - self._exc_args_limit
                        _e_args = _e_args[:self._exc_args_limit]
                        _e_args.append(
                            cstr(f" ... omitted {_arg_omit_num} argument(s) ...", styles={"dim"})
                        )
                    _e_args_space = _add_indent(_name_width + len(_tb_detail) + len(tb_prefix) + 5, nowrap=True)
                    arg_lines = []
                    for e_arg_idx, e_arg in enumerate(_e_args):
                        # for each exception argument
                        if e_arg_idx == 0:
                            # first exception argument
                            _prefix = f" {_BRACE['upper']}" if len(_e_args) > 1 else " "
                            arg_lines.append(cstr(_prefix, e_arg, styles=[(None, _tb_styles)]))
                        else:
                            # non-first exception argument
                            _prefix = _BRACE["lower"] if e_arg_idx == len(_e_args) - 1 else _BRACE["middle"]
                            arg_lines.extend([_tb_indent, _e_args_space, _prefix, e_arg])
                else:
                    # non-final traceback
                    tb_prefix = _BRACE["upper"] if tb_idx == 0 else _BRACE["middle"]
                    _tb_name = cstr(
                        f"{_TB_STR}-{str(len(tb_stack) - tb_idx - 1).zfill(tb_idx_width)}",
                        fg="lg",
                        styles={"bold"}
                    )
                    _tb_styles = {"dim"}
                    arg_lines = [cstr(" >>> ", fg="ly", styles={"bold", *_tb_styles}),
                                 cstr(tb.line, styles=_tb_styles)]
                tb_indent = "" if tb_idx == 0 else _tb_indent
                # traceback head
                tb_head = cstr("<", _tb_name.center(_name_width), ": ", _tb_detail,
                               ">", styles=[(None, {"italic", *_tb_styles})])
                # 3. assemble
                trace_lines.extend([tb_indent, tb_prefix, tb_head, *arg_lines])
            # update
            indent += 4

        return trace_lines

    def _fmt_exc_args(self, e_args: Tuple[Any, ...], /, is_final: bool, is_top=True) -> List[str]:
        """Format exception arguments."""
        fmt_args: List[str] = []
        for m in e_args:
            if isinstance(m, Tuple):
                fmt_args.extend(self._fmt_exc_args(m, is_final, is_top=is_top))
            elif isinstance(m, Exception):
                # exception head
                exc_name = cstr(m.__class__.__name__, fg="r" if is_final else "c")
                e_msg = cstr("<", exc_name, "> ", styles={"italic"})
                # exception args
                sub_args = self._fmt_exc_args(m.args, is_final, is_top=False)
                if len(sub_args) > 1:
                    rest_msgs = [f", {_fmt_msg(arg, 12)}" for arg in sub_args[1:]]
                    e_msg += cstr("( ", styles={"dim"}) + sub_args[0] +\
                        cstr(*rest_msgs, " )", styles={"dim"})
                else:
                    e_msg += sub_args[0]
                fmt_args.append(e_msg)
            else:
                prefix = _SHORT_LINE if is_top and len(e_args) > 1 else ""
                fmt_args.append(prefix + _fmt_msg(m))

        return fmt_args
