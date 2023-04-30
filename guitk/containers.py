""" Container classes for guitk """

import tkinter as tk

from guitk.constants import GUITK

from .constants import DEFAULT_PADX, DEFAULT_PADY
from .frame import _Container, _LayoutMixin
from .layout import get_parent, pop_parent, push_parent
from .types import Window
from .widget import Widget


class Stack(_Container):
    """A container that stacks widgets vertically when added to a Layout"""

    def __init__(
        self,
        key: str | None = None,
        width: int | None = None,
        height: int | None = None,
        padding: int | None = None,
        disabled: bool | None = False,
        sticky: str | None = "ns",
    ):
        super().__init__(
            frametype=GUITK.ELEMENT_FRAME,
            key=key,
            width=width,
            height=height,
            layout=None,
            style=None,
            borderwidth=None,
            padding=padding,
            relief=None,
            disabled=disabled,
            rowspan=None,
            columnspan=None,
            sticky=sticky,
            tooltip=None,
            autoframe=False,
            padx=0,
            pady=0,
        )

    def _create_widget(self, parent: tk.BaseWidget, window: Window, row: int, col: int):
        super()._create_widget(parent, window, row, col)
        parent.grid_rowconfigure(row, weight=1)


    def __enter__(self):
        push_parent(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # reorder the layout to be vertical
        self.layout = [[x] for x in self.layout[0]]
        pop_parent()
        return False


class Row(_Container):
    """A container that stacks widgets horizontally when added to a Layout"""

    def __init__(
        self,
        disabled: bool | None = False,
        sticky: str | None = "ew",
    ):
        super().__init__(
            frametype=GUITK.ELEMENT_FRAME,
            key=None,
            width=None,
            height=None,
            layout=None,
            style=None,
            borderwidth=None,
            padding=0,
            relief=None,
            disabled=disabled,
            rowspan=None,
            columnspan=None,
            sticky=sticky,
            tooltip=None,
            autoframe=False,
            padx=0,
            pady=0,
        )


    def _create_widget(self, parent: tk.BaseWidget, window: Window, row: int, col: int):
        super()._create_widget(parent, window, row, col)
        parent.grid_columnconfigure(col, weight=1)


    def __enter__(self):
        push_parent(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pop_parent()
        return False
