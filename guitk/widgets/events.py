"""Events """


from collections import namedtuple

EventCommand = namedtuple("EventCommand", ["widget", "key", "event_type", "command"])

from enum import Enum, auto


class Event:
    """Event that occurred and values for widgets in the window"""

    def __init__(self, widget: object, window: "Window", key, event_type):
        self.id = id(window)
        self.widget = widget
        self.key = key
        self.event_type = event_type
        self.event = None  # placeholder for Tk event, will be set in _make_callback

    def __str__(self):
        return f"id={self.id}, widget={self.widget}, key={self.key}, event_type={self.event_type}, event={self.event}"

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
    NotebookTabChanged = "<<NotebookTabChanged>>"
    MenuCommand = "<<MenuCommand>>"
