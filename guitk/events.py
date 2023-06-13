"""Events """

from __future__ import annotations

import tkinter
from collections import namedtuple
from typing import TYPE_CHECKING, Hashable

EventCommand = namedtuple("EventCommand", ["widget", "key", "event_type", "command"])

from enum import Enum

if TYPE_CHECKING:
    from .basewidget import BaseWidget
    from .window import Window


class Event:
    """Event that occurred and values for widgets in the window"""

    def __init__(
        self, widget: BaseWidget, window: Window, key: Hashable, event_type: EventType
    ):
        self.id: int = id(window)
        self.widget: BaseWidget = widget
        self.key: Hashable = key
        self.event_type: EventType = event_type
        self.event: tkinter.Event | None = (
            None  # placeholder for Tk event, will be set in _make_callback
        )

    def __str__(self):
        return f"id={self.id}, widget={self.widget}, key={self.key}, event_type={self.event_type}, event={self.event}"


class EventType(Enum):
    """Constants for event types"""

    Any = "*"  # special case for binding to all events
    BrowseDirectory = "<<BrowseDirectory>>"
    BrowseFile = "<<BrowseFile>>"
    ButtonPress = "<<Button>>"
    CheckButton = "<<Checkbutton>>"
    Checkbutton = "<<Checkbutton>>"
    ComboboxReturn = "<<ComboboxReturn>>"
    ComboBoxReturn = "<<ComboboxReturn>>"
    ComboBoxSelected = "<<ComboboxSelected>>"
    ComboboxSelected = "<<ComboboxSelected>>"
    DeleteWindow = "WM_DELETE_WINDOW"
    EntryReturn = "<<EntryReturn>>"
    ImagePress = "<<ImagePress>>"
    KeyRelease = "<KeyRelease>"
    LinkLabel = "<<LinkLabel>>"
    ListBoxSelect = "<<ListboxSelect>>"
    ListboxSelect = "<<ListboxSelect>>"
    MenuCommand = "<<MenuCommand>>"
    NotebookTabChanged = "<<NotebookTabChanged>>"
    OutputWrite = "<<OutputWrite>>"
    Quit = "WM_DELETE_WINDOW"
    RadioButton = "<<Radiobutton>>"
    Radiobutton = "<<Radiobutton>>"
    ScaleUpdate = "<<ScaleUpdate>>"
    Setup = "<<Setup>>"
    SpinboxDecrement = "<<SpinboxDecrement>>"
    SpinboxIncrement = "<<SpinboxIncrement>>"
    SpinboxUpdate = "<<SpinboxUpdate>>"
    Teardown = "<<Teardown>>"
    TreeViewHeading = "<<TreeviewHeading>>"
    TreeViewSelect = "<<TreeviewSelect>>"
    TreeViewTag = "<<TreeviewTag>>"
    TreeviewHeading = "<<TreeviewHeading>>"
    TreeviewSelect = "<<TreeviewSelect>>"
    TreeviewTag = "<<TreeviewTag>>"
    VirtualEvent = "<<VirtualEvent>>"
    WM_DELETE_WINDOW = "WM_DELETE_WINDOW"
    WindowFinishedLoading = "<<WindowFinishedLoading>>"
