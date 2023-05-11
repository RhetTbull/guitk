""" HLayout class for use with guitk widgets"""


from __future__ import annotations

import contextlib
import threading
from inspect import currentframe, getmro
from typing import Any

from .types import HAlign, LayoutType, VAlign

_current_parent = {}

__all__ = ["HLayout", "VLayout"]


class DummyParent:
    """Dummy class that allows get_parent() to be used whether or not HLayout context manager in use"""

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


class HLayout:
    """A HLayout manager that aligns widgets horizontally"""

    def __init__(
        self,
        layout: LayoutType = None,
        *,
        valign: VAlign | None = None,
        halign: HAlign | None = None,
    ):
        self._layout = layout or []
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
                # HLayout is being used in a Window, so set the Window's layout automatically
                caller_instance.layout = self

    def add_widget(self, widget):
        self._layout.append(widget)

    @property
    def layout(self) -> LayoutType:
        """Return the layout list"""
        # if layout manually created, it will be a list of lists
        # otherwise it's a row of widgets, so wrap it in a list
        return (
            self._layout
            if self._layout and isinstance(self._layout[0], (list, tuple))
            else [self._layout]
        )

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


class VLayout(HLayout):
    """A HLayout manager that aligns widgets vertically"""

    @property
    def layout(self):
        return [[w] for w in self._layout]
