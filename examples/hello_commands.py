""" Example program showing different ways to handle events in guitk"""


import guitk as ui


class HelloWorld(ui.Window):
    def config(self):
        self.title = "Hello, World"

        # Define the window's contents
        with ui.VLayout():
            ui.Label("What's your name?")
            ui.Entry(key="ENTRY_NAME")
            ui.Label("", width=40, key="OUTPUT")
            with ui.HStack():
                ui.Button("Ok")
                ui.Button("Press Me", key="PRESSME")
                ui.Button("Quit", command=self.on_quit)

    @ui.on(key="Ok")
    @ui.on(event_type=ui.EventType.EntryReturn)
    def on_ok(self):
        # commands can be bound to a key using the @on decorator
        # @on decorator can be used to respond to a key or an event type
        # @on decorator can be chained to respond to multiple keys or event types
        print("Hello!")

    def on_quit(self):
        # this is bound using the command keyword argument in the Button constructor
        print("Goodbye!")

    def on_button(self):
        print("Button press!")

    def on_pressme(self):
        print("I got pressed!")

    def on_entry_press(self):
        print("Release me!")

    def setup(self):
        # commands can also be bound by event type or key value
        self.bind_command(event_type=ui.EventType.ButtonPress, command=self.on_button)
        self.bind_command(key="PRESSME", command=self.on_pressme)

        # commands can be bound via the widget as well
        self["ENTRY_NAME"].bind_event("<FocusIn>", command=self.on_entry_press)

    # Interact with the Window using an event Loop
    def handle_event(self, event):
        # handle_event method will automatically run an event loop
        # handle_event will be called after bound commands have run
        print(event)
        if event.key == "Quit":
            self.quit()

        if event.key == "Ok":
            # set the output Label to the value of the Entry box
            name = self["ENTRY_NAME"].value
            self["OUTPUT"].value = f"Hello {name}! Thanks for trying ui."

    @ui.on(event_type=ui.EventType.Any)
    def on_any_event(self, event):
        """An event handler bound to EventType.Any will be called for every event"""
        print(f"Any event!: {event}")


if __name__ == "__main__":
    HelloWorld().run()
