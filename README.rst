guitk: GUI Toolkit for TKinter
==============================

What is guitk?
------------------


GUITk is a declarative framework for building nice-looking, cross-platform GUIs with tkinter inspired by SwiftUI.

GUITk allows you to build complete GUI applications with a few lines of code. GUITk makes it easy to layout your GUI elements and respond to events using a declarative syntax. Because GUITk is built on top of tkinter, you can access the underlying tkinter API if you need to but for many use cases, you can build your GUI without needing to know much about tkinter.

GUITk is in alpha stage but is in constant development so check back frequently if this interests you or open an issue to start a conversation about what pain points this project could help you solve!

Example
--------
.. image:: https://raw.githubusercontent.com/RhetTbull/guitk/main/examples/hello.py.png

And here's the code:

.. code-block:: python
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
            with ui.HLayout():
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

License
-------
Published under the MIT License.

