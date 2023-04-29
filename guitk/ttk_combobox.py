"""ttk Combobox widget"""

import tkinter.ttk as ttk
from typing import Hashable

from .events import Event, EventCommand, EventType
from .types import CommandType, TooltipType
from .widget import Widget

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
    # "values",
    "width",
} | _valid_standard_attributes


class Combobox(Widget):
    """ttk Combobox"""

    def __init__(
        self,
        key: Hashable | None = None,
        default: str | None = None,
        values: list[str] | None = None,
        disabled: bool = False,
        columnspan: int | None = None,
        rowspan: int | None = None,
        padx: int | None = None,
        pady: int | None = None,
        events: bool = True,
        sticky: str | None = None,
        tooltip: TooltipType | None = None,
        command: CommandType | None = None,
        readonly: bool = False,
        autosize: bool = False,
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
            **kwargs,
        )

        self.widget_type = "ttk.Combobox"
        self.key = key or "Combobox"
        self.columnspan = columnspan
        self.rowspan = rowspan
        self._readonly = readonly
        self._autosize = autosize
        self.kwargs = kwargs
        self.values = values
        self.default = default

    def _create_widget(self, parent, window: "Window", row, col):
        self.window = window
        self._parent = parent

        # build arg list for Combobox
        kwargs_combobox = {
            k: v for k, v in self.kwargs.items() if k in _valid_ttk_combobox_attributes
        }

        if self._autosize:
            # automatically set width, override any width value provided
            width = len(max(self.values, key=len))
            kwargs_combobox["width"] = width + 1

        self.widget = ttk.Combobox(
            parent,
            textvariable=self._value,
            values=self.values,
            **kwargs_combobox,
        )
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        event_release = Event(self.widget, window, self.key, EventType.KeyRelease)
        self.widget.bind("<KeyRelease>", window._make_callback(event_release))

        event_selected = Event(
            self.widget, window, self.key, EventType.ComboboxSelected
        )
        self.widget.bind("<<ComboboxSelected>>", window._make_callback(event_selected))

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
