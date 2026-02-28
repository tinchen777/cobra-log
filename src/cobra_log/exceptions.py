# src/cobra_log/exceptions.py
"""
Exceptions for for :pkg:`cobra_log` package.
"""


# === WARNING ===
class CobraLogWarning(Warning):
    r"""Base warning class for :pkg:`cobra_log` package."""


class NoColorWarning(CobraLogWarning):
    r"""Warning raised when the color library `cobra-color` is not available."""


class InvalidHandlerWarning(CobraLogWarning):
    r"""Warning raised when an invalid handler is added to a logger."""


# === ERROR ===
class CobraLogError(Exception):
    r"""Base error class for :pkg:`cobra_log` package."""


# === EXCEPTION ===
class CriticalErrorException(Exception):
    r"""Exception raised for critical errors in the cobra_log module."""


class ErrorException(Exception):
    r"""Exception raised for errors in the cobra_log module."""


class WarningException(Exception):
    r"""Exception raised for warnings in the cobra_log module."""
