""" ttk Radiobutton widget """

from __future__ import annotations

import tkinter as tk
import tkinter.ttk as ttk
from typing import TYPE_CHECKING, Any, Hashable, TypeVar, Union

from .basewidget import BaseWidget
from .events import Event, EventCommand, EventType
from .types import CommandType, PadType, TooltipType

if TYPE_CHECKING:
    from .window import Window

__all__ = ["Radiobutton", "RadioButton"]

_valid_standard_attributes = {
    "class",
    "compound",
    "cursor",
    "image",
    "state",
    "style",
    "takefocus",
    "textvariable",
    "underline",
    "width",
}

_valid_ttk_radiobutton_attributes = _valid_standard_attributes


Window = TypeVar("Window")

# TODO: need a better way to get radio button value
# only way now is the key but you really only need one key for the group to get the value


class Radiobutton(BaseWidget):
    """ttk.Radiobutton class"""

    def __init__(
        self,
        text: str,
        group: Hashable,
        key: Hashable | None = None,
        value: Union[int, str, None] = None,
        disabled: bool = False,
        columnspan: int | None = None,
        rowspan: int | None = None,
        padx: PadType | None = None,
        pady: PadType | None = None,
        events: bool = True,
        sticky: str | None = None,
        tooltip: TooltipType = None,
        selected: bool = False,
        command: CommandType | None = None,
        weightx: int | None = None,
        weighty: int | None = None,
        focus: bool = False,
        **kwargs: Any,
    ):
        """Initialize a ttk.Radiobutton widget

        Args:
            text (str): Text to display
            group (Hashable): Group name (must be unique and will be used as key unless a separate key is specified)
            key (Hashable, optional): Key to use for this widget. Defaults to None.
            value (Union[int, str, None], optional): Value to return when selected. Defaults to None.
            disabled (bool, optional): Whether to disable the widget. Defaults to False.
            columnspan (int, optional): Number of columns to span. Defaults to None.
            rowspan (int, optional): Number of rows to span. Defaults to None.
            padx (int, optional): Padding in x direction. Defaults to None.
            pady (int, optional): Padding in y direction. Defaults to None.
            events (bool, optional): Whether to enable events. Defaults to True.
            sticky (str, optional): Sticky direction. Defaults to None.
            tooltip (TooltipType, optional): Tooltip text. Defaults to None.
            selected (bool, optional): Whether to select this widget. Defaults to False.
            command (CommandType, optional): Command to execute when selected. Defaults to None.
            weightx (int, optional): Weight in x direction. Defaults to None.
            weighty (int, optional): Weight in y direction. Defaults to None.
            focus (bool, optional): If True, widget will have focus. Defaults to False.
                Only one widget in a window can have focus.HLayout
            **kwargs: Additional keyword arguments are passed to ttk.Radiobutton.

        Note:
            Emits EventType.Radiobutton event.
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
        self.widget_type = "ttk.Radiobutton"
        self.text = text
        self.group = group
        self.key = key or group
        self._radiobutton_value = value if value is not None else text
        self._value = None  # will be set in _create_widget
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.selected = selected
        self.kwargs = kwargs

    def _create_widget(self, parent, window: "Window", row, col):
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

        # Arg list for ttk.Radiobutton
        kwargs_radiobutton = {
            k: v
            for k, v in self.kwargs.items()
            if k in _valid_ttk_radiobutton_attributes
        }
        self.widget = ttk.Radiobutton(
            parent,
            text=self.text,
            command=window._make_callback(event),
            variable=self._value,
            value=self._radiobutton_value,
            **kwargs_radiobutton,
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


class RadioButton(Radiobutton):
    """ttk.Radiobutton class"""

    pass
