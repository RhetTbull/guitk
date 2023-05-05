""" Layout class for use with guitk widgets"""


from __future__ import annotations

import contextlib
import threading
from inspect import currentframe, getmro
from typing import Any, Literal

from .types import HAlign, VAlign

_current_parent = {}


class DummyParent:
    """Dummy class that allows get_parent() to be used whether or not Layout context manager in use"""

    def add_widget(self, widget: Any):
        pass


def push_parent(parent: Any):
    """push parent onto stack"""
    global _current_parent
    current_thread = threading.current_thread().ident
    if current_thread not in _current_parent:
        _current_parent[current_thread] = [parent]
    else:
        _current_parent[current_thread].append(parent)


def pop_parent():
    """pop parent off stack"""
    global _current_parent
    current_thread = threading.current_thread().ident
    if current_thread in _current_parent:
        _current_parent[current_thread].pop()


def get_parent() -> Any:
    """Returns current parent"""
    global _current_parent
    current_thread = threading.current_thread().ident
    if current_thread in _current_parent:
        return _current_parent[current_thread][-1]
    return DummyParent()


class Layout:
    """A Layout manager that aligns widgets horizontally"""

    def __init__(self, valign: VAlign | None = None, halign: HAlign | None = None):
        self._layout = []
        self.index = 0
        self.valign = valign
        self.halign = halign

        # get the caller's instance so we can set the layout
        caller_frame = currentframe().f_back
        with contextlib.suppress(IndexError, KeyError):
            first_arg = caller_frame.f_code.co_varnames[0]
            caller_instance = caller_frame.f_locals[first_arg]
            # determine if the caller is a Window
            # need to use repr() because we can't import Window here without causing a circular import
            if "guitk.window.Window" in repr(getmro(caller_instance.__class__)):
                # Layout is being used in a Window, so set the Window's layout automatically
                caller_instance.layout = self

    def add_widget(self, widget):
        self._layout.append(widget)

    @property
    def layout(self):
        return [self._layout]

    def __enter__(self):
        push_parent(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pop_parent()
        return False

    def __iter__(self):
        self.index = 0
        return iter(self.layout)

    def __next__(self):
        if self.index >= len(self.layout):
            raise StopIteration
        value = self.layout[self.index]
        self.index += 1
        return value


class VerticalLayout(Layout):
    """A Layout manager that aligns widgets vertically"""

    @property
    def layout(self):
        return [[w] for w in self._layout]
