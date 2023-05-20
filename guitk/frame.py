"""HLayout widget to enable SwiftUI style layout"""

from __future__ import annotations

import contextlib
import tkinter as tk
from tkinter import ttk

from guitk.constants import GUITK

from ._debug import debug, debug_borderwidth, debug_relief, debug_watch
from .layout import pop_parent, push_parent
from .spacer import HSpacer, VSpacer
from .tooltips import Hovertip
from .ttk_label import Label
from .types import HAlign, LayoutType, TooltipType, VAlign, Window
from .widget import Widget

_valid_frame_attributes = {
    "cursor",
    "height",
    "padding",
    "relief",
    "style",
    "takefocus",
    "width",
}


class _LayoutMixin:
    """Mixin class to provide layout; for internal use only"""

    row_count = 0
    col_count = 0
    layout = []

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

        layout = list(self.layout)

        if valign in {"bottom", "center"}:
            layout.insert(0, [VSpacer()])
        if valign == "center":
            layout.append([VSpacer()])

        if halign in {"right", "center"}:
            for row in layout:
                row.insert(0, HSpacer())
        if halign == "center":
            for row in layout:
                row.append(HSpacer())

        debug(f"{layout=}")

        for row_count, row in enumerate(layout):
            if self.autoframe and (
                len(row) != 1
                or row[0].widget_type not in {"ttk.Frame", "tk.Frame", "LabelFrame"}
            ):
                row_ = [
                    _Container(layout=[row], autoframe=False, sticky="nsew", weightx=1)
                ]
            else:
                row_ = row
            self.row_count = row_count
            for col_count, widget in enumerate(row_):
                if widget is None:
                    # add blank label to maintain column spacing
                    widget = Label("", disabled=True, events=False)
                self._create_and_add_widget(
                    widget, parent, window, row_count, col_count
                )
                widget._row, widget._col = row_count, col_count
                self.col_count = col_count

        debug(f"{self.row_count=}, {self.col_count=}")

    def _create_and_add_widget(self, widget, parent, window, row, col):
        """Create the widget and add it to layout"""

        if not widget._has_been_created:
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
            # widget already created just need to re-grid it
            widget._grid(
                row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
            )

        # in either case, configure the widget
        self._configure_widget(widget, parent, window, row, col)

        # take focus if needed
        if widget._focus:
            widget.widget.focus()

    def _configure_widget(
        self, widget: Widget, parent: tk.BaseWidget, window: Window, row: int, col: int
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
        padx = widget.padx if widget.padx is not None else window.padx
        pady = widget.pady if widget.pady is not None else window.pady
        widget.widget.grid_configure(padx=padx, pady=pady)


class _Container(Widget, _LayoutMixin):
    """Container base class for Frame and other containers; intended for internal use only"""

    def __init__(
        self,
        frametype: GUITK = GUITK.ELEMENT_FRAME,
        key: str | None = None,
        layout: LayoutType | None = None,
        height: int | None = None,
        width: int | None = None,
        style: str | None = None,
        borderwidth: int | None = None,
        padding: int | None = None,
        relief: str = None,
        disabled: bool | None = False,
        rowspan: int | None = None,
        columnspan: int | None = None,
        text: str | None = None,
        labelanchor: str | None = None,
        sticky: str | None = None,
        tooltip: TooltipType | None = None,
        autoframe: bool | None = True,
        padx: int | None = None,
        pady: int | None = None,
        weightx: int | None = None,
        weighty: int | None = None,
        valign: VAlign | None = None,
        halign: HAlign | None = None,
        **kwargs,
    ):
        # padx and pady passed to Widget not Frame
        Widget.__init__(
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
        self.valign = valign
        self.halign = halign

    def _create_widget(self, parent, window: Window, row, col):
        self.window = window
        self._parent = parent

        kwargs = {
            k: v
            for k, v in self.kwargs.items()
            if k in _valid_frame_attributes and v is not None
        }
        if self._style is not None:
            kwargs["style"] = self._style

        if self.frametype == GUITK.ELEMENT_FRAME:
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
            self._layout(self.frame, self.window)

        if self.width or self.height:
            self.widget.grid_propagate(False)

        if self._disabled:
            self.widget.state(["disabled"])
        return self.widget

    @debug_watch
    def _add_widget_row_col(self, widget: Widget, row: int, col: int):
        """Add a widget to the container after the container has been created
            Intended for use at run-time only when widgets need to be added dynamically

        Args:
            widget: (Widget) the widget to add
        """
        # add widget to self.layout
        self._ensure_layout_size(row, col)
        self.layout[row][col] = widget
        debug(self.layout)

        # redraw the layout which will create the widget
        self._layout(self.frame, self.window)

    @debug_watch
    def _insert_widget_row_col(
        self, widget: Widget, row: int, col: int, vertical: bool = False
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
        debug(f"before insert: {self.layout}")
        if vertical:
            row = min(row, len(self.layout))
            self._ensure_layout_size(row - 1, col)
            self.layout.insert(row, [widget])
        else:
            # python list.insert() will insert at the end if index is greater than the length
            # so copy that behavior here
            self._ensure_layout_size(row, 0)
            col = min(col, len(self.layout[row]))
            self.layout[row].insert(col, widget)
        debug(f"after insert: {self.layout}")

        # redraw the layout which will create the widget
        self._layout(self.frame, self.window)

    def _ensure_layout_size(self, row: int, col: int):
        """Ensure the layout is at least row x col in size"""
        while len(self.layout) <= row:
            self.layout.append([])
        while len(self.layout[row]) <= col:
            self.layout[row].append(None)

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

    def _add_widget(self, widget: Widget):
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
        key: str | None = None,
        width: int | None = None,
        height: int | None = None,
        style: str | None = None,
        borderwidth: int | None = None,
        padding: int | None = None,
        relief: str = None,
        disabled: bool | None = False,
        rowspan: int | None = None,
        columnspan: int | None = None,
        sticky: str | None = None,
        tooltip: TooltipType | None = None,
        autoframe: bool = True,
        valign: VAlign | None = None,
        halign: HAlign | None = None,
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
        )


class LabelFrame(_Container):
    """A Frame widget with a label that can contain other widgets."""

    def __init__(
        self,
        text: str | None = None,
        layout: LayoutType | None = None,
        key: str | None = None,
        width: int | None = None,
        height: int | None = None,
        style: str | None = None,
        borderwidth: int | None = None,
        padding: int | None = None,
        relief: str = None,
        disabled: bool | None = False,
        rowspan: int | None = None,
        columnspan: int | None = None,
        labelanchor: str | None = None,
        sticky: str | None = None,
        tooltip: TooltipType | None = None,
        autoframe: bool = True,
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
        )
