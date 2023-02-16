""" Widget base class """

from __future__ import annotations
from guitk.tkroot import _TKRoot
import tkinter as tk
import tkinter.ttk as ttk
from .events import Event, EventType, EventCommand


class Widget:
    """Basic abstract base class for all tk widgets"""

    def __init__(
        self,
        key=None,
        disabled=False,
        rowspan=None,
        columnspan=None,
        padx=None,
        pady=None,
        events=True,
        sticky=None,
        tooltip=None,
        anchor=None,
        cursor=None,
        takefocus=None,
        command=None,
        value_type=None,
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
        self.anchor = anchor
        self.cursor = cursor
        if takefocus is not None:
            self.takefocus = 1 if takefocus else 0
        else:
            self.takefocus = None

        self._command = command
        self._commands = {}

        self.widget_type = None
        self._tk = _TKRoot()
        self.widget = None
        self._value = value_type() if value_type is not None else tk.StringVar()

        # get set by _create_widget in inherited classes
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

    def bind_event(self, event_name, command=None):
        """Bind a tkinter event to widget; will result in an Event of event_type type being sent to handle_event when triggered.
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
    def state(self):
        return self.widget["state"]

    @property
    def disabled(self):
        return self.widget["state"] == "disabled"

    @disabled.setter
    def disabled(self, value):
        self.widget["state"] = "disabled" if value else "normal"
