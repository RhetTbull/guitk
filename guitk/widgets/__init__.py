from .debugwindow import DebugWindow
from .events import Event, EventCommand, EventType
from .layout import Layout
from .menu import Command, Menu
from .tk_text import Output, Text
from .ttk_button import BrowseDirectoryButton, BrowseFileButton, Button
from .ttk_checkbutton import Checkbutton, CheckButton
from .ttk_combobox import Combobox, ComboBox
from .ttk_entry import Entry, LabelEntry
from .ttk_label import Label, LinkLabel
from .ttk_notebook import Notebook, NoteBook
from .ttk_progressbar import (
    PROGRESS_DETERMINATE,
    PROGRESS_INDETERMINATE,
    Progressbar,
    ProgressBar,
)
from .ttk_radiobutton import Radiobutton, RadioButton
from .ttk_scale import Scale
from .ttk_treeview import Listbox, ListBox, Treeview, TreeView
from .window import Frame, HStack, LabelFrame, VStack, Widget, Window

__all__ = [
    "BrowseDirectoryButton",
    "BrowseFileButton",
    "Button",
    "CheckButton",
    "Checkbutton",
    "ComboBox",
    "Combobox",
    "Command",
    "DebugWindow",
    "Entry",
    "Event",
    "EventCommand",
    "EventType",
    "Frame",
    "HStack",
    "Label",
    "LabelEntry",
    "LabelFrame",
    "Layout",
    "LinkLabel",
    "ListBox",
    "Listbox",
    "Menu",
    "NoteBook",
    "Notebook",
    "Output",
    "PROGRESS_DETERMINATE",
    "PROGRESS_INDETERMINATE",
    "ProgressBar",
    "Progressbar",
    "RadioButton",
    "Radiobutton",
    "Scale",
    "Text",
    "TreeView",
    "Treeview",
    "VStack",
    "Widget",
    "Window",
]


def _get_docstring(name):
    """Return the docstring of an object with name"""
    try:
        obj = globals()[name]
    except KeyError as e:
        raise ValueError(f"Invalid object name: {e}") from e
    return obj.__doc__ or ""
