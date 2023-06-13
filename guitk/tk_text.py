""" tk Text and Output widgets """


from __future__ import annotations

import contextlib
import tkinter as tk
from typing import Hashable, TypeVar

from guitk.redirect import StdErrRedirect, StdOutRedirect

from .basewidget import BaseWidget
from .events import Event, EventCommand, EventType
from .types import CommandType, PadType, TooltipType
from .utils import scrolled_widget_factory

__all__ = ["Text", "Output"]


_valid_standard_attributes = {
    "background",
    "borderwidth",
    "cursor",
    "exportselection",
    "font",
    "foreground",
    "highlightbackground",
    "highlightcolor",
    "highlightthickness",
    "insertbackground",
    "insertborderwidth",
    "insertofftime",
    "insertontime",
    "insertwidth",
    "padx",
    "pady",
    "relief",
    "selectbackground",
    "selectborderwidth",
    "selectforeground",
    "setgrid",
    "takefocus",
    "xscrollcommand",
    "yscrollcommand",
}

_valid_tk_text_attributes = {
    "autoseparators",
    "maxundo",
    "spacing1",
    "spacing2",
    "spacing3",
    "state",
    "tabs",
    "undo",
    "wrap",
} | _valid_standard_attributes


Window = TypeVar("Window")


class Text(BaseWidget):
    """A tk Text box"""

    def __init__(
        self,
        text: str | None = None,
        key: Hashable | None = None,
        width: int = 40,
        height: int = 20,
        disabled: bool = False,
        columnspan: int | None = None,
        rowspan: int | None = None,
        padx: PadType | None = None,
        pady: PadType | None = None,
        events: bool = False,
        sticky: str | None = None,
        tooltip: TooltipType = None,
        command: CommandType | None = None,
        vscrollbar: bool = False,
        hscrollbar: bool = False,
        weightx: int | None = None,
        weighty: int | None = None,
        focus: bool = False,
        **kwargs,
    ):
        """
        Initialize a Text widget.

        Args:
            text (str | None, optional): Default text for the text box. Defaults to None.
            key (Hashable, optional): Unique key for this widget. Defaults to None.
            width (int, optional): Width of the text box. Defaults to 40.
            height (int, optional): Height of the text box. Defaults to 20.
            disabled (bool, optional): If True, widget is disabled. Defaults to False.
            columnspan (int | None, optional): Number of columns to span. Defaults to None.
            rowspan (int | None, optional): Number of rows to span. Defaults to None.
            padx (PadType | None, optional): X padding. Defaults to None.
            pady (PadType | None, optional): Y padding. Defaults to None.
            events (bool, optional): Enable events for this widget. Defaults to False.
            sticky (str | None, optional): Sticky direction for widget layout. Defaults to None.
            tooltip (TooltipType | None, optional): Tooltip text or callback to generate tooltip text. Defaults to None.
            command (CommandType | None, optional): Command callback. Defaults to None.
            vscrollbar (bool, optional): Show vertical scrollbar. Defaults to False.
            hscrollbar (bool, optional): Show horizontal scrollbar. Defaults to False.
            weightx (int | None, optional): Weight of the widget in the x direction. Defaults to None.
            weighty (int | None, optional): Weight of the widget in the y direction. Defaults to None.
            focus (bool, optional): If True, widget has focus. Defaults to False.
                Only one widget in a window can have focus.HLayout
            **kwargs: Additional keyword arguments are passed to tk Text.

        Note:
            Emits EventType.KeyRelease events when the text is changed and events is True.
        """
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
            command=command,
            weightx=weightx,
            weighty=weighty,
            focus=focus,
        )
        self.widget_type = "tk.Text"
        self.key = key or "Text"
        self.width = width
        self.height = height
        self._value = text if text is not None else ""
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.vscrollbar = vscrollbar
        self.hscrollbar = hscrollbar
        self.kwargs = kwargs

    def _create_widget(self, parent, window: "Window", row, col):
        kwargs_text = {
            k: v for k, v in self.kwargs.items() if k in _valid_tk_text_attributes
        }
        self.widget = scrolled_widget_factory(
            parent,
            tk.Text,
            vscrollbar=self.vscrollbar,
            hscrollbar=self.hscrollbar,
            width=self.width,
            height=self.height,
            **kwargs_text,
        )
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        event = Event(self, window, self.key, EventType.KeyRelease)
        self.widget.bind("<KeyRelease>", window._make_callback(event))

        self.value = self._value

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
            self.widget["state"] = "disabled"

        return self.widget

    @property
    def value(self):
        return self.widget.get("1.0", tk.END).rstrip()

    @value.setter
    def value(self, text):
        self.widget.delete("1.0", tk.END)
        self.widget.insert("1.0", text)

    @property
    def text(self):
        """Return the Tk text widget"""
        return self.widget


# TODO: how to make Output read-only?
class Output(Text):
    """Text box that redirects stderr and/or stdout to the text box."""

    def __init__(
        self,
        text: str | None = None,
        key: Hashable | None = None,
        width: int = 40,
        height: int = 20,
        disabled: bool = False,
        columnspan: int | None = None,
        rowspan: int | None = None,
        padx: PadType | None = None,
        pady: PadType | None = None,
        events: bool = False,
        sticky: str | None = None,
        tooltip: TooltipType = None,
        vscrollbar: bool = True,
        hscrollbar: bool = False,
        stdout: bool = True,
        stderr: bool = True,
        echo: bool = False,
        weightx: int | None = None,
        weighty: int | None = None,
        focus: bool = False,
        **kwargs,
    ):
        """
        Initialize an Output widget.

        Args:
            text (str | None, optional): Default text for the text box. Defaults to None.
            key (Hashable, optional): Unique key for this widget. Defaults to None.
            width (int, optional): Width of the text box. Defaults to 40.
            height (int, optional): Height of the text box. Defaults to 20.
            disabled (bool, optional): If True, widget is disabled. Defaults to False.
            columnspan (int | None, optional): Number of columns to span. Defaults to None.
            rowspan (int | None, optional): Number of rows to span. Defaults to None.
            padx (PadType | None, optional): X padding. Defaults to None.
            pady (PadType | None, optional): Y padding. Defaults to None.
            events (bool, optional): Enable events for this widget. Defaults to False.
            sticky (str | None, optional): Sticky direction for widget layout. Defaults to None.
            tooltip (TooltipType | None, optional): Tooltip text or callback to generate tooltip text. Defaults to None.
            command (CommandType | None, optional): Command callback. Defaults to None.
            vscrollbar (bool, optional): Show vertical scrollbar. Defaults to False.
            hscrollbar (bool, optional): Show horizontal scrollbar. Defaults to False.
            stdout (bool, optional): Redirect stdout to the text box. Defaults to True.
            stderr (bool, optional): Redirect stderr to the text box. Defaults to True.
            echo (bool, optional): Echo stdout and stderr to the console. Defaults to False.
            weightx (int | None, optional): Weight of the widget in the x direction. Defaults to None.
            weighty (int | None, optional): Weight of the widget in the y direction. Defaults to None.
            focus (bool, optional): If True, widget has focus. Defaults to False.
                Only one widget in a window can have focus.HLayout
            **kwargs: Additional keyword arguments are passed to tk Text.
        """
        super().__init__(
            text=text,
            key=key,
            width=width,
            height=height,
            disabled=disabled,
            rowspan=rowspan,
            columnspan=columnspan,
            padx=padx,
            pady=pady,
            events=events,
            sticky=sticky,
            tooltip=tooltip,
            vscrollbar=vscrollbar,
            hscrollbar=hscrollbar,
            weightx=weightx,
            weighty=weighty,
            focus=focus,
            **kwargs,
        )

        self.kwargs = kwargs
        self._echo = echo
        self._stdout = stdout
        self._stderr = stderr

        # stores state for stdout and stderr redirection
        self._redirect = []
        self._redirect_id = {}

    def _create_widget(self, parent, window: "Window", row, col):
        self.widget = super()._create_widget(parent, window, row, col)

        # Unbind <KeyRelease> since this isn't for user input
        self.widget.unbind("<KeyRelease>")

        if self.events:
            event = Event(self, window, self.key, EventType.OutputWrite)
            self.window.root.bind_all(
                EventType.OutputWrite.value, window._make_callback(event)
            )

        self._configure_redirect()
        self.enable_redirect()

        return self.widget

    def _configure_redirect(self):
        """Configure stdout and stderr redirection."""
        if self._stdout:
            self._redirect.append(StdOutRedirect())
        if self._stderr:
            self._redirect.append(StdErrRedirect())
        for r in self._redirect:
            r.echo = self._echo
            self._redirect_id[r] = r.register(self._write)

    def _write(self, line):
        with contextlib.suppress(tk.TclError):
            # ignore TclError if widget has been destroyed while trying to write
            self.text.insert(tk.END, line)
            self.text.yview(tk.END)
        self.window.root.event_generate(EventType.OutputWrite.value)

    @property
    def echo(self):
        """Return True if stdout and stderr are echoed to the console."""
        return self._echo

    @echo.setter
    def echo(self, echo):
        """Set whether stdout and stderr are echoed to the console."""
        self._echo = echo
        for r in self._redirect:
            r.echo = echo

    def disable_redirect(self):
        """Disable redirecting stdout and stderr to the text box."""
        for r in self._redirect:
            r.disable_redirect()

    def enable_redirect(self):
        """Enable redirecting stdout and stderr to the text box."""
        for r in self._redirect:
            r.enable_redirect()

    def __del__(self):
        for r, id_ in self._redirect_id.items():
            r.deregister(id_)
