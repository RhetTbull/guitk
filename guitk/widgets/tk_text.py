""" tk Text and Output widgets """

import tkinter as tk

from guitk.redirect import StdErrRedirect, StdOutRedirect

from .events import Event, EventCommand, EventType
from .utils import scrolled_widget_factory
from .widget import Widget


class Text(Widget):
    """Text box"""

    def __init__(
        self,
        text=None,
        key=None,
        width=40,
        height=20,
        disabled=False,
        rowspan=None,
        columnspan=None,
        padx=None,
        pady=None,
        events=False,
        sticky=None,
        tooltip=None,
        command=None,
        vscrollbar=False,
        hscrollbar=False,
        **kwargs,
    ):
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
        self.window = window
        self._parent = parent
        self.widget = scrolled_widget_factory(
            parent,
            tk.Text,
            vscrollbar=self.vscrollbar,
            hscrollbar=self.hscrollbar,
            width=self.width,
            height=self.height,
            **self.kwargs,
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
    """Text box with stderr/stdout redirected"""

    def __init__(
        self,
        text=None,
        key=None,
        width=40,
        height=20,
        disabled=False,
        echo=False,
        rowspan=None,
        columnspan=None,
        padx=None,
        pady=None,
        events=False,
        sticky=None,
        tooltip=None,
        stdout=True,
        stderr=True,
    ):
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
            vscrollbar=True,
        )
        self._echo = echo
        self._redirect = []
        self._redirect_id = {}
        if stdout:
            self._redirect.append(StdOutRedirect())
        if stderr:
            self._redirect.append(StdErrRedirect())
        for r in self._redirect:
            r.echo = self._echo
            self._redirect_id[r] = r.register(self._write)

    def _create_widget(self, parent, window: "Window", row, col):
        super()._create_widget(parent, window, row, col)
        # Unbind <KeyRelease> since this isn't for user input
        self.widget.unbind("<KeyRelease>")

        if self.events:
            event = Event(self, window, self.key, EventType.OutputWrite)
            self.window.root.bind_all(
                EventType.OutputWrite.value, window._make_callback(event)
            )

        self.enable_redirect()

        return self.widget

    def _write(self, line):
        self.text.insert(tk.END, line)
        self.text.yview(tk.END)
        self.window.root.event_generate(EventType.OutputWrite.value)

    @property
    def echo(self):
        return self._echo

    @echo.setter
    def echo(self, echo):
        self._echo = echo
        for r in self._redirect:
            r.echo = echo

    def disable_redirect(self):
        for r in self._redirect:
            r.disable_redirect()

    def enable_redirect(self):
        for r in self._redirect:
            r.enable_redirect()

    def __del__(self):
        for r, id_ in self._redirect_id.items():
            r.deregister(id_)
