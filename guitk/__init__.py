""" Set of classes to simplify building a GUI app with tkinter.
    No dependencies outside python standard library.
    Published under the MIT License.
    Copyright Rhet Turnbull, 2023, all rights reserved.
"""

# TODO: add way to specify tooltip delay
# TODO: add style to all controls
# TODO: standardize value_type

from ._debug import debug, debug_watch, is_debug, set_debug
from ._on import on
from .basewidget import BaseWidget
from .containers import HGrid, HStack, VGrid, VStack
from .debugwindow import DebugWindow
from .events import Event, EventCommand, EventType
from .frame import Frame, LabelFrame
from .image import Image
from .layout import HLayout, VLayout
from .menu import Command, Menu, MenuBar, MenuSeparator
from .spacer import HSpacer, VSpacer
from .tk_text import Output, Text
from .tkroot import *
from .ttk_button import BrowseDirectoryButton, BrowseFileButton, Button
from .ttk_checkbutton import Checkbutton, CheckButton
from .ttk_combobox import Combobox, ComboBox
from .ttk_entry import Entry, LabelEntry
from .ttk_label import Label, LinkLabel, Linklabel
from .ttk_notebook import HTab, Notebook, NoteBook, VTab
from .ttk_panedwindow import (
    HLabelPane,
    HPane,
    Panedwindow,
    PanedWindow,
    VLabelPane,
    VPane,
)
from .ttk_progressbar import (
    PROGRESS_DETERMINATE,
    PROGRESS_INDETERMINATE,
    Progressbar,
    ProgressBar,
)
from .ttk_radiobutton import Radiobutton, RadioButton
from .ttk_scale import Scale
from .ttk_separator import HSeparator, VSeparator
from .ttk_spinbox import Spinbox, SpinBox
from .ttk_treeview import Listbox, ListBox, Treeview, TreeView
from .widget import Widget, widget_class_factory
from .window import Window

__version__ = "0.4.4"
__author__ = "Rhet Turnbull"

__all__ = [
    "BaseWidget",
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
    "HGrid",
    "HLabelPane",
    "HLayout",
    "HPane",
    "HSeparator",
    "HSpacer",
    "HStack",
    "HTab",
    "Image",
    "Label",
    "LabelEntry",
    "LabelFrame",
    "LinkLabel",
    "Linklabel",
    "ListBox",
    "Listbox",
    "Menu",
    "MenuBar",
    "MenuSeparator",
    "NoteBook",
    "Notebook",
    "Output",
    "PROGRESS_DETERMINATE",
    "PROGRESS_INDETERMINATE",
    "PanedWindow",
    "Panedwindow",
    "ProgressBar",
    "Progressbar",
    "RadioButton",
    "Radiobutton",
    "Scale",
    "SpinBox",
    "Spinbox",
    "Text",
    "TreeView",
    "Treeview",
    "VGrid",
    "VLabelPane",
    "VLayout",
    "VPane",
    "VSeparator",
    "VSpacer",
    "VStack",
    "VTab",
    "Widget",
    "Window",
    "debug",
    "debug_watch",
    "is_debug",
    "on",
    "set_debug",
    "widget_class_factory",
]
