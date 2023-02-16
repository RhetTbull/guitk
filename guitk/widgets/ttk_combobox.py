"""ttk Combobox widget"""

import tkinter.ttk as ttk

from .events import Event, EventCommand, EventType
from .widget import Widget

class Combobox(Widget):
    """ttk Combobox"""

    def __init__(
        self,
        key=None,
        cursor=None,
        exportselection=None,
        height=None,
        justify=None,
        # postcommand=None,
        style=None,
        takefocus=None,
        # validate=None,
        # validatecommand=None,
        values=None,
        default=None,
        width=None,
        # default=None,
        disabled=False,
        columnspan=None,
        rowspan=None,
        padx=None,
        pady=None,
        events=False,
        sticky=None,
        tooltip=None,
        readonly=False,
        autosize=False,
        command=None,
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
        self.widget_type = "ttk.Combobox"
        # default = default or ""
        # self._value.set(default)
        self.key = key or "Combobox"
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.width = width
        self._readonly = readonly
        self._autosize = autosize

        # ttk.Combobox args
        self.cursor = cursor  # TODO: take cursor out of Widget?
        self.exportselection = exportselection
        self.height = height
        self.justify = justify
        self.style = style
        self.takefocus = takefocus
        self.combobox_values = values or []
        self.default = default
        self.width = width

    def _create_widget(self, parent, window: "Window", row, col):
        self.window = window
        self._parent = parent

        # build arg list for Entry
        kwargs = {}
        for kw in [
            "cursor",
            "exportselection",
            "height",
            "justify",
            "style",
            "takefocus",
            "width",
        ]:
            val = getattr(self, kw)
            if val is not None:
                kwargs[kw] = val
        if self.combobox_values is not None:
            kwargs["values"] = self.combobox_values

        if self._autosize:
            # automatically set width, override any width value provided
            width = len(max(self.combobox_values, key=len))
            kwargs["width"] = width + 1

        self.widget = ttk.Combobox(parent, textvariable=self._value, **kwargs)
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        event_release = Event(self.widget, window, self.key, EventType.KeyRelease)
        self.widget.bind("<KeyRelease>", window._make_callback(event_release))

        event_selected = Event(
            self.widget, window, self.key, EventType.ComboboxSelected
        )
        self.widget.bind("<<ComboboxSelected>>", window._make_callback(event_selected))

        if self._command:
            self.events = True
            window._bind_command(
                EventCommand(
                    widget=self,
                    key=self.key,
                    event_type=EventType.ComboboxSelected,
                    command=self._command,
                )
            )

        if self.default is not None:
            self.value = self.default

        if self._disabled:
            self.widget.state(["disabled"])

        if self._readonly:
            self.widget.state(["readonly"])

        return self.widget

    @property
    def combobox(self):
        """Return the Tk combobox widget"""
        return self.widget

