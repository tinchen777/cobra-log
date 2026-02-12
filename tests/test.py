import sys
sys.path.insert(0, "/data/tianzhen/my_packages/cobra-log/src")


import logging
from logging.handlers import RotatingFileHandler
from cobra_log.handlers import stream_handler, _name_to_level
from typing import (Any, Optional, Tuple, List, Union)




# print(_name_to_level("error"))
# print(logging.ERROR)
# print(logging._nameToLevel)



logger = logging.getLogger("my_logger")

# print(logger)

logger.setLevel("DEBUG")

# print(logger)
# print(logging.root.manager.loggerDict)
# logger = logging.getLogger("my_logger1")
# print(logging.root.manager.loggerDict)



# exit()




# 创建 handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# # 设置格式
formatter = logging.Formatter(
    "[%(levelname)s] %(name)s: %(message)s"
)
console_handler.setFormatter(formatter)

console_handler.setLevel("ERROR")

# logger.addHandler(console_handler)


# 添加
h = stream_handler(level="info")
logger.addHandler(h)
# logger.addHandler(h)

print(logger.handlers)



# print(h.get_name())
# print(h.name)
# h.set_name("my_stream_handler")
# print(logger.handlers)


# _FILE_HANDLER = RotatingFileHandler(
#     filename="test.log",
#     mode="a",
#     maxBytes=100*1024,
#     delay=True
# )
# # logger.addHandler(_FILE_HANDLER)
# _FILE_HANDLER.setFormatter(logging.Formatter(
#     fmt=r"%(asctime)s - <%(levelname)s> - <%(filename)s(%(funcName)s)-%(lineno)d> - %(message)s",
#     datefmt=r"%y-%m-%d %H:%M:%S"
# ))
# _FILE_HANDLER.setLevel("DEBUG")


# print(logger.handlers)


# assert _FILE_HANDLER in logger.handlers


# logger.warning("This is a warning message.")
# logger.error("This is an error message.")
logger.info("This is an info message.")

# logging.warning("This is a warning message from logging.")
# logging.error("This is an error message from logging.")

