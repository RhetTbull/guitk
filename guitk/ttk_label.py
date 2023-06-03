"""ttk.Label widget"""

from __future__ import annotations

import sys
import tkinter.ttk as ttk
from tkinter import font
from typing import TYPE_CHECKING, Hashable

from .basewidget import BaseWidget
from .events import Event, EventCommand, EventType
from .types import CommandType, PadType, TooltipType, Window
from .utils import load_image

if TYPE_CHECKING:
    from .window import Window

__all__ = ["Label", "LinkLabel", "Linklabel"]

_valid_standard_attributes = {
    "class",
    "compound",
    "cursor",
    "image",
    "style",
    "takefocus",
    "text",
    "textvariable",
    "underline",
    "width",
}

_valid_ttk_label_attributes = {
    "anchor",
    "background",
    "font",
    "foreground",
    "justify",
    "padding",
    "relief",
    "text",
    "wraplength",
} | _valid_standard_attributes


class Label(BaseWidget):
    """ttk.Label widget"""

    def __init__(
        self,
        text: str,
        image: str | None = None,
        key: Hashable | None = None,
        disabled: bool = False,
        columnspan: int | None = None,
        rowspan: int | None = None,
        padx: PadType | None = None,
        pady: PadType | None = None,
        events: bool = False,
        sticky: str | None = None,
        tooltip: TooltipType = None,
        weightx: int | None = None,
        weighty: int | None = None,
        **kwargs,
    ):
        """
        Initialize a Label widget.

        Args:
            key (Hashable, optional): Unique key for this widget. Defaults to None.
            text (str): Text to display in the label.
            image: (str, optional): Path to image to display in the label. Defaults to None.
            disabled (bool, optional): If True, widget is disabled. Defaults to False.
            columnspan (int | None, optional): Number of columns to span. Defaults to None.
            rowspan (int | None, optional): Number of rows to span. Defaults to None.
            padx (PadType | None, optional): X padding. Defaults to None.
            pady (PadType | None, optional): Y padding. Defaults to None.
            events (bool, optional): Enable events for this widget. Defaults to False.
            sticky (str | None, optional): Sticky direction for widget layout. Defaults to None.
            tooltip (TooltipType | None, optional): Tooltip text or callback to generate tooltip text. Defaults to None.
            weightx (int | None, optional): Weight of this widget in the horizontal direction. Defaults to None.
            weighty (int | None, optional): Weight of this widget in the vertical direction. Defaults to None.
            **kwargs: Additional keyword arguments are passed to ttk.Entry.
        """
        super().__init__(
            key=key,
            disabled=disabled,
            rowspan=rowspan,
            columnspan=columnspan,
            padx=padx,
            pady=pady,
            events=events,
            sticky=sticky,
            tooltip=tooltip,
            weightx=weightx,
            weighty=weighty,
        )
        self.widget_type = "ttk.Label"
        self.text = text
        self.key = key or text
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.image = image
        self.kwargs = kwargs

    def _create_widget(self, parent, window: Window, row, col):
        """Create the ttk.Label widget"""

        # Arg list for ttk.Label
        kwargs_label = {
            k: v for k, v in self.kwargs.items() if k in _valid_ttk_label_attributes
        }

        if self.image:
            self._photoimage = load_image(self.image)
            kwargs_label["image"] = self._photoimage

        self.widget = ttk.Label(
            parent,
            text=self.text,
            **kwargs_label,
        )
        self.widget["textvariable"] = self._value
        self._value.set(self.text)
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )
        if self._disabled:
            self.widget.state(["disabled"])
        return self.widget

    @property
    def label(self):
        """Return the Tk label widget"""
        return self.widget


class LinkLabel(Label):
    """Link label that responds to click"""

    def __init__(
        self,
        text: str,
        key: Hashable | None = None,
        disabled: bool = False,
        columnspan: int | None = None,
        rowspan: int | None = None,
        padx: PadType | None = None,
        pady: PadType | None = None,
        events: bool = True,
        sticky: str | None = None,
        tooltip: TooltipType = None,
        command: CommandType | None = None,
        weightx: int | None = None,
        weighty: int | None = None,
        **kwargs,
    ):
        """Initialize a LinkLabel widget.

        Args:
            key (Hashable, optional): Unique key for this widget. Defaults to None.
            text (str): Text to display in the label.
            disabled (bool, optional): If True, widget is disabled. Defaults to False.
            columnspan (int | None, optional): Number of columns to span. Defaults to None.
            rowspan (int | None, optional): Number of rows to span. Defaults to None.
            padx (PadType | None, optional): X padding. Defaults to None.
            pady (PadType | None, optional): Y padding. Defaults to None.
            events (bool, optional): Enable events for this widget. Defaults to True.
            sticky (str | None, optional): Sticky direction for widget layout. Defaults to None.
            tooltip (TooltipType | None, optional): Tooltip text or callback to generate tooltip text. Defaults to None.
            command (CommandType | None, optional): Command to execute when clicked. Defaults to None.
            weightx (int | None, optional): Weight of this widget in the horizontal direction. Defaults to None.
            weighty (int | None, optional): Weight of this widget in the vertical direction. Defaults to None.
            **kwargs: Additional keyword arguments are passed to ttk.Entry.
        """
        self.cursor = (
            kwargs.get("cursor") or "pointinghand"
            if sys.platform == "darwin"
            else "hand2"
        )
        super().__init__(
            text=text,
            key=key,
            disabled=disabled,
            rowspan=rowspan,
            columnspan=columnspan,
            padx=padx,
            pady=pady,
            events=events,
            sticky=sticky,
            tooltip=tooltip,
            cursor=self.cursor,
            weightx=weightx,
            weighty=weighty,
        )
        self.widget_type = "guitk.LinkLabel"
        self.text = text
        self.key = key or text
        self.columnspan = columnspan
        self.rowspan = rowspan
        self._command = command
        self.kwargs = kwargs

    def _create_widget(self, parent, window: "Window", row, col):
        self.widget = super()._create_widget(parent, window, row, col)

        event = Event(self, window, self.key, EventType.LinkLabel)
        self.widget.bind("<Button-1>", window._make_callback(event))

        self.widget.configure(cursor=self.cursor)

        if self._command:
            self.events = True
            window._bind_command(
                EventCommand(
                    widget=self,
                    key=self.key,
                    event_type=EventType.LinkLabel,
                    command=self._command,
                )
            )
        return self.widget


class Linklabel(LinkLabel):
    """Non-camel case version"""

    pass
