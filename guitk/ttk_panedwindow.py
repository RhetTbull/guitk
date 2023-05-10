""" ttk PanedWindow widget """

from __future__ import annotations

import tkinter.ttk as ttk
from typing import Hashable, Literal, TypeVar

from guitk.constants import GUITK

from .events import EventCommand, EventType
from .frame import _Container, _VerticalContainer
from .types import CommandType, TooltipType
from .frame import LabelFrame, Frame

__all__ = [
    "Panedwindow",
    "PanedWindow",
    "Pane",
    "VerticalPane",
    "LabelPane",
    "VerticalLabelPane",
]

_valid_standard_attributes = {
    "width",
    "height",
    "padding",
    "takefocus",
    "cursor",
    "style",
    "class",
}

_valid_ttk_panedwindow_attributes = {
    "height",
    "width",
    "orient",
} | _valid_standard_attributes


Window = TypeVar("Window")


class Panedwindow(_Container):
    """ttk.Panedwindow widget"""

    def __init__(
        self,
        key: Hashable | None = None,
        panes: list[Pane] | None = None,
        orient: Literal["horizontal", "vertical"] = "horizontal",
        disabled: bool = False,
        columnspan: int | None = None,
        rowspan: int | None = None,
        padx: int | None = None,
        pady: int | None = None,
        sticky: str | None = None,
        tooltip: TooltipType = None,
        command: CommandType | None = None,
        weightx: int | None = None,
        weighty: int | None = None,
        **kwargs,
    ):
        """
        Initialize a Notebook widget.

        Args:
            key (Hashable, optional): Unique key for this widget. Defaults to None.
            panes: (list[Panes], optional): Panes to add to the Panedwindow. Defaults to None.
            disabled (bool, optional): If True, widget is disabled. Defaults to False.
            columnspan (int | None, optional): Number of columns to span. Defaults to None.
            rowspan (int | None, optional): Number of rows to span. Defaults to None.
            padx (int | None, optional): X padding. Defaults to None.
            pady (int | None, optional): Y padding. Defaults to None.
            sticky (str | None, optional): Sticky direction for widget layout. Defaults to None.
            tooltip (TooltipType | None, optional): Tooltip text or callback to generate tooltip text. Defaults to None.
            command (CommandType | None, optional): Command to execute when clicked. Defaults to None.
            weightx (int | None, optional): Horizontal weight. Defaults to None.
            weighty (int | None, optional): Vertical weight. Defaults to None.
            **kwargs: Additional keyword arguments are passed to ttk.Entry.
        """
        super().__init__(
            frametype=GUITK.ELEMENT_FRAME,
            key=None,
            width=None,
            height=None,
            layout=None,
            style=None,
            borderwidth=None,
            padding=0,
            relief=None,
            disabled=disabled,
            rowspan=None,
            columnspan=None,
            sticky=sticky,
            tooltip=None,
            autoframe=False,
            padx=0,
            pady=0,
            weightx=weightx,
            weighty=weighty,
        )
        self.widget_type = "ttk.Panedwindow"
        self.key = key or "Panedwindow"
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.panes = panes or []
        self._command = command
        self.kwargs = kwargs
        self._pane_count = 0
        self.orient = orient
        self.padx = padx
        self.pady = pady
        self.tooltip = tooltip

    def _create_widget(self, parent, window: "Window", row, col):
        self.window = window
        self._parent = parent

        # Arg list for ttk.Label
        kwargs_panedwindow = {
            k: v
            for k, v in self.kwargs.items()
            if k in _valid_ttk_panedwindow_attributes
        }

        self.widget = ttk.Panedwindow(parent, orient=self.orient, **kwargs_panedwindow)
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        if self.layout:
            for row in self.layout:
                for pane in row:
                    self.add(pane)

        if self._command:
            self.events = True
            window._bind_command(
                # the actual widget will be a tk widget in form widget=.!toplevel.!frame.!notebook, so it won't match self.widget
                # so set widget=None or _handle_commands won't correctly handle the command
                EventCommand(
                    widget=None,
                    key=self.key,
                    event_type=EventType.NotebookpaneChanged,
                    command=self._command,
                )
            )

        if self.width or self.height:
            self.widget.grid_propagate(0)

        if self._disabled:
            self.widget.state(["disabled"])

        return self.widget

    def add(self, pane: Pane):
        """Add a pane to the Panedwindow as new pane"""
        pane_ = pane._create_widget(self.widget, self.window, 0, 0)
        self.panedwindow.add(pane_, **pane.kwargs)

    def insert(self, pos, pane: Pane):
        """Insert a layout to the Panedwindow as new pane at position pos"""
        pane_ = pane._create_widget(self.widget, self.window, 0, 0)
        self.panedwindow.insert(pos, pane_, **pane.kwargs)

    @property
    def panedwindow(self):
        """Return the ttk.Panedwindow widget"""
        return self.widget


class PanedWindow(Panedwindow):
    """ttk.Panedwindow widget"""

    pass


class Pane(Frame):
    """Pane for Panedwindow widget that arranges its widgets horizontally"""

    def __init__(self, sticky: str | None = "nsew", **kwargs):
        """Initialize a pane"""

        super().__init__(
            frametype=GUITK.ELEMENT_FRAME,
            key=None,
            width=None,
            height=None,
            layout=None,
            style=None,
            borderwidth=None,
            padding=0,
            relief=None,
            disabled=False,
            rowspan=None,
            columnspan=None,
            sticky=sticky,
            tooltip=None,
            autoframe=True,
            padx=0,
            pady=0,
        )
        self.kwargs = kwargs


class VerticalPane(_VerticalContainer, Pane):
    """pane for Panedwindow widget that arranges its widgets vertically"""

    def __init__(self, sticky: str | None = "nsew", **kwargs):
        """Initialize a VerticalPane"""

        super().__init__(
            frametype=GUITK.ELEMENT_FRAME,
            key=None,
            width=None,
            height=None,
            layout=None,
            style=None,
            borderwidth=None,
            padding=0,
            relief=None,
            disabled=False,
            rowspan=None,
            columnspan=None,
            sticky=sticky,
            tooltip=None,
            autoframe=True,
            padx=0,
            pady=0,
        )
        self.kwargs = kwargs


class LabelPane(LabelFrame):
    """Pane for Panedwindow widget that arranges its widgets horizontally and includes a label"""

    def __init__(self, name=None, sticky: str | None = "nsew", **kwargs):
        """Initialize a pane"""

        super().__init__(
            frametype=GUITK.ELEMENT_LABEL_FRAME,
            text=name,
            key=None,
            width=None,
            height=None,
            layout=None,
            style=None,
            borderwidth=None,
            padding=0,
            relief=None,
            disabled=False,
            rowspan=None,
            columnspan=None,
            sticky=sticky,
            tooltip=None,
            autoframe=True,
            padx=0,
            pady=0,
        )
        self.name = name
        self.kwargs = kwargs


class VerticalLabelPane(_VerticalContainer, LabelPane):
    """pane for Panedwindow widget that includes a name and  arranges its widgets vertically"""

    def __init__(self, name=None, sticky: str | None = "nsew", **kwargs):
        """Initialize a VerticalLabelPane"""

        super().__init__(
            frametype=GUITK.ELEMENT_LABEL_FRAME,
            text=name,
            key=None,
            width=None,
            height=None,
            layout=None,
            style=None,
            borderwidth=None,
            padding=0,
            relief=None,
            disabled=False,
            rowspan=None,
            columnspan=None,
            sticky=sticky,
            tooltip=None,
            autoframe=True,
            padx=0,
            pady=0,
        )
        self.name = name
        self.kwargs = kwargs