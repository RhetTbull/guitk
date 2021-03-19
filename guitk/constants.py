"""Constants for guitk """

from enum import Enum, auto


class GUITK(Enum):
    """Constants used internally by guitk """

    ELEMENT_FRAME = ("Frame",)
    ELEMENT_LABEL_FRAME = "LabelFrame"


class EventType(Enum):
    """Constants for event types"""

    WM_DELETE_WINDOW = "WM_DELETE_WINDOW"
    BUTTON_PRESS = auto()
    CHECK_BUTTON = auto()
    VIRTUAL_EVENT = auto()
    BROWSE_FILE = auto()
    BROWSE_DIRECTORY = auto()
    LINK_LABEL_CLICKED = auto()
    TREEVIEW_HEADING = auto()
    TREEVIEW_TAG = auto()
    OUTPUT_WRITE = "<<OutputWrite>>"

