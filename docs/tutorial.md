<!--* DO NOT EDIT tutorial.md, instead edit tutorial.mdpp and process with MarkdownPP using doit (see dodo.py) -->

# GUITk Tutorial

## Overview of the GUITk Library

GUITk is a declarative framework, built on [tkinter](https://docs.python.org/3/library/tkinter.html),
for building nice-looking, cross-platform GUIs in Python. The goal of GUITk is to make it easy to build
GUIs without knowing a lot about tkinter.
The GUITk object model is partially inspired by [SwiftUI](https://developer.apple.com/documentation/swiftui).

GUITk wraps tkinter widgets in GUITk objects. Instead of the standard tkinter geometry managers
([pack](https://docs.python.org/3/library/tkinter.html?highlight=tkinter#the-packer), 
[grid](https://tkdocs.com/tutorial/grid.html), [place](https://www.pythonguis.com/faq/pack-place-and-grid-in-tkinter/)),
GUITk uses declarative layout objects to place widgets in a window. GUITk also provides a declarative

### Why tkinter?

GUITk builds on tkinter because tkinter is a mature, stable, cross-platform GUI framework that is included
in the Python standard library. tkinter was first added to Python 1.4 in 1996 and runs on most platforms.
It is not, however, the easiest to use nor the most pythonic GUI framework. GUITk aims to make it easier
to build GUIs with tkinter. Standard tkinter widgets look somewhat dated but tkinter includes themed widgets
([ttk](https://docs.python.org/3/library/tkinter.ttk.html)) that look much better. GUITk uses ttk widgets
whenever possible.

## Basic Concepts

Let's start with an example. The following "hello world" example creates a window with a label, a text entry box, and a button.
When the user presses Return or clicks the button, a greeting is printed to the console.

<!--* This image updated with doit for README.md -->
![hello.py example](images/hello.py.png "Hello World example")

<!--* The code is updated with mdpp which is run from project root so include paths are relative to project root -->
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
        with ui.HLayout():
            ui.Label("What's your name?")
            ui.Entry(key="name", focus=True)
            ui.Button("Ok", key="ok")

    @ui.on(key="ok")
    def on_ok(self, event: ui.Event):
        """Handle the Ok button click"""
        print("Hello, ", self.get("name").value)


# run your event loop
if __name__ == "__main__":
    HelloWindow().run()
```

A few things to note about this example:

- The `HelloWindow` class subclasses `guitk.Window`. This is the starting point for your app's main window.
- The `HelloWindow` class defines a `config` method that configures the window. `config()` is a special method
   that is called by GUITk before the window is created. It is used to configure the window's title, size, and
   widgets. Your window class must define a `config()` method.
- Widgets are added to your window using a layout manager. Creating an instance of a layout manager within your
   `config()` method adds it to the window. The `HelloWindow` class uses an `HLayout()` layout manager which
    arranges widgets horizontally.
- Widgets, such as `Label` (static text), `Entry` (text entry box), and `Button`, are added to the window by
   creating instances of them within the context of the layout manager.
- Every widget has an optional key, which is a unique identifier for the widget. In this example, the "Ok" button
   has a key of "ok".
- Events (such as a button press) are handled using the `@on()` decorator. The `@on()` decorator is used to
   register a callback function that is called when the event occurs. In this example, the `on_ok()` function
    is called when the user presses Return or clicks the "Ok" button (because the button has a key of "ok" which
    the `on_ok()` function is registered to handle).

## Creating a Window

Every GUITk app must have at least one class that subclasses `guitk.Window`. This class is the starting point
for your app's main window. An app may have multiple windows but one of them must be the main window. The main
window is created by calling the `run()` method on the window class. The `run()` method starts the main event
loop and displays the window.

The `Window` class has a `config()` method that is called by GUITk before the window is created. You must define
a `config()` method in your window class in order to display any widgets in the window (and without widgets, your
window would be a pretty boring GUI). The config method will be automatically called by GUITk before the window
is displayed. You should not need to create an `__init__()` method in your window class as all configuration
is done in the `config()` method.

Here is a minimal window class:

<!--[[[cog
import os
os.system("python3 utils/screenshot.py docs/examples/minimal_window.py MinimalWindow docs/images/minimal_window.py.png --overwrite")
]]]-->
<!--[[[end]]]-->
![minimal_window.py example](https://raw.githubusercontent.com/RhetTbull/guitk/main/docs/images/minimal_window.py.png "Minimal Window example")

<!--* The code is updated with mdpp which is run from project root so include paths are relative to project root -->
```python
"""Minimal example of a GUITk Window"""

import guitk as ui


class MinimalWindow(ui.Window):
    def config(self):
        with ui.VLayout():
            ui.Label("Hello World!")

if __name__ == "__main__":
    MinimalWindow().run()```