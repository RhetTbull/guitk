"""Utilities for the guitk package."""

from __future__ import annotations

import tkinter as tk
import tkinter.ttk as ttk


def scrolled_widget_factory(
    master: tk.BaseWidget,
    widget_class: tk.BaseWidget,
    vscrollbar: bool = False,
    hscrollbar: bool = False,
    **kwargs,
) -> tk.BaseWidget:
    """Create a widget that includes optional scrollbars"""

    # scrollbar code based on cpython source with edits to use ttk scrollbar:
    # https://github.com/python/cpython/blob/3.9/Lib/tkinter/scrolledtext.py

    frame = ttk.Frame(master) if vscrollbar or hscrollbar else None
    parent = frame or master
    widget = widget_class()

    widget.vbar = None
    if vscrollbar:
        widget.vbar = ttk.Scrollbar(frame)
        widget.vbar.grid(column=1, row=0, sticky="NS")
        # vbar.pack(side=tk.RIGHT, fill=tk.Y)
        kwargs["yscrollcommand"] = widget.vbar.set

    widget.hbar = None
    if hscrollbar:
        widget.hbar = ttk.Scrollbar(frame, orient=tk.HORIZONTAL)
        widget.hbar.grid(column=0, row=1, sticky="EW")
        # hbar.pack(side=tk.BOTTOM, fill=tk.X)
        kwargs["xscrollcommand"] = widget.hbar.set

    widget_class.__init__(widget, parent, **kwargs)
    widget.grid(column=0, row=0, sticky="NSEW")
    # widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    if vscrollbar:
        widget.vbar["command"] = widget.yview

    if hscrollbar:
        widget.hbar["command"] = widget.xview

    if vscrollbar or hscrollbar:
        # Copy geometry methods of self.frame without overriding Widget methods -- hack!
        widget_meths = vars(widget_class).keys()
        methods = vars(tk.Pack).keys() | vars(tk.Grid).keys() | vars(tk.Place).keys()
        methods = methods.difference(widget_meths)

        for m in methods:
            if m[0] != "_" and m not in {"config", "configure"}:
                setattr(widget, m, getattr(frame, m))

    # keep track of whether widget is framed
    # so the correct geometry methods can be used
    widget._guitk_framed_widget = bool(frame)

    return widget


def load_image(file: str) -> tk.PhotoImage:
    """Load a photo image from a file and return it.

    If Pillow is installed, this will support more image formats than the default
    tkinter PhotoImage class. Pillow will be used automatically if it is installed.
    """
    try:
        from PIL import Image, ImageTk
    except ImportError:
        return tk.PhotoImage(file=file)
    else:
        image = Image.open(file)
        return ImageTk.PhotoImage(image)
