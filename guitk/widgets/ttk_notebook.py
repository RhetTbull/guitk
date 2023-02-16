""" ttk Notebook widget """

import tkinter.ttk as ttk

from .events import Event, EventCommand, EventType
from .widget import Widget
from .window import Frame, _Layout


class Notebook(Widget, _Layout):
    """ttk.Notebook"""

    def __init__(
        self,
        key=None,
        tabs=None,
        disabled=False,
        columnspan=None,
        rowspan=None,
        padx=None,
        pady=None,
        sticky=None,
        tooltip=None,
        style=None,
        events=True,
        command=None,
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
            command=command,
        )
        self.widget_type = "ttk.Notebook"
        self.key = key or "Notebook"

        self.style = style

        self.columnspan = columnspan
        self.rowspan = rowspan
        self.tooltip = tooltip
        self.tabs = tabs

    def _create_widget(self, parent, window: "Window", row, col):
        self.window = window
        self._parent = parent

        kwargs = {}
        for kw in ["style"]:
            val = getattr(self, kw)
            if val is not None:
                kwargs[kw] = val

        self.widget = ttk.Notebook(parent, **kwargs)
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        event_tab_change = Event(
            self.widget, window, self.key, EventType.NotebookTabChanged
        )
        self.widget.bind(
            "<<NotebookTabChanged>>", window._make_callback(event_tab_change)
        )

        if self.tabs:
            for tab in self.tabs:
                self.add(tab, self.tabs[tab])

        if self._command:
            self.events = True
            window._bind_command(
                # the actual widget will be a tk widget in form widget=.!toplevel.!frame.!notebook, so it won't match self.widget
                # so set widget=None or _handle_commands won't correctly handle the command
                EventCommand(
                    widget=None,
                    key=self.key,
                    event_type=EventType.NotebookTabChanged,
                    command=self._command,
                )
            )

        if self._disabled:
            self.widget.state(["disabled"])

        return self.widget

    def add(self, text, layout, **kwargs):
        """Add a layout to the Notebook as new tab"""
        frame = Frame(layout=layout)
        frame_ = frame._create_widget(self.widget, self.window, 0, 0)
        kwargs["text"] = text
        self.notebook.add(frame_, **kwargs)

    def insert(self, pos, text, layout, **kwargs):
        """Insert a layout to the Notebook as new tab at position pos"""
        frame = Frame(layout=layout)
        frame_ = frame._create_widget(self.widget, self.window, 0, 0)
        kwargs["text"] = text
        self.notebook.insert(pos, frame_, **kwargs)

    @property
    def notebook(self):
        """Return the ttk.Notebook widget"""
        return self.widget
