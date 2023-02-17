from .debugwindow import DebugWindow
from .events import Event, EventCommand, EventType
from .menu import Command, Menu
from .tk_text import Output, Text
from .ttk_button import BrowseDirectoryButton, BrowseFileButton, Button
from .ttk_checkbutton import Checkbutton
from .ttk_combobox import Combobox
from .ttk_entry import Entry, LabelEntry
from .ttk_label import Label, LinkLabel
from .ttk_notebook import Notebook
from .ttk_progressbar import Progressbar
from .ttk_radiobutton import Radiobutton
from .ttk_scale import Scale
from .ttk_treeview import Listbox, Treeview
from .window import Frame, LabelFrame, Widget, Window

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
    "EventType",
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


def _get_docstring(name):
    """Return the docstring of an object with name"""
    try:
        obj = globals()[name]
    except KeyError as e:
        raise ValueError(f"Invalid object name: {e}")
    return obj.__doc__ or ""
