"""Window class"""

from __future__ import annotations

import contextlib
import inspect
import time
import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING, Any, Hashable

from guitk.tkroot import _TKRoot

from ._debug import debug, debug_watch
from .basewidget import BaseWidget
from .constants import DEFAULT_PADX, DEFAULT_PADY, MENU_MARKER
from .events import Event, EventCommand, EventType
from .frame import _LayoutMixin
from .layout import push_parent
from .menu import Command, Menu, MenuBar
from .ttk_label import Label
from .types import PadType, SizeType, TooltipType


class _WindowBaseClass:
    # only needed to keep typing happy
    pass


class Window(_LayoutMixin, _WindowBaseClass):
    """Basic Window class from which all windows are derived

    Notes:
        Classes which inherit from window should implement handle_event, setup, and teardown as needed
    """

    def __init__(
        self,
        parent: tk.Tk | None = None,
        title: str | None = None,
        padx: PadType | None = None,
        pady: PadType | None = None,
        topmost: bool | None = None,
        autoframe: bool = False,
        theme: str | None = None,
        tooltip: TooltipType | None = None,
        modal: bool | None = None,
        size: SizeType = None,
    ):
        # call _config then subclass's config to initialize
        # layout, title, menu, etc.

        self.autoframe = autoframe

        self._config()
        self.config()

        # override any layout defaults from constructor
        self.title: str | None = title if title is not None else self.title
        self.padx: int | None = padx if padx is not None else self.padx
        self.pady: int | None = pady if pady is not None else self.pady
        self.theme: str | None = theme if theme is not None else self.theme
        self.tooltip: TooltipType | None = (
            tooltip if tooltip is not None else self.tooltip
        )
        self.modal: bool | None = modal if modal is not None else self.modal
        self.size: SizeType = size if size is not None else self.size

        self._id: int = id(self)
        self._tk: _TKRoot = _TKRoot()
        self._parent = parent or self._tk.root
        self._topmost = topmost

        self.window: tk.TopLevel = tk.Toplevel(self._parent)
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

        self._destroyed = False
        """ set to True when window is destroyed """

        self._mainframe = ttk.Frame(self.window, padding="3 3 12 12")
        self._mainframe.grid(column=0, row=0, sticky="nsew")
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

        self._layout(self._mainframe, self)

        # apply theme if necessary
        if self.theme is not None:
            self._tk.theme = self.theme

        self._grid_configure_widgets()

        if self.menu:
            self._build_menu()

        if self._topmost or self.modal:
            self.window.attributes("-topmost", 1)

        if self.modal:
            windowingsystem = self.root.call("tk", "windowingsystem")
            if windowingsystem == "aqua":
                with contextlib.suppress(Exception):
                    self.root.call(
                        "::tk::unsupported::MacWindowStyle",
                        "style",
                        self._w,
                        "moveableModal",
                        "",
                    )
            if self._parent is not None and self._parent.winfo_viewable():
                self.window.transient(self._parent)
            self.window.wait_visibility()
            self.window.grab_set()

        if self.size is not None:
            size = (
                self.size
                if isinstance(self.size, str)
                else f"{self.size[0]}x{self.size[1]}"
            )
            self.window.geometry(size)

        # TODO: add geometry code to ensure window appears in good spot relative to parent

        # setup event handling
        self.events = True
        self._bind_timer_event(
            100, EventType.WindowFinishedLoading.value, EventType.WindowFinishedLoading
        )
        self._bind_event_handlers()
        self._create_setup_teardown_events()

        self.setup()
        self.root.event_generate(EventType.Setup.value)

        if self.modal:
            self.window.wait_window()

    def _grid_configure_widgets(self):
        """Apply padding to all widgets in the window"""
        # apply padding, widget padding takes precedent over window
        for widget in self._widgets:
            padx = widget.padx if widget.padx is not None else self.padx
            pady = widget.pady if widget.pady is not None else self.pady
            widget.widget.grid_configure(padx=padx, pady=pady)

    def _config(self):
        self.title = "My Window"
        """Title to display in the window's title bar """

        self.layout = []
        """Every class that inherits from Window must define it's own layout """

        self.menu: MenuBar | None = None
        """ Optionally provide a menu """

        self.padx = DEFAULT_PADX
        self.pady = DEFAULT_PADY
        """Default padding around widgets """

        self.theme = None
        """The ttk theme to use, if None, uses ttk default"""

        self.tooltip = None
        """ A callable which returns the tooltip text for a given key or a str """

        self.modal = False
        """ Set to True to create modal window """

        self.size = None
        """ Set to a tuple of (width, height) to set the window size """

        push_parent(self)

    def config(self):
        pass

    def handle_event(self, event: Event):
        """Handle event objects, inheriting classes should implement handle_event"""
        ...
        # if event.event_type == EventType.Quit:
        # self.quit(self._return_value)

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

    @debug_watch
    def quit(self, return_value: Any = None):
        """Called when closing the window"""
        # set return value which is returned by run()
        self._return_value = return_value
        self._destroy()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def geometry(self):
        return self.size

    @geometry.setter
    def geometry(self, value):
        self.size = value

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

    def _create_setup_teardown_events(self):
        """Create the setup and teardown events"""
        setup_event = Event(self, self, EventType.Setup.value, EventType.Setup)
        self.root.bind(EventType.Setup.value, self._make_callback(setup_event))

        teardown_event = Event(self, self, EventType.Teardown.value, EventType.Teardown)
        self.root.bind(EventType.Teardown.value, self._make_callback(teardown_event))

    def cancel_timer_event(self, timer_id):
        """Cancel a timer event created with bind_timer_event"""
        try:
            after_id = self._timer_events[timer_id]
            self.root.after_cancel(after_id)
            self._timer_events.pop(timer_id)
            self._timer_events_cancelled[timer_id] = after_id
        except KeyError as e:
            raise ValueError(f"Timer event {timer_id} not found") from e
        except Exception as e:
            raise e

    def _bind_event_handlers(self):
        """Bind any event handlers decorated with @on"""
        for method in self.__class__.__dict__.values():
            if hasattr(method, "_guitk_event_handlers"):
                for key, event_type in getattr(method, "_guitk_event_handlers"):
                    self.bind_command(key=key, event_type=event_type, command=method)

    def add_widget(self, widget: BaseWidget, row: int, col: int):
        """Add a widget to the window's mainframe"""
        widget._create_widget(self._mainframe, self, row, col)
        self._widgets.append(widget)
        self._widget_by_key[widget.key] = widget
        self._grid_configure_widgets()

    def remove(self, key_or_widget: Hashable | BaseWidget):
        """Remove widget from window and destroy it."""
        for idx, widget in enumerate(self._widgets):
            debug(f"{idx=} {widget=} {key_or_widget=}")
            if widget == key_or_widget or widget.key == key_or_widget:
                widget = self._widgets[idx]
                if widget.parent == self:
                    self._remove(widget)
                else:
                    widget.parent.remove(widget)
                return
        raise ValueError(f"Widget {key_or_widget} not found in Window")

    def _remove(self, widget: BaseWidget):
        """Remove widget from window and destroy it."""
        widget.widget.grid_forget()
        widget.widget.destroy()
        self._widget_by_key.pop(widget.key, None)
        self._widgets.remove(widget)
        self.window.update_idletasks()

    def _insert_widget_row_col(self, widget: BaseWidget, row: int, col: int):
        """Insert a widget into the window's mainframe after the container has been created
            Intended for use at run-time only when widgets need to be added dynamically

        Args:
            widget: (Widget) the widget to add
            row: (int) the row to insert the widget into
            col: (int) the column to insert the widget into

        Note:
            This method is included in Window so that Widget.replace() works properly for
            widgets added directly to a layout. It does not expand the layout like the similar
            method in _Container.
        """
        # TODO: fix this so it actually inserts instead of replaces
        self.add_widget(widget, row, col)

    def run(self):
        self._tk.run_mainloop()
        return self._return_value

    @property
    def root(self):
        """Return Tk root instance"""
        return self._tk.root

    @property
    def widgets(self) -> list[BaseWidget]:
        """ "Return list of all widgets belonging to the window"""
        return self._widgets

    def children(self):
        """Return child windows"""
        return self._tk.get_children(self)

    def get(self, key: Hashable) -> BaseWidget:
        """Get widget with key or raise KeyError if not found"""
        try:
            return self._widget_by_key[key]
        except KeyError as e:
            raise KeyError(f"Widget with key {key} not found") from e

    def _add_widget(self, widget: BaseWidget):
        """Dummy method to allow widgets to be added with VLayout()/HLayout()"""
        pass

    def _forget_widget(self, widget: BaseWidget):
        """Remove widget from the window's bookkeeping but don't destroy it"""
        self._widget_by_key.pop(widget.key, None)
        self._widgets.remove(widget)

    def _add_menus(self, menu: Menu, path: str | None = None):
        """Add menus to the window recursively

        Args:
            menu (Menu): the Menu object to add
            path (str, optional): the path to the menu item which is used as the key
        """
        path = f"{MENU_MARKER}{menu._label}" if path is None else path
        for m in menu:
            subpath = f"{path}|{m._label}"
            m._create_widget(menu._menu, self, subpath)
            self._widgets.append(m)
            self._widget_by_key[m.key] = m
            if isinstance(m, Menu):
                self._add_menus(m, subpath)

    def _build_menu(self):
        """Build the menu bar"""
        if self._root_menu is None:
            # create the root menu
            self.root.option_add("*tearOff", tk.FALSE)
            self._root_menu = tk.Menu(self.root)
            self.window["menu"] = self._root_menu

        for m in self.menu:
            if not isinstance(m, Menu):
                raise ValueError("self.menu items must be Menu objects")
            path = f"{MENU_MARKER}{m._label}"
            m._create_widget(self._root_menu, self, path)
            self._widgets.append(m)
            self._widget_by_key[m.key] = m
            self._add_menus(m, path)

    @debug_watch
    def _destroy(self):
        """Destroy the window and all child windows and perform cleanup"""
        if self._destroyed:
            # HACK: avoid multiple calls to _destroy which can occur if
            # the user handles the Quit event themselves
            # TODO: find a better way to handle this
            return

        # call teardown to perform any cleanup
        self.teardown()

        # generate a Teardown event
        self.root.event_generate(EventType.Teardown.value)

        # kill any child windows
        for child in self.children():
            event = Event(child, child.window, EventType.Quit, EventType.Quit)
            child.handle_event(event)
            with contextlib.suppress(Exception):
                child._destroy()

        # disable event processing in _handle_event
        self.events = False

        # disable any stdout/stderr redirection and event handling
        for widget in self._widgets:
            widget.events = False

            if "guitk.widgets.tk_text.Output" in str(type(widget)):
                widget.disable_redirect()

        if self.modal:
            self.window.grab_release()

        # cancel any timer events
        for timer_id in self._timer_events:
            with contextlib.suppress(Exception):
                after_id = self._timer_events[timer_id]
                self._tk.root.after_cancel(after_id)
        self._parent.focus_set()
        self.window.destroy()
        self._tk.deregister(self)
        self._destroyed = True

    def _make_callback(self, event):
        def _callback(*arg):
            if arg:
                event.event = arg[0]
            self._handle_event(event)

        return _callback

    @debug_watch
    def _handle_event(self, event: Event):
        """Handle events for this window"""
        # only handle events if widget has events=True; Window objects always get events
        if isinstance(event.widget, (BaseWidget, Window)) and not event.widget.events:
            return

        # filter events for this window
        if event.id != self._id:
            return

        # swallow MenuCommand events if the menu is disabled
        # if event.event_type == EventType.MenuCommand and not self.menu.enabled:

        # handle custom commands
        self._handle_commands(event)

        # call subclass handle_event
        self.handle_event(event)

        # if deleting the window, call _destroy after handle_event has had a chance to handle it
        if event.event_type == EventType.Quit:
            self._destroy()

    @debug_watch
    def _handle_commands(self, event):
        """Handle commands bound to widgets in the window"""
        for command in self._commands:
            if (
                (command.widget is None or command.widget == event.widget)
                and (command.key is None or command.key == event.key)
                and (
                    command.event_type is None or command.event_type == event.event_type
                )
            ) or command.event_type == EventType.Any:
                if hasattr(command.command, "_guitk_event_handlers"):
                    # command was decorated with @on, so it's a method of this class
                    if len(inspect.signature(command.command).parameters) == 2:
                        # command has a second argument, assume it's the event
                        command.command(self, event)
                    else:
                        command.command(self)
                else:
                    command.command()

    def __getitem__(self, key) -> BaseWidget:
        try:
            return self._widget_by_key[key]
        except KeyError as e:
            raise KeyError(f"Invalid key: no widget with key {key}") from e
