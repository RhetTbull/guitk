"""ttk checkbutton widget"""

from __future__ import annotations

import tkinter as tk
import tkinter.ttk as ttk
from typing import Hashable

from .events import Event, EventCommand, EventType
from .types import CommandType, TooltipType
from .widget import Widget

__all__ = ["Checkbutton", "CheckButton"]

_valid_standard_attributes = {
    "class",
    "compound",
    "cursor",
    "image",
    "state",
    "style",
    "takefocus",
    "text",
    "textvariable",
    "underline",
    "width",
}

_valid_ttk_checkbutton_attributes = {
    "command",
    "variable",
    # "offvalue",
    # "onvalue",
} | _valid_standard_attributes


class Checkbutton(Widget):
    """Checkbox / checkbutton"""

    def __init__(
        self,
        text: str,
        key=Hashable,
        disabled: bool = False,
        columnspan: int | None = None,
        rowspan: int | None = None,
        padx: int | None = None,
        pady: int | None = None,
        events: bool = True,
        sticky: str | None = None,
        tooltip: TooltipType | None = None,
        command: CommandType | None = None,
        **kwargs,
    ):
        """
        Initialize a Checkbutton widget.

        Args:
            text (str): Text for the checkbutton.
            key (Hashable, optional): Unique key for this widget. Defaults to None.
            disabled (bool, optional): If True, widget is disabled. Defaults to False.
            columnspan (int | None, optional): Number of columns to span. Defaults to None.
            rowspan (int | None, optional): Number of rows to span. Defaults to None.
            padx (int | None, optional): X padding. Defaults to None.
            pady (int | None, optional): Y padding. Defaults to None.
            events (bool, optional): Enable events for this widget. Defaults to False.
            sticky (str | None, optional): Sticky direction for widget layout. Defaults to None.
            tooltip (TooltipType | None, optional): Tooltip text or callback to generate tooltip text. Defaults to None.
            command (CommandType | None, optional): Command callback. Defaults to None.
            **kwargs: Additional keyword arguments are passed to ttk.Checkbutton.

        Notes:
            Unlike a regular ttk.Checkbutton, the onvalue and offvalue are always True and False.
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
        )
        self.widget_type = "ttk.Checkbutton"
        self.text = text
        self.key = key or text
        self.columnspan = columnspan
        self.rowspan = rowspan
        self._value = tk.BooleanVar()
        self.kwargs = kwargs

    def _create_widget(self, parent, window: "Window", row, col):
        self.window = window
        self._parent = parent
        event = Event(self, window, self.key, EventType.Checkbutton)

        # build arg list for Checkbutton
        kwargs_checkbutton = {
            k: v
            for k, v in self.kwargs.items()
            if k in _valid_ttk_checkbutton_attributes
        }

        self.widget = ttk.Checkbutton(
            parent,
            text=self.text,
            anchor=self.kwargs.get("anchor"),
            command=window._make_callback(event),
            variable=self._value,
            onvalue=True,
            offvalue=False,
            **kwargs_checkbutton,
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
                    event_type=EventType.Checkbutton,
                    command=self._command,
                )
            )

        if self._disabled:
            self.widget.state(["disabled"])
        return self.widget

    @property
    def checkbutton(self):
        """Return the ttk.Checkbutton widget"""
        return self.widget


class CheckButton(Checkbutton):
    """Checkbox / checkbutton"""

    pass
