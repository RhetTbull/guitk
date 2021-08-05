"""Constants for guitk """

from enum import Enum, auto


class GUITK(Enum):
    """Constants used internally by guitk"""

    ELEMENT_FRAME = ("Frame",)
    ELEMENT_LABEL_FRAME = "LabelFrame"


class EventType(Enum):
    """Constants for event types"""

    BrowseFile = "<<BrowseFile>>"
    BrowseDirectory = "<<BrowseDirectory>>"
    ButtonPress = "<<Button>>"
    Checkbutton = "<<Checkbutton>>"
    CheckButton = "<<Checkbutton>>"
    ComboboxSelected = "<<ComboboxSelected>>"
    ComboBoxSelected = "<<ComboboxSelected>>"
    Radiobutton = "<<Radiobutton>>"
    RadioButton = "<<Radiobutton>>"
    VirtualEvent = "<<VirtualEvent>>"
    KeyRelease = "<KeyRelease>"
    LinkLabel = "<<LinkLabel>>"
    ListboxSelect = "<<ListboxSelect>>"
    ListBoxSelect = "<<ListboxSelect>>"
    OutputWrite = "<<OutputWrite>>"
    ScaleUpdate = "<<ScaleUpdate>>"
    TreeviewHeading = "<<TreeviewHeading>>"
    TreeViewHeading = "<<TreeviewHeading>>"
    TreeviewSelect = "<<TreeviewSelect>>"
    TreeViewSelect = "<<TreeviewSelect>>"
    TreeviewTag = "<<TreeviewTag>>"
    TreeViewTag = "<<TreeviewTag>>"
    WM_DELETE_WINDOW = "WM_DELETE_WINDOW"
    DeleteWindow = "WM_DELETE_WINDOW"
    Quit = "WM_DELETE_WINDOW"
    WindowFinishedLoading = "<<WindowFinishedLoading>>"
