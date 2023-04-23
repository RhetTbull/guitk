"""Layout widget to enable SwiftUI style layout"""

import threading
from typing import Any

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
    """Layout widget"""

    def __init__(self):
        self._layout = []
        self.index = 0

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
