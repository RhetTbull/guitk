"""Custom types for guitk"""

from __future__ import annotations

import tkinter as tk
from typing import Any, Callable, Literal, TypeVar

Widget = TypeVar("Widget")
TooltipType = Callable[[str], str | None]
CommandType = Callable[[], Any]
ValueType = tk.Variable
LayoutType = list[list[Widget | None]]
Window = TypeVar("Window")
VAlign = Literal["top", "bottom", "center"]
HAlign = Literal["left", "right", "center"]
DecoratedType = TypeVar("DecoratedType")
SizeType = tuple[int, int] | str | None


class _WindowBaseClass:
    """Just to keep typing happy"""

    ...
