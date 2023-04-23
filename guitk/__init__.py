""" Set of classes to simplify building a GUI app with tkinter.
    Inspired by PySimpleGUI. 

    No dependencies outside python standard library.

    Published under the MIT License.

    Copyright Rhet Turnbull, 2021, all rights reserved.
"""

# TODO: add way to specify tooltip delay
# TODO: add style to all controls
# TODO: standardize value_type

from .tkroot import *
from .widgets import *

__version__ = "0.2.1"
__author__ = "Rhet Turnbull"

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
    "Label",
    "LabelEntry",
    "LabelFrame",
    "Labelframe",
    "LinkLabel",
    "Linklabel",
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
    "Text",
    "TreeView",
    "Treeview",
    "Window",
]
