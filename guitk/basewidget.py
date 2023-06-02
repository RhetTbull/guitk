""" Widget base class """

from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING, Any, Callable, Hashable

from guitk.tkroot import _TKRoot

from ._debug import debug, debug_watch
from .events import Event, EventCommand
from .layout import DummyParent, get_parent
from .types import CommandType, HAlign, PadType, TooltipType, VAlign, ValueType

if TYPE_CHECKING:
    from .frame import _Container
    from .window import Window


class BaseWidget:
    """Basic abstract base class for all tk widgets"""

    def __init__(
        self,
        key: Hashable | None = None,
        disabled: bool = False,
        rowspan: int | None = None,
        columnspan: int | None = None,
        padx: PadType | None = None,
        pady: PadType | None = None,
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
            padx (PadType | None, optional): X padding. Defaults to None.
            pady (PadType | None, optional): Y padding. Defaults to None.
            events (bool, optional): Enable events for this widget. Defaults to False.
            sticky (str | None, optional): Sticky direction for widget layout. Defaults to None.
            tooltip (TooltipType | None, optional): Tooltip text or callback to generate tooltip text. Defaults to None.
            command (CommandType | None, optional): Command callback. Defaults to None.
            value_type (ValueType | None, optional): Type of value to store (for example, tk.StringVar). Defaults to None.
                If None, a tk.StringVar is used.
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

        # set by _create_widget in inherited classes or the __init_subclass__ method
        self._parent = None
        self.window = None
        self.parent = None

        # used by style()
        self._style_kwargs = {}

        # will store where widget is placed in layout grid (row, column)
        # set by the layout manager
        self._row = None
        self._col = None

        # set to True when _layout creates the widget
        self._has_been_created = False

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

        debug("_grid", self, self.widget, row, column, rowspan, columnspan, sticky)
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
            debug(f"{self=} {self.padx=} {self.pady=}")
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

    def style(self, **kwargs) -> BaseWidget:
        """Configure the widget style

        Args:
            **kwargs -- style options

        Returns: Widget instance (self)

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
        self._configure()
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
    ) -> BaseWidget:
        """Configure the widget font

        Args:
            font -- font specifier (name, system font, or (family, size, style)-tuple)
            family -- font 'family', e.g. Courier, Times, Helvetica
            size -- font size in points
            weight -- font thickness: NORMAL, BOLD
            slant -- font slant: ROMAN, ITALIC
            underline -- font underlining: false (0), true (1)
            overstrike -- font strikeout: false (0), true (1)

        Returns: Widget instance (self)

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
        self._configure()
        return self

    # def valign(self, valign: VAlign | None = None) -> Widget:
    #     """Set valign the widget

    #     Args:
    #         valign (VAlign | None): Vertical alignment

    #     Returns: Widget instance (self)
    #     """

    #     return self

    @debug_watch
    def destroy(self) -> None:
        """Remove the widget from the layout and destroy it.

        Note:
            You should call this destroy() method and not the tkinter destroy() method
            so that the widget is removed from its parent and necessary bookkeeping is done
            in the Window class.
        """
        debug("destroy", self, self.parent)
        self.parent.remove(self)

    def replace(self, widget: BaseWidget) -> BaseWidget:
        """Replace widget with another widget.
        This destroys the parent widget and replaces it with the new widget in the layout.

        Args;
            widget (Widget): New widget

        Returns: Widget instance
        """
        self.widget.grid_forget()
        self.destroy()
        self.parent._insert_widget_row_col(widget, row=self._row, col=self._col)
        return widget

    def _set_parent_window(self, tk_parent: tk.BaseWidget, window: Window):
        """Called during widget creation to set the widget attributes"""
        self.window = window
        self._parent = tk_parent

    def _set_row_col(self, row: int, col: int):
        """Called during widget creation or configuration to set the widget attributes"""
        self._row = row
        self._col = col

    def _configure(self):
        """Configure the widget after it has been created.
        This allows font(), style() to be used before or after creation.
        """
        if self._has_been_created:
            self.parent._configure_widget(
                self, self._parent, self.window, self._row, self._col
            )

    def __init_subclass__(subclass, *args, **kwargs):
        """Ensure that all widgets are added to the parent layout"""

        # This rewrites the __init__ method of the subclass to add the widget to the parent layout
        super().__init_subclass__(*args, **kwargs)

        @debug_watch
        def new_init(self, *args, init=subclass.__init__, **kwargs):
            init(self, *args, **kwargs)
            if subclass is type(self):
                # only do this for the bottom grandchild class
                # in the case of subclassed widgets
                self.parent = get_parent()
                if isinstance(self.parent, DummyParent):
                    raise RuntimeError(
                        "Widget must created within a Layout or Container"
                    )
                debug(f"{self.parent=} {self=}")
                self.parent._add_widget(self)

        subclass.__init__ = new_init
