""" ttk Progressbar widget """

import tkinter as tk
import tkinter.ttk as ttk

from .widget import Widget


class Progressbar(Widget):
    """ttk.Progressbar"""

    def __init__(
        self,
        value=None,
        key=None,
        orient=tk.HORIZONTAL,
        length=200,
        mode="determinate",
        maximum=100,
        disabled=False,
        columnspan=None,
        rowspan=None,
        padx=None,
        pady=None,
        sticky=None,
        tooltip=None,
        style=None,
        events=True,
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
            value_type=tk.DoubleVar,
        )
        self.widget_type = "ttk.Progressbar"
        self.key = key or "Progressbar"

        self.orient = orient
        self.length = length
        self.mode = mode
        self.maximum = maximum
        self.style = style
        self._initial_value = value

        self.columnspan = columnspan
        self.rowspan = rowspan
        self.tooltip = tooltip

    @property
    def value(self):
        return self.widget["value"]

    @value.setter
    def value(self, value):
        self._value.set(float(value))

    def _create_widget(self, parent, window: "Window", row, col):
        self.window = window
        self._parent = parent

        kwargs = {}
        for kw in ["length", "orient", "mode", "maximum"]:
            val = getattr(self, kw)
            if val is not None:
                kwargs[kw] = val

        kwargs["variable"] = self._value
        if self._initial_value is not None:
            self._value.set(self._initial_value)

        self.widget = ttk.Progressbar(parent, **kwargs)
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

