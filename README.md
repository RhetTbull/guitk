<!--* DO NOT EDIT README.md, instead edit README.mdpp and process with MarkdownPP using build_readme.sh -->

# Python GUI Toolkit for TK (GUITk)

## Synopsis

GUITk is a declarative framework for building nice-looking, cross-platform GUIs with [tkinter](https://docs.python.org/3/library/tkinter.html) inspired by [SwiftUI](https://developer.apple.com/documentation/swiftui).

GUITk allows you to build complete GUI applications with a few lines of code. GUITk makes it easy to layout your GUI elements and respond to events using a declarative syntax. Because GUITk is built on top of tkinter, you can access the underlying tkinter API if you need to but for many use cases, you can build your GUI without needing to know much about tkinter.

GUITk apps are built by subclasses the `guitk.Window` class. Your GUI elements are layed out using a `guitk.HLayout` (horizontal layout) or `guitk.VLayout` (vertical layout) object which takes care of placing all widgets in the window using a declarative syntax. This is much simpler than using the underlying tkinter [grid manager](https://tkdocs.com/shipman/grid.html) or [pack](https://dafarry.github.io/tkinterbook/pack.htm) geometry managers.

GUITk is in alpha stage but is in constant development so check back frequently if this interests you or open an issue to start a conversation about what pain points this project could help you solve!

## Code Example

### Simple VLayout

![hello.py example](https://raw.githubusercontent.com/RhetTbull/guitk/main/examples/hello.py.png "Hello World example")

```python
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
```

## Motivation

The goal of GUITk is to make it very easy to create simple and attractive GUI apps with python. It borrows ideas from several other libraries include [PySimpleGUI](https://www.pysimplegui.org/en/latest/), [SwiftUI](https://developer.apple.com/documentation/swiftui), [textual](https://github.com/Textualize/textual), and [applepy](https://github.com/eduardohleite/applepy). GUITk builds on [tkinter](https://docs.python.org/3/library/tkinter.html) which ships with the Python standard library and works across many platforms. tkinter is a mature and powerful GUI framework but requires a fair bit of boiler plate and understanding of the underlying framework to use effectively. GUITk attempts to simplify this by providing a higher level interface to tkinter while still allowing you to access the underlying tkinter API if you need to.

Though you can build simple apps without knowing much about tkinter, GUITk is not intended to fully abstract away the tkinter interface. A basic understanding of tkinter will be helpful when building with GUITk. I highly recommend Mark Roseman's excellent [Modern Tkinter for Busy Python Developers](https://tkdocs.com/book.html) book as a starting point.


## Installation

* `python3 -m pip install guitk`

## Anatomy of a guitk program

![hello2.py example](https://raw.githubusercontent.com/RhetTbull/guitk/main/examples/hello2.py.png "Hello World example")

```python
"""Hello World example using guitk """

import guitk as ui


# subclass guitk.Window as the starting point for your app's main window
class HelloWorld(ui.Window):
    # every Window class needs a config() method that
    # defines the title and the layout (and optionally menu and other other settings)
    def config(self):
        # Your Window class needs to define a config() method that describes the layout, title, etc for your app
        # config() is called by the Window class when the Window is created

        # Title for the window
        self.title = "Hello, World"

        # optionally set size as a tuple of (width, height)
        self.size = (320, 240)

        # Define the window's contents
        # guitk.Label corresponds to a tkinter.ttk.Label, etc.
        # optionally provide a unique key to each element to easily reference the element later
        # use a HLayout or VLayout class to define the layout of the window
        with ui.VLayout():
            ui.Label("What's your name?", sticky="ew", anchor="center", weightx=1)
            ui.Entry(key="ENTRY_NAME", events=True, focus=True, sticky="ew", weightx=1)
            ui.Label("", width=40, key="OUTPUT", columnspan=2)
            with ui.HStack():
                # align these two buttons in a horizontal row
                ui.Button("Ok")
                ui.Button("Quit")

    def setup(self):
        # your setup() method is called by the Window class after config() just before the Window is displayed
        # use this to initialize any internal state you need
        # you do not need to provide a setup() method if no initialization is needed
        print("setup")

    def teardown(self):
        # your teardown() method is called by the Window class after the Window is closed
        # use this to clean up before the Window is destroyed
        # you do not need to provide a teardown() method if no cleanup is needed
        print("teardown")

    # Interact with the Window using an event Loop
    # every guitk.Window will call self.handle_event() to handle GUI events
    # event is a guitk.Event object
    def handle_event(self, event: ui.Event):
        name = self["ENTRY_NAME"].value

        if event.key == "Quit":
            # a key wasn't supplied in `guitk.Button("Quit")` so guitk uses the name of the button
            # value passed to quit will be returned by HelloWorld.run()
            self.quit(name)

        if event.key == "Ok" or event.event_type == ui.EventType.EntryReturn:
            # User pressed the OK button or the Return key inside the Entry box
            # set the output Label to the value of the Entry box
            # individual widgets can be accessed by their key; the window object acts as a dictionary of widgets
            self["OUTPUT"].value = f"Hello {name}! Thanks for trying guitk."


if __name__ == "__main__":
    # instantiate your Window class and run it
    name = HelloWorld().run()
    print(f"Hello {name}")
```

guitk supports both an event-loop style of app-development (very similar to how PySimpleGUI works) and also callbacks which are triggered by events.  The above example can be rewritten using a callback style:

```python
"""Hello World example using guitk, shows how to use callback style instead of event loop """

from guitk import Button, Entry, Event, HStack, Label, VLayout, Window


# subclass Window as the starting point for your app's main window
class HelloWorld(Window):
    # every Window class needs a config() method that
    # defines the title and the layout (and optionally menu and other other settings)
    def config(self):
        # Title for the window
        self.title = "Hello, World"

        # Define the window's contents
        # Label corresponds to a tkinter.ttk.Label, etc.
        # optionally provide a unique key to each element to easily reference the element later
        # callbacks are functions that will be called when the user interact with the widget
        # callbacks are specified with the `command` parameter
        with VLayout() as layout:
            Label("What's your name?")
            Entry(
                key="ENTRY_NAME", events=True, command=self.on_entry_changed, focus=True
            )
            Label("", width=40, key="OUTPUT", columnspan=2)
            with HStack():
                Button("Ok", command=self.on_ok)
                Button("Quit", command=self.on_quit)
        self.layout = layout

    def setup(self):
        # this method is called after the window is created
        # you can use it to set up any internal state you need

        # bind_event_command() binds a callback command to a specific event,
        # in this case, when user hits return in the entry field, the same command as hitting "Ok" will be called
        # the widget objects can be accessed as self["KEY"] in setup() but not in config() as they aren't created until after config() is called
        self["ENTRY_NAME"].bind_event("<Return>", command=self.on_ok)

    def on_ok(self):
        # the underlying guitk widgets are accessible as self["KEY"]
        # the value of each widget is accessible as self["KEY"].value
        name = self["ENTRY_NAME"].value
        self["OUTPUT"].value = f"Hello {name}! Thanks for trying "

    def on_entry_changed(self):
        print(self["ENTRY_NAME"].value)

    def on_quit(self):
        name = self["ENTRY_NAME"].value
        # value passed to quit will be returned by HelloWorld.run()
        self.quit(name)

    def handle_event(self, event: Event):
        print(event)


if __name__ == "__main__":
    # instantiate your Window class and run it
    name = HelloWorld().run()
    print(f"HelloWorld: {name}")
```

## Documentation

Not much documentation at this point.  Take a look at the [examples](https://github.com/RhetTbull/guitk/tree/main/examples) directory for a number of self-documenting examples on use of various widgets.

## Testing

There are currently no automated tests as I haven't figured out how to do these with tkinter. I am working on adding tests and there are several tests that run with `pytest` in the `tests` directory.  These are not automated and require user interaction.

You can also run `python3 -m guitk` which opens a window with examples of all the widgets. I find this useful for quick testing of layout and widget behavior.

## Contributors

Contributions welcome! If this project interests you, open an Issue or send a PR!

## TODO

* [x] Basic prototype
* [x] Frame
* [x] Label
* [x] Entry
* [x] Button
* [x] Checkbutton
* [x] Radiobutton
* [x] Text
* [x] ScrolledText
* [x] Treeview
* [x] Listbox
* [x] Combobox
* [ ] Spinner
* [ ] Other widgets
* [ ] Menus
* [x] Tooltips
* [ ] Documentation
* [x] Add docstrings
* [x] Add type hints to public API
* [ ] Tests

## License

Licensed under the MIT License.

## See Also

* [Textual](https://github.com/Textualize/textual) - An amazing Python framework for building user interfaces in the terminal.
* [PySimpleGUI](https://www.PySimpleGUI.org) - A Python GUI Framework.
* [applepy](https://github.com/eduardohleite/applepy) - A declarative GUI framework for developing native macOS applications in Python 3.
