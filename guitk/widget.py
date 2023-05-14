""" Widget base class """

from __future__ import annotations

import tkinter as tk
from typing import Any, Callable, Hashable

from guitk.tkroot import _TKRoot

from .events import Event, EventCommand
from .layout import DummyParent, get_parent
from .types import CommandType, TooltipType, ValueType


class Widget:
    """Basic abstract base class for all tk widgets"""

    def __init__(
        self,
        key: Hashable | None = None,
        disabled: bool = False,
        rowspan: int | None = None,
        columnspan: int | None = None,
        padx: int | None = None,
        pady: int | None = None,
        events: bool = True,
        sticky: str | None = None,
        tooltip: TooltipType = None,
        command: CommandType | None = None,
        value_type: ValueType | None = None,
        weightx: int | None = None,
        weighty: int | None = None,
        focus: bool = False,
    ):
        """Initialize a widget.

        Args:
            key (Hashable, optional): Unique key for this widget. Defaults to None.
            default (str | None, optional): Default text for the entry box. Defaults to None.
            disabled (bool, optional): If True, widget is disabled. Defaults to False.
            columnspan (int | None, optional): Number of columns to span. Defaults to None.
            rowspan (int | None, optional): Number of rows to span. Defaults to None.
            padx (int | None, optional): X padding. Defaults to None.
            pady (int | None, optional): Y padding. Defaults to None.
            events (bool, optional): Enable events for this widget. Defaults to False.
            sticky (str | None, optional): Sticky direction for widget layout. Defaults to None.
            tooltip (TooltipType | None, optional): Tooltip text or callback to generate tooltip text. Defaults to None.
            command (CommandType | None, optional): Command callback. Defaults to None.
            weightx (int | None, optional): Weight for horizontal resizing. Defaults to None.
            weighty (int | None, optional): Weight for vertical resizing. Defaults to None.
            focus (bool, optional): If True, widget has focus. Defaults to False.
                Only one widget in a window can have focus.HLayout
        """
        super().__init__()

        self.key = key
        self._disabled = disabled
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.padx = padx
        self.pady = pady
        self.events = events
        self.sticky = sticky or ""
        self.tooltip = tooltip
        self.weightx = weightx
        self.weighty = weighty
        self._focus = focus

        self._command = command
        self._commands = {}

        self.widget_type = None
        self._tk = _TKRoot()
        self.widget: tk.BaseWidget | None = None
        self._value = value_type() if value_type is not None else tk.StringVar()

        # set by _create_widget in inherited classes
        self.parent = None
        self.window = None

        # used by style()
        self._style_kwargs = {}

    @property
    def value(self):
        return self._value.get()

    @value.setter
    def value(self, value):
        self._value.set(value)

    def focus(self):
        self.widget.focus()

    def _grid(self, row, column, rowspan, columnspan):
        sticky = self.sticky or tk.W

        self.widget.grid(
            row=row,
            column=column,
            columnspan=columnspan,
            rowspan=rowspan,
            sticky=sticky,
            padx=self.padx,
            pady=self.pady,
        )

        if self.padx is not None or self.pady is not None:
            self.widget.grid_configure(padx=self.padx, pady=self.pady)

    def bind_event(self, event_name: str, command: Callable[[], Any] | None = None):
        """Bind a tkinter event to widget; will result in an Event being sent to handle_event when triggered.
        Optionally bind command to the event"""
        event = Event(self, self.window, self.key, event_name)
        self.widget.bind(event_name, self.window._make_callback(event))

        if command:
            self.window._bind_command(
                EventCommand(
                    widget=self, key=self.key, event_type=event_name, command=command
                )
            )

    @property
    def state(self) -> bool:
        return self.widget["state"]

    @property
    def disabled(self) -> bool:
        return self.widget["state"] == "disabled"

    @disabled.setter
    def disabled(self, value: bool) -> None:
        self.widget["state"] = "disabled" if value else "normal"

    def style(self, **kwargs) -> Widget:
        """Configure the widget style

        Args:
            **kwargs -- style options

        Note:
        The specific style options available depend on the widget type.
        For example, to configure the foreground color to blue of a Label widget:
            Label("Hello").style(foreground="blue")

        Refer to the tk documentation for the specific widget type for more information.
        https://tkdocs.com/index.html

        style() returns the widget instance, so it can be chained with other methods,
        for example:
            Label("Hello").style(foreground="blue").font(size=20)
        """
        self._style_kwargs |= kwargs
        return self

    def font(
        self,
        font: str | None = None,
        family: str | None = None,
        size: int | None = None,
        weight: str | None = None,
        slant: str | None = None,
        underline: bool | None = None,
        overstrike: bool | None = None,
    ) -> Widget:
        """Configure the widget font

        Args:
            font -- font specifier (name, system font, or (family, size, style)-tuple)
            family -- font 'family', e.g. Courier, Times, Helvetica
            size -- font size in points
            weight -- font thickness: NORMAL, BOLD
            slant -- font slant: ROMAN, ITALIC
            underline -- font underlining: false (0), true (1)
            overstrike -- font strikeout: false (0), true (1)

        Note:
            The font parameter is a string of the form "family size style", where style is a string
            containing any combination of "bold", "italic", "underline", and "overstrike" separated by spaces.
            The size may be specified as an integer, or as a floating point number followed by the unit "p" or "P".
            The unit "p" or "P" stands for points, 1/72 of an inch, and is the standard unit used by X fonts.
            If font is specified, then the other font-related options (size, weight, slant, underline, overstrike)
            are ignored.
        """
        locals_ = locals()
        locals_.pop("self")
        if font_kwargs := {k: v for k, v in locals_.items() if v is not None}:
            self._style_kwargs["font"] = tk.font.Font(**font_kwargs)
        return self

    def __init_subclass__(subclass, *args, **kwargs):
        """Ensure that all widgets are added to the parent layout"""

        # This rewrites the __init__ method of the subclass to add the widget to the parent layout
        super().__init_subclass__(*args, **kwargs)

        def new_init(self, *args, init=subclass.__init__, **kwargs):
            init(self, *args, **kwargs)
            if subclass is type(self):
                # only do this for the bottom grandchild class
                # in the case of subclassed widgets
                self.parent = get_parent()
                if isinstance(self.parent, DummyParent):
                    raise RuntimeError(
                        "Widget must created within a HLayout or Container"
                    )
                self.parent._add_widget(self)

        subclass.__init__ = new_init
