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

- 🚀 Vivid and detailed terminal output (need `cobra-color`).
- 🚀 Optional file persistence with rotation.
- 🚀 Simple, dependency-light design.

## Installation

Stable (once published):

```bash
pip install cobra-log
```

## Quick Start

- Simple warning

  ```python
  from cobra_log import warning, log_init

  log_init("your_log_file.log")

  warning("warning message")
  ```

## Example

```python
from cobra_log import (log_init, info, warning, error)

# Initialize the log system
log_init("log_save_path.log", use_color=True)

try:
    try:
        try:
            1 / 0
        except Exception as e:
            raise error("An error occurred during the test.", throw=None) from e
    except Exception as ee:
        raise error("An error(TimeoutError) occurred during the test.", throw=TimeoutError) from ee
except Exception:
    critical("A critical error occurred during the test.", throw=None)
```

## Requirements

- Python >= 3.9
- (Optional) cobra-color >= 1.3.0

## License

See LICENSE in the repository.

## Links

- Homepage/Repo: https://github.com/tinchen777/cobra-log.git
- Issues: https://github.com/tinchen777/cobra-log.git/issues
