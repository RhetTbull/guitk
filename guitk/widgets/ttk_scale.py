""" ttk Scale widget"""

from __future__ import annotations

import tkinter as tk
import tkinter.ttk as ttk

from .events import Event, EventCommand, EventType
from .widget import Widget


def _interval(from_, to, interval, value, tolerance=1e-9):
    """clamp value to an interval between from_ and to range"""

    if interval > (to - from_):
        raise ValueError("Invalid increment")

    if value < from_ or value > to:
        raise ValueError("Invalid value")

    if abs(value - from_) < tolerance or abs(value - to) < tolerance:
        return value

    quotient, remainder = divmod(value, interval)
    if remainder < tolerance:
        return quotient * interval

    half_increment = interval / 2
    if remainder > half_increment:
        return interval * (quotient + 1)
    else:
        return interval * quotient

class Scale(Widget):
    """ttk.Scale / slider"""

    def __init__(
        self,
        from_value: float,
        to_value: float,
        value: float | None =None,
        orient=tk.VERTICAL,
        interval=None,
        precision=None,
        key=None,
        target_key=None,
        disabled=False,
        columnspan=None,
        rowspan=None,
        padx=None,
        pady=None,
        length=None,
        events=True,
        sticky=None,
        tooltip=None,
        takefocus=None,
        command=None,
        cursor=None,
        style=None,
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
            anchor=None,
            takefocus=takefocus,
            command=command,
            value_type=tk.DoubleVar,
        )
        self.widget_type = "ttk.Scale"
        self.key = key or "Scale"
        self.target_key = target_key

        self._cursor = cursor
        self._from_ = from_value
        self._to = to_value
        self._orient = orient
        self._interval = interval
        self._precision = precision
        self._style = style
        self._length = length
        self._initial_value = value
        self._takefocus = takefocus

        self.columnspan = columnspan
        self.rowspan = rowspan
        self.tooltip = tooltip

    @property
    def value(self):
        value = self.widget.get()
        if self._interval:
            value = _interval(self._from_, self._to, self._interval, value)
        if self._precision is not None:
            value = round(float(value), self._precision)
        return value

    @value.setter
    def value(self, value):
        self.widget.set(value)

    def _create_widget(self, parent, window: "Window", row, col):
        self.window = window
        self._parent = parent
        event = Event(self, window, self.key, EventType.ScaleUpdate)

        # TODO: standardize attribute names
        kwargs = {}
        for kw in ["cursor", "takefocus", "from_", "to", "length", "orient", "style"]:
            val = getattr(self, f"_{kw}")
            if val is not None:
                kwargs[kw] = val

        kwargs["variable"] = self._value
        if self._initial_value is not None:
            self._value.set(self._initial_value)

        self.widget = ttk.Scale(parent, command=window._make_callback(event), **kwargs)
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        if self._command:
            self.events = True
            window._bind_command(
                EventCommand(
                    widget=self,
                    key=self.key,
                    event_type=EventType.ScaleUpdate,
                    command=self._command,
                )
            )

        if self.target_key is not None:
            self.events = True

            def update_target():
                self.window[self.target_key].value = self.value

            window._bind_command(
                EventCommand(
                    widget=self,
                    key=self.key,
                    event_type=EventType.ScaleUpdate,
                    command=update_target,
                )
            )

        if self._disabled:
            self.widget.state(["disabled"])

        return self.widget

    @property
    def scale(self):
        """Return the ttk.Scale widget"""
        return self.widget

