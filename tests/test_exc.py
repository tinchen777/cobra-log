# tests/test_exc.py

import sys
sys.path.insert(0, "/data/tianzhen/my_packages/cobra-log/src")

from cobra_log import (warning, info, error, use_logger, critical)


def test_cobra_log():
    try:
        try:
            raise KeyError("This is the first exception")
        except Exception:
            try:
                raise KeyError("This is the second exception")
            except Exception:
                # error("An error occurred during the test.", throw=True)
                raise critical("A critical error occurred during the test1.", throw=None)

    except Exception:
        warning("An error occurred during the test.")
        info("Continuing execution after warning.")
        error("An error occurred during the test.", None)
        # critical("A critical error occurred during the test.")


def test_cobra_log_2():
    try:
        raise KeyError("This is the first exception")

    except Exception as e:
        warning("An error occurred during the test.", e, stack=True)
        info("Continuing execution after warning.")
        info("Continuing execution after warning.", e, outline=True)
        critical("A critical error occurred during the test.")

def test_cobra_log_3():
    try:
        try:
            try:
                1 / 0
            except Exception as e:
                raise error("An error occurred during the test31.", throw=None) from e
        except Exception as ee:
            raise error("An error occurred during the test32.", throw=TimeoutError) from ee
    except Exception:
        critical("A critical error occurred during the test33.", throw=None)


def test_cobra_log_4():
    try:
        try:
            1 / 0
        except ZeroDivisionError as e:
            try:
                int("abc")  # 这里又抛出一个异常
            except ValueError as ve:
                new_exc = RuntimeError("New exception")
                raise new_exc from ve  # 将原始异常作为新异常的 cause
    except Exception as e:
        print("Caught exception:", e)
        print("Cause:", e.__cause__)
        print("Context:", e.__context__)
        print("Suppress Context:", e.__suppress_context__)
        # raise
        error("An error occurred")


if __name__ == "__main__":
    use_logger("my log 1", "console", "test_log1.log", level="debug")
    test_cobra_log()
    print("\n" + "=" * 80 + "\n")
    use_logger("my log 2", "console", "test_log2.log", level="debug")
    test_cobra_log_2()
    print("\n" + "=" * 80 + "\n")
    use_logger("my log 3", "console", "test_log3.log", level="debug")
    test_cobra_log_3()
    print("\n" + "=" * 80 + "\n")
    use_logger("my log 4", "console", "test_log4.log", level="debug")
    test_cobra_log_4()
    
