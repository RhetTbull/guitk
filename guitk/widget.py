"""Widget wrapper class to use custom widgets with GUITk"""

from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING, Any, Hashable

from .basewidget import BaseWidget
from .events import Event, EventCommand, EventType
from .types import CommandType, PadType, TooltipType

if TYPE_CHECKING:
    from .window import Window


def widget_class_factory(
    widget_class: type[tk.BaseWidget],
    value_type: tk.Variable | None = None,
    value_name: str | None = None,
    event_type: Any = None,
) -> type[BaseWidget]:
    """Create a Widget class for a custom widget.

    Args:
        widget_class (type[tk.BaseWidget]): Tkinter widget class.
        value_type (tk.Variable | None): Type of value to get/set from widget. For example, tk.StringVar.
        value_name (str): Name of widget bound value variable, if any.
            For example, 'textvariable' for tk.Entry or 'variable' for tk.Checkbutton.
        event_type (Any): Event type to use for this widget if the widget should generate events.
            Defaults to None.

    Returns:
        Widget class (type[guitk.BaseWidget]) for the custom widget.

    Note:
        If you widget supports bound values, for example, the `textvariable` argument of tk.Entry,
        you should pass the `value_type` and `value_name` arguments to this constructor which will
        ensure that the Widget class's `value` property is bound to the widget's value. If one of
        these arguments is specified, both must be specified.
    """

    if value_type and not value_name or value_name and not value_type:
        raise ValueError(
            "value_type and value_name must both be specified or both be None"
        )

    # _Widget class for custom widgets
    # defined here as a closure so it has access to widget_class, value_type, and value_name

    class _Widget(BaseWidget):
        """Widget wrapper class to use custom widgets with GUITk"""

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
            weightx: int | None = None,
            weighty: int | None = None,
            focus: bool = False,
            **kwargs: Any,
        ):
            """Initialize a widget.

            Args:
                widget_class (type): Tkinter widget class.
                value_type: Type of value to get/set from widget. For example, tk.StringVar.
                value_name (str, optional): Name of widget bound value variable, if any.
                    For example, 'textvariable' for tk.Entry or 'variable' for tk.Checkbutton.
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
                weightx (int | None, optional): Weight for horizontal resizing. Defaults to None.
                weighty (int | None, optional): Weight for vertical resizing. Defaults to None.
                focus (bool, optional): If True, widget has focus. Defaults to False.
                    Only one widget in a window can have focus.HLayout
                **kwargs: Additional keyword arguments are passed to widget_class.__init__().

            Note:
                If you widget supports bound values, for example, the `textvariable` argument of tk.Entry,
                you should pass the `value_type` and `value_name` arguments to this constructor which will
                ensure that the Widget class's `value` property is bound to the widget's value. If one of
                these arguments is specified, both must be specified.
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
                command=command,
                weightx=weightx,
                weighty=weighty,
                focus=focus,
                value_type=value_type,
            )
            self.widget_class = widget_class
            self.kwargs = kwargs
            self.event_type = event_type
            self.value_name = value_name

        def _create_widget(self, parent: Any, window: Window, row: int, col: int):
            """Create the widget."""

            if self.event_type or self._command:
                self.event_type = self.event_type or f"{self.widget_class}"
                event = Event(self, window, self.key, self.event_type)
                command = window._make_callback(event)
                self.kwargs["command"] = command

            if self.value_name:
                self.kwargs[self.value_name] = self._value

            self.widget = self.widget_class(
                parent,
                **self.kwargs,
            )
            self._grid(
                row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
            )

            if self._command:
                self.events = True
                window._bind_command(
                    EventCommand(
                        widget=self,
                        key=self.key,
                        event_type=self.event_type,
                        command=self._command,
                    )
                )

            if self._disabled:
                self.widget.state(["disabled"])

            return self.widget

    return _Widget


class Widget(BaseWidget):
    """Widget wrapper class to use custom widgets with GUITk"""

    # use widget_class_Factory to create a Widget class for a custom widget in the __new__ method
    # so that the widget_class, value_type, and value_name arguments are available to the _Widget class
    # defined in the widget_class_Factory closure
    def __new__(cls, **kwargs: Any):
        """Create a Widget class for a custom widget.

        Args:
            widget_class (type[tk.BaseWidget]): Tkinter widget class.
            value_type (tk.Variable | None): Type of value to get/set from widget. For example, tk.StringVar.
            value_name (str): Name of widget bound value variable, if any.
                For example, 'textvariable' for tk.Entry or 'variable' for tk.Checkbutton.
            event_type (Any): Event type to use for this widget if the widget should generate events.
                Defaults to None.

        Returns:
            Widget class (type[guitk.BaseWidget]) for the custom widget.

        Note:
            If you widget supports bound values, for example, the `textvariable` argument of tk.Entry,
            you should pass the `value_type` and `value_name` arguments to this constructor which will
            ensure that the Widget class's `value` property is bound to the widget's value. If one of
            these arguments is specified, both must be specified.
        """
        widget_class = kwargs.pop("widget_class")
        value_type = kwargs.pop("value_type", None)
        value_name = kwargs.pop("value_name", None)
        event_type = kwargs.pop("event_type", None)

        _Widget = widget_class_factory(widget_class, value_type, value_name, event_type)

        return _Widget(**kwargs)

    def __init__(
        self,
        widget_class: type[tk.BaseWidget],
        value_type: tk.Variable | None = None,
        value_name: str | None = None,
        event_type: Any = None,
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
        weightx: int | None = None,
        weighty: int | None = None,
        focus: bool = False,
        **kwargs: Any,
    ):
        # This method is only needed to satisfy the type checker and IDE autocomplete
        # The actual Widget class is created in the __new__ method
        ...
