""" ttk Progressbar widget """

from __future__ import annotations

import tkinter as tk
import tkinter.ttk as ttk
from typing import TYPE_CHECKING, Hashable, TypeVar

from .basewidget import BaseWidget
from .types import PadType, TooltipType

if TYPE_CHECKING:
    from .window import Window


__all__ = [
    "Progressbar",
    "ProgressBar",
    "PROGRESS_DETERMINATE",
    "PROGRESS_INDETERMINATE",
]

_valid_standard_attributes = {"takefocus", "cursor", "style", "class"}

_valid_ttk_progressbar_attributes = {
    "orient",
    "length",
    "mode",
    "maximum",
    "variable",
    "value",
    "phase",
} | _valid_standard_attributes


Window = TypeVar("Window")

PROGRESS_DETERMINATE = "determinate"
PROGRESS_INDETERMINATE = "indeterminate"


class Progressbar(BaseWidget):
    """ttk.Progressbar"""

    def __init__(
        self,
        key: Hashable | None = None,
        value: float | None = None,
        orient: str = tk.HORIZONTAL,
        length: int = 200,
        mode: str = "determinate",
        maximum: float = 100.0,
        disabled: bool = False,
        columnspan: int | None = None,
        rowspan: int | None = None,
        padx: PadType | None = None,
        pady: PadType | None = None,
        sticky: str | None = None,
        tooltip: TooltipType = None,
        events: bool = True,
        weightx: int | None = None,
        weighty: int | None = None,
        **kwargs,
    ):
        """Initialize a ttk.Progressbar widget

        Args:
            key (Hashable, optional): Key for the widget. Defaults to None.
            value (float, optional): Initial value. Defaults to None.
            orient (str, optional): Orientation of the progress bar. Defaults to tk.HORIZONTAL.
            length (int, optional): Length of the progress bar. Defaults to 200.
            mode (str, optional): Mode of the progress bar. Defaults to "determinate". Can be "determinate" or "indeterminate".
            maximum (float, optional): Maximum value. Defaults to 100.0.
            disabled (bool, optional): If True, widget is disabled. Defaults to False.
            columnspan (int, optional): Number of columns to span. Defaults to None.
            rowspan (int, optional): Number of rows to span. Defaults to None.
            padx (int, optional): Padding in x direction. Defaults to None.
            pady (int, optional): Padding in y direction. Defaults to None.
            sticky (str, optional): Sticky direction. Defaults to None.
            tooltip (TooltipType, optional): Tooltip for the widget. Defaults to None.
            events (bool, optional): Enable events for this widget. Defaults to True.
            weightx (int, optional): Weight in x direction. Defaults to None.
            weighty (int, optional): Weight in y direction. Defaults to None.
            **kwargs: Additional keyword arguments to pass to ttk.Progressbar.
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
            value_type=tk.DoubleVar,
        )
        self.widget_type = "ttk.Progressbar"
        self.key = key or "Progressbar"

        self.orient = orient
        self.length = length
        self.mode = mode
        self.maximum = maximum
        self._initial_value = value
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.tooltip = tooltip
        self.kwargs = kwargs

    @property
    def value(self):
        return self.widget["value"]

    @value.setter
    def value(self, value):
        self._value.set(float(value))

    def _create_widget(self, parent, window: "Window", row, col):
        # Arg list for ttk.ProgressBar
        kwargs_progressbar = {
            k: v
            for k, v in self.kwargs.items()
            if k in _valid_ttk_progressbar_attributes
        }
        kwargs_progressbar["variable"] = self._value
        kwargs_progressbar["orient"] = self.orient
        kwargs_progressbar["length"] = self.length
        kwargs_progressbar["mode"] = self.mode
        kwargs_progressbar["maximum"] = self.maximum
        if self._initial_value is not None:
            self._value.set(self._initial_value)

        self.widget = ttk.Progressbar(parent, **kwargs_progressbar)
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        if self._disabled:
            self.widget.state(["disabled"])

        return self.widget

    @property
    def progressbar(self):
        """Return the ttk.Progressbar widget"""
        return self.widget

    def stop(self):
        self.widget.stop()


class ProgressBar(Progressbar):
    """ttk.Progressbar"""

    pass
