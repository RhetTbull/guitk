""" Simple hello world example using guitk demoing use of the event handler """

from guitk import Button, Entry, Event, EventType, Label, Row, VerticalLayout, Window


class HelloWorld(Window):
    def config(self):
        """Define the window's contents and configuration"""

        self.title = "Hello, World"

        with VerticalLayout():
            Label("What's your name?")
            Entry(key="ENTRY_NAME", events=True, focus=True)
            Label("", width=40, key="OUTPUT")
            with Row():
                Button("Ok")
                Button("Quit")

    def handle_event(self, event: Event):
        """Interact with the Window using an event loop"""

        if event.key == "Quit":
            self.quit()

        if event.key == "Ok" or event.event_type == EventType.EntryReturn:
            # set the output Label to the value of the Entry box
            self[
                "OUTPUT"
            ].value = f"Hello {self['ENTRY_NAME'].value}! Thanks for trying "


if __name__ == "__main__":
    HelloWorld().run()
