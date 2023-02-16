"""ttk Button widgets"""

import tkinter.ttk as ttk
from tkinter import filedialog

from .events import Event, EventCommand, EventType
from .widget import Widget


class Button(Widget):
    """Basic button"""

    def __init__(
        self,
        text,
        key=None,
        disabled=False,
        columnspan=None,
        rowspan=None,
        padx=None,
        pady=None,
        width=None,
        events=True,
        sticky=None,
        tooltip=None,
        anchor=None,
        takefocus=None,
        command=None,
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
            anchor=anchor,
            takefocus=takefocus,
            command=command,
        )
        self.widget_type = "ttk.Button"
        self.text = text
        self.key = key or text
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.tooltip = tooltip
        self.width = width

    @property
    def value(self):
        return self.widget["text"]

    @value.setter
    def value(self, text):
        self.widget["text"] = text

    def _create_widget(self, parent, window: "Window", row, col):
        self.window = window
        self._parent = parent
        event = Event(self, window, self.key, EventType.ButtonPress)

        # build arg list for Button()
        # TODO: standardize attribute names
        kwargs = {}
        for kw in ["text", "anchor", "width", "takefocus"]:
            val = getattr(self, f"{kw}")
            if val is not None:
                kwargs[kw] = val

        self.widget = ttk.Button(parent, command=window._make_callback(event), **kwargs)
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        if self._command:
            self.events = True
            window._bind_command(
                EventCommand(
                    widget=self,
                    key=self.key,
                    event_type=EventType.ButtonPress,
                    command=self._command,
                )
            )

        if self._disabled:
            self.widget.state(["disabled"])

        return self.widget

    @property
    def button(self):
        """Return the Tk button widget"""
        return self.widget


class BrowseFileButton(Button):
    def __init__(
        self,
        text="Browse",
        key=None,
        target_key=None,
        disabled=False,
        columnspan=None,
        rowspan=None,
        padx=None,
        pady=None,
        events=True,
        sticky=None,
        tooltip=None,
        anchor=None,
        filename_only=None,
        **options,
        # initialdir=None,
        # filetypes=None,
        # title=None,
    ):
        super().__init__(
            text,
            key=key,
            disabled=disabled,
            columnspan=columnspan,
            rowspan=rowspan,
            padx=padx,
            pady=pady,
            events=events,
            sticky=sticky,
            tooltip=tooltip,
            anchor=anchor,
        )
        self.target_key = target_key
        self.widget_type = "guitk.BrowseFileButton"
        self._filename = None
        self._options = options
        self._filename_only = filename_only

    def _create_widget(self, parent, window: "Window", row, col):
        self.window = window
        self._parent = parent
        self.widget = ttk.Button(
            parent, text=self.text, anchor=self.anchor, command=self.browse_dialog
        )
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )
        if self._disabled:
            self.widget.state(["disabled"])

        return self.widget

    @property
    def filename(self):
        return self._filename

    def browse_dialog(self):
        self._filename = filedialog.askopenfilename(**self._options)
        if self._filename_only and self._filename:
            # only want the name, not the path
            self._filename = str(pathlib.Path(self._filename).name)
        if self.target_key and self._filename:
            self.window[self.target_key].value = self._filename
        event = Event(self, self.window, self.key, EventType.BrowseFile)
        self.window._handle_event(event)


class BrowseDirectoryButton(Button):
    def __init__(
        self,
        text="Browse",
        key=None,
        target_key=None,
        disabled=False,
        columnspan=None,
        rowspan=None,
        padx=None,
        pady=None,
        events=True,
        sticky=None,
        tooltip=None,
        anchor=None,
        **options,
    ):
        super().__init__(
            text,
            key=key,
            disabled=disabled,
            columnspan=columnspan,
            rowspan=rowspan,
            padx=padx,
            pady=pady,
            events=events,
            sticky=sticky,
            tooltip=tooltip,
            anchor=anchor,
        )
        self.target_key = target_key
        self.widget_type = "guitk.BrowseDirectoryButton"
        self._dirname = None
        self._options = options

    def _create_widget(self, parent, window: "Window", row, col):
        self.window = window
        self._parent = parent
        self.widget = ttk.Button(
            parent, text=self.text, anchor=self.anchor, command=self.browse_dialog
        )
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )
        if self._disabled:
            self.widget.state(["disabled"])

        return self.widget

    @property
    def directory(self):
        return self._dirname

    def browse_dialog(self):
        self._dirname = filedialog.askdirectory(**self._options)
        if self.target_key and self._dirname:
            self.window[self.target_key].value = self._dirname
        event = Event(self, self.window, self.key, EventType.BrowseDirectory)
        self.window._handle_event(event)

