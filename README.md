<div align="center">

<h2 id="title">cobra-log</h2>

[![Build](https://github.com/tinchen777/cobra-log/actions/workflows/tests.yml/badge.svg)](https://github.com/tinchen777/cobra-log/actions/workflows/tests.yml)
[![PyPI version](https://img.shields.io/pypi/v/cobra-log.svg)](https://pypi.org/project/cobra-log/)
![Python Versions](https://img.shields.io/pypi/pyversions/cobra-log.svg)
![License](https://img.shields.io/github/license/tinchen777/cobra-log.svg)
[![Pull Requests Welcome](https://img.shields.io/badge/pull%20requests-welcome-brightgreen.svg)](https://github.com/tinchen777/cobra-log/pulls)
![Github stars](https://img.shields.io/github/stars/tinchen777/cobra-log.svg)

</div>

## About

A lightweight Python library for enhanced terminal display: simple text color/style conventions and image-to-terminal rendering.

- Python: 3.9+
- Runtime deps: Pillow (>=9,<11), NumPy (>=1.21,<2)

## Features

- :rocket: Concise color/style names for terminal text.
- :rocket: Image rendering in multiple modes: ASCII, color, half-color, gray, half-gray.
- :rocket: Minimal dependencies and easy integration.

## Installation

Stable (once published):

```bash
pip install cobra-log
```

## Quick Start

```python
from cobra_log import (log_init, info, warning, trace_exc)

# Initialize the log system
log_init("log_save_path", display_type="style")

try:
    try:
        1 / 0  # This will raise a ZeroDivisionError
    except Exception as e1:
        raise RuntimeError(trace_exc("This is the main exception", e1))
except Exception as e:
    warning("A warning occurred.", e)
    info("Continuing execution after warning.")
```

## Image Modes

- ascii: monochrome ASCII using a density charset.
- color: colorized character fill.
- half-color: half-block characters with color (higher density, good visual quality).
- gray: grayscale characters.
- half-gray: half-block grayscale.

Tip: For best results, use a TrueColor-capable terminal and a monospaced font.

## Requirements

- Python >= 3.9
- Pillow >= 9.0, < 11
- NumPy >= 1.21, < 2.0

## License

See LICENSE in the repository.

## Links

- Homepage/Repo: https://github.com/tinchen777/cobra-log.git
- Issues: https://github.com/tinchen777/cobra-log.git/issues
