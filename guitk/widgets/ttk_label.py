"""ttk.Label widget"""

from __future__ import annotations

import tkinter.ttk as ttk
from tkinter import font

from .events import Event, EventCommand, EventType
from .widget import Widget


class Label(Widget):
    """Text label"""

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
        events=False,
        sticky=None,
        tooltip=None,
        anchor=None,
        cursor=None,
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
            anchor=anchor,
            cursor=cursor,
        )
        self.widget_type = "ttk.Label"
        self.text = text
        self.key = key or text
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.width = width

    def _create_widget(self, parent, window: "Window", row, col):
        self.window = window
        self._parent = parent
        self.widget = ttk.Label(
            parent,
            text=self.text,
            width=self.width,
            anchor=self.anchor,
            cursor=self.cursor,
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
            cursor=cursor or "hand1",
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

