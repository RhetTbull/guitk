"""ttk checkbutton widget"""

from __future__ import annotations

import tkinter as tk
import tkinter.ttk as ttk
from typing import TYPE_CHECKING, Hashable

from .basewidget import BaseWidget
from .events import Event, EventCommand, EventType
from .types import CommandType, PadType, TooltipType

if TYPE_CHECKING:
    from .window import Window

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


class Checkbutton(BaseWidget):
    """Checkbox / checkbutton"""

    def __init__(
        self,
        text: str,
        key: Hashable | None = None,
        checked: bool = False,
        disabled: bool = False,
        columnspan: int | None = None,
        rowspan: int | None = None,
        padx: PadType | None = None,
        pady: PadType | None = None,
        events: bool = True,
        sticky: str | None = None,
        tooltip: TooltipType | None = None,
        command: CommandType | None = None,
        weightx: int | None = None,
        weighty: int | None = None,
        focus: bool = False,
        **kwargs,
    ):
        """
        Initialize a ttk.Checkbutton widget.

        Args:
            text (str): Text for the checkbutton.
            key (Hashable, optional): Unique key for this widget. Defaults to None.
            checked (bool, optional): Initial state. Defaults to False (not checked).
            disabled (bool, optional): If True, widget is disabled. Defaults to False.
            columnspan (int | None, optional): Number of columns to span. Defaults to None.
            rowspan (int | None, optional): Number of rows to span. Defaults to None.
            padx (PadType | None, optional): X padding. Defaults to None.
            pady (PadType | None, optional): Y padding. Defaults to None.
            events (bool, optional): Enable events for this widget. Defaults to False.
            sticky (str | None, optional): Sticky direction for widget layout. Defaults to None.
            tooltip (TooltipType | None, optional): Tooltip text or callback to generate tooltip text. Defaults to None.
            command (CommandType | None, optional): Command callback. Defaults to None.
            weightx (int | None, optional): Weight of widget in X direction. Defaults to None.
            weighty (int | None, optional): Weight of widget in Y direction. Defaults to None.
            focus (bool, optional): If True, widget has focus. Defaults to False.
                Only one widget in a window can have focus.HLayout
            **kwargs: Additional keyword arguments are passed to ttk.Checkbutton.

        Notes:
            Unlike a regular ttk.Checkbutton, the onvalue and offvalue are always True and False.
            Emits an EventType.Checkbutton event when the checkbutton is clicked.
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
            weightx=weightx,
            weighty=weighty,
            focus=focus,
        )
        self.widget_type = "ttk.Checkbutton"
        self.text = text
        self.key = key or text
        self.columnspan = columnspan
        self.rowspan = rowspan
        self._value: tk.BooleanVar = tk.BooleanVar()
        self._checked = checked
        self.kwargs = kwargs

    def _create_widget(self, parent, window: Window, row, col):
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

        if self._checked:
            self.widget.invoke()

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
