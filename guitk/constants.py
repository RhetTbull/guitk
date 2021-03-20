"""Constants for guitk """

from enum import Enum, auto


class GUITK(Enum):
    """Constants used internally by guitk """

    ELEMENT_FRAME = ("Frame",)
    ELEMENT_LABEL_FRAME = "LabelFrame"


class EventType(Enum):
    """Constants for event types"""

    BROWSE_FILE = auto()
    BROWSE_DIRECTORY = auto()
    BUTTON_PRESS = auto()
    Checkbutton = "<<Checkbutton>>"
    CheckButton = "<<Checkbutton>>"
    ComboboxSelected = "<<ComboboxSelected>>"
    ComboBoxSelected = "<<ComboboxSelected>>"
    Radiobutton = "<<Radiobutton>>"
    RadioButton = "<<Radiobutton>>"
    VIRTUAL_EVENT = auto()
    KeyRelease = "<KeyRelease>"
    LINK_LABEL_CLICKED = auto()
    ListboxSelect = "<<ListboxSelect>>"
    ListBoxSelect = "<<ListboxSelect>>"
    OUTPUT_WRITE = "<<OutputWrite>>"
    TreeviewHeading = auto()
    TreeviewSelect = "<<TreeviewSelect>>"
    TreeViewSelect = "<<TreeviewSelect>>"
    TreeviewTag = auto()
    WM_DELETE_WINDOW = "WM_DELETE_WINDOW"

