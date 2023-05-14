"""Debug utilities for guitk"""

from __future__ import annotations

from .types import Widget
import inspect

_global_debug = False

__all__ = ["set_debug", "is_debug", "debug", "debug_borderwidth", "debug_relief"]


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
