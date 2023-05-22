""" Example program showing how to use bind_command """


import guitk as gui


class HelloWorld(gui.Window):
    def config(self):
        self.title = "Hello, World"

        # Define the window's contents
        with gui.VLayout():
            gui.Label("What's your name?")
            gui.Entry(key="ENTRY_NAME", events=True)
            gui.Label("", width=40, key="OUTPUT")
            with gui.HStack():
                gui.Button("Ok", command=self.on_ok)
                gui.Button("Press Me", key="PRESSME")
                gui.Button("Quit", command=self.on_quit)

    def on_ok(self):
        print("Hello!")

    def on_quit(self):
        print("Goodbye!")

    def on_button(self):
        print("Button press!")

    def on_pressme(self):
        print("I got pressed!")

    def on_entry_press(self):
        print("Release me!")

    def setup(self):
        # commands can also be bound by event type or key value
        self.bind_command(event_type=gui.EventType.ButtonPress, command=self.on_button)
        self.bind_command(key="PRESSME", command=self.on_pressme)

        # commands can be bound via the widget as well
        self["ENTRY_NAME"].bind_event("<FocusIn>", command=self.on_entry_press)

    # Interact with the Window using an event Loop
    def handle_event(self, event):
        print(event)
        if event.key == "Quit":
            self.quit()

        if event.key == "Ok":
            # set the output Label to the value of the Entry box
            name = self["ENTRY_NAME"].value
            self["OUTPUT"].value = f"Hello {name}! Thanks for trying gui."


if __name__ == "__main__":
    HelloWorld().run()
