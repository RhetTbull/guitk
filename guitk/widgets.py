""" Window, Layout, and Widget classes """

import pathlib
import time
import tkinter as tk
from collections import namedtuple
from tkinter import filedialog, font, ttk
from typing import Any, Callable, List, Optional, Union

from .constants import GUITK, EventType
from .redirect import StdErrRedirect, StdOutRedirect
from .tkroot import _TKRoot
from .tooltips import Hovertip

EventCommand = namedtuple("EventCommand", ["widget", "key", "event_type", "command"])


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
        kw.update({"yscrollcommand": widget.vbar.set})

    widget.hbar = None
    if hscrollbar:
        widget.hbar = ttk.Scrollbar(frame, orient=tk.HORIZONTAL)
        widget.hbar.grid(column=0, row=1, sticky="EW")
        # hbar.pack(side=tk.BOTTOM, fill=tk.X)
        kw.update({"xscrollcommand": widget.hbar.set})

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


def _map_key_binding_from_shortcut(shortcut):
    """Return a keybinding sequence given a menu command shortcut"""
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


def _interval(from_, to, interval, value, tolerance=1e-9):
    """clamp value to an interval between from_ and to range"""

    if interval > (to - from_):
        raise ValueError("Invalid increment")

    if value < from_ or value > to:
        raise ValueError("Invalid value")

    if abs(value - from_) < tolerance or abs(value - to) < tolerance:
        return value

    quotient, remainder = divmod(value, interval)
    if remainder < tolerance:
        return quotient * interval

    half_increment = interval / 2
    if remainder > half_increment:
        return interval * (quotient + 1)
    else:
        return interval * quotient


def _get_docstring(name):
    """Return the docstring of an object with name"""
    try:
        obj = globals()[name]
    except KeyError:
        raise ValueError("Invalid object name")
    return obj.__doc__ or ""


class _WindowBaseClass:
    # only needed to keep typing happy
    pass


class _Layout:
    """Mixin class to provide layout"""

    layout = []

    def __init__(self, *args, **kwargs):
        pass

    def _layout(self, parent, window: _WindowBaseClass, autoframe):
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
                tooltip = widget.tooltip or window.tooltip
                if tooltip:
                    _tooltip = tooltip(widget.key) if callable(tooltip) else tooltip
                    widget._tooltip = (
                        Hovertip(widget.widget, _tooltip) if _tooltip else None
                    )
                else:
                    widget._tooltip = None

                window._widgets.append(widget)
                widget.parent = self
                window._widget_by_key[widget.key] = widget
                if widget.rowspan and widget.rowspan > 1:
                    row_offset += widget.rowspan - 1
                if widget.columnspan and widget.columnspan > 1:
                    col_offset += widget.columnspan - 1


class Menu:
    def __init__(
        self,
        label: str,
        underline: Optional[bool] = None,
        separator: Optional[bool] = False,
    ) -> None:
        """[summary]

        Parameters
        ----------
        label : str
            [description]
        underline : Optional[bool], optional
            [description], by default None
        separator : Optional[bool], optional
            [description], by default False
        """
        self._label = label
        self._menu = None
        self._underline = underline
        self._separator = separator
        self.window = None

    def _create_widget(self, parent, window: _WindowBaseClass):
        self.window = window
        menu = tk.Menu(parent)
        if self._underline is None:
            idx = self._label.find("&")
            if idx != -1:
                self._label = self._label.replace("&", "", 1)
                self._underline = idx
        parent.add_cascade(menu=menu, label=self._label, underline=self._underline)

        if self._separator:
            parent.add_separator()

        self._menu = menu


class Command(Menu):
    def __init__(
        self,
        label: str,
        separator: Optional[bool] = False,
        disabled: Optional[bool] = False,
        shortcut: Optional[str] = None,
        key: Optional[str] = None,
        command: Optional[Callable] = None,
    ):
        self._label = label
        self._separator = separator  # add separator line after this command
        self._disabled = disabled
        self._shortcut = shortcut
        self._parent = None
        self._key = key
        self._command = command

    def _create_widget(self, parent, window: _WindowBaseClass, path):
        self._parent = parent
        self.window = window
        self._key = self._key or path
        callback = (
            self.window._make_callback(
                Event(self, self.window, self._key, EventType.MenuCommand)
            ),
        )
        parent.add_command(
            label=self._label,
            command=self.window._make_callback(
                Event(self, self.window, self._key, EventType.MenuCommand)
            ),
            accelerator=self._shortcut,
        )

        if self._command:
            self.window.bind_command(
                key=self._key, event_type=EventType.MenuCommand, command=self._command
            )

        if self._separator:
            parent.add_separator()

        key_binding = _map_key_binding_from_shortcut(self._shortcut)
        window.window.bind_all(
            key_binding,
            self.window._make_callback(
                Event(self, self.window, self._key, EventType.MenuCommand)
            ),
        )


# Place Widget before Window in the file so pylance is happy with type hints on __getitem__
class Widget:
    """Basic abstract base class for all tk widgets"""

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
        takefocus=None,
        command=None,
        value_type=None,
    ):
        self.key = key
        self._disabled = disabled
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.padx = padx
        self.pady = pady
        self.events = events
        self.sticky = sticky or ""
        self.tooltip = tooltip
        self.anchor = anchor
        self.cursor = cursor
        if takefocus is not None:
            self.takefocus = 1 if takefocus else 0
        else:
            self.takefocus = None

        self._command = command
        self._commands = {}

        self.widget_type = None
        self._tk = _TKRoot()
        self.widget = None
        self._value = value_type() if value_type is not None else tk.StringVar()

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

    def bind_event(self, event_name, command=None):
        """Bind a tkinter event to widget; will result in an Event of event_type type being sent to handle_event when triggered.
        Optionally bind command to the event"""
        event = Event(self, self.window, self.key, event_name)
        self.widget.bind(event_name, self.window._make_callback(event))

        if command:
            self.window._bind_command(
                EventCommand(
                    widget=self, key=self.key, event_type=event_name, command=command
                )
            )

    @property
    def state(self):
        return self.widget["state"]

    @property
    def disabled(self):
        return self.widget["state"] == "disabled"

    @disabled.setter
    def disabled(self, value):
        self.widget["state"] = "disabled" if value else "normal"


class Window(_Layout, _WindowBaseClass):
    """Basic Window class from which all windows are derived

    Notes:
        Classes which inherit from window should implement handle_event, setup, and teardown as needed
    """

    def __init__(
        self,
        parent=None,
        title=None,
        padx=None,
        pady=None,
        topmost=None,
        autoframe=True,
        theme=None,
        tooltip=None,
        modal=None,
    ):
        # call _config then subclass's config to initialize
        # layout, title, menu, etc.

        self._config()
        self.config()

        # override any layout defaults from constructor
        self.title = title if title is not None else self.title
        self.padx = padx if padx is not None else self.padx
        self.pady = pady if pady is not None else self.pady
        self.theme = theme if theme is not None else self.theme
        self.tooltip = tooltip if tooltip is not None else self.tooltip
        self.modal = modal if modal is not None else self.modal

        self._id = id(self)
        self._tk = _TKRoot()
        self._parent = self._tk.root if not parent else parent
        self._topmost = topmost

        self.window = tk.Toplevel(self._parent)
        self.window.title(self.title)
        self._widgets = []
        self._widget_by_key = {}

        self._timer_events = {}
        """ timer events that have been set by bind_timer_event, stores most recent after() id for event"""

        self._timer_events_cancelled = {}
        """ timer events that have been set by bind_timer_event but then cancelled """

        self._return_value = None
        """ value returned from run() if set in quit() """

        self._root_menu = None
        """ will hold root tk.Menu widget"""

        self._radiobuttons = {}
        """ will hold group name/variable for radio buttons in the window """

        self._mainframe = ttk.Frame(self.window, padding="3 3 12 12")
        self._mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)

        self._tk.register(self)
        self.window.protocol(
            "WM_DELETE_WINDOW",
            self._make_callback(Event(self, self, EventType.Quit, EventType.Quit)),
        )

        if not self.layout:
            self.layout = [
                [
                    Label(
                        "Looks like you forgot to include a layout in your class definition"
                    )
                ]
            ]

        self._commands = []
        self._layout(self._mainframe, self, autoframe=autoframe)

        # apply theme if necessary
        if self.theme is not None:
            self._tk.theme = self.theme

        # apply padding, widget padding takes precedent over window
        for widget in self._widgets:
            padx = widget.padx or self.padx
            pady = widget.pady or self.pady
            widget.widget.grid_configure(padx=padx, pady=pady)

        if self.menu:
            self._build_menu()

        if self._topmost or self.modal:
            self.window.attributes("-topmost", 1)

        if self.modal:
            windowingsystem = self.root.call("tk", "windowingsystem")
            if windowingsystem == "aqua":
                try:
                    self.root.call(
                        "::tk::unsupported::MacWindowStyle",
                        "style",
                        self._w,
                        "moveableModal",
                        "",
                    )
                except:
                    pass

            if self._parent is not None and self._parent.winfo_viewable():
                self.window.transient(self._parent)
            self.window.wait_visibility()
            self.window.grab_set()

        # TODO: add geometry code to ensure window appears in good spot relative to parent

        self.events = True

        self.setup()

        if self.modal:
            self.window.wait_window()

        self._bind_timer_event(
            100, EventType.WindowFinishedLoading.value, EventType.WindowFinishedLoading
        )

    def _config(self):
        self.title = "My Window"
        """Title to display in the window's title bar """

        self.layout = [
            [
                Label(
                    "Looks like you forgot to add self.layout to your config() method."
                )
            ],
            [Button("Quit")],
        ]
        """Every class that inherits from Window must define it's own layout """

        self.menu = {}
        """ Optionally provide a menu """

        self.padx = 5
        self.pady = 5
        """Default padding around widgets """

        self.theme = None
        """The ttk theme to use, if None, uses ttk default"""

        self.tooltip = None
        """ A callable which returns the tooltip text for a given key or a str """

        self.modal = False
        """ Set to True to create modal window """

    def config(self):
        pass

    def handle_event(self, event):
        """Handle event objects, inheriting classes should implement handle_event"""
        if event.event_type == EventType.Quit:
            self.quit(self._return_value)

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
        """Close the window"""
        self._return_value = return_value
        self._destroy()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    def bind_command(self, key=None, event_type=None, command=None):
        if not any([key, event_type]):
            raise ValueError("At least one of key, event_type must be specified")
        self._bind_command(
            EventCommand(widget=None, key=key, event_type=event_type, command=command)
        )

    def _bind_command(self, event_command: EventCommand):
        self._commands.append(event_command)

    def bind_timer_event(self, delay, event_name, repeat=False, command=None):
        """Create a new virtual event `event_name` that fires after `delay` ms,
        repeats every `delay` ms if repeat=True, otherwise fires once"""
        if command:
            self.bind_command(
                key=event_name, event_type=EventType.VirtualEvent, command=command
            )
        return self._bind_timer_event(delay, event_name, EventType.VirtualEvent, repeat)

    def _bind_timer_event(self, delay, event_name, event_type, repeat=False):
        # create a unique name for the timer
        timer_id = f"{event_name}_{time.time_ns()}"

        # callback that generates event and respawns the timer if repeat=True
        # when cancelling with cancel_timer_event, sometimes the call to after_cancel doesn't apparently work so check
        # if timer_id is in _timer_events_cancelled before respawning
        def _generate_event():
            self.root.event_generate(event_name)
            if repeat and timer_id not in self._timer_events_cancelled:
                self._timer_events[timer_id] = self._tk.root.after(
                    delay, _generate_event
                )

        event = Event(self, self, event_name, event_type)
        self.root.bind(event_name, self._make_callback(event))
        self._timer_events[timer_id] = self._tk.root.after(delay, _generate_event)
        return timer_id

    def cancel_timer_event(self, timer_id):
        """Cancel a timer event created with bind_timer_event"""
        try:
            after_id = self._timer_events[timer_id]
            self.root.after_cancel(after_id)
            self._timer_events.pop(timer_id)
            self._timer_events_cancelled[timer_id] = after_id
        except KeyError:
            raise ValueError(f"Timer event {timer_id} not found")
        except Exception as e:
            raise e

    def run(self):
        self._tk.run_mainloop()
        return self._return_value

    @property
    def root(self):
        """Return Tk root instance"""
        return self._tk.root

    def children(self):
        """Return child windows"""
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
            event = Event(child, child.window, EventType.Quit, EventType.Quit)
            child.handle_event(event)
            try:
                child._destroy()
            except Exception:
                pass

        # disable event processing in _handle_event
        self.events = False

        # disable any stdout/stderr redirection and event handling
        for widget in self._widgets:
            widget.events = False
            if type(widget) == Output:
                widget.disable_redirect()

        if self.modal:
            self.window.grab_release()

        # cancel any timer events
        for timer_id in self._timer_events:
            try:
                after_id = self._timer_events[timer_id]
                self._tk.root.after_cancel(after_id)
            except Exception:
                pass

        self.teardown()
        self._parent.focus_set()
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
        if isinstance(event.widget, (Widget, Window)) and not event.widget.events:
            return

        # filter events for this window
        if event.id == self._id:
            # handle custom commands
            self._handle_commands(event)

            self.handle_event(event)

            # if deleting the window, call _destroy after handle_event has had a chance to handle it
            if event.event_type == EventType.Quit:
                self._destroy()

    def _handle_commands(self, event):
        for command in self._commands:
            if (
                (command.widget is None or command.widget == event.widget)
                and (command.key is None or command.key == event.key)
                and (
                    command.event_type is None or command.event_type == event.event_type
                )
            ):
                command.command()

    def __getitem__(self, key) -> Widget:
        try:
            return self._widget_by_key[key]
        except KeyError:
            raise KeyError(f"Invalid key: no widget with key {key}")


class Event:
    """Event that occurred and values for widgets in the window"""

    def __init__(self, widget: object, window: Window, key, event_type):
        self.id = id(window)
        self.widget = widget
        self.key = key
        self.event_type = event_type
        self.event = None  # placeholder for Tk event, will be set in _make_callback

    def __str__(self):
        return f"id={self.id}, widget={self.widget}, key={self.key}, event_type={self.event_type}, event={self.event}"


class Label(Widget):
    """Text label"""

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
        if self._disabled:
            self.widget.state(["disabled"])
        return self.widget

    @property
    def label(self):
        """Return the Tk label widget"""
        return self.widget


class _Frame(Widget, _Layout):
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
        elif self.style is not None:
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

        if self._disabled:
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

    def _create_widget(self, parent, window: Window, row, col):
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

    def _create_widget(self, parent, window: Window, row, col):
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

    def _create_widget(self, parent, window: Window, row, col):
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

    def _create_widget(self, parent, window: Window, row, col):
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


class LinkLabel(Label):
    """Link label that responds to click"""

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
        events=True,
        sticky=None,
        tooltip=None,
        anchor=None,
        cursor=None,
        underline_font=False,
        command=None,
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
        self._command = command

    def _create_widget(self, parent, window: Window, row, col):
        super()._create_widget(parent, window, row, col)
        event = Event(self, window, self.key, EventType.LinkLabel)
        self.widget.bind("<Button-1>", window._make_callback(event))
        if self.underline_font:
            f = font.Font(self.widget, self.widget.cget("font"))
            f.configure(underline=True)
            self.widget.configure(font=f)

        if self._command:
            self.events = True
            window._bind_command(
                EventCommand(
                    widget=self,
                    key=self.key,
                    event_type=EventType.LinkLabel,
                    command=self._command,
                )
            )


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

    def _create_widget(self, parent, window: Window, row, col):
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

    def _create_widget(self, parent, window: Window, row, col):
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


class Checkbutton(Widget):
    """Checkbox / checkbutton"""

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
            command=command,
        )
        self.widget_type = "ttk.Checkbutton"
        self.text = text
        self.key = key or text
        self.columnspan = columnspan
        self.rowspan = rowspan
        self._value = tk.BooleanVar()

    def _create_widget(self, parent, window: Window, row, col):
        self.window = window
        self._parent = parent
        event = Event(self, window, self.key, EventType.Checkbutton)
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

        if self._command:
            self.events = True
            window._bind_command(
                EventCommand(
                    widget=self,
                    key=self.key,
                    event_type=EventType.Checkbutton,
                    command=self._command,
                )
            )

        if self._disabled:
            self.widget.state(["disabled"])
        return self.widget

    @property
    def checkbutton(self):
        """Return the ttk.Checkbutton widget"""
        return self.widget


class Radiobutton(Widget):
    """Radiobutton class

    Note: group must be specified and will be used as key unless a separate key is specified."""

    def __init__(
        self,
        text: str,
        group: Any,
        key: str = "",
        value: Union[int, str, None] = None,
        disabled=False,
        rowspan=None,
        columnspan=None,
        padx=None,
        pady=None,
        events=True,
        sticky=None,
        tooltip=None,
        anchor=None,
        selected=False,
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
            command=command,
        )
        self.widget_type = "ttk.Radiobutton"
        self.text = text
        self.group = group
        self.key = key or group
        self._radiobutton_value = value if value is not None else text
        self._value = None  # will be set in _create_widget
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.selected = selected

    def _create_widget(self, parent, window: Window, row, col):
        self.window = window
        self._parent = parent

        # assign control variable or create it if necessary
        if self.group not in self.window._radiobuttons:
            # determine type of control variable based on value
            var_type = type(self._radiobutton_value)
            if var_type == int:
                self.window._radiobuttons[self.group] = tk.IntVar(
                    value=self._radiobutton_value
                )
            elif var_type == str:
                self.window._radiobuttons[self.group] = tk.StringVar(
                    value=self._radiobutton_value
                )
            else:
                # unsupported type
                raise ValueError("value must be str or int")

        self._value = self.window._radiobuttons[self.group]

        event = Event(self, window, self.key, EventType.Radiobutton)
        self.widget = ttk.Radiobutton(
            parent,
            text=self.text,
            anchor=self.anchor,
            command=window._make_callback(event),
            variable=self._value,
            value=self._radiobutton_value,
        )
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        if self._command:
            self.events = True
            window._bind_command(
                EventCommand(
                    widget=self,
                    key=self.key,
                    event_type=EventType.Radiobutton,
                    command=self._command,
                )
            )

        if self._disabled:
            self.widget.state(["disabled"])

        if self.selected:
            self.widget.state(["selected"])
        else:
            self.widget.state(["!selected"])

        return self.widget

    @property
    def radiobutton(self):
        """Return the ttk Radiobutton widget"""
        return self.widget


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

    def _create_widget(self, parent, window: Window, row, col):
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

    def _create_widget(self, parent, window: Window, row, col):
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


class Treeview(Widget):
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
        command=None,
        vscrollbar=False,
        hscrollbar=False,
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
            command=command,
        )
        """ columns is optional, if not provided, will use headings for column names """
        self.key = key or "Treeview"
        self.widget_type = "ttk.Treeview"

        if headings and columns and len(headings) != len(columns):
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

        self._disabled = disabled
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.padx = padx
        self.pady = pady
        self.events = events
        self.sticky = sticky or ""
        self.tooltip = tooltip
        self.anchor = anchor
        self.vscrollbar = vscrollbar
        self.hscrollbar = hscrollbar

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

        self.widget = scrolled_widget_factory(
            parent,
            ttk.Treeview,
            vscrollbar=self.vscrollbar,
            hscrollbar=self.hscrollbar,
            **kwargs,
        )
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        # set column headings
        if self._headings:
            for column, heading in zip(self._columns, self._headings):
                self.widget.heading(column, text=heading)

        if self._disabled:
            self.widget.state(["disabled"])

        event = Event(self, window, self.key, EventType.TreeviewSelect)
        self.widget.bind("<<TreeviewSelect>>", window._make_callback(event))

        if self._command:
            self.events = True
            window._bind_command(
                EventCommand(
                    widget=self,
                    key=self.key,
                    event_type=EventType.TreeviewSelect,
                    command=self._command,
                )
            )

        return self.widget

    @property
    def value(self):
        return self.tree.selection()

    @value.setter
    def value(self, *values):
        self.tree.selection_set(*values)

    def bind_heading(self, column_name, event_name, command=None):
        """Bind event to click on column heading"""
        event = Event(self, self.window, event_name, EventType.TreeviewHeading)
        self.tree.heading(column_name, command=self.window._make_callback(event))

        if command:
            self.window.bind_command(
                key=event.key, event_type=event.event_type, command=command
            )

    def bind_tag(self, tagname, event_name, sequence=None, command=None):
        """Bind event to item with tag when sequence occurs
        If sequence is None, will bind to <Button-1>"""
        if sequence is None:
            sequence = "<Button-1>"
        event = Event(self, self.window, event_name, EventType.TreeviewTag)
        self.tree.tag_bind(
            tagname, sequence=sequence, callback=self.window._make_callback(event)
        )

        if command:
            self.window.bind_command(
                key=event.key, event_type=event.event_type, command=command
            )

    def sort_on_column(self, column_name, key=None, reverse=False):
        """sort the tree view contents based on column_name
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


class Listbox(Treeview):
    def __init__(
        self,
        text: Optional[List] = None,
        key=None,
        cursor=None,
        height=None,
        width=None,
        padding=None,
        selectmode=None,
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
        command=None,
        vscrollbar=None,
        hscrollbar=None,
    ):
        self.key = key or "Listbox"
        self.widget_type = "guitk.Listbox"
        self._show = "tree"
        self._columns = ["list"]
        self._width = width

        if text and type(text) != list:
            raise ValueError("text must be a list of strings")
        self._text = text

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
            show=self._show,
            columns=self._columns,
            height=height,
            padding=padding,
            selectmode=selectmode,
            style=style,
            takefocus=takefocus,
            command=command,
            vscrollbar=vscrollbar,
            hscrollbar=hscrollbar,
        )

    def _create_widget(self, parent, window: Window, row, col):
        super()._create_widget(parent, window, row, col)
        self.tree.column("#0", width=0, minwidth=0)
        if self._width:
            self.tree.column("#1", width=self._width)

        self.listbox = self.tree
        if self._text:
            for line in self._text:
                self.append(line)

        event = Event(self, window, self.key, EventType.ListboxSelect)
        self.widget.bind("<<TreeviewSelect>>", window._make_callback(event))

        if self._command:
            self.events = True
            window._bind_command(
                EventCommand(
                    widget=self,
                    key=self.key,
                    event_type=EventType.ListboxSelect,
                    command=self._command,
                )
            )

    def insert(self, index, line):
        """Insert a line into Listbox"""
        self.widget.insert("", index, iid=line, values=(line))

    def append(self, line):
        """Apppend a line to end of Listbox"""
        self.widget.insert("", "end", iid=line, values=(line))

    def delete(self, line):
        """Delete a line from Listbox"""
        self.widget.delete(line)


class DebugWindow(Window):
    """Debug window that captures stdout/stderr"""

    def __init__(self, output_width=80, output_height=20, **kwargs):
        self._output_width = output_width
        self._output_height = output_height
        super().__init__(**kwargs)

    def config(self):
        self.title = "Debug"
        self.padx = self.pady = 2
        self.layout = [
            [
                Label("Filter"),
                Entry(key="FILTER_TEXT", width=40),
                Button("Filter", key="FILTER"),
            ],
            [
                Output(
                    width=self._output_width,
                    height=self._output_height,
                    key="OUTPUT",
                    events=True,
                )
            ],
        ]

    def handle_event(self, event):
        if event.key in ["FILTER", "OUTPUT"]:
            filter = self["FILTER_TEXT"].value
            if filter:
                lines = self["OUTPUT"].value.split("\n")
                lines = [l for l in lines if filter in l]
                self["OUTPUT"].value = "\n".join(lines) + "\n"


class Scale(Widget):
    """ttk.Scale / slider"""

    def __init__(
        self,
        from_=None,
        to=None,
        value=None,
        orient=tk.VERTICAL,
        interval=None,
        precision=None,
        key=None,
        target_key=None,
        disabled=False,
        columnspan=None,
        rowspan=None,
        padx=None,
        pady=None,
        length=None,
        events=True,
        sticky=None,
        tooltip=None,
        takefocus=None,
        command=None,
        cursor=None,
        style=None,
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
            anchor=None,
            takefocus=takefocus,
            command=command,
            value_type=tk.DoubleVar,
        )
        self.widget_type = "ttk.Scale"
        self.key = key or "Scale"
        self.target_key = target_key

        self._cursor = cursor
        self._from_ = from_
        self._to = to
        self._orient = orient
        self._interval = interval
        self._precision = precision
        self._style = style
        self._length = length
        self._initial_value = value
        self._takefocus = takefocus

        self.columnspan = columnspan
        self.rowspan = rowspan
        self.tooltip = tooltip

    @property
    def value(self):
        value = self.widget.get()
        if self._interval:
            value = _interval(self._from_, self._to, self._interval, value)
        if self._precision is not None:
            value = round(float(value), self._precision)
        return value

    @value.setter
    def value(self, value):
        self.widget.set(value)

    def _create_widget(self, parent, window: Window, row, col):
        self.window = window
        self._parent = parent
        event = Event(self, window, self.key, EventType.ScaleUpdate)

        # TODO: standardize attribute names
        kwargs = {}
        for kw in ["cursor", "takefocus", "from_", "to", "length", "orient", "style"]:
            val = getattr(self, f"_{kw}")
            if val is not None:
                kwargs[kw] = val

        kwargs["variable"] = self._value
        if self._initial_value is not None:
            self._value.set(self._initial_value)

        self.widget = ttk.Scale(parent, command=window._make_callback(event), **kwargs)
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        if self._command:
            self.events = True
            window._bind_command(
                EventCommand(
                    widget=self,
                    key=self.key,
                    event_type=EventType.ScaleUpdate,
                    command=self._command,
                )
            )

        if self.target_key is not None:
            self.events = True

            def update_target():
                self.window[self.target_key].value = self.value

            window._bind_command(
                EventCommand(
                    widget=self,
                    key=self.key,
                    event_type=EventType.ScaleUpdate,
                    command=update_target,
                )
            )

        if self._disabled:
            self.widget.state(["disabled"])

        return self.widget

    @property
    def scale(self):
        """Return the ttk.Scale widget"""
        return self.widget


class Progressbar(Widget):
    """ttk.Progressbar"""

    def __init__(
        self,
        value=None,
        key=None,
        orient=tk.HORIZONTAL,
        length=200,
        mode="determinate",
        maximum=100,
        disabled=False,
        columnspan=None,
        rowspan=None,
        padx=None,
        pady=None,
        sticky=None,
        tooltip=None,
        style=None,
        events=True,
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
            anchor=None,
            value_type=tk.DoubleVar,
        )
        self.widget_type = "ttk.Progressbar"
        self.key = key or "Progressbar"

        self.orient = orient
        self.length = length
        self.mode = mode
        self.maximum = maximum
        self.style = style
        self._initial_value = value

        self.columnspan = columnspan
        self.rowspan = rowspan
        self.tooltip = tooltip

    @property
    def value(self):
        return self.widget["value"]

    @value.setter
    def value(self, value):
        self._value.set(float(value))

    def _create_widget(self, parent, window: Window, row, col):
        self.window = window
        self._parent = parent

        kwargs = {}
        for kw in ["length", "orient", "mode", "maximum"]:
            val = getattr(self, kw)
            if val is not None:
                kwargs[kw] = val

        kwargs["variable"] = self._value
        if self._initial_value is not None:
            self._value.set(self._initial_value)

        self.widget = ttk.Progressbar(parent, **kwargs)
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        if self._disabled:
            self.widget.state(["disabled"])

        return self.widget

    @property
    def progressbar(self):
        """Return the ttk.Progressbar widget"""
        return self.widget

    def stop(self):
        self.widget.stop()


class Notebook(Widget, _Layout):
    """ttk.Notebook"""

    def __init__(
        self,
        key=None,
        tabs=None,
        disabled=False,
        columnspan=None,
        rowspan=None,
        padx=None,
        pady=None,
        sticky=None,
        tooltip=None,
        style=None,
        events=True,
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
            anchor=None,
            command=command,
        )
        self.widget_type = "ttk.Notebook"
        self.key = key or "Notebook"

        self.style = style

        self.columnspan = columnspan
        self.rowspan = rowspan
        self.tooltip = tooltip
        self.tabs = tabs

    def _create_widget(self, parent, window: Window, row, col):
        self.window = window
        self._parent = parent

        kwargs = {}
        for kw in ["style"]:
            val = getattr(self, kw)
            if val is not None:
                kwargs[kw] = val

        self.widget = ttk.Notebook(parent, **kwargs)
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        event_tab_change = Event(
            self.widget, window, self.key, EventType.NotebookTabChanged
        )
        self.widget.bind(
            "<<NotebookTabChanged>>", window._make_callback(event_tab_change)
        )

        if self.tabs:
            for tab in self.tabs:
                self.add(tab, self.tabs[tab])

        if self._command:
            self.events = True
            window._bind_command(
                # the actual widget will be a tk widget in form widget=.!toplevel.!frame.!notebook, so it won't match self.widget
                # so set widget=None or _handle_commands won't correctly handle the command
                EventCommand(
                    widget=None,
                    key=self.key,
                    event_type=EventType.NotebookTabChanged,
                    command=self._command,
                )
            )

        if self._disabled:
            self.widget.state(["disabled"])

        return self.widget

    def add(self, text, layout, **kwargs):
        """Add a layout to the Notebook as new tab"""
        frame = Frame(layout=layout)
        frame_ = frame._create_widget(self.widget, self.window, 0, 0)
        kwargs["text"] = text
        self.notebook.add(frame_, **kwargs)

    def insert(self, pos, text, layout, **kwargs):
        """Insert a layout to the Notebook as new tab at position pos"""
        frame = Frame(layout=layout)
        frame_ = frame._create_widget(self.widget, self.window, 0, 0)
        kwargs["text"] = text
        self.notebook.insert(pos, frame_, **kwargs)

    @property
    def notebook(self):
        """Return the ttk.Notebook widget"""
        return self.widget


__all__ = [
    "BrowseDirectoryButton",
    "BrowseFileButton",
    "Button",
    "Checkbutton",
    "Combobox",
    "Command",
    "DebugWindow",
    "Entry",
    "Event",
    "EventCommand",
    "Frame",
    "Label",
    "LabelEntry",
    "LabelFrame",
    "LinkLabel",
    "Listbox",
    "Menu",
    "Notebook",
    "Output",
    "Radiobutton",
    "Scale",
    "Text",
    "Treeview",
    "Widget",
    "Window",
    "Progressbar",
]
