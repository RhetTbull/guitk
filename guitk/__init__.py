""" Set of classes to simplify building a GUI app with tkinter
    Inspired by PySimpleGUI but built in a cleanroom manner (did not use PySimpleGUI code)

    No dependencies outside python standard library.

    Published under the MIT License.

    Copyright Rhet Turnbull, 2020, all rights reserved.
"""

# TODO: add Column?
# TODO: add way to specify tooltip delay

import time
import tkinter as tk
from tkinter import filedialog, font, ttk
from typing import List, Optional

from .constants import GUITK, EventType
from .redirect import StdErrRedirect, StdOutRedirect
from .tooltips import Hovertip


def _map_key_binding_from_shortcut(shortcut):
    """Return a keybinding sequence given a menu command shortcut """
    if not shortcut:
        return None
    keys = shortcut.split("+")

    key_mappings = {"Cmd": "Command", "Ctrl": "Control"}
    keybinding = []
    for k in keys:
        if k in key_mappings:
            keybinding.append(key_mappings[k])
        else:
            if len(k) == 1 and ord("A") <= ord(k) <= ord("Z"):
                k = k.lower()
            keybinding.append(k)
    return "<" + "-".join(keybinding) + ">"


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
        if not self.first_window:
            self.first_window = True
        self.windows[window] = 1

    def deregister(self, window):
        """De-register a new child window
           Once all children are de-registered, the root Tk object is destroyed
        """
        try:
            del self.windows[window]
        except KeyError:
            pass
        if self.first_window and not self.windows:
            # last window
            self.root.destroy()

    def get_children(self, window):
        """Return child windows of parent window"""
        return [w for w in self.windows if w._parent == window.window]

    def run_mainloop(self):
        if not self.mainloop_is_running:
            self.root.mainloop()


class WindowBaseClass:
    # only needed to keep typing happy
    pass


class Layout:
    """Mixin class to provide layout"""

    layout = []

    def __init__(self, *args, **kwargs):
        pass

    def _layout(self, parent, window: WindowBaseClass, autoframe):
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
                    widget.key or f"{widget.widget_type},{row_count},{col_count}"
                )
                widget._create_widget(
                    parent, window, row_count + row_offset, col_count + col_offset
                )
                widget._tooltip = (
                    Hovertip(widget.widget, widget.tooltip) if widget.tooltip else None
                )
                window._widgets.append(widget)
                widget.parent = self
                window._widget_by_key[widget.key] = widget
                if widget.rowspan and widget.rowspan > 1:
                    row_offset += widget.rowspan - 1
                if widget.columnspan and widget.columnspan > 1:
                    col_offset += widget.columnspan - 1


class Menu:
    def __init__(self, label, underline=None) -> None:
        self._label = label
        self._menu = None
        self._underline = underline
        self.window = None

    def _create_widget(self, parent, window: WindowBaseClass):
        self.window = window
        menu = tk.Menu(parent)
        if self._underline is None:
            idx = self._label.find("&")
            if idx != -1:
                self._label = self._label.replace("&", "", 1)
                self._underline = idx
        parent.add_cascade(menu=menu, label=self._label, underline=self._underline)
        self._menu = menu


class Command(Menu):
    def __init__(self, label, disabled=False, shortcut=None):
        self._label = label
        self._disabled = disabled
        self._shortcut = shortcut
        self._parent = None
        self._key = None

    def _create_widget(self, parent, window: WindowBaseClass, path):
        self._parent = parent
        self.window = window
        self._key = path
        callback = (
            self.window._make_callback(
                Event(self, self.window, self._key, "MENU_COMMAND")
            ),
        )
        parent.add_command(
            label=self._label,
            command=self.window._make_callback(
                Event(self, self.window, self._key, "MENU_COMMAND")
            ),
            accelerator=self._shortcut,
        )
        key_binding = _map_key_binding_from_shortcut(self._shortcut)
        window.window.bind_all(
            key_binding,
            self.window._make_callback(
                Event(self, self.window, self._key, "MENU_COMMAND")
            ),
        )


class Window(Layout, WindowBaseClass):
    """Basic Window class from which all windows are derived
    
    Notes:
        Classes which inherit from window should implement handle_event, setup, and teardown as needed
    """

    title = "My Window"
    """Title to display in the window's title bar """

    layout = []
    """Every class that inherits from Window must define it's own class level layout """

    menu = {}
    """ Optionally provide a menu """

    padx = 5
    pady = 5
    """Default padding around widgets """

    def __init__(
        self,
        title=None,
        parent=None,
        padx=None,
        pady=None,
        topmost=None,
        autoframe=True,
    ):
        self.title = title or self.title
        self.padx = padx or self.padx
        self.pady = pady or self.pady

        self._id = id(self)
        self._tk = TKRoot()
        self._parent = self._tk.root if not parent else parent
        self._topmost = topmost

        self.window = tk.Toplevel(self._parent)
        self.window.title(self.title)
        self._widgets = []
        self._widget_by_key = {}

        self._timer_events = {}
        """ timer events that have been set by bind_timer_event, stores most recent after() id for event"""

        self._return_value = None
        """ value returned from run() if set in quit() """

        self._root_menu = None
        """ will hold root tk.Menu widget"""

        self.mainframe = ttk.Frame(self.window, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)

        self._tk.register(self)
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

        # apply padding, widget padding takes precedent over window
        for widget in self._widgets:
            padx = widget.padx or self.padx
            pady = widget.pady or self.pady
            widget.widget.grid_configure(padx=padx, pady=pady)

        if self.menu:
            self._build_menu()

        if self._topmost:
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
            self.root.event_generate(event_name)
            if repeat:
                self._timer_events[timer_id] = self._tk.root.after(
                    delay, _generate_event
                )

        event = Event(self, self, event_name, EventType.VIRTUAL_EVENT)
        self.root.bind(event_name, self._make_callback(event))
        self._timer_events[timer_id] = self._tk.root.after(delay, _generate_event)
        return timer_id

    def cancel_timer_event(self, timer_id):
        """ Cancel a timer event created with bind_timer_event """
        try:
            after_id = self._timer_events[timer_id]
            self.root.after_cancel(after_id)
        except Exception:
            pass

    def run(self):
        self._tk.run_mainloop()
        return self._return_value

    @property
    def root(self):
        """Return Tk root instance """
        return self._tk.root

    def children(self):
        """ Return child windows """
        return self._tk.get_children(self)

    def _add_menus(self, menu: Menu, menu_items, path=None):
        path = f"MENU:{menu._label}" if path is None else path
        for m in menu_items:
            if type(m) == dict:
                # submenu
                for subm in m:
                    subm._create_widget(menu._menu, self)
                    subpath = f"{path}|{subm._label}"
                    self._add_menus(subm, m[subm], subpath)
            elif isinstance(m, Command):
                command_path = f"{path}|{m._label}"
                m._create_widget(menu._menu, self, command_path)

    def _build_menu(self):
        if type(self.menu) != dict:
            raise ValueError("self.menu must be a dict")

        if self._root_menu is None:
            # create the root menu
            self.root.option_add("*tearOff", tk.FALSE)
            self._root_menu = tk.Menu(self.root)
            self.window["menu"] = self._root_menu

        for m in self.menu:
            if not isinstance(m, Menu):
                raise ValueError("self.menu keys must be Menu objects")
            m._create_widget(self._root_menu, self)
            self._add_menus(m, self.menu[m])

    def _destroy(self):
        # kill any child windows
        for child in self.children():
            child._destroy()

        # disable any stdout/stderr redirection
        for widget in self._widgets:
            if type(widget) == Output:
                widget.disable_redirect()
        self.teardown()
        self.window.destroy()
        self._tk.deregister(self)

    def _make_callback(self, event):
        def _callback(*arg):
            if arg:
                event.event = arg[0]
            self._handle_event(event)

        return _callback

    def _handle_event(self, event):
        # only handle events if widget has events=True; Window objects always get events
        if isinstance(event.widget, Widget) and not event.widget.events:
            return

        event.values = {
            elem.key: elem.value for elem in self._widgets if type(elem) != Output
        }

        # filter events for this window
        if event.id == self._id:
            self.handle_event(event)

            # if deleting the window, call call _destroy after handle_event has had a chance to handle it
            if event.event_type == "WM_WINDOW_DELETE":
                self._destroy()

    def __getitem__(self, key):
        try:
            return self._widget_by_key[key]
        except KeyError:
            return None


class Event:
    """Event that occurred and values for widgets in the window """

    def __init__(self, widget: object, window: Window, key, event_type):
        self.id = id(window)
        self.widget = widget
        self.key = key
        self.event_type = event_type
        self.event = None  # placeholder for Tk event
        self.values = {}

    def __str__(self):
        return f"id={self.id}, widget={self.widget}, key={self.key}, event_type={self.event_type}, event={self.event}, values={self.values}"


class Widget:
    """Basic abstract base class for all tk widget"""

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
        cursor=None,
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
        self.cursor = cursor

        self.widget_type = None
        self._tk = TKRoot()
        self.widget = None
        self._value = tk.StringVar()

        # get set by _create_widget in inherited classes
        self._parent = None
        self.window = None

    @property
    def value(self):
        return self._value.get()

    @value.setter
    def value(self, value):
        self._value.set(value)

    def _grid(self, row, column, rowspan, columnspan):
        sticky = self.sticky or tk.W
        self.widget.grid(
            row=row,
            column=column,
            columnspan=columnspan,
            rowspan=rowspan,
            sticky=sticky,
        )

        if self.padx is not None or self.pady is not None:
            self.widget.grid_configure(padx=self.padx, pady=self.pady)

    def bind_event(self, event_name):
        """Bind a tkinter event to widget; will result in an Event of event_type type being sent to handle_event when triggered"""
        event = Event(self, self, self.key, event_name)
        self.widget.bind(event_name, self.window._make_callback(event))


class Entry(Widget):
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
        cursor=None,
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
        )
        self.widget_type = "ttk.Entry"
        default = default or ""
        self._value.set(default)
        self.key = key or "Entry"
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.width = width

    def _create_widget(self, parent, window: Window, row, col):
        self.window = window
        self._parent = parent
        self.widget = ttk.Entry(
            parent, textvariable=self._value, width=self.width, cursor=self.cursor
        )
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        event = Event(self, window, self.key, "<KeyRelease>")
        self.widget.bind("<KeyRelease>", window._make_callback(event))

        if self.disabled:
            self.widget.state(["disabled"])
        return self.widget

    @property
    def entry(self):
        """Return the Tk entry widget"""
        return self.widget


class Label(Widget):
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
        cursor=None,
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
            cursor=cursor,
        )
        self.widget_type = "ttk.Label"
        self.text = text
        self.key = key or text
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.width = width

    def _create_widget(self, parent, window: Window, row, col):
        self.window = window
        self._parent = parent
        self.widget = ttk.Label(
            parent,
            text=self.text,
            width=self.width,
            anchor=self.anchor,
            cursor=self.cursor,
        )
        self.widget["textvariable"] = self._value
        self._value.set(self.text)
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )
        if self.disabled:
            self.widget.state(["disabled"])
        return self.widget

    @property
    def label(self):
        """Return the Tk label widget"""
        return self.widget


class LinkLabel(Label):
    """Link label that responds to click """

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
        cursor=None,
        underline_font=False,
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
            anchor=anchor,
            cursor=cursor or "hand1",
        )
        self.widget_type = "guitk.LinkLabel"
        self.text = text
        self.key = key or text
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.width = width
        self.underline_font = underline_font

    def _create_widget(self, parent, window: Window, row, col):
        super()._create_widget(parent, window, row, col)
        event = Event(self.widget, window, self.key, EventType.LINK_LABEL_CLICKED)
        self.widget.bind("<Button-1>", window._make_callback(event))
        if self.underline_font:
            f = font.Font(self.widget, self.widget.cget("font"))
            f.configure(underline=True)
            self.widget.configure(font=f)


class Button(Widget):
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
        self.widget_type = "ttk.Button"
        self.text = text
        self.key = key or text
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.tooltip = tooltip

    @property
    def value(self):
        return self.widget["text"]

    @value.setter
    def value(self, text):
        self.widget["text"] = text

    def _create_widget(self, parent, window: Window, row, col):
        self.window = window
        self._parent = parent
        event = Event(self, window, self.key, EventType.BUTTON_PRESS)
        self.widget = ttk.Button(
            parent,
            text=self.text,
            anchor=self.anchor,
            command=window._make_callback(event),
        )
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )
        if self.disabled:
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

    def _create_widget(self, parent, window: Window, row, col):
        self.window = window
        self._parent = parent
        self.widget = ttk.Button(
            parent, text=self.text, anchor=self.anchor, command=self.browse_dialog
        )
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )
        if self.disabled:
            self.widget.state(["disabled"])

        return self.widget

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
        self.widget_type = "guitk.BrowseDirectoryButton"
        self._dirname = None

    def _create_widget(self, parent, window: Window, row, col):
        self.window = window
        self._parent = parent
        self.widget = ttk.Button(
            parent, text=self.text, anchor=self.anchor, command=self.browse_dialog
        )
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )
        if self.disabled:
            self.widget.state(["disabled"])

        return self.widget

    @property
    def directory(self):
        return self._dirname

    def browse_dialog(self):
        self._dirname = filedialog.askdirectory()
        if self.target_key:
            self.window[self.target_key].value = self._dirname
        event = Event(self, self.window, self.key, EventType.BROWSE_DIRECTORY)
        self.window._handle_event(event)


class CheckButton(Widget):
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
        self.widget_type = "ttk.CheckButton"
        self.text = text
        self.key = key or text
        self.columnspan = columnspan
        self.rowspan = rowspan
        self._value = tk.BooleanVar()

    def _create_widget(self, parent, window: Window, row, col):
        self.window = window
        self._parent = parent
        event = Event(self, window, self.key, EventType.CHECK_BUTTON)
        self.widget = ttk.Checkbutton(
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
            self.widget.state(["disabled"])
        return self.widget

    @property
    def checkbutton(self):
        """Return the Tk checkbutton widget"""
        return self.widget


class Text(Widget):
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
        self.widget_type = "tk.Text"
        self.key = key or "Text"
        self.width = width
        self.height = height
        self._value = text or ""
        self.columnspan = columnspan
        self.rowspan = rowspan

    def _create_widget(self, parent, window: Window, row, col):
        self.window = window
        self._parent = parent
        self.widget = tk.Text(parent, width=self.width, height=self.height)
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        event = Event(self, window, self.key, "<KeyRelease>")
        self.widget.bind("<KeyRelease>", window._make_callback(event))

        if self.disabled:
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
        self.widget_type = "guitk.ScrolledText"
        self.key = key or "ScrolledText"
        self.width = width
        self.height = height
        self._value = text if text is not None else ""
        self.columnspan = columnspan
        self.rowspan = rowspan

    def _create_widget(self, parent, window: Window, row, col):
        self.window = window
        self._parent = parent
        self.widget = _ttkScrolledText(parent, width=self.width, height=self.height)
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        event = Event(self, window, self.key, "<KeyRelease>")
        self.widget.bind("<KeyRelease>", window._make_callback(event))

        if self.disabled:
            self.widget["state"] = "disabled"

        self.value = self._value

        return self.widget

    @property
    def value(self):
        return self.widget.get("1.0", tk.END).rstrip()

    @value.setter
    def value(self, text):
        self.widget.delete("1.0", tk.END)
        self.widget.insert("1.0", text)
        self.widget.yview(tk.END)


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

    def _create_widget(self, parent, window: Window, row, col):
        super()._create_widget(parent, window, row, col)
        self.enable_redirect()
        self.widget.unbind("<KeyRelease>")
        return self.widget

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


class _Frame(Widget, Layout):
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
        self.widget_type = (
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

    def _create_widget(self, parent, window: Window, row, col):
        self.window = window
        self._parent = parent

        if self.frametype == GUITK.ELEMENT_FRAME:
            if self.style is not None:
                self.widget = ttk.Frame(
                    parent,
                    width=self.width,
                    height=self.height,
                    borderwidth=self.borderwidth,
                    style=self.style,
                )
            else:
                self.widget = ttk.Frame(
                    parent,
                    width=self.width,
                    borderwidth=self.borderwidth,
                    height=self.height,
                )
        else:
            if self.style is not None:
                self.widget = ttk.LabelFrame(
                    parent,
                    text=self.text,
                    width=self.width,
                    height=self.height,
                    style=self.style,
                    labelanchor=self.labelanchor,
                    borderwidth=self.borderwidth,
                )
            else:
                self.widget = ttk.LabelFrame(
                    parent,
                    text=self.text,
                    width=self.width,
                    height=self.height,
                    labelanchor=self.labelanchor,
                    borderwidth=self.borderwidth,
                )

        if self.padding is not None:
            self.widget["padding"] = self.padding
        if self.relief is not None:
            self.widget["relief"] = self.relief
        if self.borderwidth is not None:
            self.widget["borderwidth"] = self.borderwidth

        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        if self.layout:
            self._layout(self.widget, self.window, autoframe=self._autoframe)

        if self.width or self.height:
            self.widget.grid_propagate(0)

        if self.disabled:
            self.widget.state(["disabled"])
        return self.widget

    @property
    def frame(self):
        """Return the Tk frame widget"""
        return self.widget

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


# TODO: for ListView, set tree.column("#0", width=0) and show="tree"
class TreeView(Widget):
    def __init__(
        self,
        key=None,
        headings: Optional[List] = None,
        columns: Optional[List] = None,
        cursor=None,
        displaycolumns=None,
        height=None,
        padding=None,
        selectmode=None,
        show=None,
        style=None,
        takefocus=None,
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
            cursor=cursor,
        )
        """ columns is optional, if not provided, will use headings for column names """
        self.key = key or "TreeView"
        self.widget_type = "ttk.TreeView"

        if headings and columns:
            # ensure heading provided for each column
            if len(headings) != len(columns):
                raise ValueError("headings and columns lists must be the same length")

        self._headings = headings

        # ttk.Treeview arguments
        self._columns = tuple(columns) if columns is not None else tuple(headings)
        self._displaycolumns = displaycolumns
        self._height = height
        self._padding = padding
        self._selectmode = selectmode
        self._show = show
        self._style = style
        self._takefocus = takefocus
        self._cursor = cursor

        self.disabled = disabled
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.padx = padx
        self.pady = pady
        self.events = events
        self.sticky = sticky or ""
        self.tooltip = tooltip
        self.anchor = anchor

    def _create_widget(self, parent, window: Window, row, col):
        self.window = window
        self._parent = parent

        # build arg list for Treeview()
        kwargs = {}
        for kw in [
            "columns",
            "cursor",
            "displaycolumns",
            "height",
            "padding",
            "selectmode",
            "show",
            "style",
            "takefocus",
        ]:
            val = getattr(self, f"_{kw}")
            if val is not None:
                kwargs[kw] = val

        self.widget = ttk.Treeview(parent, **kwargs)

        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        # set column headings
        if self._headings:
            for column, heading in zip(self._columns, self._headings):
                self.widget.heading(column, text=heading)

        if self.disabled:
            self.widget.state(["disabled"])

        event = Event(self, window, self.key, "<<TreeviewSelect>>")
        self.widget.bind("<<TreeviewSelect>>", window._make_callback(event))

        return self.widget

    @property
    def value(self):
        return self.tree.selection()

    @value.setter
    def value(self, *values):
        self.tree.selection_set(*values)

    def bind_heading(self, column_name, event_name):
        """Bind event to click on column heading """
        event = Event(self, self.window, event_name, EventType.TREEVIEW_HEADING)
        self.tree.heading(column_name, command=self.window._make_callback(event))

    def bind_tag(self, tagname, event_name, sequence=None):
        """Bind event to item with tag when sequence occurs
           If sequence is None, will bind to <Button-1>"""
        if sequence is None:
            sequence = "<Button-1>"
        event = Event(self, self.window, event_name, EventType.TREEVIEW_TAG)
        self.tree.tag_bind(
            tagname, sequence=sequence, callback=self.window._make_callback(event)
        )

    def sort_on_column(self, column_name, key=None, reverse=False):
        """ sort the tree view contents based on column_name
            optional key same as sort(key=)
        """
        values = [
            (self.tree.set(k, column_name), k) for k in self.tree.get_children("")
        ]
        values.sort(key=key, reverse=reverse)
        for index, (val, k) in enumerate(values):
            self.tree.move(k, "", index)

    @property
    def tree(self):
        """Return the ttk Treeview widget"""
        return self.widget
