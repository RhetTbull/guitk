""" Demonstrates use of LinkLabel widget """

import guitk
from tkinter import ttk


class ClickMe(guitk.Window):
    def config(self):
        self.title = "Click me!"

        # you can pass tkinter.ttk options to the widgets
        # e.g. width and anchor
        self.layout = [
            [
                guitk.LinkLabel(
                    "Click me!",
                    width=20,
                    anchor="center",
                    key="CLICK_ME",
                    underline_font=True,
                )
            ]
        ]
        self.padx = 20
        self.pady = 20

    def setup(self):
        # setup gets called immediately before the window is shown

        # configure the Click Me label to be blue
        style = ttk.Style()
        style.configure("Blue.TLabel", foreground="blue")

        # use .widget to access the underlying tkinter ttk object, 
        # in this case, a tkinter.ttk.Label
        self["CLICK_ME"].widget.configure(style="Blue.TLabel")

    def handle_event(self, event):
        print(event)


if __name__ == "__main__":
    ClickMe().run()
