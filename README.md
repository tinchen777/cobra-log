<div align="center">

<h2 id="title">🐱‍👓 cobra-log 🐱‍👓</h2>

[![PyPI version](https://img.shields.io/pypi/v/cobra-log.svg)](https://pypi.org/project/cobra-log/)
![Python](https://img.shields.io/pypi/pyversions/cobra-log?color=brightgreen)
[![codecov](https://codecov.io/gh/tinchen777/cobra-log/branch/main/graph/badge.svg)](https://codecov.io/gh/tinchen777/cobra-log)
![License](https://img.shields.io/github/license/tinchen777/cobra-log.svg)

[![Tests](https://github.com/tinchen777/cobra-log/actions/workflows/test.yml/badge.svg)](https://github.com/tinchen777/cobra-log/actions/workflows/test.yml)
![Github stars](https://img.shields.io/github/stars/tinchen777/cobra-log.svg)

</div>

## About

A lightweight and easy-to-use logging library for Python.

- Python: 3.9+

## Features

- 🚀 Seamless integration with Python's native exception mechanism.
- 🚀 Vivid and detailed terminal output (need `cobra-color`).
- 🚀 User-friendly log file management.

## Installation

Stable (once published):

```bash
pip install cobra-log
```

## Quick Start

- Simple warning

  ```python
  from cobra_log import warning, use_logger

  use_logger("your_log_file.log")

  warning("warning message")
  ```

## Example

```python
from cobra_log import (use_logger, info, warning, error)

# initialize and activate loggers
use_logger("my_logger_1", "stdout", "console")
use_logger("my_logger_2", "log_save_path.log", ("stdout", "error"))
# use my_logger_2
try:
    try:
        try:
            1 / 0
        except Exception as e:
            raise error("An error occurred.", throw=None) from e
    except Exception as ee:
        raise error(
            "An error(TimeoutError) occurred.",
            throw=TimeoutError
        ) from ee
except Exception:
    critical("A critical error occurred.", throw=None)
# activate my_logger_1
use_logger("my_logger_1")
# use my_logger_1
warning("A warning occurred.")
info("An info occurred.")
```

## Requirements

- Python >= 3.9
- (Optional) cobra-color >= 1.3.0

## License

See LICENSE in the repository.

## Links

- [Homepage/Repo](https://github.com/tinchen777/cobra-log.git)
- [Issues](https://github.com/tinchen777/cobra-log.git/issues)
