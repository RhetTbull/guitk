"""_LayoutMixin, _Container, and Frame classes"""

from __future__ import annotations

import contextlib
import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING, Hashable

from guitk.constants import GUITK

from ._debug import debug, debug_borderwidth, debug_relief, debug_watch
from .basewidget import BaseWidget
from .layout import HLayout, VLayout, pop_parent, push_parent
from .scrolledframe import ScrolledFrame
from .spacer import HSpacer, VSpacer
from .tooltips import Hovertip
from .ttk_label import Label
from .ttk_separator import HSeparator, VSeparator
from .types import HAlign, LayoutType, PaddingType, PadType, TooltipType, VAlign

_valid_frame_attributes = {
    "cursor",
    "height",
    "padding",
    "relief",
    "style",
    "takefocus",
    "width",
}

if TYPE_CHECKING:
    from .window import Window


def rows_columns(layout: LayoutType) -> tuple[int, int]:
    """Return the number of rows and columns in a layout"""
    rows = 0
    cols = 0
    for row in layout:
        rows += 1
        cols = max(cols, len(row))
    return rows, cols


class _LayoutMixin:
    """Mixin class to provide layout; for internal use only"""

    row_count: int = 0
    col_count: int = 0
    layout = []
    distribute: bool = False
    vspacing: PadType | None = None
    hspacing: PadType | None = None

    @debug_watch
    def _layout(self, parent: tk.BaseWidget, window: Window):
        """Create widgets from layout"""
        # as this is a mixin, make sure class being mixed into has necessary attributes

        # get alignment from layout or from class attributes
        debug(self)

        valign = "top"
        halign = "left"

        # first get alignment from layout
        with contextlib.suppress(AttributeError):
            valign = self.layout.valign.lower() if self.layout.valign else valign
            halign = self.layout.halign.lower() if self.layout.halign else halign

        # if widget has alignment attributes (e.g. VStack, HStack...), use those instead
        with contextlib.suppress(AttributeError):
            valign = self.valign.lower() if self.valign else valign
            halign = self.halign.lower() if self.halign else halign

        debug(f"valign={valign}, halign={halign}")

        if isinstance(self.layout, (HLayout, VLayout)):
            # layout may have been created outside of a Window
            # so ensure the layout has a reference to the Window
            self.layout.window = window

        layout = list(self.layout)
        rows, columns = rows_columns(layout)
        debug(f"{layout=} {rows=}, {columns=}")

        layout = self._add_spacers(layout, valign, halign)
        rows, columns = rows_columns(layout)
        debug(f"_add_spacers(): {layout=} {rows=}, {columns=}")

        for row_count, row in enumerate(layout):
            # if self.autoframe and (
            #     len(row) != 1
            #     or row[0].widget_type not in {"ttk.Frame", "tk.Frame", "LabelFrame"}
            # ):
            #     row_ = [
            #         _Container(layout=[row], autoframe=False, sticky="nsew", weightx=1)
            #     ]
            # else:
            #     row_ = row
            row_ = row
            self.row_count = row_count
            for col_count, widget in enumerate(row_):
                if widget is None:
                    # add blank label to maintain column spacing
                    # widget = Label("", disabled=True, events=False)
                    continue
                self._stickyfy(widget, valign, halign)
                debug(
                    f"{widget=}, {row_count=}, {col_count=}, {widget.sticky=} {widget.weightx=} {widget.weighty=}"
                )
                self._create_and_add_widget(
                    widget, parent, window, row_count, col_count
                )
                self.col_count = col_count

        debug(f"{self.row_count=}, {self.col_count=}")

    def _add_spacers(
        self, layout: LayoutType, valign: VAlign, halign: HAlign
    ) -> LayoutType:
        """Add spacers to layout"""

        rows, columns = rows_columns(layout)
        orientation = "vertical" if rows > 1 else "horizontal"
        new_layout = []
        for row in layout:
            new_row = row.copy()
            widget_idx = -1
            if halign in {"right", "center"}:
                if widget := new_row[0]:
                    # not None
                    if not widget.weightx:
                        new_row.insert(0, HSpacer())
                    else:
                        widget.columnspan = (
                            widget.columnspan + 1 if widget.columnspan else 2
                        )
                        new_row.append(None)
                        widget_idx = 0
            if halign == "center":
                if widget := new_row[widget_idx]:
                    if not widget.weightx:
                        new_row.append(HSpacer())
                    else:
                        widget.columnspan = widget.columnspan + 1
                        new_row.append(None)

            new_layout.append(new_row)

        if orientation == "horizontal":
            if valign in {"bottom", "center"}:
                # there's only one row so add spacers above/below as needed
                spacer_row = []
                for idx, widget in enumerate(new_layout[0]):
                    if not widget.weighty:
                        spacer_row.append(VSpacer())
                    else:
                        spacer_row.append(widget)
                        rowspan = 1 if valign == "bottom" else 2
                        widget.rowspan = (
                            widget.rowspan + rowspan if widget.rowspan else rowspan + 1
                        )
                        new_layout[0][idx] = None
                new_layout.insert(0, spacer_row)
            if valign in {"center"}:
                spacer_row = []
                for widget in new_layout[-1]:
                    if widget is None or widget.weighty is not None:
                        spacer_row.append(None)
                    else:
                        spacer_row.append(VSpacer())
                new_layout.append(spacer_row)
        else:
            rows, columns = rows_columns(new_layout)
            if valign in {"bottom", "center"}:
                new_layout.insert(
                    0,
                    [VSpacer(columnspan=columns), *[None for _ in range(columns - 1)]],
                )
            if valign in {"center"}:
                new_layout.append(
                    [
                        VSpacer(columnspan=columns),
                        *[None for _ in range(columns - 1)],
                    ]
                )

        return new_layout

    def _stickyfy(self, widget: BaseWidget, valign: str, halign: str):
        """Add correct stickiness to widget to achieve alignment"""
        sticky = ""
        weightx = 0
        weighty = 0
        if valign in {"top"}:
            sticky += "n"
        if valign in {"bottom"}:
            sticky += "s"
        if halign in {"right"}:
            sticky += "e"
        if halign in {"left"}:
            sticky += "w"
        if not widget.sticky:
            widget.sticky = sticky

    def _create_and_add_widget(self, widget, parent, window, row, col):
        """Create the widget and add it to layout"""

        if not widget._has_been_created:
            widget._set_parent_window(parent, window)
            # create the widget
            widget.key = widget.key or f"{widget.widget_type},{row},{col}"
            widget._create_widget(parent, window, row, col)

            # add tooltip if needed
            if tooltip := widget.tooltip or window.tooltip:
                _tooltip = tooltip(widget.key) if callable(tooltip) else tooltip
                widget._tooltip = (
                    Hovertip(widget.widget, _tooltip) if _tooltip else None
                )
            else:
                widget._tooltip = None

            window._widgets.append(widget)
            widget.parent = self
            window._widget_by_key[widget.key] = widget

            widget._has_been_created = True
        else:
            # grid the widget
            widget._grid(
                row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
            )

        widget._set_row_col(row, col)
        self._configure_widget(widget, parent, window, row, col)

    @debug_watch
    def _configure_widget(
        self,
        widget: BaseWidget,
        parent: tk.BaseWidget,
        window: Window,
        row: int,
        col: int,
    ):
        """Configure the widget"""

        # configure style if needed
        if widget._style_kwargs:
            style = ttk.Style()
            style_name = f"{id(widget)}.{widget.widget.winfo_class()}"
            style.configure(style_name, **widget._style_kwargs)
            widget.widget.configure(style=style_name)

        # configure row/columns/weight
        row_offset = 0
        col_offset = 0

        if widget.rowspan and widget.rowspan > 1:
            row_offset += widget.rowspan - 1
        if widget.columnspan and widget.columnspan > 1:
            col_offset += widget.columnspan - 1

        if widget.weightx is not None:
            parent.grid_columnconfigure(col + col_offset, weight=widget.weightx)
            # if widget created with scrolled_widget_factory
            # then need to configure the inner widget
            if getattr(widget.widget, "_guitk_framed_widget", False):
                widget.widget.grid_columnconfigure(0, weight=widget.weightx)
        if widget.weighty is not None:
            parent.grid_rowconfigure(row + row_offset, weight=widget.weighty)
            # configure inner widget if needed
            if getattr(widget.widget, "_guitk_framed_widget", False):
                widget.widget.grid_rowconfigure(0, weight=widget.weighty)

        # configure padding
        # if container has vspacing/hspacing and widget does not, use container's values
        if self.vspacing is not None and widget.pady is None:
            widget.pady = self.vspacing
        if self.hspacing is not None and widget.padx is None:
            widget.padx = self.hspacing
        padx = widget.padx if widget.padx is not None else window.padx
        pady = widget.pady if widget.pady is not None else window.pady
        widget.widget.grid_configure(padx=padx, pady=pady)

        # take focus if needed
        if widget._focus:
            widget.widget.focus()


class _Container(BaseWidget, _LayoutMixin):
    """Container base class for Frame and other containers; intended for internal use only"""

    def __init__(
        self,
        frametype: GUITK = GUITK.ELEMENT_FRAME,
        key: Hashable | None = None,
        layout: LayoutType | None = None,
        height: int | None = None,
        width: int | None = None,
        style: str | None = None,
        borderwidth: int | None = None,
        padding: PaddingType | None = None,
        relief: str = None,
        disabled: bool | None = False,
        rowspan: int | None = None,
        columnspan: int | None = None,
        text: str | None = None,
        labelanchor: str | None = None,
        sticky: str | None = None,
        tooltip: TooltipType | None = None,
        autoframe: bool | None = True,
        padx: PadType | None = None,
        pady: PadType | None = None,
        weightx: int | None = None,
        weighty: int | None = None,
        valign: VAlign | None = None,
        halign: HAlign | None = None,
        vspacing: PadType | None = None,
        hspacing: PadType | None = None,
        vscrollbar: bool = False,
        # hscrollbar: bool = False,
        autohide_scrollbars: bool = True,
        **kwargs,
    ):
        # padx and pady passed to Widget not Frame
        BaseWidget.__init__(
            self,
            key=key,
            disabled=disabled,
            rowspan=rowspan,
            columnspan=columnspan,
            sticky=sticky,
            tooltip=tooltip,
            padx=padx,
            pady=pady,
            weightx=weightx,
            weighty=weighty,
        )
        _LayoutMixin.__init__(self)

        # if autoframe is True, each widget or row of widgets will be placed in a frame
        self.autoframe = autoframe

        if frametype not in {
            GUITK.ELEMENT_FRAME,
            GUITK.ELEMENT_LABEL_FRAME,
            GUITK.ELEMENT_TK_FRAME,
        }:
            raise ValueError(f"bad frametype: {frametype}")
        self.frametype = frametype
        self.widget_type = frametype.value
        self.key = key or self.widget_type
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.width = width
        self.height = height
        self._style = style  # Widget has style() method so can't use self.style
        self.borderwidth = debug_borderwidth() or borderwidth
        self.padding = padding
        self.relief = debug_relief() or relief
        self.layout = layout or [[]]
        self.text = text
        self.labelanchor = labelanchor or "nw"
        self.kwargs = kwargs
        self.valign = valign.lower() if valign else None
        self.halign = halign.lower() if halign else None
        self.vspacing = vspacing
        self.hspacing = hspacing
        self.vscrollbar = vscrollbar
        # self.hscrollbar = hscrollbar
        self.autohide = autohide_scrollbars

    def remove(self, key_or_widget: Hashable | BaseWidget):
        """ "Remove widget from layout and destroy it.

        Args:
            key_or_widget (Hashable | Widget): The key or widget to remove. If a key is given,
                the first widget with that key will be removed.

        Raises:
            ValueError: If the widget is not found in the layout.
        """
        for row in self.layout:
            for idx, widget in enumerate(row):
                if widget == key_or_widget or widget.key == key_or_widget:
                    widget = row.pop(idx)
                    self.window._forget_widget(widget)
                    widget.widget.grid_forget()
                    widget.widget.destroy()
                    return
        raise ValueError(f"Widget not found: {key_or_widget}")

    def _create_widget(self, parent, window: Window, row, col):
        kwargs = {
            k: v
            for k, v in self.kwargs.items()
            if k in _valid_frame_attributes and v is not None
        }
        if self._style is not None:
            kwargs["style"] = self._style

        if self.frametype == GUITK.ELEMENT_FRAME:
            # if self.vscrollbar or self.hscrollbar:
            if self.vscrollbar:
                self.widget = ScrolledFrame(
                    parent,
                    vscrollbar=self.vscrollbar,
                    # hscrollbar=self.hscrollbar,
                    autohide=self.autohide,
                    width=self.width,
                    height=self.height,
                    borderwidth=self.borderwidth,
                    relief=self.relief,
                    **kwargs,
                )
            else:
                self.widget = ttk.Frame(
                    parent,
                    width=self.width,
                    height=self.height,
                    borderwidth=self.borderwidth,
                    relief=self.relief,
                    **kwargs,
                )
        elif self.frametype == GUITK.ELEMENT_TK_FRAME:
            self.widget = tk.Frame(
                parent,
                width=self.width,
                height=self.height,
                borderwidth=self.borderwidth,
                padx=self.padx,
                pady=self.pady,
                **kwargs,
            )
        else:
            self.widget = ttk.LabelFrame(
                parent,
                text=self.text,
                width=self.width,
                height=self.height,
                labelanchor=self.labelanchor,
                borderwidth=self.borderwidth,
                relief=self.relief,
                **kwargs,
            )

        if self.padding is not None and self.frametype != GUITK.ELEMENT_TK_FRAME:
            self.widget.configure(padding=self.padding)
        if self.relief is not None:
            self.widget["relief"] = self.relief
        if self.borderwidth is not None:
            self.widget["borderwidth"] = self.borderwidth

        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        if self.layout:
            self._layout(self.frame, window)

        if self.width or self.height:
            debug(f"{self.width=} {self.height=}")
            self.widget.grid_propagate(False)

        if self._disabled:
            self.widget.state(["disabled"])
        return self.widget

    def _insert_widget_row_col(
        self, widget: BaseWidget, row: int, col: int, vertical: bool = False
    ):
        """Insert a widget into the container after the container has been created
            Intended for use at run-time only when widgets need to be added dynamically

        Args:
            widget: (Widget) the widget to add
            row: (int) the row to insert the widget into
            col: (int) the column to insert the widget into
            vertical: (bool) if True, insert the widget vertically
        """
        # add widget to self.layout
        if vertical:
            row = min(row, len(self.layout))
            self._ensure_layout_size(row - 1, col or None)
            self.layout.insert(row, [widget])
        else:
            # python list.insert() will insert at the end if index is greater than the length
            # so copy that behavior here
            col = min(col, len(self.layout[row]))
            self._ensure_layout_size(row, None)
            self.layout[row].insert(col, widget)

        # redraw the layout which will create the widget
        self._layout(self.frame, self.window)

    def _ensure_layout_size(self, row: int, col: int | None):
        """Ensure the layout is at least row x col in size

        Args:
            row: (int) the row size to ensure
            col: (int or None) the column size to ensure; if None, does not add None to columns
        """
        while len(self.layout) <= row:
            self.layout.append([])
        if col is not None:
            while len(self.layout[row]) <= col:
                self.layout[row].append(None)

    def _pop_widget_row_col(
        self, row: int, col: int, vertical: bool = False
    ) -> BaseWidget:
        """Remove a widget from the container after the container has been created and return it
            Intended for use at run-time only when widgets need to be added dynamically

        Args:
            row: (int) the row to remove the widget from
            col: (int) the column to remove the widget from
            vertical: (bool) if True, remove the widget vertically

        Returns:
            Widget: the widget that was removed

        Raises:
            IndexError: if the row or column is out of range
        """
        try:
            widget = self.layout[row].pop(col)
            if vertical and not self.layout[row]:
                self.layout.pop(row)
        except IndexError as e:
            raise IndexError(f"No widget at row={row}, col={col}") from e

        widget.widget.grid_forget()
        self._layout(self.frame, self.window)

        return widget

    @property
    def frame(self):
        """Return the Tk Frame widget"""
        return self.widget

    @property
    def value(self):
        pass

    @value.setter
    def value(self, value):
        pass

    def _add_widget(self, widget: BaseWidget):
        """Add a widget to the frame's layout"""
        self.layout[0].append(widget)

    def __enter__(self):
        push_parent(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pop_parent()
        return False


class _VerticalContainer(_Container):
    """A Container class that lays out widgets vertically"""

    def __exit__(self, exc_type, exc_val, exc_tb):
        # reorder the layout to be vertical
        self.layout = [[x] for x in self.layout[0]]
        pop_parent()
        return False


class Frame(_Container):
    """A Frame widget that can contain other widgets."""

    def __init__(
        self,
        layout: LayoutType | None = None,
        key: Hashable | None = None,
        width: int | None = None,
        height: int | None = None,
        style: str | None = None,
        borderwidth: int | None = None,
        padding: PaddingType | None = None,
        relief: str = None,
        disabled: bool | None = False,
        rowspan: int | None = None,
        columnspan: int | None = None,
        sticky: str | None = None,
        tooltip: TooltipType | None = None,
        autoframe: bool = True,
        valign: VAlign | None = None,
        halign: HAlign | None = None,
        weightx: int | None = None,
        weighty: int | None = None,
        **kwargs,
    ):
        super().__init__(
            frametype=GUITK.ELEMENT_FRAME,
            key=key,
            width=width,
            height=height,
            layout=layout,
            style=style,
            borderwidth=borderwidth,
            padding=padding,
            relief=relief,
            disabled=disabled,
            rowspan=rowspan,
            columnspan=columnspan,
            sticky=sticky,
            tooltip=tooltip,
            autoframe=autoframe,
            kwargs=kwargs,
            valign=valign,
            halign=halign,
            weightx=weightx,
            weighty=weighty,
        )


class LabelFrame(_Container):
    """A Frame widget with a label that can contain other widgets."""

    def __init__(
        self,
        text: str | None = None,
        layout: LayoutType | None = None,
        key: Hashable | None = None,
        width: int | None = None,
        height: int | None = None,
        style: str | None = None,
        borderwidth: int | None = None,
        padding: PaddingType | None = None,
        relief: str = None,
        disabled: bool | None = False,
        rowspan: int | None = None,
        columnspan: int | None = None,
        labelanchor: str | None = None,
        sticky: str | None = None,
        tooltip: TooltipType | None = None,
        autoframe: bool = True,
        weightx: int | None = None,
        weighty: int | None = None,
        valign: VAlign | None = None,
        halign: HAlign | None = None,
        **kwargs,
    ):
        super().__init__(
            frametype=GUITK.ELEMENT_LABEL_FRAME,
            key=key,
            text=text,
            width=width,
            height=height,
            layout=layout,
            style=style,
            borderwidth=borderwidth,
            padding=padding,
            relief=relief,
            disabled=disabled,
            rowspan=rowspan,
            columnspan=columnspan,
            labelanchor=labelanchor,
            sticky=sticky,
            tooltip=tooltip,
            autoframe=autoframe,
            kwargs=kwargs,
            valign=valign,
            halign=halign,
            weightx=weightx,
            weighty=weighty,
        )
