""" ttk Scale widget"""

from __future__ import annotations

import tkinter as tk
import tkinter.ttk as ttk
from typing import TYPE_CHECKING, Hashable, Union

from .basewidget import BaseWidget
from .events import Event, EventCommand, EventType
from .types import CommandType, PadType, TooltipType

if TYPE_CHECKING:
    from .window import Window

__all__ = ["Scale"]


_valid_standard_attributes = {
    "class",
    "command",
    "cursor",
    "length",
    "orient",
    "state",
    "style",
    "takefocus",
    "value",
    "variable",
}

_valid_ttk_scale_attributes = {
    "from",
    "to",
} | _valid_standard_attributes


def _interval(from_, to, interval, value, tolerance=1e-9):
    """Clamp value to an interval between from_ and to range"""

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


class Scale(BaseWidget):
    """ttk.Scale / slider"""

    def __init__(
        self,
        from_value: float,
        to_value: float,
        value: float | None = None,
        orient: Union[tk.VERTICAL, tk.HORIZONTAL] = tk.VERTICAL,
        interval: float | None = None,
        precision: int | None = None,
        key: Hashable = None,
        target_key: Hashable = None,
        disabled: bool = False,
        columnspan: int | None = None,
        rowspan: int | None = None,
        padx: PadType | None = None,
        pady: PadType | None = None,
        events: bool = False,
        sticky: str | None = None,
        tooltip: TooltipType = None,
        command: CommandType | None = None,
        weightx: int | None = None,
        weighty: int | None = None,
        focus: bool = False,
        **kwargs,
    ):
        """Initialize a ttk.Scale widget

        Args:
            from_value (float): Minimum value for the scale.
            to_value (float): Maximum value for the scale.
            value (float, optional): Initial value for the scale. Defaults to None (from_value).
            orient (tk.VERTICAL | tk.HORIZONTAL, optional): Orientation of the scale. Defaults to tk.VERTICAL.
            interval (float, optional): Interval between values. Defaults to None (no interval).
            precision (int, optional): Number of decimal places to display. Defaults to None (no rounding).
            key (Hashable, optional): Unique key for this widget. Defaults to None.
            target_key: (Hashable, optional): Unique key for the target widget. Defaults to None.
            default (str | None, optional): Default text for the entry box. Defaults to None.
            disabled (bool, optional): If True, widget is disabled. Defaults to False.
            columnspan (int | None, optional): Number of columns to span. Defaults to None.
            rowspan (int | None, optional): Number of rows to span. Defaults to None.
            padx (PadType | None, optional): X padding. Defaults to None.
            pady (PadType | None, optional): Y padding. Defaults to None.
            events (bool, optional): Enable events for this widget. Defaults to False.
            sticky (str | None, optional): Sticky direction for widget layout. Defaults to None.
            tooltip (TooltipType | None, optional): Tooltip text or callback to generate tooltip text. Defaults to None.
            command (CommandType | None, optional): Command callback. Defaults to None.
            hscrollbar (bool, optional): Show horizontal scrollbar. Defaults to False.
            weightx (int | None, optional): Weight for horizontal resizing. Defaults to None.
            weighty (int | None, optional): Weight for vertical resizing. Defaults to None.
            focus (bool, optional): If True, widget has focus. Defaults to False.
                Only one widget in a window can have focus.HLayout
            **kwargs: Additional keyword arguments are passed to ttk.Entry.

        Note:
            Emits EventType.ScaleUpdate event when the scale value changes.
        """
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
            command=command,
            value_type=tk.DoubleVar,
            weightx=weightx,
            weighty=weighty,
            focus=focus,
        )
        self.widget_type = "ttk.Scale"
        self.key = key or "Scale"
        self.target_key = target_key
        self.kwargs = kwargs

        self.from_ = from_value
        self.to = to_value
        self.orient = orient
        self.interval = interval
        self.precision = precision
        self.initial_value = value

    @property
    def value(self):
        value = self.widget.get()
        if self.interval:
            value = _interval(self.from_, self.to, self.interval, value)
        if self.precision is not None:
            value = round(float(value), self.precision)
        return value

    @value.setter
    def value(self, value):
        self.widget.set(value)

    def _create_widget(self, parent, window: "Window", row, col):
        self.window = window
        event = Event(self, window, self.key, EventType.ScaleUpdate)
        # build arg list for ttk.Scale
        kwargs = {
            k: v for k, v in self.kwargs.items() if k in _valid_ttk_scale_attributes
        }
        kwargs["variable"] = self._value
        if self.initial_value is not None:
            self._value.set(self.initial_value)

        self.widget = ttk.Scale(
            parent,
            from_=self.from_,
            to=self.to,
            orient=self.orient,
            command=window._make_callback(event),
            **kwargs,
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
