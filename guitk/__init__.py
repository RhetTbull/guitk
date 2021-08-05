""" Set of classes to simplify building a GUI app with tkinter.
    Inspired by PySimpleGUI. 

    No dependencies outside python standard library.

    Published under the MIT License.

    Copyright Rhet Turnbull, 2021, all rights reserved.
"""

# TODO: add way to specify tooltip delay
# TODO: add cursor to all controls
# TODO: add style to all controls
# TODO: standardize value_type

from .constants import GUITK, EventType
from .tkroot import *
from .widgets import *

__version__ = "0.0.1"
__author__ = "Rhet Turnbull"

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
    "Output",
    "Radiobutton",
    "ScrolledText",
    "Text",
    "Treeview",
    "Window",
]

# Aliases for classnames as I don't like tkinter's naming convention
# You can use either CapWords or Firstword names in guitk
ComboBox = Combobox
CheckButton = Checkbutton
RadioButton = Radiobutton
TreeView = Treeview
ListBox = Listbox
Linklabel = LinkLabel
Scrolledtext = ScrolledText
Labelframe = LabelFrame
