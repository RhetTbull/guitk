"""Hello World example using guitk """

from guitk import (
    Button,
    Entry,
    Event,
    EventType,
    Label,
    Row,
    VerticalLayout,
    Window,
    Frame,
)


# subclass guitk.Window as the starting point for your app's main window
class HelloWorld(Window):
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
        # use a Layout or VerticalLayout class to define the layout of the window
        with VerticalLayout() as layout:
            Label("What's your name?")
            Entry(key="ENTRY_NAME", events=True)
            Label("", width=40, key="OUTPUT", columnspan=2)
            with Row():
                # align these two buttons in a row
                Button("Ok")
                Button("Quit")

        self.layout = layout

        # optionally set size as a tuple of (width, height)
        self.size = (640, 480)

    def setup(self):
        # your setup() method is called by the Window class after config() just before the Window is displayed
        # use this to initialize any internal state you need
        # you do not need to provide a setup() method if no initialization is needed
        print("setup")

    def teardown(self):
        # your teardown() method is called by the Window class after the Window is closed
        # use this to clean up before the Window is destroyed
        # you do not need to provide a teardown() method if no cleanup is needed
        print("teardown")

    # Interact with the Window using an event Loop
    # every guitk.Window will call self.handle_event() to handle GUI events
    # event is a guitk.Event object
    def handle_event(self, event: Event):
        name = self["ENTRY_NAME"].value

        if event.key == "Quit":
            # a key wasn't supplied in `guitk.Button("Quit")` so guitk uses the name of the button
            # value passed to quit will be returned by HelloWorld.run()
            self.quit(name)

        if event.key == "Ok" or event.event_type == EventType.EntryReturn:
            # User pressed the OK button or the Return key inside the Entry box
            # set the output Label to the value of the Entry box
            # individual widgets can be accessed by their key; the window object acts as a dictionary of widgets
            self["OUTPUT"].value = f"Hello {name}! Thanks for trying guitk."


if __name__ == "__main__":
    # instantiate your Window class and run it
    name = HelloWorld().run()
    print(f"Hello {name}")
