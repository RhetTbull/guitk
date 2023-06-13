""" ttk Spinbox widget"""

from __future__ import annotations

import tkinter as tk
import tkinter.ttk as ttk
from typing import TYPE_CHECKING, Hashable

from .basewidget import BaseWidget
from .events import Event, EventCommand, EventType
from .types import CommandType, PadType, TooltipType

if TYPE_CHECKING:
    from .window import Window

__all__ = ["Spinbox", "SpinBox"]

# Reference: https://tkdocs.com/pyref/ttk_spinbox.html and https://tkdocs.com/shipman/spinbox.html

_valid_ttk_spinbox_attributes = {
    "values",
    "from_",
    "to",
    "increment",
    "format",
    "command",
    "wrap",
    "exportselection",
    "font",
    "invalidcommand",
    "justify",
    "show",
    "state",
    "textvariable",
    "validate",
    "validatecommand",
    "width",
    "xscrollcommand",
    "foreground",
    "background",
    "takefocus",
    "cursor",
    "style",
    "class",
}


class Spinbox(BaseWidget):
    """ttk.Spinbox"""

    def __init__(
        self,
        from_value: float | None = None,
        to_value: float | None = None,
        values: tuple[str] | None = None,
        increment: float | None = None,
        wrap: bool = False,
        key: Hashable = None,
        target_key: Hashable = None,
        disabled: bool = False,
        columnspan: int | None = None,
        rowspan: int | None = None,
        padx: PadType | None = None,
        pady: PadType | None = None,
        events: bool = True,
        sticky: str | None = None,
        tooltip: TooltipType = None,
        command: CommandType | None = None,
        weightx: int | None = None,
        weighty: int | None = None,
        focus: bool = False,
        **kwargs,
    ):
        """Initialize a ttk.Spinbox widget

        Args:
            from_value (float): Minimum value for the spinbox. See also values.
            to_value (float): Maximum value for the spinbox. See also values.
            values: (tuple[str], optional): Tuple of strings for the spinbox values. Defaults to None.
            increment (float, optional): Increment between from_value and to_value. Defaults to None (which is equivalent to 1.0).
            wrap (bool, optional): If True, wrap around from_value to to_value. Defaults to False.
            key (Hashable, optional): Unique key for this widget. Defaults to None.
            target_key: (Hashable, optional): Unique key for the target widget. Defaults to None.
            default (str | None, optional): Default text for the entry box. Defaults to None.
            disabled (bool, optional): If True, widget is disabled. Defaults to False.
            columnspan (int | None, optional): Number of columns to span. Defaults to None.
            rowspan (int | None, optional): Number of rows to span. Defaults to None.
            padx (PadType | None, optional): X padding. Defaults to None.
            pady (PadType | None, optional): Y padding. Defaults to None.
            events (bool, optional): Enable events for this widget. Defaults to True.
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
            There are two ways to specify the possible values of the widget.
            One way is to provide a tuple of strings as the value of the values option.
            For example, values=('red', 'blue', 'green') would allow only those three strings as values.
            To configure the widget to accept a range of numeric values, see from_value, to_value, and interval.

            Emits the following events:
                EventType.SpinboxUpdate: When the spinbox value is updated.
                EventType.SpinboxDecrement: When the spinbox value is decremented.
                EventType.SpinboxIncrement: When the spinbox value is incremented.
        """

        if values and (from_value or to_value):
            raise ValueError(
                "Spinbox: Cannot specify both values and from_value/to_value"
            )

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
        self.widget_type = "ttk.Spinbox"
        self.key = key or "Spinbox"
        self.target_key = target_key
        self.kwargs = kwargs

        self.from_ = from_value
        self.to = to_value
        self.increment = increment
        self.values = values
        self.wrap = wrap

    @property
    def value(self):
        return self.widget.get()

    @value.setter
    def value(self, value):
        self.widget.set(value)

    def _create_widget(self, parent, window: "Window", row, col):
        """Create the ttk.Spinbox widget"""

        self.window = window
        event = Event(self, window, self.key, EventType.SpinboxUpdate)

        # build arg list for ttk.Spinbox
        kwargs = {
            k: v for k, v in self.kwargs.items() if k in _valid_ttk_spinbox_attributes
        }

        self.widget = ttk.Spinbox(
            parent,
            from_=self.from_,
            to=self.to,
            values=self.values,
            wrap=self.wrap,
            increment=self.increment,
            command=window._make_callback(event),
            **kwargs,
        )
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        # bind <<Decrement>> and <<Increment>> events
        event_decrement = Event(self, window, self.key, EventType.SpinboxDecrement)
        self.widget.bind("<<Decrement>>", window._make_callback(event_decrement))
        event_increment = Event(self, window, self.key, EventType.SpinboxIncrement)
        self.widget.bind("<<Increment>>", window._make_callback(event_increment))

        if self._command:
            self.events = True
            window._bind_command(
                EventCommand(
                    widget=self,
                    key=self.key,
                    event_type=EventType.SpinboxUpdate,
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
                    event_type=EventType.SpinboxUpdate,
                    command=update_target,
                )
            )

        if self._disabled:
            self.widget.state(["disabled"])

        return self.widget

    @property
    def spinbox(self):
        """Return the ttk.Spinbox widget"""
        return self.widget


class SpinBox(Spinbox):
    """Snake case alias for Spinbox"""

    ...
