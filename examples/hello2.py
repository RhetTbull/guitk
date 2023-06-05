"""Hello World example using guitk """

import guitk as ui


class HelloWorld(ui.Window):
    # subclass guitk.Window as the starting point for your app's main window
    def config(self):
        # Your Window class needs to define a config() method that describes the layout, title, etc for your app
        # config() is called by the Window class when the Window is being created

        # Title for the window
        self.title = "Hello, World"

        # optionally set size as a tuple of (width, height)
        self.size = (320, 240)

        # you can also use self.geometry for consistency with tkinter
        # self.geometry = "320x240"

        # Define the window's contents
        # guitk.Label corresponds to a tkinter.ttk.Label, etc.
        # optionally provide a unique key to each element to easily reference the element later
        # use a HLayout or VLayout class to define the layout of the window
        # HLayout arranges widgets horizontally, VLayout arranges widgets vertically
        with ui.VLayout():
            # use a VLayout to stack the widgets vertically
            # standard tkinter layout options such as sticky and weight are supported
            ui.Label("What's your name?", sticky="ew", anchor="center", weightx=1)
            # most widgets emit events; Entry has events turned off by default so enable with events=True
            # each widget can be assigned a key, which should be unique, to easily reference the widget later
            # set focus=True so the Entry box has focus when the window is displayed
            ui.Entry(key="entry_name", events=True, focus=True, weightx=1, sticky="ew")
            ui.Label("", width=40, key="output")
            with ui.HStack():
                # align these two buttons in a horizontal row using HStack
                ui.Button("Ok")
                ui.Button("Quit")

    # Every Window class has 3 special methods that can be overridden to provide custom behavior
    # you do not need to provide any of these methods if you do not need to customize the default behavior
    # (the default behavior is to do nothing)
    # These special methods are: setup(), teardown(), and handle_event()

    def setup(self):
        """Perform any initialization needed before the Window is displayed"""
        # your setup() method is called by the Window class after config() just before the Window is displayed
        # use this to initialize any internal state you need
        # you do not need to provide a setup() method if no initialization is needed
        print("setup")

    def teardown(self):
        """Perform any cleanup needed before destroying the window"""
        # your teardown() method is called by the Window class after the Window is closed
        # use this to clean up before the Window is destroyed
        # you do not need to provide a teardown() method if no cleanup is needed
        print("teardown")

    def handle_event(self, event: ui.Event):
        """handle_event() is called by the Window class when an event occurs"""
        # you do not need to provide a handle_event() method if you prefer to use
        # the @on decorator to bind functions to events (see below)
        # handle_event() is a useful place to put code that needs to run for every event
        # or for use during debugging
        print(f"handle_event: {event}")

    @ui.on(key="Quit")
    def on_quit(self):
        # return the value of the Entry box
        self.quit(self["entry_name"].value)

    @ui.on(key="Ok")
    @ui.on(event_type=ui.EventType.EntryReturn)
    def on_ok(self):
        # User pressed the OK button or the Return key inside the Entry box
        # the @on decorator can be used to bind a function to an event
        # @on can be repeated to bind the function to multiple events
        # set the output Label to the value of the Entry box
        # individual widgets can be accessed by their key; the window object acts as a dictionary of widgets
        greeting = f"Hello {self['entry_name'].value}! Thanks for trying guitk."

        # if you prefer, you can use get() instead of the dictionary syntax
        self.get("output").value = greeting


if __name__ == "__main__":
    # instantiate your Window class and run it
    name = HelloWorld().run()
    print(f"Hello {name}")
