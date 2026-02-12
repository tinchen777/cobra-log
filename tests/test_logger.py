# tests/test_logger.py

import sys
sys.path.insert(0, "/data/tianzhen/my_packages/cobra-log/src")

from cobra_log import (warning, info, error, use_logger, critical)
import logging
import cobra_log


def test_logger_switch():
    # initialize and activate loggers
    use_logger("my_logger_1", "test1.log", "test11.log", ("stdout", "info"))
    use_logger("my_logger_2", ("test2.log", "error"), ("stdout", "info"))
    print(logging.root.manager.loggerDict)

    # use my_logger_2
    print(cobra_log._core._ACTIVATED_LOGGER.handlers)
    print("===========")
    info("A info 2 occurred.")
    error("A error 2 occurred.")

    print("===========")
    use_logger("my_logger_1")
    print(cobra_log._core._ACTIVATED_LOGGER.handlers)
    info("A info 1 occurred.")
    error("A error 1 occurred.")


def test_logger_overwrite():
    handler1 = logging.StreamHandler()
    handler1.setLevel("ERROR")

    handler2 = logging.handlers.RotatingFileHandler("test11.log", mode="a", backupCount=5, maxBytes=10*1024*1024)
    handler2.setLevel("ERROR")

    use_logger("my_logger_1", "test1.log", "test11.log", ("stdout", "info"), handler2)
    print(cobra_log._core._ACTIVATED_LOGGER.handlers)

    use_logger("my_logger_1", "test1.log", "test11.log", ("stdout", "info"), handler1, overwrite_handler=True)
    print(cobra_log._core._ACTIVATED_LOGGER.handlers)


if __name__ == "__main__":
    # test_logger_switch()
    
    test_logger_overwrite()


