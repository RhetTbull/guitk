"""HSpacer class that expands to fill space in the layout"""

from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING

from ._debug import debug_borderwidth, debug_relief
from .ttk_label import Label

if TYPE_CHECKING:
    from .window import Window

__all__ = ["HSpacer", "VSpacer"]


class HSpacer(Label):
    """HSpacer widget that expands to fill the horizontal space in the layout"""

    def __init__(self, rowspan=1):
        super().__init__(
            "",
            padding=0,
            disabled=True,
            sticky="nsew",
            autoframe=False,
            borderwidth=debug_borderwidth() or None,
            relief=debug_relief() or None,
            weightx=1,
            rowspan=rowspan,
        )

    def _create_widget(self, parent: tk.BaseWidget, window: Window, row: int, col: int):
        super()._create_widget(parent, window, row, col)
        # parent.grid_columnconfigure(col, weight=1)


class VSpacer(Label):
    """ "HSpacer widget that expands to fill the vertical space in the layout"""

    def __init__(self, columnspan=1):
        super().__init__(
            "",
            padding=0,
            disabled=True,
            sticky="nsew",
            autoframe=False,
            borderwidth=debug_borderwidth() or None,
            relief=debug_relief() or None,
            weighty=1,
            columnspan=columnspan,
        )

    def _create_widget(self, parent: tk.BaseWidget, window: Window, row: int, col: int):
        super()._create_widget(parent, window, row, col)
        # parent.grid_rowconfigure(row, weight=1)
