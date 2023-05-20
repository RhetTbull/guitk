""" Container classes for guitk """

import tkinter as tk

from guitk.constants import GUITK

from ._debug import debug_borderwidth, debug_relief, debug_watch
from .frame import _Container, _VerticalContainer
from .types import HAlign, VAlign, Window
from .widget import Widget


class VStack(_VerticalContainer):
    """A container that stacks widgets vertically when added to a Layout"""

    def __init__(
        self,
        key: str | None = None,
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
            key (str, optional): The key to use for the VStack. Defaults to None.
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

    def add_widget(self, widget: Widget):
        """Add a widget to the bottom of the VStack"""
        self.row_count += 1
        self._add_widget_row_col(widget, self.row_count, 0)

    def _add_widget_row_col(self, widget: Widget, row: int, col: int):
        super()._add_widget_row_col(widget, row, col)


class HStack(_Container):
    """A container that stacks widgets horizontally when added to a Layout"""

    def __init__(
        self,
        disabled: bool | None = False,
        sticky: str | None = "nsew",
        valign: VAlign | None = None,
        halign: HAlign | None = None,
        expand: bool = True,
    ):
        """A container that stacks widgets horizontally when added to a Layout

        Args:
            disabled (bool, optional): Whether the HStack is disabled. Defaults to False.
            sticky (str, optional): The sticky value for the HStack. Defaults to "nsew".
            valign (VAlign, optional): The vertical alignment for the widgets in the HStack. Defaults to None.
            halign (HAlign, optional): The horizontal alignment for the widgets in the HStack. Defaults to None.
            expand (bool, optional): Whether the HStack should expand to fill the available space. Defaults to True.
        """
        super().__init__(
            frametype=GUITK.ELEMENT_FRAME,
            key=None,
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

    def add_widget(self, widget: Widget):
        """Add a widget to the end of the HStack"""
        self.col_count += 1
        self._add_widget_row_col(widget, 0, self.col_count)

    def _add_widget_row_col(self, widget: Widget, row: int, col: int):
        super()._add_widget_row_col(widget, row, col)
