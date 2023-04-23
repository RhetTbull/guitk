<!-* DO NOT EDIT README.md, instead edit README.mdpp and process with MarkdownPP using build_readme.sh -->

# Python GUI Toolkit for TK (guitk)

## Synopsis

guitk is an experiment to design a lightweight framework that simplifies creating simple GUIs with [tkinter](https://docs.python.org/3/library/tkinter.html).  This is very much early alpha stage but in constant development so check back frequently if this interests you or open an issue to start a conversation about what pain points this project could help you solve!

guitk allows you to build complete GUI applications with a few lines of code. guitk allows you to use either an event loop, inspired by [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI#example-2---interactive-window), or callbacks for event handling. For simple apps, I find an event loop is easy and intuitive to use. guitk also allows you to layout your app using a simple grid, also inspired by [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI#layouts-are-funny-lol-) -- no need to learn about tkinter packing or grid managers. You provide your layout as a list of lists where each row in the list represents a row in a grid and each element in the row represents a column in the grid. This makes laying out your app very easy and intuitive. guitk also provides a hierarchical layout system inspired by [SwiftUI](https://developer.apple.com/documentation/swiftui) and [applepy](https://github.com/eduardohleite/applepy) which allows you to create complex layouts with minimal code.

## Code Example

### List of Lists Layout

![hello.py example](https://raw.githubusercontent.com/RhetTbull/guitk/main/examples/hello.py.png "Hello World example")

```python
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
        if event.key == "Ok":
            print(f"Hello {self['name'].value}")


# run your event loop
if __name__ == "__main__":
    HelloWindow().run()
```

### Hierarchical Layout

![context_layout.py example](https://raw.githubusercontent.com/RhetTbull/guitk/main/examples/context_layout.py.png "Hierarchical layout example")

```python
"""Demo to show how to use context managers to create widget layout"""

import guitk


class ShoppingList(guitk.Window):
    def config(self):
        self.title = "My Shopping List"

        with guitk.Layout() as layout:
            with guitk.HStack() as hs:
                # these will be stacked horizontally (side by side)
                guitk.Label("Item to buy:")
                guitk.Entry(key="item", events=True)
                guitk.Button("Add", key="add")
            with guitk.VStack() as vs:
                # these will be stacked vertically (one on top of the other)
                guitk.Label("Shopping list", anchor="center")
                guitk.ListBox(key="list")
                guitk.Button("Quit", key="quit")

        self.layout = layout

    def handle_event(self, event: guitk.Event):
        print(event)
        if (
            event.key == "item" and event.event.keysym == "Return"
        ) or event.key == "add":
            # add item to the list if user presses Enter in the Entry field
            # or clicks the Add button
            name = self["item"].value
            self["list"].append(name)

            # clear the Entry field
            self["item"].value = ""

        if event.key == "quit":
            self.quit()


if __name__ == "__main__":
    ShoppingList().run()
```

## Motivation

The goal of guitk is to make it very easy to create simple and attractive GUI apps with python. It borrows ideas from several other libraries include [PySimpleGUI](https://www.pysimplegui.org/en/latest/), [SwiftUI](https://developer.apple.com/documentation/swiftui), and [applepy](https://github.com/eduardohleite/applepy). guitk builds on [tkinter](https://docs.python.org/3/library/tkinter.html) which ships with the Python standard library and works across many platforms. tkinter is a mature and powerful GUI framework but requires a fair bit of boiler plate and understanding of the underlying framework to use effectively. guitk attempts to simplify this by providing a higher level interface to tkinter while still allowing you to access the underlying tkinter API if you need to.

guitk is not intended to fully abstract away the tkinter interface and you'll need some knowledge of tkinter to use guitk.  I highly recommend Mark Roseman's excellent [Modern Tkinter for Busy Python Developers](https://tkdocs.com/book.html) book as a starting point.

## Installation

* `python3 -m pip install guitk`

## Anatomy of a guitk program

![hello2.py example](https://raw.githubusercontent.com/RhetTbull/guitk/main/examples/hello2.py.png "Hello World example")

```python
"""Hello World example using guitk """

import guitk


# subclass guitk.Window as the starting point for your app's main window
class HelloWorld(guitk.Window):

    # every Window class needs a config() method that
    # defines the title and the layout (and optionally menu and other other settings)
    def config(self):
        # Your Window class needs to define a config() method that describes the layout, title, etc for your app
        # config() is called by the Window class when the Window is created

        # Title for the window
        self.title = "Hello, World"

        # Define the window's contents
        # guitk.Label corresponds to a tkinter.ttk.Label, etc.
        # optionally provide a unique key to each element to easily reference the element later
        # layouts are lists of lists where each list corresponds to a row in the GUI
        self.layout = [
            [guitk.Label("What's your name?")],
            [guitk.Entry(key="ENTRY_NAME", events=True)],
            [guitk.Label("", width=40, key="OUTPUT", columnspan=2)],
            [guitk.Button("Ok"), guitk.Button("Quit")],
        ]

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
    def handle_event(self, event):
        name = self["ENTRY_NAME"].value

        if event.key == "Quit":
            # a key wasn't supplied in `guitk.Button("Quit")` so guitk uses the name of the button
            # value passed to quit will be returned by HelloWorld.run()
            self.quit(name)

        if event.key == "Ok":
            # set the output Label to the value of the Entry box
            # individual widgets can be accessed by their key; the window object acts as a dictionary of widgets
            self["OUTPUT"].value = f"Hello {name}! Thanks for trying guitk."

        if event.event_type == guitk.EventType.KeyRelease:
            # events can be handled by event type as well as event key
            print(event)


if __name__ == "__main__":
    # instantiate your Window class and run it
    name = HelloWorld().run()
    print(f"HelloWorld: {name}")
```

guitk supports both an event-loop style of app-development (very similar to how PySimpleGUI works) and also callbacks which are triggered by events.  The above example can be rewritten using a callback style:

```python
"""Hello World example using guitk, shows how to use callback style instead of event loop """

import guitk


# subclass guitk.Window as the starting point for your app's main window
class HelloWorld(guitk.Window):

    # every Window class needs a config() method that
    # defines the title and the layout (and optionally menu and other other settings)
    def config(self):
        # Title for the window
        self.title = "Hello, World"

        # Define the window's contents
        # guitk.Label corresponds to a tkinter.ttk.Label, etc.
        # optionally provide a unique key to each element to easily reference the element later
        # layouts are lists of lists where each list corresponds to a row in the GUI
        # callbacks are functions that will be called when the user interact with the widget
        # callbacks are specified with the `command` parameter
        self.layout = [
            [guitk.Label("What's your name?")],
            [guitk.Entry(key="ENTRY_NAME", events=True, command=self.on_entry_changed)],
            [guitk.Label("", width=40, key="OUTPUT", columnspan=2)],
            [
                guitk.Button("Ok", command=self.on_ok),
                guitk.Button("Quit", command=self.on_quit),
            ],
        ]

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
        self["OUTPUT"].value = f"Hello {name}! Thanks for trying guitk."

    def on_entry_changed(self):
        print(self["ENTRY_NAME"].value)

    def on_quit(self):
        name = self["ENTRY_NAME"].value
        # value passed to quit will be returned by HelloWorld.run()
        self.quit(name)

    def handle_event(self, event):
        print(event)


if __name__ == "__main__":
    # instantiate your Window class and run it
    name = HelloWorld().run()
    print(f"HelloWorld: {name}")
```

guitk GUIs are created using a lists of lists where each element in the lists corresponds to a ttk or tk element.  This design pattern is borrowed from PySimpleGUI.

![layout_lol.py example](https://raw.githubusercontent.com/RhetTbull/guitk/main/examples/layouts_lol.py.png "Layout using lists of lists example")

```python
""" Example for guitk showing how to use lists of lists for creating GUI layout """

import guitk


class LayoutDemo(guitk.Window):
    def config(self):
        self.title = "Layouts are Lists of Lists"
        self.layout = [
            [guitk.Label("Row 1"), guitk.Label("What's your name?")],
            [guitk.Label("Row 2"), guitk.Entry()],
            [guitk.Label("Row 3"), guitk.Button("Ok")],
        ]

    def handle_event(self, event):
        if event.key == "Ok":
            print("Ok!")


if __name__ == "__main__":
    LayoutDemo().run()
```

Because layouts are simply lists of lists, you can use python to create layouts programmatically, for example using list comprehensions.

![layout2.py example](https://github.com/RhetTbull/guitk/raw/main/examples/layout2.py.png "Layout using list comprehensions, with tooltips!")

```python
""" Example for guitk showing how to use list comprehensions to create a GUI """

import guitk


class LayoutDemo(guitk.Window):
    def config(self):
        self.title = "List Comprehension"
        # use list comprehension to generate 4x4 grid of buttons with tooltips
        # use the tooltip named argument to add tooltip text to any element
        self.layout = [
            [
                guitk.Button(
                    f"{row}, {col}", padx=0, pady=0, tooltip=f"Tooltip: {row},{col}"
                )
                for col in range(4)
            ]
            for row in range(4)
        ]

    # Interact with the Window using an event Loop
    def handle_event(self, event):
        if event.event_type == guitk.EventType.ButtonPress:
            # print the key for the button that was pressed
            print(self[event.key].value)


if __name__ == "__main__":
    LayoutDemo().run()
```

A more complex example showing how to use the event handler to react to events and change the value of other GUI elements.

![hello4.py example](https://github.com/RhetTbull/guitk/raw/main/examples/hello4.py.png "A more complex example showing how to use the event handler.")

```python
""" Another Hello World example for guitk showing how to use the event handler """

import guitk
import tkinter as tk


class HelloWorld(guitk.Window):

    def config(self):
        self.title = "Hello, World"

        # Define the window's contents
        # use variables to define rows to make your layout more readable
        # use guitk.Frame to group sub-layouts into columns
        label_frame = guitk.LabelFrame(
            "Label Frame",
            labelanchor=tk.N,
            layout=[
                [
                    guitk.Frame(
                        layout=[
                            [guitk.Output(width=20, height=10)],
                            [guitk.Label("Output", key="LABEL_OUTPUT", sticky=tk.S)],
                        ]
                    ),
                    guitk.Frame(
                        layout=[
                            [None, guitk.Checkbutton("Upper case", key="CHECK_UPPER")],
                            [None, guitk.Checkbutton("Green text", key="CHECK_GREEN")],
                        ],
                        sticky="n",
                    ),
                ]
            ],
        )

        self.layout = [
            [guitk.Label("What's your name?")],
            [guitk.Entry(key="ENTRY_NAME")],
            [guitk.Label("", width=40, key="OUTPUT")],
            [label_frame],
            [guitk.Button("Ok"), guitk.Button("Quit")],
        ]

        # you can define custom padding around widgets with padx, pady
        # see https://tkdocs.com/tutorial/grid.html#padding
        self.padx = 3
        self.pady = 3

    # Interact with the Window using an event Loop
    def handle_event(self, event):
        if event.key == "Quit":
            self.quit()

        if event.key == "Ok":
            # set the output Label to the value of the Entry box
            # the Window class acts like a dictionary for looking up guitk element objects by key
            name = self["ENTRY_NAME"].value
            print(f"Hello {name}")
            self["OUTPUT"].value = f"Hello {name}! Thanks for trying guitk."

        if event.key == "CHECK_UPPER" and self["CHECK_UPPER"].value:
            # True if checked
            # "Upper case" check button is checked, so make text upper case
            self["OUTPUT"].value = self["OUTPUT"].value.upper()

        if event.key == "CHECK_GREEN":
            # change label text color to green if needed
            # use .widget to access the underlying ttk element for each object
            # tkinter is not abstracted -- you can easily use tkinter methods and properties if needed
            if self["CHECK_GREEN"].value:
                # checked
                self["OUTPUT"].widget["foreground"] = "green"
            else:
                # not checked
                self["OUTPUT"].widget["foreground"] = ""


if __name__ == "__main__":
    # add some padding around GUI elements to make it prettier
    HelloWorld().run()
```

You can create virtual events that fire after a time delay and these can be repeating.

![bind_timer_event example](https://github.com/RhetTbull/guitk/raw/main/examples/bind_timer_event.py.png "Creating timed virtual events.")

```python
""" Example showing how to use bind_timer_event """

import time
import tkinter as tk

import guitk


class TimerWindow(guitk.Window):
    def config(self):
        self.title = "Timer Window"

        self.layout = [
            [guitk.Label("Press Start Timer to fire event after 2000 ms")],
            [guitk.Label("", width=60, key="OUTPUT")],
            [
                guitk.Button("Start Timer"),
                guitk.Button("Cancel Timer"),
                guitk.Checkbutton("Repeat", key="REPEAT"),
            ],
        ]

    def setup(self):
        # store the id of the running timer so it can be cancelled
        self.data = {"timer_id": None}

    # Interact with the Window using an event Loop
    def handle_event(self, event):
        if event.key == "Quit":
            self.quit()

        if event.key == "Start Timer":
            # this simple demo assumes only one timer running at a time
            repeat = self["REPEAT"].value  # value of Repeat Checkbutton
            self.data["timer_id"] = self.bind_timer_event(
                2000, "<<MyTimer>>", repeat=repeat
            )
            self[
                "OUTPUT"
            ].value = f"Timer {self.data['timer_id']} started at {time.time():.2f}"

        if event.key == "<<MyTimer>>":
            self["OUTPUT"].value = f"Timer went off at {time.time():.2f}!"

        if event.key == "Cancel Timer":
            self.cancel_timer_event(self.data["timer_id"])
            self[
                "OUTPUT"
            ].value = f"Timer {self.data['timer_id']} canceled at {time.time():.2f}"


if __name__ == "__main__":
    TimerWindow().run()
```

You can access the underlying ttk widget, for example, to change style.  guitk also implements some additional widgets link `LinkLabel` which is a `ttk.Label()` that generates an event when clicked and changes mouse cursor to pointing hand (like a URL does).

![LinkLabel example](https://github.com/RhetTbull/guitk/raw/main/examples/link.py.png "Using LinkLabel widget.")

```python
""" Demonstrates use of LinkLabel widget """

import guitk
from tkinter import ttk


class ClickMe(guitk.Window):
    def config(self):
        self.title = "Click me!"

        # you can pass tkinter.ttk options to the widgets
        # e.g. width and anchor
        self.layout = [
            [
                guitk.LinkLabel(
                    "Click me!",
                    width=20,
                    anchor="center",
                    key="CLICK_ME",
                    underline_font=True,
                )
            ]
        ]
        self.padx = 20
        self.pady = 20

    def setup(self):
        # setup gets called immediately before the window is shown

        # configure the Click Me label to be blue
        style = ttk.Style()
        style.configure("Blue.TLabel", foreground="blue")

        # use .widget to access the underlying tkinter ttk object, 
        # in this case, a tkinter.ttk.Label
        self["CLICK_ME"].widget.configure(style="Blue.TLabel")

    def handle_event(self, event):
        print(event)


if __name__ == "__main__":
    ClickMe().run()
```

## Documentation

Not much documentation at this point.  Take a look at the [examples](https://github.com/RhetTbull/guitk/tree/main/examples) directory for a number of self-documenting examples on use of various widgets.

## Testing

There are currently no automated tests as I haven't figured out how to do these with tkinter.  You can run `python3 -m guitk` which opens a window with examples of all the widgets.  I currently use this for testing to ensure each widget still works but it's a manual process.

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
* [ ] Other widgets
* [ ] Menus
* [x] Tooltips
* [ ] Documentation
* [x] Add docstrings
* [x] Add type hints to public API
* [ ] Tests

## License

MIT License with exception of `tooltips.py` which is licensed under the Python Software Foundation License Version 2 because it includes code from the Python standard library. Both are very permissive licenses.
