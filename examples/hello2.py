"""Hello World example using guitk """

import guitk


# subclass guitk.Window as the starting point for your app's main window
class HelloWorld(guitk.Window):
    # Define the window's contents
    # you must have a class variable named `layout` or you'll get an empty window
    # guitk.Label corresponds to a tkinter.ttk.Label, etc.
    # optionally provide a unique key to each element to easily reference the element later
    # layouts are lists of lists where each list corresponds to a row in the GUI
    layout = [
        [guitk.Label("What's your name?")],
        [guitk.Entry(key="ENTRY_NAME")],
        [guitk.Label("", width=40, key="OUTPUT", columnspan=2)],
        [guitk.Button("Ok"), guitk.Button("Quit")],
    ]

    # Interact with the Window using an event Loop
    # every guitk.Window will call self.handle_event to handle GUI events
    # event is a guitk.Event object
    def handle_event(self, event):
        if event.key == "Quit":
            self.quit()

        if event.key == "Ok":
            # set the output Label to the value of the Entry box
            name = event.values["ENTRY_NAME"]
            self["OUTPUT"].value = f"Hello {name}! Thanks for trying guitk."


if __name__ == "__main__":
    # instantiate your Window class with a title and run it
    HelloWorld("Hello, World").run()
