from __future__ import annotations

import tkinter as tk
from typing import Any, Callable

TooltipType = Callable[[str], str | None]
CommandType = Callable[[], Any]
ValueType = tk.Variable
