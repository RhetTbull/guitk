""" ttk PanedWindow widget """

from __future__ import annotations

import tkinter.ttk as ttk
from typing import TYPE_CHECKING, Hashable, Literal, TypeVar

from guitk.constants import GUITK

from .events import EventCommand, EventType
from .frame import Frame, LabelFrame, _Container, _VerticalContainer
from .types import CommandType, PadType, TooltipType

if TYPE_CHECKING:
    from .window import Window

# TODO: Add remove() to PanedWindow and Pane

__all__ = [
    "HLabelPane",
    "HPane",
    "PanedWindow",
    "Panedwindow",
    "VLabelPane",
    "VPane",
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
        panes: list[HPane] | None = None,
        orient: Literal["horizontal", "vertical"] = "horizontal",
        disabled: bool = False,
        columnspan: int | None = None,
        rowspan: int | None = None,
        padx: PadType | None = None,
        pady: PadType | None = None,
        sticky: str | None = None,
        tooltip: TooltipType = None,
        weightx: int | None = None,
        weighty: int | None = None,
        focus: bool = False,
        **kwargs,
    ):
        """Initialize a PanedWindow widget.

        Args:
            key (Hashable, optional): Unique key for this widget. Defaults to None.
            panes: (list[Panes], optional): Panes to add to the Panedwindow. Defaults to None.
            disabled (bool, optional): If True, widget is disabled. Defaults to False.
            columnspan (int | None, optional): Number of columns to span. Defaults to None.
            rowspan (int | None, optional): Number of rows to span. Defaults to None.
            padx (PadType | None, optional): X padding. Defaults to None.
            pady (PadType | None, optional): Y padding. Defaults to None.
            sticky (str | None, optional): Sticky direction for widget layout. Defaults to None.
            tooltip (TooltipType | None, optional): Tooltip text or callback to generate tooltip text. Defaults to None.
            weightx (int | None, optional): Horizontal weight. Defaults to None.
            weighty (int | None, optional): Vertical weight. Defaults to None.
            focus (bool, optional): If True, widget will have focus. Defaults to False.
                Only one widget in a window can have focus.HLayout
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
            focus=focus,
        )
        self.widget_type = "ttk.Panedwindow"
        self.key = key or "Panedwindow"
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.panes = panes or []
        self.kwargs = kwargs
        self._pane_count = 0
        self.orient = orient
        self.padx = padx
        self.pady = pady
        self.tooltip = tooltip

    def _create_widget(self, parent, window: "Window", row, col):
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

        if self.width or self.height:
            self.widget.grid_propagate(0)

        if self._disabled:
            self.widget.state(["disabled"])

        return self.widget

    def add(self, pane: HPane):
        """Add a pane to the Panedwindow as new pane"""
        pane_ = pane._create_widget(self.widget, self.window, 0, 0)
        self.panedwindow.add(pane_, **pane.kwargs)

    def insert(self, pos, pane: HPane):
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


class HPane(Frame):
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


class VPane(_VerticalContainer, HPane):
    """Pane for Panedwindow widget that arranges its widgets vertically"""

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


class HLabelPane(LabelFrame):
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


class VLabelPane(_VerticalContainer, HLabelPane):
    """Pane for Panedwindow widget that includes a name and  arranges its widgets vertically"""

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
