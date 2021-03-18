import guitk


class HelloWorld(guitk.Window):
    def config(self):
        self.title = "Hello, World"
        # Define the window's contents
        self.layout = [
            [guitk.Label("What's your name?")],
            [guitk.Entry(key="ENTRY_NAME")],
            [guitk.Label("", width=40, key="OUTPUT")],
            [guitk.Button("Ok"), guitk.Button("Quit")],
        ]

    # Interact with the Window using an event Loop
    def handle_event(self, event):
        if event.key == "Quit":
            self.quit()

        if event.key == "Ok":
            # set the output Label to the value of the Entry box
            name = event.values["ENTRY_NAME"]
            self["OUTPUT"].value = f"Hello {name}! Thanks for trying guitk."


if __name__ == "__main__":
    HelloWorld().run()
