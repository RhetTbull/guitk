"""ttk checkbutton widget"""

import tkinter as tk
import tkinter.ttk as ttk

from .events import Event, EventCommand, EventType
from .widget import Widget


class Checkbutton(Widget):
    """Checkbox / checkbutton"""

    def __init__(
        self,
        text,
        key="",
        disabled=False,
        rowspan=None,
        columnspan=None,
        padx=None,
        pady=None,
        events=True,
        sticky=None,
        tooltip=None,
        command=None,
        **kwargs,
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
        self.widget = ttk.Checkbutton(
            parent,
            text=self.text,
            anchor=self.kwargs.get("anchor"),
            command=window._make_callback(event),
            variable=self._value,
            onvalue=True,
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

