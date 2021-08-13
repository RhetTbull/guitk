"""Hello World example using guitk, shows how to use callback style instead of event loop """

import guitk


# subclass guitk.Window as the starting point for your app's main window
class HelloWorld(guitk.Window):

    # every Window class needs a config() method that
    # defines the title and the layout (and optionally menu and other other settings)
    def config(self):
        # Title for the window
        self.title = "Hello, World"

        # Define the window's contents
        # guitk.Label corresponds to a tkinter.ttk.Label, etc.
        # optionally provide a unique key to each element to easily reference the element later
        # layouts are lists of lists where each list corresponds to a row in the GUI
        # callbacks are functions that will be called when the user interact with the widget
        # callbacks are specified with the `command` parameter
        self.layout = [
            [guitk.Label("What's your name?")],
            [guitk.Entry(key="ENTRY_NAME", events=True, command=self.on_entry_changed)],
            [guitk.Label("", width=40, key="OUTPUT", columnspan=2)],
            [
                guitk.Button("Ok", command=self.on_ok),
                guitk.Button("Quit", command=self.on_quit),
            ],
        ]

    def setup(self):
        # this method is called after the window is created
        # you can use it to set up any internal state you need

        # bind_event_command() binds a callback command to a specific event,
        # in this case, when user hits return in the entry field, the same command as hitting "Ok" will be called
        # the widget objects can be accessed as self["KEY"] in setup() but not in config() as they aren't created until after config() is called
        self["ENTRY_NAME"].bind_event_command("<Return>", self.on_ok)

    def on_ok(self):
        # the underlying guitk widgets are accessible as self["KEY"]
        # the value of each widget is accessible as self["KEY"].value
        name = self["ENTRY_NAME"].value
        self["OUTPUT"].value = f"Hello {name}! Thanks for trying guitk."

    def on_entry_changed(self):
        print(self["ENTRY_NAME"].value)

    def on_quit(self):
        name = self["ENTRY_NAME"].value
        # value passed to quit will be returned by HelloWorld.run()
        self.quit(name)

    def handle_event(self, event):
        print(event)


if __name__ == "__main__":
    # instantiate your Window class and run it
    name = HelloWorld().run()
    print(f"HelloWorld: {name}")
