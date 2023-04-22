"""Window class"""

from __future__ import annotations

import contextlib
import time
import tkinter as tk
from tkinter import ttk

from guitk.constants import GUITK
from guitk.tkroot import _TKRoot
from guitk.tooltips import Hovertip

from .events import Event, EventCommand, EventType
from .menu import Command, Menu
from .ttk_label import Label
from .types import TooltipType
from .widget import Widget

LayoutType = list[list[Widget | None]]


class _WindowBaseClass:
    # only needed to keep typing happy
    pass


class _Layout:
    """Mixin class to provide layout"""

    layout = []

    def __init__(self, *args, **kwargs):
        pass

    def _layout(
        self, parent: tk.BaseWidget, window: "_WindowBaseClass", autoframe: bool
    ):
        """Create widgets from layout"""
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
                if tooltip := widget.tooltip or window.tooltip:
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


class Window(_Layout, _WindowBaseClass):
    """Basic Window class from which all windows are derived

    Notes:
        Classes which inherit from window should implement handle_event, setup, and teardown as needed
    """

    def __init__(
        self,
        parent: tk.Tk | None = None,
        title: str | None = None,
        padx: int | None = None,
        pady: int | None = None,
        topmost: bool | None = None,
        autoframe: bool = True,
        theme: str | None = None,
        tooltip: TooltipType | None = None,
        modal: bool | None = None,
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
        self._parent = parent or self._tk.root
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

        # self.layout = [
        #     [
        #         Label(
        #             "Looks like you forgot to add self.layout to your config() method."
        #         )
        #     ],
        #     [Button("Quit")],
        # ]
        self.layout = []
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
        # call teardown to perform any cleanup
        self.teardown()

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

    def __getitem__(self, key) -> "Widget":
        try:
            return self._widget_by_key[key]
        except KeyError:
            raise KeyError(f"Invalid key: no widget with key {key}")


class _Frame(Widget, _Layout):
    """Frame base class for Frame and LabelFrame"""

    def __init__(
        self,
        frametype: GUITK = GUITK.ELEMENT_FRAME,
        width: int | None = None,
        key: str | None = None,
        height: int | None = None,
        layout: LayoutType | None = None,
        style: str | None = None,
        borderwidth: int | None = None,
        padding: int | None = None,
        relief: str = None,
        disabled: bool | None = False,
        rowspan: int | None = None,
        columnspan: int | None = None,
        text: str | None = None,
        labelanchor: str | None = None,
        sticky: bool | None = None,
        tooltip: TooltipType | None = None,
        autoframe: bool | None = True,
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

    def _create_widget(self, parent, window: "Window", row, col):
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
            self.widget.configure(padding=self.padding)
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
        layout: LayoutType | None = None,
        key: str | None = None,
        width: int | None = None,
        height: int | None = None,
        style: str | None = None,
        borderwidth: int | None = None,
        padding: int | None = None,
        relief: str = None,
        disabled: bool | None = False,
        rowspan: int | None = None,
        columnspan: int | None = None,
        sticky: bool | None = None,
        tooltip: TooltipType | None = None,
        autoframe: bool = True,
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
        text: str | None = None,
        layout: LayoutType | None = None,
        key: str | None = None,
        width: int | None = None,
        height: int | None = None,
        style: str | None = None,
        borderwidth: int | None = None,
        padding: int | None = None,
        relief: str = None,
        disabled: bool | None = False,
        rowspan: int | None = None,
        columnspan: int | None = None,
        labelanchor: str | None = None,
        sticky: bool | None = None,
        tooltip: TooltipType | None = None,
        autoframe: bool = True,
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
