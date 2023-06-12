"""Constants for guitk """

from __future__ import annotations

from enum import Enum


class GUITK(Enum):
    """Constants used internally by guitk"""

    ELEMENT_FRAME = "ttk.Frame"
    ELEMENT_LABEL_FRAME = "LabelFrame"
    ELEMENT_TK_FRAME = "tk.Frame"


DEFAULT_PADX = 5
DEFAULT_PADY = 5

MENU_MARKER = "Menu:"
