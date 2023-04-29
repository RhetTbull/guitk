"""Custom types for guitk"""

from __future__ import annotations

import tkinter as tk
from typing import Any, Callable, TypeVar

Widget = TypeVar("Widget")

TooltipType = Callable[[str], str | None]
CommandType = Callable[[], Any]
ValueType = tk.Variable
LayoutType = list[list[Widget | None]]
TabType = dict[str, LayoutType]
Window = TypeVar("Window")

class _WindowBaseClass:
    ...
