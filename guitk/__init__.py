""" Set of classes to simplify building a GUI app with tkinter
    Inspired by PySimpleGUI but built in a cleanroom manner (did not use PySimpleGUI code)

    No dependencies outside python standard library.

    Published under the MIT License.

    Copyright Rhet Turnbull, 2020, all rights reserved.
"""

# TODO: add Column?
# TODO: add way to specify tooltip delay

import sys
import tkinter as tk
from enum import Enum, auto
from tkinter import filedialog, ttk
import time

from .redirect import StdOutRedirect, StdErrRedirect
from .tooltips import Hovertip


class GUITK(Enum):
    """Constants used internally by guitk """

    ELEMENT_FRAME = ("Frame",)
    ELEMENT_LABEL_FRAME = "LabelFrame"


class EventType(Enum):
    """Constants for event types"""

    BUTTON_PRESS = auto()
    CHECK_BUTTON = auto()
    VIRTUAL_EVENT = auto()
    BROWSE_FILE = auto()
    BROWSE_DIRECTORY = auto()


class TKRoot:
    """ Singleton that returns a tkinter.TK() object; there can be only one in an app"""

    def __new__(cls, *args, **kwargs):
        """ create new object or return instance of already created singleton """
        if not hasattr(cls, "instance") or not cls.instance:
            cls.instance = super().__new__(cls)

        return cls.instance

    def __init__(self):
        if hasattr(self, "root"):
            return

        # create root object, make it invisible and withdraw it
        # all other windows will be children of this invisible root object
        root = tk.Tk()
        root.attributes("-alpha", 0)
        root.withdraw()
        self.root = root
        self.first_window = False
        self.windows = {}
        self.mainloop_is_running = False

    def register(self, window):
        """Register a new child window """
        # print(f"register: {window}")
        if not self.first_window:
            self.first_window = True
        self.windows[window] = 1

    def deregister(self, window):
        """De-register a new child window
           Once all children are de-registered, the root Tk object is destroyed
        """
        # print(f"deregister: {window}")
        try:
            del self.windows[window]
        except KeyError:
            pass
        if self.first_window and not self.windows:
            # last window
            # print(f"last window!")
            self.root.destroy()

    def run_mainloop(self):
        if not self.mainloop_is_running:
            self.root.mainloop()


class Layout:
    """Mixin class to provide layout"""

    layout = []

    def __init__(self, *args, **kwargs):
        pass

    def _layout(self, parent, window, autoframe):
        # as this is a mixin, make sure class being mixed into has necessary attributes

        row_offset = 0
        for row_count, row in enumerate(self.layout):
            col_offset = 0
            if autoframe and len(row) > 1:
                row_ = [Frame(layout=[row], autoframe=False)]
            else:
                row_ = row
            for col_count, widget in enumerate(row_):
                if widget is None:
                    # add blank label to maintain column spacing
                    widget = Label("", disabled=True, events=False)

                widget.key = (
                    widget.key or f"{widget.element_type},{row_count},{col_count}"
                )
                widget.create_element(
                    parent, window, row_count + row_offset, col_count + col_offset
                )
                widget._tooltip = (
                    Hovertip(widget.element, widget.tooltip) if widget.tooltip else None
                )
                window._elements.append(widget)
                widget.parent = self
                window._element_by_key[widget.key] = widget
                if widget.rowspan and widget.rowspan > 1:
                    row_offset += widget.rowspan - 1
                if widget.columnspan and widget.columnspan > 1:
                    col_offset += widget.columnspan - 1


class Window(Layout):
    """Basic Window class from which all windows are derived
    
    Notes:
        Classes which inherit from window should implement handle_event, setup, and teardown as needed
    """

    layout = []
    """Every class that inherits from Window must define it's own class level layout """

    def __init__(
        self, title, parent=None, padx=None, pady=None, topmost=None, autoframe=True
    ):
        self.title = title
        self.id = id(self)
        self.tk = TKRoot()
        # self.root = self.tk.root
        self.parent = self.tk.root if not parent else parent
        self.padx = padx
        self.pady = pady
        self.topmost = topmost

        self.window = tk.Toplevel(self.parent)
        self.window.title(title)
        self._elements = []
        self._element_by_key = {}

        self._timer_events = {}
        """ timer events that have been set by bind_timer_event, stores most recent after() id for event"""

        self._return_value = None
        """ value returned from run() if set in quit() """

        self.mainframe = ttk.Frame(self.window, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)

        self.tk.register(self)
        self.window.protocol(
            "WM_DELETE_WINDOW",
            self._make_callback(
                Event(self, self, "WM_WINDOW_DELETE", "WM_WINDOW_DELETE")
            ),
        )

        if not self.layout:
            self.layout = [
                [
                    Label(
                        "Looks like you forgot to include a layout in your class definition"
                    )
                ]
            ]

        self._layout(self.mainframe, self, autoframe=autoframe)

        # apply padding, element padding takes precedent over window
        for element in self._elements:
            padx = element.padx or self.padx
            pady = element.pady or self.pady
            element.element.grid_configure(padx=padx, pady=pady)

        if self.topmost:
            self.window.attributes("-topmost", 1)

        self.setup()

    def handle_event(self, event):
        """Handle event objects, inheriting classes should implement handle_event"""
        pass

    def setup(self):
        """Perform any needed setup for the window. 
           Gets called immediately after __init__
        """
        pass

    def teardown(self):
        """Perform any cleanup before the window closes.
           Gets called immediately before the window is destroyed
        """
        pass

    def quit(self, return_value=None):
        """ Close the window """
        self._return_value = return_value
        self._destroy()

    def bind_timer_event(self, delay, event_name, repeat=False):
        """ Create a new virtual event `event_name` that fires after `delay` ms, 
        repeats every `delay` ms if repeat=True, otherwise fires once """

        # create a unique name for the timer
        timer_id = f"{event_name}_{time.time_ns()}"

        def _generate_event():
            self.tk.root.event_generate(event_name)
            if repeat:
                self._timer_events[timer_id] = self.tk.root.after(
                    delay, _generate_event
                )

        event = Event(self, self, event_name, EventType.VIRTUAL_EVENT)
        self.tk.root.bind(event_name, self._make_callback(event))
        self._timer_events[timer_id] = self.tk.root.after(delay, _generate_event)
        return timer_id

    def cancel_timer_event(self, timer_id):
        """ Cancel a timer event created with bind_timer_event """
        try:
            after_id = self._timer_events[timer_id]
            self.tk.root.after_cancel(after_id)
        except Exception:
            pass

    def _destroy(self):
        # disable any stdout/stderr redirection
        for element in self._elements:
            if type(element) == Output:
                element.disable_redirect()
        self.teardown()
        self.window.destroy()
        self.tk.deregister(self)

    def _make_callback(self, event):
        def _callback(*args):
            self._handle_event(event)

        return _callback

    def _handle_event(self, event):
        # only handle events if element has events=True; Window objects always get events
        # print(f"_handle_event={event}")
        if isinstance(event.element, Element) and not event.element.events:
            # print(f"skip this event: {event}")
            return

        event.values = {
            elem.key: elem.value for elem in self._elements if type(elem) != Output
        }
        # filter events for this window
        if event.id == id(self):
            self.handle_event(event)

            # if deleting the window, call call _destroy after handle_event has had a chance to handle it
            if event.event == "WM_WINDOW_DELETE":
                self._destroy()

    def run(self):
        self.tk.run_mainloop()
        return self._return_value

    def __getitem__(self, key):
        try:
            return self._element_by_key[key]
        except KeyError:
            return None


class Event:
    """Event that occurred and values for elements in the window """

    def __init__(self, element: object, window: Window, key, event):
        self.id = id(window)
        self.element = element
        self.key = key
        self.event = event
        self.values = {}

    def __str__(self):
        return f"id={self.id}, element={self.element}, key={self.key}, event={self.event}, values={self.values}"


class Element:
    """Basic abstract base class for all tk elements """

    def __init__(
        self,
        key=None,
        disabled=False,
        rowspan=None,
        columnspan=None,
        padx=None,
        pady=None,
        events=True,
        sticky=None,
        tooltip=None,
        anchor=None,
    ):
        self.key = key
        self.disabled = disabled
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.padx = padx
        self.pady = pady
        self.events = events
        self.sticky = sticky or ""
        self.tooltip = tooltip
        self.anchor = anchor

        self.element_type = None
        self._tk = TKRoot()
        self.element = None
        self._value = tk.StringVar()

        # get set by create_element in inherited classes
        self.parent = None
        self.window = None

    @property
    def value(self):
        return self._value.get()

    @value.setter
    def value(self, value):
        self._value.set(value)

    def _grid(self, row, column, rowspan, columnspan):
        sticky = self.sticky or tk.W
        self.element.grid(
            row=row,
            column=column,
            columnspan=columnspan,
            rowspan=rowspan,
            sticky=sticky,
        )

        if self.padx is not None or self.pady is not None:
            self.element.grid_configure(padx=self.padx, pady=self.pady)

    def bind_event(self, event_name):
        """Bind a tkinter event to element; will result in an Event of event_type type being sent to handle_event when triggered"""
        event = Event(self, self, self.key, event_name)
        self.element.bind(event_name, self.window._make_callback(event))


class Entry(Element):
    """Text entry / input box """

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
        )
        self.element_type = "ttk.Entry"
        default = default or ""
        self._value.set(default)
        self.key = key or "Entry"
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.width = width

    def create_element(self, parent, window, row, col):
        self.window = window
        self.parent = parent
        self.element = ttk.Entry(parent, textvariable=self._value, width=self.width)
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        event = Event(self, self, self.key, "<KeyRelease>")
        self.element.bind("<KeyRelease>", window._make_callback(event))

        if self.disabled:
            self.element.state(["disabled"])
        return self.element

    @property
    def entry(self):
        """Return the Tk entry element"""
        return self.element


class Label(Element):
    """Text label """

    def __init__(
        self,
        text,
        key=None,
        disabled=False,
        rowspan=None,
        columnspan=None,
        width=None,
        padx=None,
        pady=None,
        events=False,
        sticky=None,
        tooltip=None,
        anchor=None,
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
        )
        self.element_type = "ttk.Label"
        self.text = text
        self.key = key or text
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.width = width

    def create_element(self, parent, window, row, col):
        self.window = window
        self.parent = parent
        self.element = ttk.Label(
            parent, text=self.text, width=self.width, anchor=self.anchor
        )
        self.element["textvariable"] = self._value
        self._value.set(self.text)
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )
        if self.disabled:
            self.element.state(["disabled"])
        return self.element

    @property
    def label(self):
        """Return the Tk label element"""
        return self.element


class Button(Element):
    """Basic button """

    def __init__(
        self,
        text,
        key=None,
        disabled=False,
        columnspan=None,
        rowspan=None,
        padx=None,
        pady=None,
        events=True,
        sticky=None,
        tooltip=None,
        anchor=None,
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
        )
        self.element_type = "ttk.Button"
        self.text = text
        self.key = key or text
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.tooltip = tooltip

    @property
    def value(self):
        return self.element["text"]

    @value.setter
    def value(self, text):
        self.element["text"] = text

    def create_element(self, parent, window, row, col):
        self.window = window
        self.parent = parent
        event = Event(self, window, self.key, EventType.BUTTON_PRESS)
        self.element = ttk.Button(
            parent,
            text=self.text,
            anchor=self.anchor,
            command=window._make_callback(event),
        )
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )
        if self.disabled:
            self.element.state(["disabled"])

        return self.element

    @property
    def button(self):
        """Return the Tk button element"""
        return self.element


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
        self.element_type = "guitk.BrowseFileButton"
        self._filename = None

    def create_element(self, parent, window, row, col):
        self.window = window
        self.parent = parent
        self.element = ttk.Button(
            parent, text=self.text, anchor=self.anchor, command=self.browse_dialog
        )
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )
        if self.disabled:
            self.element.state(["disabled"])

        return self.element

    @property
    def filename(self):
        return self._filename

    def browse_dialog(self):
        self._filename = filedialog.askopenfilename()
        if self.target_key:
            self.window[self.target_key].value = self._filename
        event = Event(self, self.window, self.key, EventType.BROWSE_FILE)
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
        self.element_type = "guitk.BrowseDirectoryButton"
        self._dirname = None

    def create_element(self, parent, window, row, col):
        self.window = window
        self.parent = parent
        self.element = ttk.Button(
            parent, text=self.text, anchor=self.anchor, command=self.browse_dialog
        )
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )
        if self.disabled:
            self.element.state(["disabled"])

        return self.element

    @property
    def directory(self):
        return self._dirname

    def browse_dialog(self):
        self._dirname = filedialog.askdirectory()
        if self.target_key:
            self.window[self.target_key].value = self._dirname
        event = Event(self, self.window, self.key, EventType.BROWSE_DIRECTORY)
        self.window._handle_event(event)


class CheckButton(Element):
    """Checkbox / checkbutton """

    def __init__(
        self,
        text,
        key="",
        disabled=False,
        rowspan=None,
        columnspan=None,
        padx=None,
        pady=None,
        events=True,
        sticky=None,
        tooltip=None,
        anchor=None,
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
        )
        self.element_type = "ttk.CheckButton"
        self.text = text
        self.key = key or text
        self.columnspan = columnspan
        self.rowspan = rowspan
        self._value = tk.BooleanVar()

    def create_element(self, parent, window, row, col):
        self.window = window
        self.parent = parent
        event = Event(self, window, self.key, EventType.CHECK_BUTTON)
        self.element = ttk.Checkbutton(
            parent,
            text=self.text,
            anchor=self.anchor,
            command=window._make_callback(event),
            variable=self._value,
            onvalue=True,
        )
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )
        if self.disabled:
            self.element.state(["disabled"])
        return self.element

    @property
    def checkbutton(self):
        """Return the Tk checkbutton element"""
        return self.element


class Text(Element):
    """Text box """

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
        )
        self.element_type = "tk.Text"
        self.key = key or "Text"
        self.width = width
        self.height = height
        self._value = text or ""
        self.columnspan = columnspan
        self.rowspan = rowspan

    def create_element(self, parent, window, row, col):
        self.window = window
        self.parent = parent
        self.element = tk.Text(parent, width=self.width, height=self.height)
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        event = Event(self, self, self.key, "<KeyRelease>")
        self.element.bind("<KeyRelease>", window._make_callback(event))

        if self.disabled:
            self.element["state"] = "disabled"
        return self.element

    @property
    def value(self):
        return self.element.get("1.0", tk.END).rstrip()

    @value.setter
    def value(self, text):
        self.element.delete("1.0", tk.END)
        self.element.insert("1.0", text)

    @property
    def text(self):
        """Return the Tk text element"""
        return self.element


class _ttkScrolledText(tk.Text):
    """ScrolledText class with ttk.ScrollBar

    Lifted from cpython source with edits to use ttk scrollbar:
    https://github.com/python/cpython/blob/3.9/Lib/tkinter/scrolledtext.py
    """

    def __init__(self, master=None, **kw):
        self.frame = ttk.Frame(master)
        self.vbar = ttk.Scrollbar(self.frame)
        self.vbar.pack(side=tk.RIGHT, fill=tk.Y)

        kw.update({"yscrollcommand": self.vbar.set})
        tk.Text.__init__(self, self.frame, **kw)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.vbar["command"] = self.yview

        # Copy geometry methods of self.frame without overriding Text
        # methods -- hack!
        text_meths = vars(tk.Text).keys()
        methods = vars(tk.Pack).keys() | vars(tk.Grid).keys() | vars(tk.Place).keys()
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != "_" and m != "config" and m != "configure":
                setattr(self, m, getattr(self.frame, m))

    def __str__(self):
        return str(self.frame)


class ScrolledText(Text):
    """Text box with scrollbars """

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
    ):
        super().__init__(
            text=text,
            key=key,
            disabled=disabled,
            rowspan=rowspan,
            columnspan=columnspan,
            padx=padx,
            pady=pady,
            events=events,
            sticky=sticky,
            tooltip=tooltip,
        )
        self.element_type = "guitk.ScrolledText"
        self.key = key or "ScrolledText"
        self.width = width
        self.height = height
        self._value = text if text is not None else ""
        self.columnspan = columnspan
        self.rowspan = rowspan

    def create_element(self, parent, window, row, col):
        self.window = window
        self.parent = parent
        self.element = _ttkScrolledText(parent, width=self.width, height=self.height)
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        event = Event(self, self, self.key, "<KeyRelease>")
        self.element.bind("<KeyRelease>", window._make_callback(event))

        if self.disabled:
            self.element["state"] = "disabled"

        self.value = self._value

        return self.element

    @property
    def value(self):
        return self.element.get("1.0", tk.END).rstrip()

    @value.setter
    def value(self, text):
        self.element.delete("1.0", tk.END)
        self.element.insert("1.0", text)
        self.element.yview(tk.END)


class Output(ScrolledText):
    """Text box with stderr/stdout redirected """

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

    def create_element(self, parent, window, row, col):
        super().create_element(parent, window, row, col)
        self.enable_redirect()
        self.element.unbind("<KeyRelease>")
        return self.element

    def _write(self, line):
        self.text.insert(tk.END, line)
        self.text.yview(tk.END)

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


class _Frame(Element, Layout):
    """Frame base class for Frame and LabelFrame"""

    def __init__(
        self,
        frametype=GUITK.ELEMENT_FRAME,
        width=None,
        key=None,
        height=None,
        layout=None,
        style=None,
        borderwidth=None,
        padding=None,
        relief=None,
        disabled=False,
        rowspan=None,
        columnspan=None,
        text=None,
        labelanchor=None,
        sticky=None,
        tooltip=None,
        autoframe=True,
    ):
        super().__init__(
            key=key,
            disabled=disabled,
            rowspan=rowspan,
            columnspan=columnspan,
            sticky=sticky,
            tooltip=tooltip,
        )
        self._autoframe = autoframe

        if frametype not in [GUITK.ELEMENT_FRAME, GUITK.ELEMENT_LABEL_FRAME]:
            raise ValueError(f"bad frametype: {frametype}")
        self.frametype = frametype
        self.element_type = (
            "ttk.Frame" if frametype == GUITK.ELEMENT_FRAME else "ttk.LabelFrame"
        )
        if key is None:
            key = "Frame" if frametype == GUITK.ELEMENT_FRAME else "LabelFrame"
        self.key = key
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.width = width
        self.height = height
        self.style = style
        self.borderwidth = borderwidth
        self.padding = padding
        self.relief = relief
        self.layout = layout
        self.text = text
        self.labelanchor = labelanchor or "nw"

    def create_element(self, parent, window, row, col):
        self.window = window
        self.parent = parent

        if self.frametype == GUITK.ELEMENT_FRAME:
            if self.style is not None:
                self.element = ttk.Frame(
                    parent,
                    width=self.width,
                    height=self.height,
                    borderwidth=self.borderwidth,
                    style=self.style,
                )
            else:
                self.element = ttk.Frame(
                    parent,
                    width=self.width,
                    borderwidth=self.borderwidth,
                    height=self.height,
                )
        else:
            if self.style is not None:
                self.element = ttk.LabelFrame(
                    parent,
                    text=self.text,
                    width=self.width,
                    height=self.height,
                    style=self.style,
                    labelanchor=self.labelanchor,
                    borderwidth=self.borderwidth,
                )
            else:
                self.element = ttk.LabelFrame(
                    parent,
                    text=self.text,
                    width=self.width,
                    height=self.height,
                    labelanchor=self.labelanchor,
                    borderwidth=self.borderwidth,
                )

        if self.padding is not None:
            self.element["padding"] = self.padding
        if self.relief is not None:
            self.element["relief"] = self.relief
        if self.borderwidth is not None:
            self.element["borderwidth"] = self.borderwidth

        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        if self.layout:
            self._layout(self.element, self.window, autoframe=self._autoframe)

        if self.width or self.height:
            self.element.grid_propagate(0)

        if self.disabled:
            self.element.state(["disabled"])
        return self.element

    @property
    def frame(self):
        """Return the Tk frame element"""
        return self.element

    @property
    def value(self):
        pass

    @value.setter
    def value(self, value):
        pass


class Frame(_Frame):
    def __init__(
        self,
        layout=None,
        key=None,
        width=None,
        height=None,
        style=None,
        borderwidth=None,
        padding=None,
        relief=None,
        disabled=False,
        rowspan=None,
        columnspan=None,
        sticky=None,
        tooltip=None,
        autoframe=True,
    ):
        super().__init__(
            frametype=GUITK.ELEMENT_FRAME,
            key=key,
            width=width,
            height=height,
            layout=layout,
            style=style,
            borderwidth=borderwidth,
            padding=padding,
            relief=relief,
            disabled=disabled,
            rowspan=rowspan,
            columnspan=columnspan,
            sticky=sticky,
            tooltip=tooltip,
            autoframe=autoframe,
        )


class LabelFrame(_Frame):
    def __init__(
        self,
        text=None,
        layout=None,
        key=None,
        labelanchor=None,
        width=None,
        height=None,
        style=None,
        borderwidth=None,
        padding=None,
        relief=None,
        disabled=False,
        rowspan=None,
        columnspan=None,
        sticky=None,
        tooltip=None,
        autoframe=True,
    ):
        super().__init__(
            frametype=GUITK.ELEMENT_LABEL_FRAME,
            key=key,
            text=text,
            width=width,
            height=height,
            layout=layout,
            style=style,
            borderwidth=borderwidth,
            padding=padding,
            relief=relief,
            disabled=disabled,
            rowspan=rowspan,
            columnspan=columnspan,
            labelanchor=labelanchor,
            sticky=sticky,
            tooltip=tooltip,
            autoframe=autoframe,
        )
