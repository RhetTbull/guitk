""" ttk Radiobutton widget """

from __future__ import annotations

import tkinter as tk
import tkinter.ttk as ttk
from typing import Any, Union

from .events import Event, EventCommand, EventType
from .widget import Widget


class Radiobutton(Widget):
    """Radiobutton class

    Note: group must be specified and will be used as key unless a separate key is specified."""

    def __init__(
        self,
        text: str,
        group: Any,
        key: str = "",
        value: Union[int, str, None] = None,
        disabled=False,
        rowspan=None,
        columnspan=None,
        padx=None,
        pady=None,
        events=True,
        sticky=None,
        tooltip=None,
        anchor=None,
        selected=False,
        command=None,
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
            command=command,
        )
        self.widget_type = "ttk.Radiobutton"
        self.text = text
        self.group = group
        self.key = key or group
        self._radiobutton_value = value if value is not None else text
        self._value = None  # will be set in _create_widget
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.selected = selected

    def _create_widget(self, parent, window: "Window", row, col):
        self.window = window
        self._parent = parent

        # assign control variable or create it if necessary
        if self.group not in self.window._radiobuttons:
            # determine type of control variable based on value
            var_type = type(self._radiobutton_value)
            if var_type == int:
                self.window._radiobuttons[self.group] = tk.IntVar(
                    value=self._radiobutton_value
                )
            elif var_type == str:
                self.window._radiobuttons[self.group] = tk.StringVar(
                    value=self._radiobutton_value
                )
            else:
                # unsupported type
                raise ValueError("value must be str or int")

        self._value = self.window._radiobuttons[self.group]

        event = Event(self, window, self.key, EventType.Radiobutton)
        self.widget = ttk.Radiobutton(
            parent,
            text=self.text,
            anchor=self.anchor,
            command=window._make_callback(event),
            variable=self._value,
            value=self._radiobutton_value,
        )
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        if self._command:
            self.events = True
            window._bind_command(
                EventCommand(
                    widget=self,
                    key=self.key,
                    event_type=EventType.Radiobutton,
                    command=self._command,
                )
            )

        if self._disabled:
            self.widget.state(["disabled"])

        if self.selected:
            self.widget.state(["selected"])
        else:
            self.widget.state(["!selected"])

        return self.widget

    @property
    def radiobutton(self):
        """Return the ttk Radiobutton widget"""
        return self.widget
