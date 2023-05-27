""" Another Hello World example for guitk showing how to use the event handler """

import tkinter as tk

from guitk import *


class HelloWorld(Window):
    def config(self):  # sourcery skip: extract-method
        self.title = "Hello, World"

        # Define the window's contents
        # use variables to define rows to make your layout more readable
        # use guitk.Frame to group sub-layouts into columns
        with VLayout():
            Label("What's your name?")
            # some widgets like Entry do not send events by default
            # so use events=True to enable them
            Entry(key="ENTRY_NAME", events=True, focus=True)
            Label("", width=40, key="OUTPUT")
            with LabelFrame("Label Frame", labelanchor=tk.N):
                with HStack():
                    with VStack():
                        Output(width=20, height=10)
                        Label("Output", key="LABEL_OUTPUT", sticky=tk.N)
                    with VStack(valign="center"):
                        Checkbutton("Upper case", key="CHECK_UPPER")
                        Checkbutton("Green text", key="CHECK_GREEN")
            with HStack():
                Button("Ok")
                Button("Quit")

        # you can define custom default padding around widgets with padx, pady
        # see https://tkdocs.com/tutorial/grid.html#padding
        self.padx = 3
        self.pady = 3

    # Interact with the Window using an event Loop
    def handle_event(self, event: Event):
        if event.key == "Quit":
            self.quit()

        if event.key == "Ok" or event.event_type == EventType.EntryReturn:
            # set the output Label to the value of the Entry box
            # the Window class acts like a dictionary for looking up guitk element objects by key
            name = self["ENTRY_NAME"].value
            print(f"Hello {name}")
            self["OUTPUT"].value = f"Hello {name}! Thanks for trying guitk."

        if event.key == "CHECK_UPPER" and self["CHECK_UPPER"].value:
            # True if checked
            # "Upper case" check button is checked, so make text upper case
            self["OUTPUT"].value = self["OUTPUT"].value.upper()

        if event.key == "CHECK_GREEN":
            # change label text color to green if needed
            # use .widget to access the underlying ttk element for each object
            # tkinter is not abstracted -- you can easily use tkinter methods and properties if needed
            if self["CHECK_GREEN"].value:
                # checked
                self["OUTPUT"].widget["foreground"] = "green"
            else:
                # not checked
                self["OUTPUT"].widget["foreground"] = ""


if __name__ == "__main__":
    HelloWorld().run()
