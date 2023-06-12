"""Menu and Command classes"""

from __future__ import annotations

import contextlib
import tkinter as tk
from inspect import currentframe, getmro
from typing import TYPE_CHECKING, Hashable

from ._debug import debug, debug_watch
from .constants import MENU_MARKER
from .events import Event, EventType
from .layout import DummyParent, get_parent, pop_parent, push_parent
from .types import CommandType

if TYPE_CHECKING:
    from .window import Window

__all__ = ["Command", "Menu", "MenuBar", "MenuSeparator"]


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


class _BaseMenu:
    """Base class for Menu and MenuBar and Command"""

    def __init__(self, label: str, disabled: bool = False):
        """Init the _BaseMenu"""
        self._label = label

        # initialize variables every subclass will need
        self._disabled: bool = disabled
        self.parent: _BaseMenu | MenuBar | None = None
        self._parent: tk.Menu | None = None
        self.key: Hashable | None = None
        self.path: str | None = None

        # _menu_list holds the list of sub-items if this is a Menu or SubMenu
        self._menu_list = []

    def __init_subclass__(subclass, *args, **kwargs):
        """Ensure that all menu items are added to the parent menu or menubar"""

        # This rewrites the __init__ method of the subclass to add the menu item to the parent menu
        super().__init_subclass__(*args, **kwargs)

        @debug_watch
        def new_init(self, *args, init=subclass.__init__, **kwargs):
            init(self, *args, **kwargs)
            if subclass is type(self):
                # only do this for the bottom grandchild class
                # in the case of subclassed menus
                self.parent = get_parent()
                if isinstance(self.parent, DummyParent):
                    raise RuntimeError(
                        "Menu item must created within a MenuBar or Menu context manager"
                    )
                debug(f"{self.parent=} {self=}")
                self.parent._add_widget(self)

        subclass.__init__ = new_init

    @property
    def disabled(self) -> bool:
        return self._parent.entrycget(self._label, "state") == tk.DISABLED

    @disabled.setter
    def disabled(self, value: bool) -> None:
        debug(f"{self=} {self._label=} {value=}")
        if value:
            self._parent.entryconfigure(self._label, state=tk.DISABLED)
        else:
            self._parent.entryconfigure(self._label, state=tk.NORMAL)
        self._disabled = self._parent.entrycget(self._label, "state") == tk.DISABLED

    def _self_or_ancestor_is_disabled(self) -> bool:
        """Returns True if self or any ancestor menu is disabled"""
        if self.disabled:
            return True
        # if self.parent is None:
        #     return self.disabled
        if isinstance(self.parent, MenuBar):
            return self.disabled
        if self._parent.entrycget(self._label, "state") == tk.DISABLED:
            return True
        return self.parent._self_or_ancestor_is_disabled()


class MenuBar:
    """Menu bar manager that can be used to create a menu bar for a Window"""

    def __init__(
        self,
    ):
        """Create a new MenuBar.

        Examples:
            ```python
            import guitk as ui

            class MenuDemo(ui.Window):
                def config(self):
                    with ui.VLayout():
                        ui.Label("This window has menus!")

                    with ui.MenuBar():
                        with ui.Menu("File"):
                            ui.Command("Open...", shortcut="Ctrl+O")
                            with ui.SubMenu("Open Recent"):
                                ui.Command("File 1")
                                ui.Command("File 2")
                                ui.Command("File 3")
                            ui.MenuSeparator()
                            ui.Command("Save", key="File|Save", disabled=True)
                            ui.Command("Save As")
                        with ui.Menu("Edit", key="Edit", disabled=True):
                            ui.Command("Cut", shortcut="Ctrl+X")
                            ui.Command("Copy", shortcut="Ctrl+C")
                            ui.Command("Paste", shortcut="Ctrl+V")
            ```
        """
        self._index = 0
        self.window = None
        self._menu_list = []

        # get the caller's instance so we can set the layout
        caller_frame = currentframe().f_back
        with contextlib.suppress(IndexError, KeyError):
            first_arg = caller_frame.f_code.co_varnames[0]
            caller_instance = caller_frame.f_locals[first_arg]
            # determine if the caller is a Window
            # need to use repr() because we can't import Window here without causing a circular import
            if "guitk.window.Window" in repr(getmro(caller_instance.__class__)):
                self.window = caller_instance
                self.window.menu = self

    def _add_widget(self, widget: _BaseMenu):
        """Add a menu item to the end of the Menu"""
        self._menu_list.append(widget)

    def __enter__(self):
        push_parent(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pop_parent()
        return False

    def __iter__(self):
        self._index = 0
        return iter(self._menu_list)

    def __next__(self) -> Menu:
        if self._index >= len(self._menu_list):
            raise StopIteration
        value = self._menu_list[self._index]
        self._index += 1
        return value


class Menu(_BaseMenu):
    def __init__(
        self,
        label: str,
        underline: int | None = None,
        key: Hashable | None = None,
        disabled: bool = False,
    ) -> None:
        """Create a new Menu.

        Args:
            label (str): The label for the menu
            underline (int, optional): The index of the character to underline in the label. Defaults to None.
            key (Hashable, optional): The key to use to access the menu from parent Window.
                Defaults to  f"Menu:{label}" for top level menus and f"Menu:{parent_label|label...}" for submenus.
            disabled: Create menu in disabled state. Defaults to False.

        Note:
            If the menu is created within a MenuBar context manager, the menu will be added to the MenuBar.
            If the menu is created within a Menu context manager, the menu will be added to the parent Menu as a submenu.

        Examples:
            ```python
            import guitk as ui

            class MenuDemo(ui.Window):
                def config(self):
                    with ui.VLayout():
                        ui.Label("This window has menus!")

                    with ui.MenuBar():
                        with ui.Menu("File"):
                            ui.Command("Open...", shortcut="Ctrl+O")
                            with ui.SubMenu("Open Recent"):
                                ui.Command("File 1")
                                ui.Command("File 2")
                                ui.Command("File 3")
                            ui.MenuSeparator()
                            ui.Command("Save", key="File|Save", disabled=True)
                            ui.Command("Save As")
                        with ui.Menu("Edit", key="Edit", disabled=True):
                            ui.Command("Cut", shortcut="Ctrl+X")
                            ui.Command("Copy", shortcut="Ctrl+C")
                            ui.Command("Paste", shortcut="Ctrl+V")
            ```
        """
        super().__init__(label, disabled=disabled)
        self._menu = None
        self._underline = underline
        self.window = None
        self._index = 0
        self.key = key

    def _create_widget(self, parent: tk.Menu, window: Window, path: str | None = None):
        """Create the Menu widget and add it to the parent

        Args:
            parent: The parent widget
            window: The Window that owns this Menu
            path: The path to the parent widget, used only by subclasses
        """
        debug(
            f"Menu._create_widget: {self=} {self._label=} {parent=} {window=} {path=}"
        )
        self.window = window
        self._parent = parent
        menu = tk.Menu(parent)
        if self._underline is None:
            idx = self._label.find("&")
            if idx != -1:
                self._label = self._label.replace("&", "", 1)
                self._underline = idx
        parent.add_cascade(menu=menu, label=self._label, underline=self._underline)

        self._menu = menu
        self.key = self.key or path
        self.path = path or ""

        if self._disabled:
            self.disabled = True

    def _add_widget(self, widget):
        """Add a menu item to the end of the Menu"""
        self._menu_list.append(widget)

    def __enter__(self):
        push_parent(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pop_parent()
        return False

    def __iter__(self):
        self._index = 0
        return iter(self._menu_list)

    def __next__(self) -> Menu | Command:
        if self._index >= len(self._menu_list):
            raise StopIteration
        value = self._menu_list[self._index]
        self._index += 1
        return value


# class SubMenu(Menu):
#     """Submenu that can be added to a Menu and holds a list of Commands or SubMenus"""

#     def __init__(
#         self,
#         label: str,
#         underline: int | None = None,
#         key: Hashable | None = None,
#         disabled: bool = False,
#     ) -> None:
#         """Create a new Submenu

#         Args:
#             label (str): The label for the submenu
#             underline (int, optional): The index of the character to underline in the label. Defaults to None.
#             key (Hashable, optional): The key to use to access the menu from parent Window.
#                 Defaults to  f"Menu:{label}" for top level menus and f"Menu:{parent_label|label...}" for submenus.
#             disabled: Create submenu in disabled state. Defaults to False.

#         Examples:
#             ```python
#             import guitk as ui

#             class MenuDemo(ui.Window):
#                 def config(self):
#                     with ui.VLayout():
#                         ui.Label("This window has menus!")

#                     with ui.MenuBar():
#                         with ui.Menu("File"):
#                             ui.Command("Open...", shortcut="Ctrl+O")
#                             with ui.SubMenu("Open Recent"):
#                                 ui.Command("File 1")
#                                 ui.Command("File 2")
#                                 ui.Command("File 3")
#                             ui.MenuSeparator()
#                             ui.Command("Save", key="File|Save", disabled=True)
#                             ui.Command("Save As")
#                         with ui.Menu("Edit", key="Edit", disabled=True):
#                             ui.Command("Cut", shortcut="Ctrl+X")
#                             ui.Command("Copy", shortcut="Ctrl+C")
#                             ui.Command("Paste", shortcut="Ctrl+V")
#             ```
#         """
#         super().__init__(label, underline=underline, key=key, disabled=disabled)


class MenuSeparator(Menu):
    """Separator that adds a dividing line between menu items.

    Examples:
        ```python
        import guitk as ui

        class MenuDemo(ui.Window):
            def config(self):
                with ui.VLayout():
                    ui.Label("This window has menus!")

                with ui.MenuBar():
                    with ui.Menu("File"):
                        ui.Command("Open...", shortcut="Ctrl+O")
                        with ui.SubMenu("Open Recent"):
                            ui.Command("File 1")
                            ui.Command("File 2")
                            ui.Command("File 3")
                        ui.MenuSeparator()
                        ui.Command("Save", key="File|Save", disabled=True)
                        ui.Command("Save As")
                    with ui.Menu("Edit", key="Edit", disabled=True):
                        ui.Command("Cut", shortcut="Ctrl+X")
                        ui.Command("Copy", shortcut="Ctrl+C")
                        ui.Command("Paste", shortcut="Ctrl+V")
        ```

    """

    def __init__(self) -> None:
        """Create a new MenuSeparator"""
        super().__init__("")

    def _create_widget(self, parent: tk.Menu, window: Window, path: str | None = None):
        """Create the Separator widget and add it to the parent

        Args:
            parent: The parent widget
            window: The Window that owns this Menu
            path: The path to the parent widget, used as the key for the command
        """
        debug(f"MenuSeparator._create_widget: {self=} {parent=} {window=} {path=}")
        self._parent = parent
        self.window = window
        parent.add_separator()
        self.key = f"{path}separator({id(self)})"
        self.path = path or ""


class Command(Menu):
    def __init__(
        self,
        label: str,
        shortcut: str = None,
        key: Hashable | None = None,
        command: CommandType | None = None,
        disabled: bool = False,
    ):
        """Create a new menu command

        Args:
            label (str): The label for the menu command
            shortcut (str, optional): The shortcut for the menu command
            key (Hashable, optional): Optional key for the menu command (defaults to the path to the menu command)
            command (CommandType, optional): The command to run when the menu command is selected
            disabled (bool): Create command in disabled state. Defaults to False.

        Note:
            Emits EventType.MenuCommand when command is selected or shortcut is pressed.

        Examples:
            ```python
            import guitk as ui

            class MenuDemo(ui.Window):
                def config(self):
                    with ui.VLayout():
                        ui.Label("This window has menus!")

                    with ui.MenuBar():
                        with ui.Menu("File"):
                            ui.Command("Open...", shortcut="Ctrl+O")
                            with ui.SubMenu("Open Recent"):
                                ui.Command("File 1")
                                ui.Command("File 2")
                                ui.Command("File 3")
                            ui.MenuSeparator()
                            ui.Command("Save", key="File|Save", disabled=True)
                            ui.Command("Save As")
                        with ui.Menu("Edit", key="Edit", disabled=True):
                            ui.Command("Cut", shortcut="Ctrl+X")
                            ui.Command("Copy", shortcut="Ctrl+C")
                            ui.Command("Paste", shortcut="Ctrl+V")
            ```
        """
        super().__init__(label, disabled=disabled)
        self.shortcut = shortcut
        self._parent = None
        self.key = key
        self._command = command

    def _create_widget(self, parent: tk.Menu, window: Window, path: str):
        """Create the Menu widget and add it to the parent

        Args:
            parent: The parent widget
            window: The Window that owns this Menu
            path: The path to the parent widget, used as the key for the command
        """
        debug(f"Command._create_widget: {self=} {parent=} {window=} {path=}")
        self._parent = parent
        self.window = window
        self.key = self.key or path
        self.path = path or ""

        parent.add_command(
            label=self._label,
            command=self.window._make_callback(
                Event(self, self.window, self.key, EventType.MenuCommand)
            ),
            accelerator=self.shortcut,
        )

        if self._command:
            self.window.bind_command(
                key=self.key, event_type=EventType.MenuCommand, command=self._command
            )

        if self._disabled:
            self.disabled = True

        key_binding = _map_key_binding_from_shortcut(self.shortcut)

        def _make_callback(event):
            def _callback(*arg):
                if self._self_or_ancestor_is_disabled():
                    # if self or any ancestor is disabled, ignore the shortcut event
                    return
                if arg:
                    event.event = arg[0]
                self.window._handle_event(event)

            return _callback

        window.window.bind_all(
            key_binding,
            _make_callback(Event(self, self.window, self.key, EventType.MenuCommand)),
        )
