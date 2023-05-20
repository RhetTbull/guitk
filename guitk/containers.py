""" Container classes for guitk """

import tkinter as tk
from typing import Hashable

from guitk.constants import GUITK

from ._debug import debug_borderwidth, debug_relief, debug_watch
from .frame import _Container, _VerticalContainer
from .types import HAlign, VAlign, Window
from .widget import Widget

# TODO: remove manual bookkeeping of row and column counts


class VStack(_VerticalContainer):
    """A container that stacks widgets vertically when added to a Layout"""

    def __init__(
        self,
        key: Hashable | None = None,
        height: int | None = None,
        padding: int | None = None,
        disabled: bool | None = False,
        sticky: str | None = "nsew",
        valign: VAlign | None = None,
        halign: HAlign | None = None,
        expand: bool = True,
    ):
        """A container that stacks widgets vertically when added to a Layout

        Args:
            key (Hashable, optional): The key to use for the VStack. Defaults to None.
            height (int, optional): The height of the VStack. Defaults to None.
            padding (int, optional): The padding around the VStack. Defaults to None.
            disabled (bool, optional): Whether the VStack is disabled. Defaults to False.
            sticky (str, optional): The sticky value for the VStack. Defaults to "nsew".
            valign (VAlign, optional): The vertical alignment for the widgets in the VStack.
                Defaults to None.
            halign (HAlign, optional): The horizontal alignment for the widgets in the VStack.
                Defaults to None.
            expand (bool, optional): Whether the VStack should expand to fill the available space.
                Defaults to True.

        Note:
            If height is specified, the VStack will not expand to fill the available space and the
            expand parameter will be ignored.
        """
        super().__init__(
            frametype=GUITK.ELEMENT_FRAME,
            key=key,
            width=None,
            height=height,
            layout=None,
            style=None,
            borderwidth=debug_borderwidth() or None,
            padding=padding,
            relief=debug_relief() or None,
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
        self.expand = expand if height is None else False

    def _create_widget(self, parent: tk.BaseWidget, window: Window, row: int, col: int):
        super()._create_widget(parent, window, row, col)
        if self.expand:
            parent.grid_rowconfigure(row, weight=1)

    def append(self, widget: Widget):
        """Add a widget to the bottom of the VStack"""
        self._add_widget_row_col(widget, len(self), 0)

    def extend(self, widgets: list[Widget]):
        """Add a list of widgets to the end of the VStack"""
        for widget in widgets:
            self.append(widget)

    def insert(self, index: int, widget: Widget):
        """Insert a widget at the given index in the HStack.

        Args:
            index (int): The index to insert the widget at.
            widget (Widget): The widget to insert.

        Note: The first argument is the index of the element before which to insert,
        so a.insert(0, x) inserts at the front of the stack, and a.insert(len(a), x)
        is equivalent to a.append(x).

        If the index is out of range, the widget will be added to the end of the VStack.
        """
        self._insert_widget_row_col(widget, index, 0, True)

    def _add_widget_row_col(self, widget: Widget, row: int, col: int):
        super()._add_widget_row_col(widget, row, col)

    def __len__(self):
        """Length of the VStack (number of widgets contained)"""
        return len(self.layout) if self.layout else 0


class HStack(_Container):
    """A container that stacks widgets horizontally when added to a Layout"""

    def __init__(
        self,
        key: Hashable | None = None,
        disabled: bool | None = False,
        sticky: str | None = "nsew",
        valign: VAlign | None = None,
        halign: HAlign | None = None,
        expand: bool = True,
    ):
        """A container that stacks widgets horizontally when added to a Layout

        Args:
            key (Hashable, optional): The key to use for the HStack. Defaults to None.
            disabled (bool, optional): Whether the HStack is disabled. Defaults to False.
            sticky (str, optional): The sticky value for the HStack. Defaults to "nsew".
            valign (VAlign, optional): The vertical alignment for the widgets in the HStack. Defaults to None.
            halign (HAlign, optional): The horizontal alignment for the widgets in the HStack. Defaults to None.
            expand (bool, optional): Whether the HStack should expand to fill the available space. Defaults to True.
        """
        # TODO: copy height, width, padding, etc. from VStack
        super().__init__(
            frametype=GUITK.ELEMENT_FRAME,
            key=key,
            width=None,
            height=None,
            layout=None,
            style=None,
            borderwidth=debug_borderwidth() or None,
            padding=0,
            relief=debug_relief() or None,
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
        self.expand = expand

    def _create_widget(self, parent: tk.BaseWidget, window: Window, row: int, col: int):
        super()._create_widget(parent, window, row, col)
        if self.expand:
            parent.grid_columnconfigure(col, weight=1)

    def append(self, widget: Widget):
        """Add a widget to the end of the HStack"""
        self._add_widget_row_col(widget, 0, len(self))

    def extend(self, widgets: list[Widget]):
        """Add a list of widgets to the end of the HStack"""
        for widget in widgets:
            self.append(widget)

    def insert(self, index: int, widget: Widget):
        """Insert a widget at the given index in the HStack.

        Args:
            index (int): The index to insert the widget at.
            widget (Widget): The widget to insert.

        Note: The first argument is the index of the element before which to insert,
        so a.insert(0, x) inserts at the front of the stack, and a.insert(len(a), x)
        is equivalent to a.append(x).

        If the index is out of range, the widget will be added to the end of the HStack.
        """
        self._insert_widget_row_col(widget, 0, index)

    def _add_widget_row_col(self, widget: Widget, row: int, col: int):
        super()._add_widget_row_col(widget, row, col)

    def __len__(self):
        """Length of the HStack (number of widgets contained"""
        # add 1 as col_count is the index of the last column
        return len(self.layout[0]) if self.layout else 0
