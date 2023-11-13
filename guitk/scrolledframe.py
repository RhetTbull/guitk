""" ScrolledFrame widget for tkinter.

    Based on similar class in [tkbootstrap](https://github.com/israel-dryer/ttkbootstrap)
    which is Copyright (c) 2021 Israel Dryer, licensed under MIT License.

    Original implementation: https://github.com/israel-dryer/ttkbootstrap/blob/7ab4e0790fb4da38c29ddffed7df0ce823b434fc/src/ttkbootstrap/scrolled.py#L184

    Unlike most other scrolled frame implementations for tkinter, this one does not use
    a canvas. Instead, it uses a ttk.Frame as the container and a ttk.Frame as the content,
    implementing xview and yview methods to scroll the content frame within the container.

    Note: The horizontal scrolling is currently not working correctly and is disabled.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import Grid, Pack, Place, ttk
from typing import Any

from ._debug import debug


class ScrolledFrame(ttk.Frame):
    """A widget container with a vertical scrollbar.

    The ScrolledFrame fills the width of its container. The height is
    either set explicitly or is determined by the content frame's
    contents.

    This widget behaves mostly like a normal frame other than the
    exceptions stated already. Another exception is when packing it
    into a Notebook or Panedwindow. In this case, you'll need to add
    the container instead of the content frame. For example,
    `mynotebook.add(myscrolledframe.container)`.

    The scrollbar has an autohide feature that can be turned on by
    setting `autohide=True`.

    Args:
        parent: The parent widget.
        padding: The amount of padding to add around the content frame.
        vscrollbar: Whether to show the vertical scrollbar.
        autohide: Whether to autohide the scrollbar.
        height: The height of the content frame or None.
        width: The width of the content frame or None.
        scrollheight: The height of the container frame or None.
    """

    def __init__(
        self,
        parent=tk.BaseWidget,
        padding: tuple[int, int, int, int] | tuple[int, int] | int | str = 2,
        vscrollbar: bool = True,
        autohide: bool = False,
        height: int | None = None,
        width: int | None = None,
        scrollheight: int | None = None,
        **kwargs: dict[str, Any],
    ):
        # content frame container
        self.container = ttk.Frame(
            master=parent,
            relief=tk.FLAT,
            borderwidth=0,
            width=width,
            height=height,
        )
        self.container.propagate(False)

        # content frame
        super().__init__(
            master=self.container,
            padding=padding,
            width=width,
            height=height,
            **kwargs,
        )
        self.place(rely=0.0, relwidth=1.0, height=scrollheight)

        # vertical scrollbar
        if vscrollbar:
            self.vscroll = ttk.Scrollbar(
                master=self.container,
                command=self.yview,
                orient=tk.VERTICAL,
            )
            self.vscroll.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            self.vscroll = None

        # horizontal scrollbar
        hscrollbar = False  # TODO: implement horizontal scrollbar
        if hscrollbar:
            self.hscroll = ttk.Scrollbar(
                master=self.container,
                command=self.xview,
                orient=tk.HORIZONTAL,
            )
            self.hscroll.pack(side=tk.BOTTOM, fill=tk.X)
        else:
            self.hscroll = None

        # get windowing system for mousewheel scrolling
        self.winsys = self.tk.call("tk", "windowingsystem")

        # setup autohide scrollbar
        self.autohide = autohide
        if self.autohide:
            self.hide_scrollbars()

        # widget event binding
        self.container.bind("<Configure>", self._on_configure, "+")
        self.container.bind("<Enter>", self._on_enter, "+")
        self.container.bind("<Leave>", self._on_leave, "+")
        self.container.bind("<Map>", self._on_map, "+")
        self.bind("<<MapChild>>", self._on_map_child, "+")
        self.bind("<Configure>", self._on_configure, "+")

        # delegate content geometry methods to container frame
        _methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        for method in _methods:
            if any(["pack" in method, "grid" in method, "place" in method]):
                # prefix content frame methods with 'content_'
                setattr(self, f"content_{method}", getattr(self, method))
                # overwrite content frame methods from container frame
                setattr(self, method, getattr(self.container, method))

    def _resize_container(self, event=None):
        """Resize the container widget to fit the window."""

        requested_width = self.winfo_reqwidth()
        container_width = self.container.winfo_width()
        requested_height = self.winfo_reqheight()
        container_height = self.container.winfo_height()
        if requested_width != container_width or requested_height != container_height:
            # Resize the container widget
            new_width = max(container_width, requested_width)
            new_height = max(container_height, requested_height)
            self.container.configure(width=new_width, height=new_height)

    def yview(self, *args):
        """Update the vertical position of the content frame within the
        container.

        Parameters:

            *args (List[Any, ...]):
                Optional arguments passed to yview in order to move the
                content frame within the container frame.
        """
        if not self.vscroll:
            return
        if not args:
            first, _ = self.vscroll.get()
            self.yview_moveto(fraction=first)
        elif args[0] == "moveto":
            self.yview_moveto(fraction=float(args[1]))
        elif args[0] == "scroll":
            self.yview_scroll(number=int(args[1]), what=args[2])
        else:
            return

    def yview_moveto(self, fraction: float):
        """Update the vertical position of the content frame within the
        container.

        Parameters:

            fraction (float):
                The relative position of the content frame within the
                container.
        """
        base, thumb = self._ymeasures()
        if fraction < 0:
            first = 0.0
        elif (fraction + thumb) > 1:
            first = 1 - thumb
        else:
            first = fraction
        self.vscroll.set(first, first + thumb)
        self.content_place(rely=-first * base)

    def yview_scroll(self, number: int, what: str):
        """Update the vertical position of the content frame within the
        container.

        Parameters:

            number (int):
                The amount by which the content frame will be moved
                within the container frame by 'what' units.

            what (str):
                The type of units by which the number is to be interpeted.
                This parameter is currently not used and is assumed to be
                'units'.
        """
        first, _ = self.vscroll.get()
        fraction = (number / 100) + first
        self.yview_moveto(fraction)

    def xview(self, *args):
        """Update the horizontal position of the content frame within the
        container.

        Parameters:

            *args (List[Any, ...]):
                Optional arguments passed to yview in order to move the
                content frame within the container frame.
        """
        if not self.hscroll:
            return
        if not args:
            first, _ = self.hscroll.get()
            self.xview_moveto(fraction=first)
        elif args[0] == "moveto":
            self.xview_moveto(fraction=float(args[1]))
        elif args[0] == "scroll":
            self.xview_scroll(number=int(args[1]), what=args[2])
        else:
            return

    def xview_moveto(self, fraction: float):
        """Update the horizontal position of the content frame within the
        container.

        Parameters:

            fraction (float):
                The relative position of the content frame within the
                container.
        """
        base, thumb = self._xmeasures()

        if fraction < 0:
            first = 0.0
        elif (fraction + thumb) > 1:
            first = 1 - thumb
        else:
            first = fraction
        self.hscroll.set(first, first + thumb)
        self.content_place(relx=-first * base)
        debug(
            f"xview_moveto: {base=}, {thumb=} {fraction=} {first=} {first + thumb=} rely: {-first * base=}"
        )

    def xview_scroll(self, number: int, what: str):
        """Update the horizontal position of the content frame within the
        container.

        Parameters:

            number (int):
                The amount by which the content frame will be moved
                within the container frame by 'what' units.

            what (str):
                The type of units by which the number is to be interpeted.
                This parameter is currently not used and is assumed to be
                'units'.
        """
        first, _ = self.hscroll.get()
        fraction = (number / 100) + first
        self.xview_moveto(fraction)

    def _add_scroll_binding(self, parent):
        """Recursive adding of scroll binding to all descendants."""
        children = parent.winfo_children()
        for widget in [parent, *children]:
            bindings = widget.bind()
            if self.winsys.lower() == "x11":
                if "<Button-4>" in bindings or "<Button-5>" in bindings:
                    continue
                else:
                    widget.bind("<Button-4>", self._on_mousewheel, "+")
                    widget.bind("<Button-5>", self._on_mousewheel, "+")
            else:
                if "<MouseWheel>" not in bindings:
                    widget.bind("<MouseWheel>", self._on_mousewheel, "+")
            if widget.winfo_children() and widget != parent:
                self._add_scroll_binding(widget)

    def _del_scroll_binding(self, parent):
        """Recursive removal of scrolling binding for all descendants"""
        children = parent.winfo_children()
        for widget in [parent, *children]:
            if self.winsys.lower() == "x11":
                widget.unbind("<Button-4>")
                widget.unbind("<Button-5>")
            else:
                widget.unbind("<MouseWheel>")
            if widget.winfo_children() and widget != parent:
                self._del_scroll_binding(widget)

    def enable_scrolling(self):
        """Enable mousewheel scrolling on the frame and all of its
        children."""
        self._add_scroll_binding(self)

    def disable_scrolling(self):
        """Disable mousewheel scrolling on the frame and all of its
        children."""
        self._del_scroll_binding(self)

    def hide_scrollbars(self):
        """Hide the scrollbars."""
        if self.vscroll:
            self.vscroll.pack_forget()
        if self.hscroll:
            self.hscroll.pack_forget()

    def show_scrollbars(self):
        """Show the scrollbars."""
        if self.vscroll:
            self.vscroll.pack(side=tk.RIGHT, fill=tk.Y)
        if self.hscroll:
            self.hscroll.pack(side=tk.BOTTOM, fill=tk.X)

    def autohide_scrollbar(self):
        """Toggle the autohide funtionality. Show the scrollbars when
        the mouse enters the widget frame, and hide when it leaves the
        frame."""
        self.autohide = not self.autohide

    def _ymeasures(self):
        """Measure the base size of the container and the thumb size
        for use in the yview methods"""
        outer = self.container.winfo_height()
        inner = max([self.winfo_height(), outer])
        base = inner / outer
        if inner == outer:
            thumb = 1.0
        else:
            thumb = outer / inner
        debug(f"_ymeasures {base=} {thumb=}")
        return base, thumb

    def _xmeasures(self):
        """Calculate the size of the horizontal scrollbar thumb and base as fraction 0 to 1."""
        total_width = self.container.winfo_reqwidth()
        visible_width = self.winfo_width()
        if visible_width >= total_width:
            return 0, 1.0
        else:
            # thumb_width = max(int(visible_width / total_width * visible_width), 1)
            thumb_width = visible_width / total_width
            base_width = total_width / visible_width
            debug(f"_xmeasures {base_width=} {thumb_width=}")
            return base_width, thumb_width

    def _on_map_child(self, event):
        """Callback for when a widget is mapped to the content frame."""
        if self.container.winfo_ismapped():
            self.yview()
            self.xview()

    def _on_enter(self, event):
        """Callback for when the mouse enters the widget."""
        self.enable_scrolling()
        if self.autohide:
            self.show_scrollbars()

    def _on_leave(self, event):
        """Callback for when the mouse leaves the widget."""
        self.disable_scrolling()
        if self.autohide:
            self.hide_scrollbars()

    def _on_configure(self, event):
        """Callback for when the widget is configured"""
        self._resize_container()
        self.yview()
        self.xview()

    def _on_map(self, event):
        self._resize_container()
        self.yview()
        self.xview()

    def _on_mousewheel(self, event):
        """Callback for when the mouse wheel is scrolled."""
        if self.winsys.lower() == "win32":
            delta = -int(event.delta / 120)
        elif self.winsys.lower() == "aqua":
            delta = -event.delta
        elif event.num == 4:
            delta = -10
        elif event.num == 5:
            delta = 10
        self.yview_scroll(delta, tk.UNITS)
