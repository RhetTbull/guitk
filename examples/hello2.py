"""Hello World example using guitk """

import guitk


# subclass guitk.Window as the starting point for your app's main window
class HelloWorld(guitk.Window):

    # every Window class needs a config() method that
    # defines the title and the layout (and optionally menu and other other settings)
    def config(self):
        # Your Window class needs to define a config() method that describes the layout, title, etc for your app
        # config() is called by the Window class when the Window is created

        # Title for the window
        self.title = "Hello, World"

        # Define the window's contents
        # guitk.Label corresponds to a tkinter.ttk.Label, etc.
        # optionally provide a unique key to each element to easily reference the element later
        # layouts are lists of lists where each list corresponds to a row in the GUI
        self.layout = [
            [guitk.Label("What's your name?")],
            [guitk.Entry(key="ENTRY_NAME", events=True)],
            [guitk.Label("", width=40, key="OUTPUT", columnspan=2)],
            [guitk.Button("Ok"), guitk.Button("Quit")],
        ]

    def setup(self):
        # your setup() method is called by the Window class after config() just before the Window is displayed
        # use this to initialize any internal state you need
        # you do not need to provide a setup() method if no inialization is needed
        print("setup")

    def teardown(self):
        # your teardown() method is called by the Window class after the Window is closed
        # use this to clean up before the Window is destroyed
        # you do not need to provide a teardown() method if no cleanup is needed
        print("teardown")

    # Interact with the Window using an event Loop
    # every guitk.Window will call self.handle_event() to handle GUI events
    # event is a guitk.Event object
    def handle_event(self, event):
        name = self["ENTRY_NAME"].value

        if event.key == "Quit":
            # a key wasn't supplied in `guitk.Button("Quit")` so guitk uses the name of the button
            # value passed to quit will be returned by HelloWorld.run()
            self.quit(name)

        if event.key == "Ok":
            # set the output Label to the value of the Entry box
            # individual widgets can be accessed by their key; the window object acts as a dictionary of widgets
            self["OUTPUT"].value = f"Hello {name}! Thanks for trying guitk."

        if event.event_type == guitk.EventType.KeyRelease:
            # events can be handled by event type as well as even key
            print(event)


if __name__ == "__main__":
    # instantiate your Window class and run it
    name = HelloWorld().run()
    print(f"HelloWorld: {name}")
