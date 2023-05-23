"""Menu and Command classes"""

from __future__ import annotations

import tkinter as tk
from typing import Callable, Optional

from .events import Event, EventType


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

    def _create_widget(self, parent, window: "_WindowBaseClass"):
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

    def _create_widget(self, parent, window: "_WindowBaseClass", path):
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
