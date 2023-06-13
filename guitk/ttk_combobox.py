"""ttk Combobox widget"""

from __future__ import annotations

import tkinter.ttk as ttk
from typing import TYPE_CHECKING, Hashable

from .basewidget import BaseWidget
from .events import Event, EventCommand, EventType
from .types import CommandType, PadType, TooltipType

if TYPE_CHECKING:
    from .window import Window

__all__ = ["Combobox", "ComboBox"]

_valid_standard_attributes = {
    "class",
    "cursor",
    "style",
    "takefocus",
}

_valid_ttk_combobox_attributes = {
    "exportselection",
    "height",
    "justify",
    "postcommand",
    "state",
    "textvariable",
    "values",
    "width",
} | _valid_standard_attributes


class Combobox(BaseWidget):
    """ttk Combobox"""

    def __init__(
        self,
        key: Hashable | None = None,
        default: str | None = None,
        values: list[str] | None = None,
        disabled: bool = False,
        columnspan: int | None = None,
        rowspan: int | None = None,
        padx: PadType | None = None,
        pady: PadType | None = None,
        events: bool = True,
        keyrelease: bool = False,
        sticky: str | None = None,
        tooltip: TooltipType | None = None,
        command: CommandType | None = None,
        readonly: bool = False,
        autosize: bool = False,
        weightx: int | None = None,
        weighty: int | None = None,
        focus: bool = False,
        **kwargs,
    ):
        super().__init__(
            key=key,
            disabled=disabled,
            columnspan=columnspan,
            rowspan=rowspan,
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
        """
        Initialize a ttk.Combobox widget.

        Args:
            key (Hashable, optional): Unique key for this widget. Defaults to None.
            default (str, optional): Default value. Defaults to None.
            values (list[str], optional): List of values for the combobox. Defaults to None.
            disabled (bool, optional): If True, widget is disabled. Defaults to False.
            columnspan (int | None, optional): Number of columns to span. Defaults to None.
            rowspan (int | None, optional): Number of rows to span. Defaults to None.
            padx (PadType | None, optional): X padding. Defaults to None.
            pady (PadType | None, optional): Y padding. Defaults to None.
            events (bool, optional): Enable events for this widget. Defaults to False.
            keyrelease (bool, optional): If True and events is True, emit EventType.KeyRelease event when a key is released.
            sticky (str | None, optional): Sticky direction for widget layout. Defaults to None.
            tooltip (TooltipType | None, optional): Tooltip text or callback to generate tooltip text. Defaults to None.
            command (CommandType | None, optional): Command callback. Defaults to None.
            readonly (bool, optional): If True, widget is read-only. Defaults to False.
                If Combobox is not readonly, user can type in a value that is not in the list of values.
            autosize (bool, optional): If True, automatically set width to fit longest value. Defaults to False.
            weightx (int | None, optional): Weight of widget in X direction. Defaults to None.
            weighty (int | None, optional): Weight of widget in Y direction. Defaults to None.
            focus (bool, optional): If True, widget has focus. Defaults to False.
                Only one widget in a window can have focus.HLayout
            **kwargs: Additional keyword arguments are passed to ttk.Checkbutton.

        Note:
            Emits EventType.ComboboxSelected event when a value is selected from the list.
            Emits EventType.ComboboxReturn event when the Return key is pressed.
            Emits EventType.KeyRelease event when a key is released (if keyrelease is True).
        """
        self.widget_type = "ttk.Combobox"
        self.key = key or "Combobox"
        self.columnspan = columnspan
        self.rowspan = rowspan
        self._readonly = readonly
        self._autosize = autosize
        self.kwargs = kwargs
        self.values = values
        self.default = default
        self.keyrelease = keyrelease

    def _create_widget(self, parent, window: Window, row, col):
        # build arg list for Combobox
        kwargs = {
            k: v for k, v in self.kwargs.items() if k in _valid_ttk_combobox_attributes
        }

        if self._autosize:
            # automatically set width, override any width value provided
            width = len(max(self.values, key=len))
            kwargs["width"] = width + 1

        self.widget = ttk.Combobox(
            parent,
            textvariable=self._value,
            values=self.values,
            **kwargs,
        )
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        # bind events
        if self.keyrelease:
            event_release = Event(self, window, self.key, EventType.KeyRelease)
            self.widget.bind("<KeyRelease>", window._make_callback(event_release))

        event_selected = Event(self, window, self.key, EventType.ComboboxSelected)
        self.widget.bind("<<ComboboxSelected>>", window._make_callback(event_selected))

        combo_return_key = Event(self, window, self.key, EventType.ComboboxReturn)
        self.widget.bind("<Return>", window._make_callback(combo_return_key))

        if self._command:
            self.events = True
            window._bind_command(
                EventCommand(
                    widget=self,
                    key=self.key,
                    event_type=EventType.ComboboxSelected,
                    command=self._command,
                )
            )

        if self.default is not None:
            self.value = self.default

        if self._disabled:
            self.widget.state(["disabled"])

        if self._readonly:
            self.widget.state(["readonly"])

        return self.widget

    @property
    def combobox(self):
        """Return the Tk combobox widget"""
        return self.widget


class ComboBox(Combobox):
    """ttk Combobox"""

    pass
