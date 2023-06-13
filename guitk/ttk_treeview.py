""" ttk Treeview and Listbox widgets """


from __future__ import annotations

import tkinter.ttk as ttk
from typing import TYPE_CHECKING, Hashable

from .basewidget import BaseWidget
from .events import Event, EventCommand, EventType
from .types import CommandType, PadType, TooltipType
from .utils import scrolled_widget_factory

if TYPE_CHECKING:
    from .window import Window

__all__ = ["ListBox", "Listbox", "TreeView", "Treeview"]

_valid_standard_attributes = {
    "class",
    "cursor",
    "displaycolumns",
    "padding",
    "selectmode",
    "show",
    "style",
    "takefocus",
    "xscrollcommand",
    "yscrollcommand",
}

_valid_ttk_treeview_attributes = _valid_standard_attributes


class Treeview(BaseWidget):
    """ttk.Treeview widget"""

    def __init__(
        self,
        headings: list[str],
        key: Hashable | None = None,
        columns: list[str] | None = None,
        disabled: bool = False,
        columnspan: int | None = None,
        rowspan: int | None = None,
        padx: PadType | None = None,
        pady: PadType | None = None,
        events: bool = True,
        sticky: str | None = None,
        tooltip: TooltipType = None,
        command: CommandType | None = None,
        hscrollbar: bool = False,
        vscrollbar: bool = False,
        weightx: int | None = None,
        weighty: int | None = None,
        focus: bool = False,
        **kwargs,
    ):
        """Initialize a ttk.Treeview widget

        Args:
            headings (list[str]): List of column headings, required.
            key (Hashable, optional): Key to use for this widget. Defaults to None.
            columns (list[str], optional): List of column names. Defaults to None.
            disabled (bool, optional): Whether the widget is disabled. Defaults to False.
            columnspan (int, optional): Number of columns to span. Defaults to None.
            rowspan (int, optional): Number of rows to span. Defaults to None.
            padx (int, optional): Padding in x direction. Defaults to None.
            pady (int, optional): Padding in y direction. Defaults to None.
            events (bool, optional): Whether to bind events. Defaults to True.
            sticky (str, optional): Sticky direction. Defaults to None.
            tooltip (TooltipType, optional): Tooltip to display. Defaults to None.
            command (CommandType, optional): Command to run when selection changes. Defaults to None.
            hscrollbar (bool, optional): Whether to display a horizontal scrollbar. Defaults to False.
            vscrollbar (bool, optional): Whether to display a vertical scrollbar. Defaults to False.
            weightx (int, optional): Horizontal weight. Defaults to None.
            weighty (int, optional): Vertical weight. Defaults to None.
            focus (bool, optional): If True, widget will have focus. Defaults to False.
                Only one widget in a window can have focus.HLayout
            **kwargs: Additional keyword arguments to pass to ttk.Treeview.

        Note:
            Emits EventType.TreeviewSelect event when selection changes.
            If bind_heading() is used, emits EventType.TreeviewHeading event when column heading is clicked.
            If bind_tag() is used, emits EventType.TreeviewTag event when tag is clicked.
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
        )
        self.key = key or "Treeview"
        self.widget_type = "ttk.Treeview"

        if headings and columns and len(headings) != len(columns):
            raise ValueError("headings and columns lists must be the same length")

        self._headings = headings

        self._columns = tuple(columns) if columns is not None else tuple(headings)
        self._disabled = disabled
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.padx = padx
        self.pady = pady
        self.events = events
        self.sticky = sticky or ""
        self.tooltip = tooltip
        self.vscrollbar = vscrollbar
        self.hscrollbar = hscrollbar
        self.kwargs = kwargs

    def _create_widget(self, parent, window: Window, row, col):
        # build arg list for Treeview()
        kwargs_treeview = {
            k: v
            for k, v in self.kwargs.items()
            if k in _valid_ttk_treeview_attributes and v is not None
        }
        if "show" not in kwargs_treeview:
            kwargs_treeview["show"] = "headings"

        self.widget = scrolled_widget_factory(
            parent,
            ttk.Treeview,
            vscrollbar=self.vscrollbar,
            hscrollbar=self.hscrollbar,
            columns=self._columns,
            **kwargs_treeview,
        )
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        # set column headings
        if self._headings:
            for column, heading in zip(self._columns, self._headings):
                self.widget.heading(column, text=heading)

        if self._disabled:
            self.widget.state(["disabled"])

        event = Event(self, window, self.key, EventType.TreeviewSelect)
        self.widget.bind("<<TreeviewSelect>>", window._make_callback(event))

        if self._command:
            self.events = True
            window._bind_command(
                EventCommand(
                    widget=self,
                    key=self.key,
                    event_type=EventType.TreeviewSelect,
                    command=self._command,
                )
            )

        return self.widget

    @property
    def value(self):
        return self.tree.selection()

    @value.setter
    def value(self, *values):
        self.tree.selection_set(*values)

    def bind_heading(self, column_name, event_name, command=None):
        """Bind event to click on column heading"""
        event = Event(self, self.window, event_name, EventType.TreeviewHeading)
        self.tree.heading(column_name, command=self.window._make_callback(event))

        if command:
            self.window.bind_command(
                key=event.key, event_type=event.event_type, command=command
            )

    def bind_tag(self, tagname, event_name, sequence=None, command=None):
        """Bind event to item with tag when sequence occurs
        If sequence is None, will bind to <Button-1>"""
        if sequence is None:
            sequence = "<Button-1>"
        event = Event(self, self.window, event_name, EventType.TreeviewTag)
        self.tree.tag_bind(
            tagname, sequence=sequence, callback=self.window._make_callback(event)
        )

        if command:
            self.window.bind_command(
                key=event.key, event_type=event.event_type, command=command
            )

    def sort_on_column(self, column_name, key=None, reverse=False):
        """sort the tree view contents based on column_name
        optional key same as sort(key=)
        """
        values = [
            (self.tree.set(k, column_name), k) for k in self.tree.get_children("")
        ]
        values.sort(key=key, reverse=reverse)
        for index, (val, k) in enumerate(values):
            self.tree.move(k, "", index)

    @property
    def tree(self):
        """Return the ttk Treeview widget"""
        return self.widget


class Listbox(Treeview):
    """Listbox widget (which is a Treeview widget with only one column)"""

    def __init__(
        self,
        text: list[str] | None = None,
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
        hscrollbar: bool = False,
        vscrollbar: bool = False,
        width: int = 200,
        weightx: int | None = None,
        weighty: int | None = None,
        **kwargs,
    ):
        """Create a Listbox widget

        Args:
            text (list[str], optional): List of strings to display in the listbox. Defaults to None.
            key (Hashable, optional): The key used to access the widget's value. Defaults to None.
            disabled (bool, optional): Disable the widget. Defaults to False.
            columnspan (int, optional): Number of columns to span in the grid. Defaults to None.
            rowspan (int, optional): Number of rows to span in the grid. Defaults to None.
            padx (int, optional): Padding in the x direction. Defaults to None.
            pady (int, optional): Padding in the y direction. Defaults to None.
            events (bool, optional): Enable events. Defaults to True.
            sticky (str, optional): Sticky setting for the grid. Defaults to None.
            tooltip (TooltipType, optional): A tooltip to show when the mouse is over the widget. Defaults to None.
            command (CommandType, optional): A command to execute when the widget is clicked. Defaults to None.
            hscrollbar (bool, optional): Show a horizontal scrollbar. Defaults to False.
            vscrollbar (bool, optional): Show a vertical scrollbar. Defaults to False.
            width (int, optional): Width of the widget in pixels. Defaults to 200.
            weightx (int, optional): Horizontal weight. Defaults to None.
            weighty (int, optional): Vertical weight. Defaults to None.
            **kwargs: Additional keyword arguments to pass to the widget constructor.

        Note:
            This Listbox widget is actually implemented as a Treeview widget with only one column.
            This is because Tk does not offer a themed ttk Listbox widget.
            Emits EventType.ListboxSelect event when the selection changes.
        """
        self.key = key or "Listbox"
        self.widget_type = "guitk.Listbox"

        if text and type(text) != list:
            raise ValueError("text must be a list of strings")
        self._text = text
        self.width = width

        super().__init__(
            headings=["list"],
            columns=["list"],
            show="tree",
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
            hscrollbar=hscrollbar,
            vscrollbar=vscrollbar,
            weightx=weightx,
            weighty=weighty,
            **kwargs,
        )

    def _create_widget(self, parent, window: Window, row, col):
        """Create the widget"""

        # build arg list for Treeview()
        kwargs_treeview = {
            k: v
            for k, v in self.kwargs.items()
            if k in _valid_ttk_treeview_attributes and v is not None
        }

        # listbox always shows tree
        kwargs_treeview["show"] = "tree"

        self.widget = scrolled_widget_factory(
            parent,
            ttk.Treeview,
            vscrollbar=self.vscrollbar,
            hscrollbar=self.hscrollbar,
            columns=["list"],
            **kwargs_treeview,
        )
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        self.tree.column("#0", width=0, minwidth=0)
        self.tree.column("#1", width=self.width)

        self.listbox = self.tree
        if self._text:
            for line in self._text:
                self.append(line)

        event = Event(self, window, self.key, EventType.ListboxSelect)
        self.widget.bind("<<TreeviewSelect>>", window._make_callback(event))

        if self._command:
            self.events = True
            window._bind_command(
                EventCommand(
                    widget=self,
                    key=self.key,
                    event_type=EventType.ListboxSelect,
                    command=self._command,
                )
            )

        return self.widget

    def insert(self, index, line):
        """Insert a line into Listbox"""
        self.widget.insert("", index, iid=line, values=(line))

    def append(self, line):
        """Append a line to end of Listbox"""
        self.widget.insert("", "end", iid=line, values=(line))

    def delete(self, line):
        """Delete a line from Listbox"""
        self.widget.delete(line)


class TreeView(Treeview):
    """
    ttk.Treeview widget
    """

    pass


class ListBox(Listbox):
    """
    Listbox widget
    """

    pass
