"""HLayout widget to enable SwiftUI style layout"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from guitk.constants import GUITK

from .layout import HLayout, VLayout, pop_parent, push_parent
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

    layout = []

    def _layout(self, parent: tk.BaseWidget, window: Window, autoframe: bool):
        """Create widgets from layout"""
        # as this is a mixin, make sure class being mixed into has necessary attributes
        try:
            valign = self.layout.valign.lower() if self.layout.valign else "top"
            halign = self.layout.halign.lower() if self.layout.halign else "left"
        except AttributeError:
            try:
                valign = self.valign.lower() if self.valign else "top"
                halign = self.halign.lower() if self.halign else "left"
            except AttributeError:
                valign = "top"
                halign = "left"

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

        row_offset = 0
        for row_count, row in enumerate(layout):
            col_offset = 0

            if autoframe and (
                len(row) != 1
                or row[0].widget_type not in {"ttk.Frame", "tk.Frame", "LabelFrame"}
            ):
                row_ = [
                    _Container(layout=[row], autoframe=False, sticky="nsew", weightx=1)
                ]
            else:
                row_ = row
            for col_count, widget in enumerate(row_):
                if widget is None:
                    # add blank label to maintain column spacing
                    widget = Label("", disabled=True, events=False)

                widget.key = (
                    widget.key or f"{widget.widget_type},{row_count},{col_count}"
                )
                widget._create_widget(
                    parent, window, row_count + row_offset, col_count + col_offset
                )
                if tooltip := widget.tooltip or window.tooltip:
                    _tooltip = tooltip(widget.key) if callable(tooltip) else tooltip
                    widget._tooltip = (
                        Hovertip(widget.widget, _tooltip) if _tooltip else None
                    )
                else:
                    widget._tooltip = None

                # configure style if needed
                if widget._style_kwargs:
                    style = ttk.Style()
                    style_name = f"{id(widget)}.{widget.widget.winfo_class()}"
                    style.configure(style_name, **widget._style_kwargs)
                    widget.widget.configure(style=style_name)

                window._widgets.append(widget)
                widget.parent = self
                window._widget_by_key[widget.key] = widget

                # configure row/columns/weight
                if widget.rowspan and widget.rowspan > 1:
                    row_offset += widget.rowspan - 1
                if widget.columnspan and widget.columnspan > 1:
                    col_offset += widget.columnspan - 1

                if widget.weightx is not None:
                    parent.grid_columnconfigure(
                        col_count + col_offset, weight=widget.weightx
                    )
                    # if widget created with scrolled_widget_factory
                    # then need to configure the inner widget
                    if getattr(widget.widget, "_guitk_framed_widget", False):
                        widget.widget.grid_columnconfigure(0, weight=widget.weightx)
                if widget.weighty is not None:
                    parent.grid_rowconfigure(
                        row_count + row_offset, weight=widget.weighty
                    )
                    # configure inner widget if needed
                    if getattr(widget.widget, "_guitk_framed_widget", False):
                        widget.widget.grid_rowconfigure(0, weight=widget.weighty)

                # take focus if needed
                if widget._focus:
                    widget.widget.focus()


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

        self._autoframe = autoframe

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
        self.style = style
        self.borderwidth = borderwidth
        self.padding = padding
        self.relief = relief
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
        if self.style is not None:
            kwargs["style"] = self.style

        if self.frametype == GUITK.ELEMENT_FRAME:
            self.widget = ttk.Frame(
                parent,
                width=self.width,
                height=self.height,
                borderwidth=self.borderwidth,
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
            self._layout(self.widget, self.window, autoframe=self._autoframe)

        if self.width or self.height:
            self.widget.grid_propagate(0)

        if self._disabled:
            self.widget.state(["disabled"])
        return self.widget

    @property
    def frame(self):
        """Return the Tk frame widget"""
        return self.widget

    @property
    def value(self):
        pass

    @value.setter
    def value(self, value):
        pass

    def add_widget(self, widget: Widget):
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
