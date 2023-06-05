""" HLayout class for use with guitk widgets"""


from __future__ import annotations

import contextlib
import threading
from inspect import currentframe, getmro
from typing import TYPE_CHECKING, Any, Hashable

from ._debug import debug, debug_watch
from .types import HAlign, LayoutType, VAlign

if TYPE_CHECKING:
    from .basewidget import BaseWidget

_current_parent = {}

__all__ = ["HLayout", "VLayout"]


class DummyParent:
    """Dummy class that allows get_parent() to be used whether or not HLayout context manager in use"""

    def _add_widget(self, widget: Any):
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
    """A Layout manager that aligns widgets horizontally"""

    def __init__(
        self,
        layout: LayoutType = None,
        *,
        valign: VAlign | None = None,
        halign: HAlign | None = None,
    ):
        self._layout_list = layout or []
        self.index = 0
        self.valign = valign
        self.halign = halign
        self.window = None

        # get the caller's instance so we can set the layout
        caller_frame = currentframe().f_back
        with contextlib.suppress(IndexError, KeyError):
            first_arg = caller_frame.f_code.co_varnames[0]
            caller_instance = caller_frame.f_locals[first_arg]
            # determine if the caller is a Window
            # need to use repr() because we can't import Window here without causing a circular import
            if "guitk.window.Window" in repr(getmro(caller_instance.__class__)):
                # HLayout is being used in a Window, so set the Window's layout automatically
                self.window = caller_instance
                self.window.layout = self

    def append(self, widget: BaseWidget):
        """Add a widget to the end of the HLayout"""
        if not self.window:
            # HLayout is not being used in a Window, can't add widget
            raise RuntimeError(
                "Layout must have been created in a Window to add widgets"
            )
        self.window.col_count += 1
        self.window.add_widget(widget, 0, self.window.col_count)

    def remove(self, key_or_widget: Hashable | BaseWidget):
        """Remove widget from layout" and destroy it.

        Args:
            key_or_widget (Hashable | Widget): The key or widget to remove. If a key is given,
                the first widget with that key will be removed.

        Raises:
            RuntimeError: If called and the layout was not created in a Window.
            ValueError: If the widget is not found in the layout.
        """
        if not self.window:
            raise RuntimeError(
                "Layout must have been created in a Window to remove widgets"
            )
        for idx, widget in enumerate(self._layout_list):
            if widget == key_or_widget or widget.key == key_or_widget:
                widget = self._layout_list.pop(idx)
                self.window._forget_widget(widget)
                widget.widget.grid_forget()
                widget.widget.destroy()
                self.window.window.update_idletasks()
                return
        raise ValueError(f"Widget {key_or_widget} not found in Layout")

    def _add_widget(self, widget):
        """Add a widget to the end of the Layout"""
        self._layout_list.append(widget)

    @property
    def layout(self) -> LayoutType:
        """Return the layout list"""
        # if layout manually created, it will be a list of lists
        # otherwise it's a row of widgets, so wrap it in a list
        return (
            self._layout_list
            if self._layout_list and isinstance(self._layout_list[0], (list, tuple))
            else [self._layout_list]
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
    """A Layout manager that aligns widgets vertically"""

    @property
    def layout(self):
        return [[w] for w in self._layout_list]

    def append(self, widget: BaseWidget):
        """Add a widget to the bottom of the VLayout"""
        if not self.window:
            # HLayout is not being used in a Window, can't add widget
            raise RuntimeError(
                "VLayout must have been created in a Window to add widgets"
            )
        self.window.row_count += 1
        self.window.add_widget(widget, self.window.row_count, 0)
