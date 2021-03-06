""" Another Hello World example for guitk showing how to use the event handler """

import guitk
import tkinter as tk


class HelloWorld(guitk.Window):

    def config(self):
        self.title = "Hello, World"

        # Define the window's contents
        # use variables to define rows to make your layout more readable
        # use guitk.Frame to group sub-layouts into columns
        label_frame = guitk.LabelFrame(
            "Label Frame",
            labelanchor=tk.N,
            layout=[
                [
                    guitk.Frame(
                        layout=[
                            [guitk.Output(width=20, height=10)],
                            [guitk.Label("Output", key="LABEL_OUTPUT", sticky=tk.S)],
                        ]
                    ),
                    guitk.Frame(
                        layout=[
                            [None, guitk.Checkbutton("Upper case", key="CHECK_UPPER")],
                            [None, guitk.Checkbutton("Green text", key="CHECK_GREEN")],
                        ],
                        sticky="n",
                    ),
                ]
            ],
        )

        self.layout = [
            [guitk.Label("What's your name?")],
            [guitk.Entry(key="ENTRY_NAME")],
            [guitk.Label("", width=40, key="OUTPUT")],
            [label_frame],
            [guitk.Button("Ok"), guitk.Button("Quit")],
        ]

        # you can define custom padding around widgets with padx, pady
        # see https://tkdocs.com/tutorial/grid.html#padding
        self.padx = 3
        self.pady = 3

    # Interact with the Window using an event Loop
    def handle_event(self, event):
        if event.key == "Quit":
            self.quit()

        if event.key == "Ok":
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
    # add some padding around GUI elements to make it prettier
    HelloWorld().run()
