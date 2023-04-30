"""Layout widget to enable SwiftUI style layout"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from guitk.constants import GUITK

from .layout import pop_parent, push_parent
from .tooltips import Hovertip
from .ttk_label import Label
from .types import LayoutType, TooltipType, Window
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


class LayoutMixin:
    """Mixin class to provide layout"""

    layout = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _layout(self, parent: tk.BaseWidget, window: Window, autoframe: bool):
        """Create widgets from layout"""
        # as this is a mixin, make sure class being mixed into has necessary attributes

        row_offset = 0
        for row_count, row in enumerate(self.layout):
            col_offset = 0

            if autoframe and (
                len(row) != 1
                or row[0].widget_type
                not in ["ttk.Frame", "tk.Frame", "LabelFrame"]
            ):
                row_ = [Container(layout=[row], autoframe=False)]
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

                window._widgets.append(widget)
                widget.parent = self
                window._widget_by_key[widget.key] = widget
                if widget.rowspan and widget.rowspan > 1:
                    row_offset += widget.rowspan - 1
                if widget.columnspan and widget.columnspan > 1:
                    col_offset += widget.columnspan - 1


class Container(Widget, LayoutMixin):
    """Container base class for Frame and other containers"""

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
        sticky: bool | None = None,
        tooltip: TooltipType | None = None,
        autoframe: bool | None = True,
        padx: int | None = None,
        pady: int | None = None,
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
        )
        LayoutMixin.__init__(self)

        self._autoframe = autoframe

        if frametype not in [
            GUITK.ELEMENT_FRAME,
            GUITK.ELEMENT_LABEL_FRAME,
            GUITK.ELEMENT_TK_FRAME,
        ]:
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


class Frame(Container):
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
        sticky: bool | None = None,
        tooltip: TooltipType | None = None,
        autoframe: bool = True,
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
        )


class LabelFrame(Container):
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
        sticky: bool | None = None,
        tooltip: TooltipType | None = None,
        autoframe: bool = True,
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
        )
