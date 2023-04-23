""" ttk Notebook widget """

from __future__ import annotations

import tkinter.ttk as ttk
from typing import Hashable, TypeVar

from .events import Event, EventCommand, EventType
from .types import CommandType, TabType, TooltipType
from .widget import Widget
from .window import Frame, _Layout

__all__ = ["Notebook", "NoteBook"]

_valid_standard_attributes = {
    "width",
    "height",
    "padding",
    "takefocus",
    "cursor",
    "style",
    "class",
}

_valid_ttk_notebook_attributes = _valid_standard_attributes


Window = TypeVar("Window")


class Notebook(Widget, _Layout):
    """
    ttk.Notebook widget
    """

    def __init__(
        self,
        key: Hashable | None = None,
        tabs: TabType | None = None,
        disabled: bool = False,
        columnspan: int | None = None,
        rowspan: int | None = None,
        padx: int | None = None,
        pady: int | None = None,
        events: bool = False,
        sticky: str | None = None,
        tooltip: TooltipType = None,
        command: CommandType | None = None,
        **kwargs,
    ):
        """
        Initialize a Notebook widget.

        Args:
            key (Hashable, optional): Unique key for this widget. Defaults to None.
            tabs: (TabType, optional): Tabs to add to the notebook. Defaults to None.
            disabled (bool, optional): If True, widget is disabled. Defaults to False.
            columnspan (int | None, optional): Number of columns to span. Defaults to None.
            rowspan (int | None, optional): Number of rows to span. Defaults to None.
            padx (int | None, optional): X padding. Defaults to None.
            pady (int | None, optional): Y padding. Defaults to None.
            events (bool, optional): Enable events for this widget. Defaults to False.
            sticky (str | None, optional): Sticky direction for widget layout. Defaults to None.
            tooltip (TooltipType | None, optional): Tooltip text or callback to generate tooltip text. Defaults to None.
            command (CommandType | None, optional): Command to execute when clicked. Defaults to None.
            **kwargs: Additional keyword arguments are passed to ttk.Entry.
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
        self.widget_type = "ttk.Notebook"
        self.key = key or "Notebook"
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.tabs = tabs
        self._command = command
        self.kwargs = kwargs

    def _create_widget(self, parent, window: "Window", row, col):
        self.window = window
        self._parent = parent

        # Arg list for ttk.Label
        kwargs_notebook = {
            k: v for k, v in self.kwargs.items() if k in _valid_ttk_notebook_attributes
        }

        self.widget = ttk.Notebook(parent, **kwargs_notebook)
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

    @property
    def current_tab(self):
        """Return the name of the currently selected tab"""
        return self.notebook.tab(self.notebook.select(), "text")

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


class NoteBook(Notebook):
    """
    ttk.Notebook widget
    """

    pass
