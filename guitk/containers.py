""" Container classes for guitk """

from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING, Hashable

from guitk.constants import GUITK

from ._debug import debug, debug_borderwidth, debug_relief, debug_watch
from .basewidget import BaseWidget
from .frame import _Container
from .spacer import HSpacer, VSpacer
from .types import HAlign, PaddingType, PadType, VAlign

if TYPE_CHECKING:
    from .window import Window


class _Stack(_Container):
    """A container that stacks widgets when added to a Layout"""

    def __init__(
        self,
        key: Hashable | None = None,
        height: int | None = None,
        width: int | None = None,
        padding: PaddingType | None = None,
        disabled: bool | None = False,
        sticky: str | None = "nsew",
        valign: VAlign | None = None,
        halign: HAlign | None = None,
        vexpand: bool = True,
        hexpand: bool = True,
        distribute: bool = False,
        vspacing: PadType | None = None,
        hspacing: PadType | None = None,
        vscrollbar: bool = False,
        # hscrollbar: bool = False,
        autohide_scrollbars: bool = True,
    ):
        """Base container container that stacks widgets when added to a Layout.

        The base container stacks widgets in a single vertical column. Subclasses
        can override the layout property to change the layout to horizontal or
        grid layouts.

        Args:
            key (Hashable, optional): The key to use for the Stack. Defaults to None.
            height (int, optional): The height of the Stack. Defaults to None.
            width (int, optional): The width of the Stack. Defaults to None.
            padding (PaddingType, optional): The padding around the Stack. Defaults to None.
            disabled (bool, optional): Whether the VStack is disabled. Defaults to False.
            sticky (str, optional): The sticky value for the Stack. Defaults to "nsew".
            valign (VAlign, optional): The vertical alignment for the widgets in the Stack.
                Defaults to None.
            halign (HAlign, optional): The horizontal alignment for the widgets in the Stack.
                Defaults to None.
            vexpand (bool, optional): Whether the Stack should expand vertically.
                Defaults to True.
            hexpand (bool, optional): Whether the Stack should expand horizontally.
                Defaults to True.
            distribute (bool, optional): Whether the Stack should distribute widgets evenly.
            vspacing (PadType, optional): Vertical spacing between widgets. Defaults to None.
            hspacing (PadType, optional): Horizontal spacing between widgets. Defaults to None.
            vscrollbar (bool): Whether to include a vertical scrollbar. Defaults to False.

        Note:
            If width or height is specified, the Stack will not expand to fill the available space and the
            expand parameter will be ignored.
        """
        super().__init__(
            frametype=GUITK.ELEMENT_FRAME,
            key=key,
            width=width,
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
            vspacing=vspacing,
            hspacing=hspacing,
            vscrollbar=vscrollbar,
            # hscrollbar=hscrollbar,
            autohide_scrollbars=autohide_scrollbars,
        )
        self.vexpand = vexpand if height is None else False
        self.hexpand = hexpand if width is None else False
        self.distribute = distribute
        self._layout_list = []
        self._layout_lol = [[]]

    def _create_widget(self, parent: tk.BaseWidget, window: Window, row: int, col: int):
        super()._create_widget(parent, window, row, col)

        if self.vexpand:
            parent.grid_rowconfigure(row, weight=1)
        if self.hexpand:
            parent.grid_columnconfigure(col, weight=1)

    @property
    def layout(self) -> list[list[BaseWidget]]:
        """Return the layout of the Stack"""
        if self.distribute:
            self._layout_lol = []
            for widget in self._layout_list:
                self._layout_lol.append([VSpacer()])
                self._layout_lol.append([widget])
            self._layout_lol.append([VSpacer()])
        else:
            self._layout_lol = (
                [[widget] for widget in self._layout_list]
                if self._layout_list
                else [[]]
            )
        return self._layout_lol

    @layout.setter
    def layout(self, layout: list[list[BaseWidget]]):
        """Set the layout of the Stack"""
        self._layout_lol = layout
        self._layout_list = [widget for row in layout for widget in row]

    @property
    def widgets(self) -> list[BaseWidget]:
        """Return a list of the widgets in the Stack"""
        return self._layout_list or []

    def append(self, widget: BaseWidget):
        """Add a widget to the bottom of the Stack"""
        self._layout_list.append(widget)
        self.redraw()

    def extend(self, widgets: list[BaseWidget]):
        """Add a list of widgets to the end of the Stack"""
        for widget in widgets:
            self.append(widget)

    def insert(self, index: int, widget: BaseWidget):
        """Insert a widget at the given index in the Stack.

        Args:
            index (int): The index to insert the widget at.
            widget (Widget): The widget to insert.

        Note: The first argument is the index of the element before which to insert,
        so a.insert(0, x) inserts at the front of the stack, and a.insert(len(a), x)
        is equivalent to a.append(x).

        If the index is out of range, the widget will be added to the end of the Stack.
        """
        self._layout_list.insert(index, widget)
        self.redraw()

    def clear(self):
        """Remove all widgets from the Stack"""
        # copy the list so we can iterate over it while removing widgets
        # which will change the list
        for widget in self._layout_list.copy():
            debug(f"{self} destroying {widget=}")
            widget.destroy()
        self._layout_list = []
        self.redraw()

    def pop(self, index: int = -1):
        """Remove and return the widget at the given index in the Stack.

        Args:
            index (int): The index of the widget to remove.

        Returns:
            Widget: The widget that was removed.

        Raises:
            IndexError: If the index is out of range.
        """
        widget = self._layout_list.pop(index)
        widget.widget.grid_forget()
        self.redraw()
        return widget

    @debug_watch
    def remove(self, key_or_widget: Hashable | BaseWidget):
        """Remove widget from the container and destroy it.

        Args:
            key_or_widget (Hashable | Widget): The key of the widget to remove or the widget object. If a key is given,
                the first widget with that key will be removed.

        Raises:
            ValueError: If the widget is not in the Stack.
        """
        for idx, widget in enumerate(self._layout_list):
            if widget == key_or_widget or widget.key == key_or_widget:
                debug(
                    f"removing {key_or_widget} from {self} {widget.key} {widget.widget}"
                )
                widget = self._layout_list.pop(idx)
                self.window._forget_widget(widget)
                widget.widget.grid_forget()
                widget.widget.destroy()
                self.redraw()
                return
        raise ValueError(f"Widget {key_or_widget} not found in Stack")

    def redraw(self):
        """Redraw the Stack"""
        self._layout(self.frame, self.window)
        self.window.window.update_idletasks()

    def _add_widget(self, widget: BaseWidget):
        """Add a widget to the frame's layout"""
        self._layout_list.append(widget)

    @debug_watch
    def _insert_widget_row_col(
        self, widget: BaseWidget, row: int, col: int, is_vertical: bool = True
    ):
        """Insert a widget into the container after the container has been created
            Intended for use at run-time only when widgets need to be added dynamically

        Args:
            widget: (Widget) the widget to add
            row: (int) the row to insert the widget into
            col: (int) the column to insert the widget into

        Note: widgets are placed in a grid with row, col coordinates by the _LayoutMixin class.
        All containers store widgets internally as a list so we need to convert the row, col
        coordinates to a list index.
        """

        if is_vertical:
            # convert row, col to list index
            index = row
        else:
            index = col

        self._layout_list.insert(index, widget)

        # redraw the layout which will create the widget
        self._layout(self.frame, self.window)

    def __len__(self):
        """Length of the Stack (number of widgets contained)"""
        return len(self._layout_list) if self._layout_list else 0

    def __getitem__(self, index: int):
        """Get the widget at the given index"""
        return self._layout_list[index]

    def __delitem__(self, index: int):
        """Remove the widget at the given index"""
        self.pop(index)


class VStack(_Stack):
    """A container that stacks widgets vertically when added to a Layout"""

    def __init__(
        self,
        key: Hashable | None = None,
        width: int | None = None,
        # height: int | None = None,
        padding: PaddingType | None = None,
        disabled: bool | None = False,
        sticky: str | None = "nsew",
        valign: VAlign | None = None,
        halign: HAlign | None = None,
        vexpand: bool = True,
        hexpand: bool = True,
        distribute: bool = False,
        vspacing: PadType | None = None,
        hspacing: PadType | None = None,
        vscrollbar: bool = False,
        # hscrollbar: bool = False,
        autohide_scrollbars: bool = True,
    ):
        """Base container container that stacks widgets vertically when added to a Layout

        Args:
            key (Hashable, optional): The key to use for the VStack. Defaults to None.
            width (int, optional): The width of the VStack. Defaults to None.
            padding (PaddingType, optional): The padding around the VStack. Defaults to None.
            disabled (bool, optional): Whether the VStack is disabled. Defaults to False.
            sticky (str, optional): The sticky value for the VStack. Defaults to "nsew".
            valign (VAlign, optional): The vertical alignment for the widgets in the VStack.
                Defaults to None.
            halign (HAlign, optional): The horizontal alignment for the widgets in the VStack.
                Defaults to None.
            vexpand (bool, optional): Whether the Stack should expand vertically.
                Defaults to True.
            hexpand (bool, optional): Whether the Stack should expand horizontally.
                Defaults to True.
            distribute (bool, optional): Whether the VStack should distribute widgets evenly.
            vspacing (PadType, optional): Vertical spacing between widgets. Defaults to None.
            hspacing (PadType, optional): Horizontal spacing between widgets. Defaults to None.
            vscrollbar (bool): Whether to include a vertical scrollbar. Defaults to False.
            autohide_scrollbars (bool): Whether to hide scrollbars when not needed. Defaults to True.

        Note:
            If width is specified, the VStack will not expand to fill the available space and the
            expand parameter will be ignored.
        """
        super().__init__(
            key=key,
            width=width,
            height=None,
            padding=padding,
            disabled=disabled,
            sticky=sticky,
            valign=valign,
            halign=halign,
            vexpand=vexpand,
            hexpand=hexpand,
            distribute=distribute,
            vspacing=vspacing,
            hspacing=hspacing,
            vscrollbar=vscrollbar,
            # hscrollbar=hscrollbar,
            autohide_scrollbars=autohide_scrollbars,
        )


class HStack(_Stack):
    """A container that stacks widgets horizontally when added to a Layout"""

    def __init__(
        self,
        key: Hashable | None = None,
        height: int | None = None,
        padding: PaddingType | None = None,
        disabled: bool | None = False,
        sticky: str | None = "nsew",
        valign: VAlign | None = None,
        halign: HAlign | None = None,
        vexpand: bool = True,
        hexpand: bool = True,
        distribute: bool = False,
        vspacing: PadType | None = None,
        hspacing: PadType | None = None,
        vscrollbar: bool = False,
        # hscrollbar: bool = False,
        autohide_scrollbars: bool = True,
    ):
        """A container that stacks widgets horizontally when added to a Layout

        Args:
            key (Hashable, optional): The key to use for the HStack. Defaults to None.
            height (int, optional): The height of the HStack. Defaults to None.
            padding (PaddingType, optional): The padding around the HStack. Defaults to None.
            disabled (bool, optional): Whether the HStack is disabled. Defaults to False.
            sticky (str, optional): The sticky value for the HStack. Defaults to "nsew".
            valign (VAlign, optional): The vertical alignment for the widgets in the HStack.
                Defaults to None.
            halign (HAlign, optional): The horizontal alignment for the widgets in the HStack.
                Defaults to None.
            vexpand (bool, optional): Whether the Stack should expand vertically.
                Defaults to True.
            hexpand (bool, optional): Whether the Stack should expand horizontally.
                Defaults to True.
            distribute (bool, optional): Whether the HStack should distribute widgets evenly.
            vspacing (PadType, optional): Vertical spacing between widgets. Defaults to None.
            hspacing (PadType, optional): Horizontal spacing between widgets. Defaults to None.
            vscrollbar (bool): Whether to include a vertical scrollbar. Defaults to False.
            autohide_scrollbars (bool): Whether to hide scrollbars when not needed. Defaults to True.

        Note:
            If height is specified, the HStack will not expand to fill the available space and the
            expand parameter will be ignored.
        """
        super().__init__(
            key=key,
            height=height,
            width=None,
            padding=padding,
            disabled=disabled,
            sticky=sticky,
            valign=valign,
            halign=halign,
            vexpand=vexpand,
            hexpand=hexpand,
            distribute=distribute,
            vspacing=vspacing,
            hspacing=hspacing,
            vscrollbar=vscrollbar,
            # hscrollbar=hscrollbar,
            autohide_scrollbars=autohide_scrollbars,
        )

    @property
    def layout(self) -> list[list[BaseWidget]]:
        """Return the layout of the HStack"""
        if self.distribute:
            self._layout_lol = [[]]
            for widget in self._layout_list:
                self._layout_lol[0].append(HSpacer())
                self._layout_lol[0].append(widget)
            self._layout_lol[0].append(HSpacer())
        else:
            self._layout_lol = [self._layout_list]
        return self._layout_lol

    @layout.setter
    def layout(self, layout: list[list[BaseWidget]]):
        """Set the layout of the VStack"""
        self._layout_lol = layout
        self._layout_list = [widget for row in layout for widget in row]

    @debug_watch
    def _insert_widget_row_col(
        self, widget: BaseWidget, row: int, col: int, is_vertical: bool = True
    ):
        """Insert a widget into the container after the container has been created
            Intended for use at run-time only when widgets need to be added dynamically

        Args:
            widget: (Widget) the widget to add
            row: (int) the row to insert the widget into
            col: (int) the column to insert the widget into

        Note: widgets are placed in a grid with row, col coordinates by the _LayoutMixin class.
        All containers store widgets internally as a list so we need to convert the row, col
        coordinates to a list index.
        """
        super()._insert_widget_row_col(widget, row, col, is_vertical=False)


class VGrid(_Stack):
    """A container that arranges widgets in a vertical grid when added to a Layout"""

    def __init__(
        self,
        rows: int,
        key: Hashable | None = None,
        width: int | None = None,
        padding: PaddingType | None = None,
        disabled: bool | None = False,
        sticky: str | None = "nsew",
        valign: VAlign | None = None,
        halign: HAlign | None = None,
        vexpand: bool = True,
        hexpand: bool = True,
        vspacing: PadType | None = None,
        hspacing: PadType | None = None,
        vscrollbar: bool = False,
        # hscrollbar: bool = False,
        autohide_scrollbars: bool = True,
    ):
        """Container that stacks widgets in a vertical grid when added to a Layout

        Args:
            rows (int): The number of rows in the grid. The number of columns is determined by the
                number of widgets added to the grid.
            key (Hashable, optional): The key to use for the VStack. Defaults to None.
            width (int, optional): The width of the VStack. Defaults to None.
            padding (PaddingType, optional): The padding around the VStack. Defaults to None.
            disabled (bool, optional): Whether the VStack is disabled. Defaults to False.
            sticky (str, optional): The sticky value for the VStack. Defaults to "nsew".
            valign (VAlign, optional): The vertical alignment for the widgets in the VStack.
                Defaults to None.
            halign (HAlign, optional): The horizontal alignment for the widgets in the VStack.
                Defaults to None.
            vexpand (bool, optional): Whether the Stack should expand vertically.
                Defaults to True.
            hexpand (bool, optional): Whether the Stack should expand horizontally.
                Defaults to True.
            vspacing (PadType, optional): Vertical spacing between widgets. Defaults to None.
            hspacing (PadType, optional): Horizontal spacing between widgets. Defaults to None.
            vscrollbar (bool): Whether to include a vertical scrollbar. Defaults to False.
            autohide_scrollbars (bool): Whether to hide scrollbars when not needed. Defaults to True.

        Note:
            If width is specified, the VStack will not expand to fill the available space and the
            expand parameter will be ignored.
        """
        super().__init__(
            key=key,
            height=None,
            width=width,
            padding=padding,
            disabled=disabled,
            sticky=sticky,
            valign=valign,
            halign=halign,
            vexpand=vexpand,
            hexpand=hexpand,
            distribute=False,
            vspacing=vspacing,
            hspacing=hspacing,
            vscrollbar=vscrollbar,
            # hscrollbar=hscrollbar,
            autohide_scrollbars=autohide_scrollbars,
        )
        self.rows = rows

    @property
    def layout(self) -> list[list[BaseWidget]]:
        """Return the layout of the Stack"""
        if self.distribute:
            raise NotImplementedError("distribute note yet implemented for VGrid")
        else:
            # grid the widgets in the order they were added
            self._layout_lol = [
                self._layout_list[i :: self.rows] for i in range(self.rows)
            ]
        return self._layout_lol

    @layout.setter
    def layout(self, layout: list[list[BaseWidget]]):
        """Set the layout of the Stack"""
        ...

    @debug_watch
    def _insert_widget_row_col(
        self, widget: BaseWidget, row: int, col: int, is_vertical: bool = True
    ):
        """Insert a widget into the container after the container has been created
            Intended for use at run-time only when widgets need to be added dynamically

        Args:
            widget: (Widget) the widget to add
            row: (int) the row to insert the widget into
            col: (int) the column to insert the widget into

        Note: widgets are placed in a grid with row, col coordinates by the _LayoutMixin class.
        All containers store widgets internally as a list so we need to convert the row, col
        coordinates to a list index.
        """
        index = self._row_col_to_index(row, col)
        self._layout_list.insert(index, widget)

        # redraw the layout which will create the widget
        self._layout(self.frame, self.window)

    def _row_col_to_index(self, row: int, col: int):
        """Convert row, col coordinates to a list index"""
        # the VGrid layout converts a list into a list of lists of length self.rows
        # convert row, col to back to a list index
        return row + col * self.rows


class HGrid(_Stack):
    """A container that arranges widgets in a horizontal grid when added to a Layout"""

    def __init__(
        self,
        cols: int,
        key: Hashable | None = None,
        width: int | None = None,
        padding: PaddingType | None = None,
        disabled: bool | None = False,
        sticky: str | None = "nsew",
        valign: VAlign | None = None,
        halign: HAlign | None = None,
        vexpand: bool = True,
        hexpand: bool = True,
        vspacing: PadType | None = None,
        hspacing: PadType | None = None,
        vscrollbar: bool = False,
        # hscrollbar: bool = False,
        autohide_scrollbars: bool = True,
    ):
        """Container that stacks widgets in a horizontal grid when added to a Layout

        Args:
            cols (int): The number of columns in the grid. The number of rows is determined by the
                number of widgets added to the grid.
            key (Hashable, optional): The key to use for the VStack. Defaults to None.
            width (int, optional): The width of the VStack. Defaults to None.
            padding (PaddingType, optional): The padding around the VStack. Defaults to None.
            disabled (bool, optional): Whether the VStack is disabled. Defaults to False.
            sticky (str, optional): The sticky value for the VStack. Defaults to "nsew".
            valign (VAlign, optional): The vertical alignment for the widgets in the VStack.
                Defaults to None.
            halign (HAlign, optional): The horizontal alignment for the widgets in the VStack.
                Defaults to None.
            vexpand (bool, optional): Whether the Stack should expand vertically.
                Defaults to True.
            hexpand (bool, optional): Whether the Stack should expand horizontally.
                Defaults to True.
            vspacing (PadType, optional): Vertical spacing between widgets. Defaults to None.
            hspacing (PadType, optional): Horizontal spacing between widgets. Defaults to None.
            vscrollbar (bool): Whether to include a vertical scrollbar. Defaults to False.
            autohide_scrollbars (bool): Whether to hide scrollbars when not needed. Defaults to True.

        Note:
            If width is specified, the VStack will not expand to fill the available space and the
            expand parameter will be ignored.
        """
        super().__init__(
            key=key,
            height=None,
            width=width,
            padding=padding,
            disabled=disabled,
            sticky=sticky,
            valign=valign,
            halign=halign,
            vexpand=vexpand,
            hexpand=hexpand,
            distribute=False,
            vspacing=vspacing,
            hspacing=hspacing,
            vscrollbar=vscrollbar,
            # hscrollbar=hscrollbar,
            autohide_scrollbars=autohide_scrollbars,
        )
        self.cols = cols

    @property
    def layout(self) -> list[list[BaseWidget]]:
        """Return the layout of the Stack"""
        if self.distribute:
            raise NotImplementedError("distribute not yet implemented for HGrid")
        else:
            # grid the widgets in the order they were added
            # chunk items into lists self.cols long
            self._layout_lol = [
                self._layout_list[i : i + self.cols]
                for i in range(0, len(self._layout_list), self.cols)
            ]
        return self._layout_lol

    @layout.setter
    def layout(self, layout: list[list[BaseWidget]]):
        """Set the layout of the Stack"""
        ...

    @debug_watch
    def _insert_widget_row_col(
        self, widget: BaseWidget, row: int, col: int, is_vertical: bool = True
    ):
        """Insert a widget into the container after the container has been created
            Intended for use at run-time only when widgets need to be added dynamically

        Args:
            widget: (Widget) the widget to add
            row: (int) the row to insert the widget into
            col: (int) the column to insert the widget into

        Note: widgets are placed in a grid with row, col coordinates by the _LayoutMixin class.
        All containers store widgets internally as a list so we need to convert the row, col
        coordinates to a list index.
        """
        index = self._row_col_to_index(row, col)
        self._layout_list.insert(index, widget)

        # redraw the layout which will create the widget
        self._layout(self.frame, self.window)

    def _row_col_to_index(self, row: int, col: int):
        """Convert row, col coordinates to a list index"""
        # the HGrid layout converts a list into a list of lists where each list is length self.cols
        # convert row, col to back to a list index
        return row * self.cols + col
