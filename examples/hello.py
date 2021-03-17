"""Simple Hello World example using guitk """

import guitk


# subclass guitk.Window as the starting point for your app's main window
class HelloWindow(guitk.Window):

    def config(self):
        # define a layout for the window
        # you must have a class variable named `layout` or you'll get an empty window
        self.layout = [
            [guitk.Label("What's your name?")],
            [guitk.Entry(key="name")],
            [guitk.Button("Ok")],
        ]
        self.title = "Hello, World"

    # define your event loop
    # every guitk.Window will call self.handle_event to handle GUI events
    # event is a guitk.Event object
    def handle_event(self, event):
        print(f"Hello {event.values['name']}")


# run your event loop
if __name__ == "__main__":
    HelloWindow().run()
