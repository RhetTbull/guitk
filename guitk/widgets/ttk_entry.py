"""ttk Entry widget"""

import tkinter as tk
import tkinter.ttk as ttk

from .events import Event, EventCommand, EventType
from .utils import scrolled_widget_factory
from .widget import Widget


class Entry(Widget):
    """Text entry / input box"""

    def __init__(
        self,
        key=None,
        default=None,
        disabled=False,
        columnspan=None,
        rowspan=None,
        width=None,
        padx=None,
        pady=None,
        events=False,
        sticky=None,
        tooltip=None,
        cursor=None,
        takefocus=None,
        command=None,
        hscrollbar=False,
    ):
        super().__init__(
            key=key,
            disabled=disabled,
            columnspan=columnspan,
            rowspan=rowspan,
            padx=padx,
            pady=pady,
            events=events,
            sticky=sticky,
            tooltip=tooltip,
            cursor=cursor,
            takefocus=takefocus,
            command=command,
        )
        self.widget_type = "ttk.Entry"
        default = default or ""
        self._value.set(default)
        self.key = key or "Entry"
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.width = width
        self.hscrollbar = hscrollbar

    def _create_widget(self, parent, window: "Window", row, col):
        self.window = window
        self._parent = parent

        # build arg list for Entry
        # TODO: Need to update all widget options to underscore format
        kwargs = {}
        for kw in ["width", "cursor", "takefocus"]:
            val = getattr(self, f"{kw}")
            if val is not None:
                kwargs[kw] = val

        # self.widget = ttk.Entry(parent, textvariable=self._value, **kwargs)
        self.widget = scrolled_widget_factory(
            parent,
            ttk.Entry,
            hscrollbar=self.hscrollbar,
            textvariable=self._value,
            **kwargs,
        )
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        event = Event(self, window, self.key, EventType.KeyRelease)
        self.widget.bind("<KeyRelease>", window._make_callback(event))

        if self._command:
            self.events = True
            window._bind_command(
                EventCommand(
                    widget=self,
                    key=self.key,
                    event_type=EventType.KeyRelease,
                    command=self._command,
                )
            )

        if self._disabled:
            self.widget.state(["disabled"])
        return self.widget

    @property
    def entry(self):
        """Return the Tk entry widget"""
        return self.widget


class _ttkLabelEntry(ttk.Entry):
    """ttk.Entry with a Label"""

    def __init__(self, master=None, text=None, **kw):
        self.frame = ttk.Frame(master)
        ttk.Entry.__init__(self, self.frame, **kw)
        self.label = ttk.Label(self.frame, text=text)
        self.label.grid(row=0, column=0)
        self.grid(row=0, column=1)

        # Copy geometry methods of self.frame without overriding Entry
        # methods -- hack!
        text_meths = vars(ttk.Entry).keys()
        methods = vars(tk.Pack).keys() | vars(tk.Grid).keys() | vars(tk.Place).keys()
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != "_" and m != "config" and m != "configure":
                setattr(self, m, getattr(self.frame, m))

    def __str__(self):
        return str(self.frame)


class LabelEntry(Entry):
    """Text entry / input box with a label"""

    def __init__(
        self,
        text,
        key=None,
        default=None,
        disabled=False,
        columnspan=None,
        rowspan=None,
        width=None,
        padx=None,
        pady=None,
        events=False,
        sticky=None,
        tooltip=None,
        cursor=None,
        takefocus=None,
        command=None,
        hscrollbar=False,
    ):
        super().__init__(
            key=key,
            default=default,
            disabled=disabled,
            columnspan=columnspan,
            rowspan=rowspan,
            width=width,
            padx=padx,
            pady=pady,
            events=events,
            sticky=sticky,
            tooltip=tooltip,
            cursor=cursor,
            takefocus=takefocus,
            command=command,
            hscrollbar=hscrollbar,
        )
        self.widget_type = "guitk.LabelEntry"
        self.text = text

    def _create_widget(self, parent, window: "Window", row, col):
        self.window = window
        self._parent = parent

        # build arg list for Entry
        # TODO: Need to update all widget options to underscore format
        kwargs = {}
        for kw in ["width", "cursor", "takefocus"]:
            val = getattr(self, f"{kw}")
            if val is not None:
                kwargs[kw] = val

        self.widget = _ttkLabelEntry(
            parent, text=self.text, textvariable=self._value, **kwargs
        )
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        event = Event(self, window, self.key, EventType.KeyRelease)
        self.widget.bind("<KeyRelease>", window._make_callback(event))

        if self._command:
            self.events = True
            window._bind_command(
                EventCommand(
                    widget=self,
                    key=self.key,
                    event_type=EventType.KeyRelease,
                    command=self._command,
                )
            )

        if self._disabled:
            self.widget.state(["disabled"])
        return self.widget

    @property
    def entry(self):
        """Return the Tk entry widget"""
        return self.widget
