"""Image widget"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Hashable

from .events import Event, EventCommand, EventType
from .ttk_label import Label
from .types import CommandType, CompoundType, PadType, TooltipType, Window

if TYPE_CHECKING:
    from .window import Window

__all__ = ["Image"]


class Image(Label):
    """Image widget"""

    def __init__(
        self,
        image: str,
        text: str | None = None,
        compound: CompoundType = None,
        key: Hashable | None = None,
        disabled: bool = False,
        columnspan: int | None = None,
        rowspan: int | None = None,
        padx: PadType | None = None,
        pady: PadType | None = None,
        events: bool = False,
        sticky: str | None = None,
        tooltip: TooltipType = None,
        command: CommandType | None = None,
        weightx: int | None = None,
        weighty: int | None = None,
        **kwargs,
    ):
        """
        Initialize an Image widget.

        Args:
            key (Hashable, optional): Unique key for this widget. Defaults to None.
            image: (str, optional): Path to image to display.
            text (str, optional): Text to display with the image.
            compound (str, optional): How to display the image and text. Defaults to None (show image only).
            disabled (bool, optional): If True, widget is disabled. Defaults to False.
            columnspan (int | None, optional): Number of columns to span. Defaults to None.
            rowspan (int | None, optional): Number of rows to span. Defaults to None.
            padx (PadType | None, optional): X padding. Defaults to None.
            pady (PadType | None, optional): Y padding. Defaults to None.
            events (bool, optional): Enable events for this widget. Defaults to False.
            sticky (str | None, optional): Sticky direction for widget layout. Defaults to None.
            tooltip (TooltipType | None, optional): Tooltip text or callback to generate tooltip text. Defaults to None.
            command (CommandType | None, optional): Command to execute when clicked. Defaults to None.
            weightx (int | None, optional): Weight of this widget in the horizontal direction. Defaults to None.
            weighty (int | None, optional): Weight of this widget in the vertical direction. Defaults to None.
            **kwargs: Additional keyword arguments are passed to ttk.Entry.

        Note:
            tkinter only supports images in GIF, PGM, PPM, and PNG formats.
            If you install the option Pillow package, you can use images in many other formats as well.
            guitk will automatically use Pillow if it is installed.

            compound can be one of: None, "top", "bottom", "left", "right", "center", "image", "text"
            If None or "image", only the image is displayed.
            If "text", only the text is displayed.
            If "top", "bottom", "left", or "right", the image is displayed above, below, to the left, or to the right of the text.

            Emits EventType.ImagePress when clicked if events is True.
        """
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
            weightx=weightx,
            weighty=weighty,
        )
        self.widget_type = "guitk.Image"
        self.image = image
        self.text = text
        self.compound = compound
        self.key = key or text
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.kwargs = kwargs

        self.cursor = (
            kwargs.get("cursor") or "pointinghand"
            if sys.platform == "darwin"
            else "hand2"
        )

    def _create_widget(self, parent, window: "Window", row, col):
        self.widget = super()._create_widget(parent, window, row, col)

        if self.compound:
            self.widget.configure(compound=self.compound)

        if self.events:
            event = Event(self, window, self.key, EventType.ImagePress)
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
