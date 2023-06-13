""" ttk Notebook widget """

from __future__ import annotations

import tkinter.ttk as ttk
from typing import TYPE_CHECKING, Hashable, TypeVar

from guitk.constants import GUITK

from .basewidget import BaseWidget
from .events import Event, EventCommand, EventType
from .frame import Frame, _Container, _LayoutMixin, _VerticalContainer
from .layout import get_parent, push_parent
from .types import CommandType, HAlign, PadType, TooltipType, VAlign

if TYPE_CHECKING:
    from .window import Window

# TODO: Add remove() to Notebook and Tab

__all__ = ["Notebook", "NoteBook", "HTab", "VTab"]

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


class Notebook(_Container):
    """ttk.Notebook widget"""

    def __init__(
        self,
        key: Hashable | None = None,
        tabs: list[HTab] | None = None,
        disabled: bool = False,
        columnspan: int | None = None,
        rowspan: int | None = None,
        padx: PadType | None = None,
        pady: PadType | None = None,
        events: bool = False,
        sticky: str | None = None,
        tooltip: TooltipType = None,
        command: CommandType | None = None,
        weightx: int | None = None,
        weighty: int | None = None,
        focus: bool = False,
        **kwargs,
    ):
        """Initialize a Notebook widget.

        Args:
            key (Hashable, optional): Unique key for this widget. Defaults to None.
            tabs: (list[Tab], optional): Tabs to add to the notebook. Defaults to None.
            disabled (bool, optional): If True, widget is disabled. Defaults to False.
            columnspan (int | None, optional): Number of columns to span. Defaults to None.
            rowspan (int | None, optional): Number of rows to span. Defaults to None.
            padx (PadType | None, optional): X padding. Defaults to None.
            pady (PadType | None, optional): Y padding. Defaults to None.
            events (bool, optional): Enable events for this widget. Defaults to False.
            sticky (str | None, optional): Sticky direction for widget layout. Defaults to None.
            tooltip (TooltipType | None, optional): Tooltip text or callback to generate tooltip text. Defaults to None.
            command (CommandType | None, optional): Command to execute when clicked. Defaults to None.
            weightx (int | None, optional): Horizontal weight. Defaults to None.
            weighty (int | None, optional): Vertical weight. Defaults to None.
            focus (bool, optional): If True, widget will have focus. Defaults to False.
                Only one widget in a window can have focus.HLayout
            **kwargs: Additional keyword arguments are passed to ttk.Entry.


        Note:
            Emits EventType.NotebookTabChanged event.
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
            focus=focus,
        )
        self.widget_type = "ttk.Notebook"
        self.key = key or "Notebook"
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.tabs = tabs or []
        self._command = command
        self.kwargs = kwargs
        self._tab_count = 0

    def _create_widget(self, parent, window: "Window", row, col):
        # Arg list for ttk.Label
        kwargs_notebook = {
            k: v for k, v in self.kwargs.items() if k in _valid_ttk_notebook_attributes
        }

        self.widget = ttk.Notebook(parent, **kwargs_notebook)
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        event_tab_change = Event(self, window, self.key, EventType.NotebookTabChanged)
        self.widget.bind(
            "<<NotebookTabChanged>>", window._make_callback(event_tab_change)
        )

        if self.layout:
            for row in self.layout:
                for tab in row:
                    self.add(tab)

        if self._command:
            self.events = True
            window._bind_command(
                # the actual widget will be a tk widget in form widget=.!toplevel.!frame.!notebook, so it won't match self.widget
                # so set widget=None or _handle_commands won't correctly handle the command
                EventCommand(
                    widget=self,
                    key=self.key,
                    event_type=EventType.NotebookTabChanged,
                    command=self._command,
                )
            )

        if self.width or self.height:
            self.widget.grid_propagate(0)

        if self._disabled:
            self.widget.state(["disabled"])

        return self.widget

    @property
    def current_tab(self):
        """Return the name of the currently selected tab"""
        return self.notebook.tab(self.notebook.select(), "text")

    def add(self, tab: HTab):
        """Add a Tab to the Notebook as new tab"""
        tab_ = tab._create_widget(self.widget, self.window, 0, 0)
        tab.kwargs["text"] = tab.name
        self.notebook.add(tab_, **tab.kwargs)

    def insert(self, pos, tab: HTab):
        """Insert a layout to the Notebook as new tab at position pos"""
        tab_ = tab._create_widget(self.widget, self.window, 0, 0)
        tab.kwargs["text"] = tab.name
        self.notebook.insert(pos, tab_, **tab.kwargs)

    @property
    def notebook(self):
        """Return the ttk.Notebook widget"""
        return self.widget


class NoteBook(Notebook):
    """ttk.Notebook widget"""

    pass


class HTab(_Container):
    """Tab for Notebook widget that arranges its widgets horizontally"""

    def __init__(
        self,
        name=None,
        sticky: str | None = "nsew",
        valign: VAlign | None = None,
        halign: HAlign | None = None,
        **kwargs,
    ):
        """Initialize a horizontal Tab

        Args:
            name (str, optional): Name of the tab. Defaults to None.
            sticky (str | None, optional): Sticky direction for widget layout. Defaults to None.
            valign (VAlign | None, optional): Vertical alignment of widgets in the tab. Defaults to None.
            halign (HAlign | None, optional): Horizontal alignment of widgets in the tab. Defaults to None.
            **kwargs: Additional keyword arguments are passed to ttk.Frame.
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
            disabled=False,
            rowspan=None,
            columnspan=None,
            sticky=sticky,
            tooltip=None,
            autoframe=True,
            valign=valign,
            halign=halign,
            padx=0,
            pady=0,
        )
        self.name = name
        self.kwargs = kwargs


class VTab(HTab, _VerticalContainer):
    """Tab for Notebook widget that arranges its widgets vertically"""

    def __init__(
        self,
        name=None,
        sticky: str | None = "nsew",
        valign: VAlign | None = None,
        halign: HAlign | None = None,
        **kwargs,
    ):
        """Initialize a vertical Tab

        Args:
            name (str, optional): Name of the tab. Defaults to None.
            sticky (str | None, optional): Sticky direction for widget layout. Defaults to None.
            valign (VAlign | None, optional): Vertical alignment of widgets in the tab. Defaults to None.
            halign (HAlign | None, optional): Horizontal alignment of widgets in the tab. Defaults to None.
            **kwargs: Additional keyword arguments are passed to ttk.Frame.
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
            disabled=False,
            rowspan=None,
            columnspan=None,
            sticky=sticky,
            tooltip=None,
            autoframe=True,
            padx=0,
            pady=0,
            valign=valign,
            halign=halign,
        )
        self.name = name
        self.kwargs = kwargs
