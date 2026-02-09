# tests/test_log.py

import sys
sys.path.insert(0, "/data/tianzhen/my_packages/cobra-log/src")

from cobra_log import (warning, info, error, log_init, set_trace, enable_color)


def test_cobra_log():
    try:
        try:
            raise KeyError("This is the first exception")
        except Exception:
            try:
                raise KeyError("This is the second exception")
            except Exception:
                error("An error occurred during the test.", throw=True)

    except Exception:
        warning("An error occurred during the test.")
        info("Continuing execution after warning.")
        error("An error occurred during the test.", "")


def test_cobra_log_2():
    try:
        raise KeyError("This is the first exception")

    except Exception as e:
        warning("An error occurred during the test.", e, loc=True)
        info("Continuing execution after warning.")
        info("Continuing execution after warning.", e, outline=True)


if __name__ == "__main__":
    log_init("test_log.log", log_level="debug", use_color=True)
    set_trace(with_border=True)
    test_cobra_log()
    print("\n" + "=" * 80 + "\n")
    test_cobra_log_2()
