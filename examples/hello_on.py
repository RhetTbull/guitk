"""Simple Hello World example using guitk demonstrating use of @on decorator"""

from guitk import Button, Entry, Event, EventType, Label, Layout, Window, on


# subclass guitk.Window as the starting point for your app's main window
class HelloWindow(Window):
    def config(self):
        """Configure the window"""

        # set the window title
        self.title = "Hello, World"

        # define a layout for the window
        # the layout manager will automatically add widgets to the window
        with Layout():
            Label("What's your name?")
            Entry(key="name", events=True, focus=True)
            Button("Ok")

    @on(event_type=EventType.EntryReturn)
    @on(key="Ok")
    def on_ok(self):
        """Called when the Ok button is pressed or user presses Enter in the Entry widget"""
        # @on decorator can be used to register event handlers
        # multiple @on decorators can be used to register the same handler for multiple events
        # decorator can be used with key, event_type, or both
        print(f"Hello {self['name'].value}")

    @on(event_type=EventType.ButtonPress)
    def on_button(self, event: Event):
        """Called when any button is pressed"""
        # if your function definition has an event parameter
        # it will be passed the Event object
        # if you don't need the event object, you can omit the parameter
        print(f"Button {event.key} was pressed")


# run your event loop
if __name__ == "__main__":
    HelloWindow().run()
