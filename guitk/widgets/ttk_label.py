"""ttk.Label widget"""

from __future__ import annotations

import sys
import tkinter.ttk as ttk
from tkinter import font
from typing import Hashable

from .events import Event, EventCommand, EventType
from .widget import Widget
from .types import TooltipType

_valid_ttk_label_attributes = {
    "width",
    "anchor",
    "cursor",
}


class Label(Widget):
    """Text label"""

    def __init__(
        self,
        text: str,
        key: Hashable | None = None,
        disabled: bool = False,
        rowspan: int | None = None,
        columnspan: int | None = None,
        padx: int | None = None,
        pady: int | None = None,
        events: bool = False,
        sticky: str | None = None,
        tooltip: TooltipType = None,
        **kwargs,
    ):
        super().__init__(
            key=key,
            disabled=disabled,
            rowspan=rowspan,
            columnspan=columnspan,
            padx=padx,
            pady=pady,
            events=events,
            sticky=sticky,
            tooltip=tooltip,
        )
        self.widget_type = "ttk.Label"
        self.text = text
        self.key = key or text
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.kwargs = kwargs

    def _create_widget(self, parent, window: "Window", row, col):
        self.window = window
        self._parent = parent
        kwargs_label = {
            k: v
            for k, v in self.kwargs.items()
            if k in _valid_ttk_label_attributes
        }
        self.widget = ttk.Label(
            parent,
            text=self.text,
            **kwargs_label,
        )
        self.widget["textvariable"] = self._value
        self._value.set(self.text)
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )
        if self._disabled:
            self.widget.state(["disabled"])
        return self.widget

    @property
    def label(self):
        """Return the Tk label widget"""
        return self.widget


class LinkLabel(Label):
    """Link label that responds to click"""

    def __init__(
        self,
        text,
        key=None,
        disabled=False,
        rowspan=None,
        columnspan=None,
        width=None,
        padx=None,
        pady=None,
        events=True,
        sticky=None,
        tooltip=None,
        anchor=None,
        cursor=None,
        underline_font=False,
        command=None,
    ):
        cursor = cursor or "pointinghand" if sys.platform == "darwin" else "hand2"
        super().__init__(
            text=text,
            key=key,
            disabled=disabled,
            rowspan=rowspan,
            columnspan=columnspan,
            padx=padx,
            pady=pady,
            events=events,
            sticky=sticky,
            tooltip=tooltip,
            anchor=anchor,
            cursor=cursor,
        )
        self.widget_type = "guitk.LinkLabel"
        self.text = text
        self.key = key or text
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.width = width
        self.underline_font = underline_font
        self._command = command

    def _create_widget(self, parent, window: "Window", row, col):
        super()._create_widget(parent, window, row, col)
        event = Event(self, window, self.key, EventType.LinkLabel)
        self.widget.bind("<Button-1>", window._make_callback(event))
        if self.underline_font:
            f = font.Font(self.widget, self.widget.cget("font"))
            f.configure(underline=True)
            self.widget.configure(font=f)

        if self._command:
            self.events = True
            window._bind_command(
                EventCommand(
                    widget=self,
                    key=self.key,
                    event_type=EventType.LinkLabel,
                    command=self._command,
                )
            )
