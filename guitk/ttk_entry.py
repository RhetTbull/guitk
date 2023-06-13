"""ttk Entry widget"""

from __future__ import annotations

import tkinter as tk
import tkinter.ttk as ttk
from typing import TYPE_CHECKING, Hashable

from .basewidget import BaseWidget
from .events import Event, EventCommand, EventType
from .types import CommandType, PadType, TooltipType
from .utils import scrolled_widget_factory

if TYPE_CHECKING:
    from .window import Window

__all__ = ["Entry", "LabelEntry"]

_valid_standard_attributes = {
    "class",
    "cursor",
    "style",
    "takefocus",
    "xscrollcommand",
}

_valid_ttk_entry_attributes = {
    "exportselection",
    "invalidcommand",
    "justify",
    "show",
    "state",
    "textvariable",
    "validate",
    "validatecommand",
    "width",
} | _valid_standard_attributes


class Entry(BaseWidget):
    """ttk.Entry text entry / input box"""

    def __init__(
        self,
        key: Hashable | None = None,
        default: str | None = None,
        disabled: bool = False,
        columnspan: int | None = None,
        rowspan: int | None = None,
        padx: PadType | None = None,
        pady: PadType | None = None,
        events: bool = True,
        keyrelease: bool = False,
        sticky: str | None = None,
        tooltip: TooltipType = None,
        command: CommandType | None = None,
        hscrollbar: bool = False,
        weightx: int | None = None,
        weighty: int | None = None,
        focus: bool = False,
        **kwargs,
    ):
        """Initialize an Entry widget.

        Args:
            key (Hashable, optional): Unique key for this widget. Defaults to None.
            default (str | None, optional): Default text for the entry box. Defaults to None.
            disabled (bool, optional): If True, widget is disabled. Defaults to False.
            columnspan (int | None, optional): Number of columns to span. Defaults to None.
            rowspan (int | None, optional): Number of rows to span. Defaults to None.
            padx (PadType | None, optional): X padding. Defaults to None.
            pady (PadType | None, optional): Y padding. Defaults to None.
            events (bool, optional): Enable events for this widget. Defaults to True.
            keyrelease (bool, optional): If True, generate events on key release. Defaults to False.
            sticky (str | None, optional): Sticky direction for widget layout. Defaults to None.
            tooltip (TooltipType | None, optional): Tooltip text or callback to generate tooltip text. Defaults to None.
            command (CommandType | None, optional): Command callback. Defaults to None.
            hscrollbar (bool, optional): Show horizontal scrollbar. Defaults to False.
            weightx (int | None, optional): Weight for horizontal resizing. Defaults to None.
            weighty (int | None, optional): Weight for vertical resizing. Defaults to None.
            focus (bool, optional): If True, widget has focus. Defaults to False.
                Only one widget in a window can have focus.HLayout
            **kwargs: Additional keyword arguments are passed to ttk.Entry.

        Note:
            Emits EventType.EntryReturn event on return key press.
            If keyrelease is True, emits EventType.KeyRelease event on every key release.
        """
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
            command=command,
            weightx=weightx,
            weighty=weighty,
            focus=focus,
        )
        self.widget_type = "ttk.Entry"
        default = default or ""
        self._value.set(default)
        self.key = key or "Entry"
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.hscrollbar = hscrollbar
        self.keyrelease = keyrelease
        self.kwargs = kwargs

    def _create_widget(self, parent, window: Window, row, col):
        # build arg list for ttk.Entry
        kwargs_entry = {
            k: v for k, v in self.kwargs.items() if k in _valid_ttk_entry_attributes
        }
        self.widget = scrolled_widget_factory(
            parent,
            ttk.Entry,
            hscrollbar=self.hscrollbar,
            textvariable=self._value,
            **kwargs_entry,
        )
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        # bind key release event
        if self.keyrelease:
            event = Event(self, window, self.key, EventType.KeyRelease)
            self.widget.bind("<KeyRelease>", window._make_callback(event))

        # bind return key event
        entry_return_key = Event(self, window, self.key, EventType.EntryReturn)
        self.widget.bind("<Return>", window._make_callback(entry_return_key))

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

    def __init__(self, master=None, text=None, **kwargs):
        """Initialize a _ttkLabelEntry widget.

        Args:
            master (tk.Widget, optional): Parent widget. Defaults to None.
            text (str, optional): Label text. Defaults to None.
            **kwargs: Additional keyword arguments are passed to ttk.Entry.
        """
        self.frame = ttk.Frame(master)
        ttk.Entry.__init__(self, self.frame, **kwargs)
        self.label = ttk.Label(self.frame, text=text)
        self.label.grid(row=0, column=0)
        self.grid(row=0, column=1)

        # Copy geometry methods of self.frame without overriding Entry
        # methods -- hack!
        text_meths = vars(ttk.Entry).keys()
        methods = vars(tk.Pack).keys() | vars(tk.Grid).keys() | vars(tk.Place).keys()
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != "_" and m not in {"config", "configure", "focus"}:
                setattr(self, m, getattr(self.frame, m))

    def __str__(self):
        return str(self.frame)


class LabelEntry(Entry):
    """Text entry / input box with a label"""

    # TODO: add option to put label above the entry box

    def __init__(
        self,
        text: str,
        key: Hashable | None = None,
        default: str | None = None,
        disabled: bool = False,
        columnspan: int | None = None,
        rowspan: int | None = None,
        padx: PadType | None = None,
        pady: PadType | None = None,
        events: bool = True,
        keyrelease: bool = False,
        sticky: str | None = None,
        tooltip: TooltipType = None,
        command: CommandType | None = None,
        hscrollbar: bool = False,
        weightx: int | None = None,
        weighty: int | None = None,
        focus: bool = False,
        **kwargs,
    ):
        """Initialize an Entry widget.

        Args:
            text (str): Label text.
            key (Hashable, optional): Unique key for this widget. Defaults to None.
            default (str | None, optional): Default text for the entry box. Defaults to None.
            disabled (bool, optional): If True, widget is disabled. Defaults to False.
            columnspan (int | None, optional): Number of columns to span. Defaults to None.
            rowspan (int | None, optional): Number of rows to span. Defaults to None.
            padx (PadType | None, optional): X padding. Defaults to None.
            pady (PadType | None, optional): Y padding. Defaults to None.
            events (bool, optional): Enable events for this widget. Defaults to True.
            keyrelease (bool, optional): If True, emits EventType.KeyRelease event on every key release.
            sticky (str | None, optional): Sticky direction for widget layout. Defaults to None.
            tooltip (TooltipType | None, optional): Tooltip text or callback to generate tooltip text. Defaults to None.
            command (CommandType | None, optional): Command callback. Defaults to None.
            hscrollbar (bool, optional): Show horizontal scrollbar. Defaults to False.
            weightx (int | None, optional): Weight for horizontal resizing. Defaults to None.
            weighty (int | None, optional): Weight for vertical resizing. Defaults to None.
            focus (bool, optional): If True, widget will have focus. Defaults to False. Only one widget can have focus.
            **kwargs: Additional keyword arguments are passed to ttk.Entry.

        Note:
            Emits EventType.EntryReturn event on return key press.
            If keyrelease is True, emits EventType.KeyRelease event on every key release.
        """
        super().__init__(
            key=key,
            default=default,
            disabled=disabled,
            columnspan=columnspan,
            rowspan=rowspan,
            padx=padx,
            pady=pady,
            events=events,
            keyrelease=keyrelease,
            sticky=sticky,
            tooltip=tooltip,
            command=command,
            hscrollbar=hscrollbar,
            focus=focus,
            weightx=weightx,
            weighty=weighty,
        )
        self.widget_type = "guitk.LabelEntry"
        self.text = text
        self.kwargs = kwargs

    def _create_widget(self, parent, window: "Window", row, col):
        # build arg list for Entry
        kwargs_entry = {
            k: v for k, v in self.kwargs.items() if k in _valid_ttk_entry_attributes
        }
        self.widget = _ttkLabelEntry(
            parent, text=self.text, textvariable=self._value, **kwargs_entry
        )
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        # bind key release event
        event = Event(self, window, self.key, EventType.KeyRelease)
        self.widget.bind("<KeyRelease>", window._make_callback(event))

        # bind return key event
        entry_return_key = Event(self, window, self.key, EventType.EntryReturn)
        self.widget.bind("<Return>", window._make_callback(entry_return_key))

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
