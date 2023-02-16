""" ttk Treeview and Listbox widgets """

from __future__ import annotations

import tkinter as tk
import tkinter.ttk as ttk
from typing import List, Optional

from .events import Event, EventCommand, EventType
from .utils import scrolled_widget_factory
from .widget import Widget


class Treeview(Widget):
    def __init__(
        self,
        key=None,
        headings: Optional[List] = None,
        columns: Optional[List] = None,
        cursor=None,
        displaycolumns=None,
        height=None,
        padding=None,
        selectmode=None,
        show=None,
        style=None,
        takefocus=None,
        disabled=False,
        rowspan=None,
        columnspan=None,
        padx=None,
        pady=None,
        events=True,
        sticky=None,
        tooltip=None,
        anchor=None,
        command=None,
        vscrollbar=False,
        hscrollbar=False,
    ):
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
            anchor=anchor,
            cursor=cursor,
            command=command,
        )
        """ columns is optional, if not provided, will use headings for column names """
        self.key = key or "Treeview"
        self.widget_type = "ttk.Treeview"

        if headings and columns and len(headings) != len(columns):
            raise ValueError("headings and columns lists must be the same length")

        self._headings = headings

        # ttk.Treeview arguments
        self._columns = tuple(columns) if columns is not None else tuple(headings)
        self._displaycolumns = displaycolumns
        self._height = height
        self._padding = padding
        self._selectmode = selectmode
        self._show = show
        self._style = style
        self._takefocus = takefocus
        self._cursor = cursor

        self._disabled = disabled
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.padx = padx
        self.pady = pady
        self.events = events
        self.sticky = sticky or ""
        self.tooltip = tooltip
        self.anchor = anchor
        self.vscrollbar = vscrollbar
        self.hscrollbar = hscrollbar

    def _create_widget(self, parent, window: "Window", row, col):
        self.window = window
        self._parent = parent

        # build arg list for Treeview()
        kwargs = {}
        for kw in [
            "columns",
            "cursor",
            "displaycolumns",
            "height",
            "padding",
            "selectmode",
            "show",
            "style",
            "takefocus",
        ]:
            val = getattr(self, f"_{kw}")
            if val is not None:
                kwargs[kw] = val

        self.widget = scrolled_widget_factory(
            parent,
            ttk.Treeview,
            vscrollbar=self.vscrollbar,
            hscrollbar=self.hscrollbar,
            **kwargs,
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
    def __init__(
        self,
        text: Optional[List] = None,
        key=None,
        cursor=None,
        height=None,
        width=None,
        padding=None,
        selectmode=None,
        style=None,
        takefocus=None,
        disabled=False,
        rowspan=None,
        columnspan=None,
        padx=None,
        pady=None,
        events=True,
        sticky=None,
        tooltip=None,
        anchor=None,
        command=None,
        vscrollbar=None,
        hscrollbar=None,
    ):
        self.key = key or "Listbox"
        self.widget_type = "guitk.Listbox"
        self._show = "tree"
        self._columns = ["list"]
        self._width = width

        if text and type(text) != list:
            raise ValueError("text must be a list of strings")
        self._text = text

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
            anchor=anchor,
            cursor=cursor,
            show=self._show,
            columns=self._columns,
            height=height,
            padding=padding,
            selectmode=selectmode,
            style=style,
            takefocus=takefocus,
            command=command,
            vscrollbar=vscrollbar,
            hscrollbar=hscrollbar,
        )

    def _create_widget(self, parent, window: "Window", row, col):
        super()._create_widget(parent, window, row, col)
        self.tree.column("#0", width=0, minwidth=0)
        if self._width:
            self.tree.column("#1", width=self._width)

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

    def insert(self, index, line):
        """Insert a line into Listbox"""
        self.widget.insert("", index, iid=line, values=(line))

    def append(self, line):
        """Apppend a line to end of Listbox"""
        self.widget.insert("", "end", iid=line, values=(line))

    def delete(self, line):
        """Delete a line from Listbox"""
        self.widget.delete(line)


