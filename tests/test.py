import sys
sys.path.insert(0, "/data/tianzhen/my_packages/cobra-log/src")


# tests/test_log.py
from cobra_log import enable_color, warning, error, critical, info, log_init, set_trace
from cobra_log._utils import trace_stack, box_lines, trace_exc
from cobra_color import cstr
import cobra_log
import logging

import os

# use_color(False)
log_init("test_log.log", log_level="debug", use_color=True)

set_trace(min_width=1, exc_mode="cause", exc_depth=4, tb_depth=2, exc_args_limit=2, with_border=True)

def a():
    s = ZeroDivisionError("123")
    raise ZeroDivisionError("division by zero44", s)
    1 / 0


def b():
    a()


def c():
    b()


class CriticalException(Exception):
    r"""
    Critical exception.
    """
    def __init__(self, message: str = ""):
        super().__init__(message)
        
        
def test_cobra_log():
    
    
    try:
        c()

    except Exception as e1:
        # dataset.multi_targets not defined
        # try:
           
        try:
            
            raise ValueError(f"Try To Create From [dataset.targets], Dimension Error")
            
        except Exception as e3:
            # dataset.targets not defined
            try:
                # try multi_targets in original_samples_arr
                raise KeyError("Dataset Has No Attribute [samples]") from e3
                
                
                # assert 1 == 0, ("Dataset Has No Attribute [samples]", e3, e3)
            except Exception as e4:
                raise ValueError(e4, "Try To Create From [dataset.samples] Error", e4, e4, "dada") from e4
        
        # except Exception as e2:
            
            # print(" ".join(e2.args) + ".")
            # raise
            # f = trace_exc(e2, with_traceback=True)
            
            # print(f"WARNING: AAA  {trace_stack(0)}", f)
            
            # print(f.plain)
    
    
try:
    try:
        test_cobra_log()
    except Exception as e:
        
        # a = trace_exc(e, mode="caue")
        
        # print(a)
        # raise

        warning("This is a warn message", throw=TypeError)

except Exception as ss:
    # raise
    error("This is a error message2", ss)
    
    
    # critical("This is a critical message", throw=None)
    
    
    
#     error("This is an error message", ee[1], loc=20)
    
#     error("This is an error message", ee[2], loc=0)
    
# ee = sys.exc_info()

# print(repr(ee[1]))
    
# error("This is an error message", ee[1], loc=2)
    
    # critical("This is a critical message", e, loc=3)

    info("This is an info message", None, indent=8, outline=False)

    # info("This is an info message", e, indent=8, outline=False)

print("\u2191")
print("\u2190\u2190\u2190")