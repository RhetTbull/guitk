"""Debug utilities; set GUITK_DEBUG=1 to enable debugging or use set_debug()"""

from __future__ import annotations

import datetime
import inspect
import os
import sys
import time
from functools import wraps

_global_debug = False

__all__ = [
    "debug",
    "debug_borderwidth",
    "debug_relief",
    "debug_watch",
    "is_debug",
    "set_debug",
]


def set_debug(value: bool):
    """Enable or disable debug"""
    global _global_debug
    _global_debug = value


def is_debug():
    """Return True if debug is enabled or False otherwise"""
    global _global_debug
    return _global_debug


def debug(*args, **kwargs):
    """Print debug message only if is_debug() is True"""
    if not is_debug():
        return

    # get caller name
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    caller = module.__name__

    # get line number of caller
    caller += f":{frame.lineno}"

    print(f"[DEBUG] {caller}: ", end="")
    print(*args, **kwargs)


def debug_borderwidth():
    """Return border width is_debug() is True or None otherwise"""
    return 1 if is_debug() else None


def debug_relief():
    """Return relief for frames if is_debug() is True or None otherwise"""
    return "raised" if is_debug() else None


def debug_watch(func):
    """decorate a function to print debug info before and after the function is called if debugging is enabled"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_debug():
            return func(*args, **kwargs)

        caller = sys._getframe().f_back.f_code.co_name
        name = func.__name__
        timestamp = datetime.datetime.now().isoformat()
        print(
            f"{timestamp} {name} called from {caller} with args: {args} and kwargs: {kwargs}"
        )
        start_t = time.perf_counter()
        rv = func(*args, **kwargs)
        stop_t = time.perf_counter()
        print(
            f"{timestamp} {name} returned: {rv}, elapsed time: {stop_t - start_t} sec"
        )
        return rv

    return wrapper


if os.getenv("GUITK_DEBUG") == "1":
    set_debug(True)
    debug("debugging enabled")
