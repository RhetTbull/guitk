"""ttk.Separator widget"""

from __future__ import annotations

import tkinter as tk
import tkinter.ttk as ttk
from typing import TypeVar

from .widget import Widget

__all__ = ["Separator", "VerticalSeparator"]

_valid_ttk_separator_attributes = {
    "orient",
}


Window = TypeVar("Window")


class Separator(Widget):
    """ttk.Separator widget with horizontal orientation"""

    def __init__(
        self,
        columnspan: int | None = None,
        padx: int | None = None,
        pady: int | None = None,
        weightx: int | None = 1,
    ):
        """Initialize a horizontal Separator widget.

        Args:
            rowspan (int | None, optional): Number of rows to span. Defaults to None.
            padx (int | None, optional): X padding. Defaults to None.
            pady (int | None, optional): Y padding. Defaults to None.
            weightx (int | None, optional): Weight of this widget in the horizontal direction. Defaults to 1.
        """
        super().__init__(
            columnspan=columnspan,
            padx=padx,
            pady=pady,
            weightx=weightx,
        )
        self.widget_type = "ttk.Separator"
        self.sticky = "EW"

    def _create_widget(self, parent, window: "Window", row, col):
        self.window = window
        self._parent = parent

        self.widget = ttk.Separator(parent, orient=tk.HORIZONTAL)
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        return self.widget

    @property
    def separator(self):
        """Return the ttk Separator widget"""
        return self.widget


class VerticalSeparator(Widget):
    """ttk.Separator widget with vertical orientation"""

    def __init__(
        self,
        rowspan: int | None = None,
        padx: int | None = None,
        pady: int | None = None,
        weighty: int | None = 1,
    ):
        """Initialize a horizontal Separator widget.

        Args:
            rowspan (int | None, optional): Number of rows to span. Defaults to None.
            padx (int | None, optional): X padding. Defaults to None.
            pady (int | None, optional): Y padding. Defaults to None.
            weightx (int | None, optional): Weight of this widget in the horizontal direction. Defaults to 1.
        """
        super().__init__(
            rowspan=rowspan,
            padx=padx,
            pady=pady,
            weighty=weighty,
        )
        self.widget_type = "ttk.Separator"
        self.sticky = "NS"

    def _create_widget(self, parent, window: "Window", row, col):
        self.window = window
        self._parent = parent

        self.widget = ttk.Separator(parent, orient=tk.VERTICAL)
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        return self.widget

    @property
    def separator(self):
        """Return the ttk Separator widget"""
        return self.widget
