"""Simple Hello World example using guitk """

import guitk as ui


# subclass guitk.Window as the starting point for your app's main window
class HelloWindow(ui.Window):
    def config(self):
        """Configure the window"""

        # set the window title
        self.title = "Hello, World"

        # define a layout for the window
        # the layout manager will automatically add widgets to the window
        with ui.VLayout():
            ui.Label("What's your name?")
            ui.Entry(key="name")
            ui.Button("Ok")

    @ui.on(key="Ok")
    def on_ok(self, event: ui.Event):
        """Handle the Ok button click"""
        print("Hello, ", self.get("name").value)


# run your event loop
if __name__ == "__main__":
    HelloWindow().run()
