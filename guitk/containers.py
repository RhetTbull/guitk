""" Container classes for guitk """

import tkinter as tk

from guitk.constants import GUITK

from .frame import _Container, _VerticalContainer
from .types import HAlign, VAlign, Window
from .widget import Widget


class VStack(_VerticalContainer):
    """A container that stacks widgets vertically when added to a Layout"""

    def __init__(
        self,
        key: str | None = None,
        width: int | None = None,
        height: int | None = None,
        padding: int | None = None,
        disabled: bool | None = False,
        sticky: str | None = "ns",
        valign: VAlign | None = None,
        halign: HAlign | None = None,
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
            valign=valign,
            halign=halign,
        )

    def _create_widget(self, parent: tk.BaseWidget, window: Window, row: int, col: int):
        super()._create_widget(parent, window, row, col)
        parent.grid_rowconfigure(row, weight=1)

    def add_widget(self, widget: Widget):
        """Add a widget to the bottom of the VStack"""
        self.row_count += 1
        super().add_widget(widget, self.row_count, 0)


class HStack(_Container):
    """A container that stacks widgets horizontally when added to a Layout"""

    def __init__(
        self,
        disabled: bool | None = False,
        sticky: str | None = "ew",
        valign: VAlign | None = None,
        halign: HAlign | None = None,
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
            valign=valign,
            halign=halign,
        )

    def _create_widget(self, parent: tk.BaseWidget, window: Window, row: int, col: int):
        super()._create_widget(parent, window, row, col)
        parent.grid_columnconfigure(col, weight=1)

    def add_widget(self, widget: Widget):
        """Add a widget to the end of the HStack"""
        self.col_count += 1
        super().add_widget(widget, 0, self.col_count)
