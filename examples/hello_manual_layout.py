"""Simple Hello World example using guitk with manual layout"""

from guitk import Button, Entry, Event, HLayout, Label, Window


# subclass guitk.Window as the starting point for your app's main window
class HelloWindow(Window):
    def config(self):
        """Configure the window"""

        # set the window title
        self.title = "Hello, World"

        # define a layout for the window
        # the layout manager will automatically add widgets to the window
        # if you don't want to use the layout context manager
        # you can manually create the layout as a list of lists of widgets
        # each inner list is a row of widgets
        HLayout(
            [
                [Label("Hello")],
                [Label("Please enter your name:"), Entry(key="name")],
                [Button("Ok")],
            ]
        )

    # define your event loop
    # every guitk.Window will call self.handle_event to handle GUI events
    # event is a guitk.Event object
    def handle_event(self, event: Event):
        """Called when an event occurs"""
        if event.key == "Ok":
            print(f"Hello {self['name'].value}")


# run your event loop
if __name__ == "__main__":
    HelloWindow().run()
