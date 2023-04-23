"""Widget utils"""

import tkinter as tk
import tkinter.ttk as ttk


def scrolled_widget_factory(
    master, widget_class, vscrollbar=False, hscrollbar=False, **kw
):
    """Create a widget that includes optional scrollbars"""
    # scrollbar code lifted from cpython source with edits to use ttk scrollbar:
    # https://github.com/python/cpython/blob/3.9/Lib/tkinter/scrolledtext.py

    frame = None
    if vscrollbar or hscrollbar:
        # create frame for the widget and the scrollbars
        frame = ttk.Frame(master)

    parent = frame or master
    widget = widget_class()

    widget.vbar = None
    if vscrollbar:
        widget.vbar = ttk.Scrollbar(frame)
        widget.vbar.grid(column=1, row=0, sticky="NS")
        # vbar.pack(side=tk.RIGHT, fill=tk.Y)
        kw["yscrollcommand"] = widget.vbar.set

    widget.hbar = None
    if hscrollbar:
        widget.hbar = ttk.Scrollbar(frame, orient=tk.HORIZONTAL)
        widget.hbar.grid(column=0, row=1, sticky="EW")
        # hbar.pack(side=tk.BOTTOM, fill=tk.X)
        kw["xscrollcommand"] = widget.hbar.set

    widget_class.__init__(widget, parent, **kw)
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
            if m[0] != "_" and m != "config" and m != "configure":
                setattr(widget, m, getattr(frame, m))

    return widget

