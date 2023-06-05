""" Classes for handling tkinter.TK() """

from __future__ import annotations

import contextlib
import tkinter as tk
from tkinter import ttk
from typing import TypeVar

# create a custom type for type hinting a Window object which is defined later in this module
Window = TypeVar("Window")

__all__ = ["_TKRoot"]


class _TKRoot:
    """Singleton that returns a tkinter.TK() object; there can be only one in an app"""

    def __new__(cls, *args, **kwargs):
        """create new object or return instance of already created singleton"""
        if not hasattr(cls, "instance") or not cls.instance:
            cls.instance = super().__new__(cls)

        return cls.instance

    def __init__(self):
        if hasattr(self, "root"):
            return

        # create root object, make it invisible and withdraw it
        # all other windows will be children of this invisible root object
        root = tk.Tk()
        # root = customtkinter.CTk()
        root.attributes("-alpha", 0)
        root.withdraw()

        self.root = root
        self.first_window: bool = False
        self.windows: dict = {}
        self.mainloop_is_running: bool = False

    def register(self, window: Window):
        """Register a new child window"""
        if not self.first_window:
            self.first_window = True
        self.windows[window] = 1

    def deregister(self, window: Window):
        """De-register a new child window
        Once all children are de-registered, the root Tk object is destroyed
        """
        with contextlib.suppress(KeyError):
            del self.windows[window]
        if self.first_window and not self.windows:
            # last window
            self.root.quit()
            self.mainloop_is_running = False
            self.first_window = False

    def get_children(self, window):
        """Return child windows of parent window"""
        return [w for w in self.windows if w._parent == window.window]

    def run_mainloop(self):
        if not self.mainloop_is_running:
            self.root.mainloop()

    @property
    def theme(self) -> str:
        """Return name of ttk theme in use"""
        s = ttk.Style()
        return s.theme_use()

    @theme.setter
    def theme(self, theme_name: str) -> None:
        """Set name of ttk theme to use"""
        s = ttk.Style()
        theme_names = s.theme_names()
        if theme_name not in theme_names:
            raise ValueError(f"theme_name {theme_name} must by in {theme_names}")
        s.theme_use(theme_name)
