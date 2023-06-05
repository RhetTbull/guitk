"""Tools for displaying tool-tips.

This includes:
 * an abstract base-class for different kinds of tooltips
 * a simple text-only Tooltip class

This code is copied directly from CPython source code:
https://github.com/python/cpython/blob/3.9/Lib/idlelib/tooltip.py

It has been modified to work with guitk and use ttk widgets.

It is licensed under the same license as python (PSF Software Foundation License Version 2).

PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2
--------------------------------------------

1. This LICENSE AGREEMENT is between the Python Software Foundation
("PSF"), and the Individual or Organization ("Licensee") accessing and
otherwise using this software ("Python") in source or binary form and
its associated documentation.

2. Subject to the terms and conditions of this License Agreement, PSF hereby
grants Licensee a nonexclusive, royalty-free, world-wide license to reproduce,
analyze, test, perform and/or display publicly, prepare derivative works,
distribute, and otherwise use Python alone or in any derivative version,
provided, however, that PSF's License Agreement and PSF's notice of copyright,
i.e., "Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021 Python Software Foundation;
All Rights Reserved" are retained in Python alone or in any derivative version
prepared by Licensee.

3. In the event Licensee prepares a derivative work that is based on
or incorporates Python or any part thereof, and wants to make
the derivative work available to others as provided herein, then
Licensee hereby agrees to include in any such work a brief summary of
the changes made to Python.

4. PSF is making Python available to Licensee on an "AS IS"
basis.  PSF MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
IMPLIED.  BY WAY OF EXAMPLE, BUT NOT LIMITATION, PSF MAKES NO AND
DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR FITNESS
FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF PYTHON WILL NOT
INFRINGE ANY THIRD PARTY RIGHTS.

5. PSF SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF PYTHON
FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS
A RESULT OF MODIFYING, DISTRIBUTING, OR OTHERWISE USING PYTHON,
OR ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.

6. This License Agreement will automatically terminate upon a material
breach of its terms and conditions.

7. Nothing in this License Agreement shall be deemed to create any
relationship of agency, partnership, or joint venture between PSF and
Licensee.  This License Agreement does not grant permission to use PSF
trademarks or trade name in a trademark sense to endorse or promote
products or services of Licensee, or any third party.

8. By copying, installing or otherwise using Python, Licensee
agrees to be bound by the terms and conditions of this License
Agreement.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class _TooltipBase:
    """abstract base class for tooltips"""

    def __init__(self, anchor_widget):
        """Create a tooltip.

        anchor_widget: the widget next to which the tooltip will be shown

        Note that a widget will only be shown when showtip() is called.
        """
        self.anchor_widget = anchor_widget
        self.tipwindow = None

    def __del__(self):
        self.hidetip()

    def showtip(self):
        """display the tooltip"""
        if self.tipwindow:
            return
        self.tipwindow = tw = tk.Toplevel(self.anchor_widget)
        # show no border on the top level window
        tw.wm_overrideredirect(1)
        try:
            # This command is only needed and available on Tk >= 8.4.0 for OSX.
            # Without it, call tips intrude on the typing process by grabbing
            # the focus.
            tw.tk.call(
                "::tk::unsupported::MacWindowStyle",
                "style",
                tw._w,
                "help",
                "noActivates",
            )
        except tk.TclError:
            pass

        self.position_window()
        self.showcontents()
        self.tipwindow.update_idletasks()  # Needed on MacOS -- see #34275.
        self.tipwindow.lift()  # work around bug in Tk 8.5.18+ (issue #24570)

    def position_window(self):
        """(re)-set the tooltip's screen position"""
        x, y = self.get_position()
        root_x = self.anchor_widget.winfo_rootx() + x
        root_y = self.anchor_widget.winfo_rooty() + y
        self.tipwindow.wm_geometry("+%d+%d" % (root_x, root_y))

    def get_position(self):
        """choose a screen position for the tooltip"""
        # The tip window must be completely outside the anchor widget;
        # otherwise when the mouse enters the tip window we get
        # a leave event and it disappears, and then we get an enter
        # event and it reappears, and so on forever :-(
        #
        # Note: This is a simplistic implementation; sub-classes will likely
        # want to override this.
        return 20, self.anchor_widget.winfo_height() + 1

    def showcontents(self):
        """content display hook for sub-classes"""
        # See ToolTip for an example
        raise NotImplementedError

    def hidetip(self):
        """hide the tooltip"""
        # Note: This is called by __del__, so careful when overriding/extending
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            try:
                tw.destroy()
            except tk.TclError:  # pragma: no cover
                pass


class _OnHoverTooltipBase(_TooltipBase):
    """abstract base class for tooltips, with delayed on-hover display"""

    def __init__(self, anchor_widget, hover_delay=1000):
        """Create a tooltip with a mouse hover delay.

        anchor_widget: the widget next to which the tooltip will be shown
        hover_delay: time to delay before showing the tooltip, in milliseconds

        Note that a widget will only be shown when showtip() is called,
        e.g. after hovering over the anchor widget with the mouse for enough
        time.
        """
        super(_OnHoverTooltipBase, self).__init__(anchor_widget)
        self.hover_delay = hover_delay

        self._after_id = None
        self._id1 = self.anchor_widget.bind("<Enter>", self._show_event)
        self._id2 = self.anchor_widget.bind("<Leave>", self._hide_event)
        self._id3 = self.anchor_widget.bind("<Button>", self._hide_event)

    def __del__(self):
        try:
            self.anchor_widget.unbind("<Enter>", self._id1)
            self.anchor_widget.unbind("<Leave>", self._id2)  # pragma: no cover
            self.anchor_widget.unbind("<Button>", self._id3)  # pragma: no cover
        except tk.TclError:
            pass
        super(_OnHoverTooltipBase, self).__del__()

    def _show_event(self, event=None):
        """event handler to display the tooltip"""
        if self.hover_delay:
            self.schedule()
        else:
            self.showtip()

    def _hide_event(self, event=None):
        """event handler to hide the tooltip"""
        self.hidetip()

    def schedule(self):
        """schedule the future display of the tooltip"""
        self.unschedule()
        self._after_id = self.anchor_widget.after(self.hover_delay, self.showtip)

    def unschedule(self):
        """cancel the future display of the tooltip"""
        after_id = self._after_id
        self._after_id = None
        if after_id:
            self.anchor_widget.after_cancel(after_id)

    def hidetip(self):
        """hide the tooltip"""
        try:
            self.unschedule()
        except ttk.TclError:  # pragma: no cover
            pass
        super(_OnHoverTooltipBase, self).hidetip()


class Hovertip(_OnHoverTooltipBase):
    "A tooltip that pops up when a mouse hovers over an anchor widget."

    def __init__(self, anchor_widget, text, hover_delay=1000):
        """Create a text tooltip with a mouse hover delay.

        anchor_widget: the widget next to which the tooltip will be shown
        hover_delay: time to delay before showing the tooltip, in milliseconds

        Note that a widget will only be shown when showtip() is called,
        e.g. after hovering over the anchor widget with the mouse for enough
        time.
        """
        super(Hovertip, self).__init__(anchor_widget, hover_delay=hover_delay)
        self.text = text

    def showcontents(self):
        label = ttk.Label(
            self.tipwindow,
            text=self.text,
            justify=tk.LEFT,
            relief=tk.SOLID,
            borderwidth=1,
        )
        label.pack()
