""" Widget base class """

from __future__ import annotations

import tkinter as tk
import tkinter.ttk as ttk
from typing import Any, Callable, Hashable

from guitk.tkroot import _TKRoot

from .events import Event, EventCommand, EventType
from .types import CommandType, TooltipType, ValueType


class Widget:
    """Basic abstract base class for all tk widgets"""

    def __init__(
        self,
        key: Hashable | None = None,
        disabled: bool = False,
        rowspan: int | None = None,
        columnspan: int | None = None,
        padx: int | None = None,
        pady: int | None = None,
        events: bool = True,
        sticky: str | None = None,
        tooltip: TooltipType = None,
        command: CommandType | None = None,
        value_type: ValueType | None = None,
        **kwargs,
    ):
        self.key = key
        self._disabled = disabled
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.padx = padx
        self.pady = pady
        self.events = events
        self.sticky = sticky or ""
        self.tooltip = tooltip

        self._command = command
        self._commands = {}

        self.widget_type = None
        self._tk = _TKRoot()
        self.widget = None
        self._value = value_type() if value_type is not None else tk.StringVar()

        # set by _create_widget in inherited classes
        self._parent = None
        self.window = None

    @property
    def value(self):
        return self._value.get()

    @value.setter
    def value(self, value):
        self._value.set(value)

    def _grid(self, row, column, rowspan, columnspan):
        sticky = self.sticky or tk.W
        self.widget.grid(
            row=row,
            column=column,
            columnspan=columnspan,
            rowspan=rowspan,
            sticky=sticky,
        )

        if self.padx is not None or self.pady is not None:
            self.widget.grid_configure(padx=self.padx, pady=self.pady)

    def bind_event(self, event_name: str, command: Callable[[], Any] | None = None):
        """Bind a tkinter event to widget; will result in an Event being sent to handle_event when triggered.
        Optionally bind command to the event"""
        event = Event(self, self.window, self.key, event_name)
        self.widget.bind(event_name, self.window._make_callback(event))

        if command:
            self.window._bind_command(
                EventCommand(
                    widget=self, key=self.key, event_type=event_name, command=command
                )
            )

    @property
    def state(self) -> bool:
        return self.widget["state"]

    @property
    def disabled(self) -> bool:
        return self.widget["state"] == "disabled"

    @disabled.setter
    def disabled(self, value: bool) -> None:
        self.widget["state"] = "disabled" if value else "normal"
