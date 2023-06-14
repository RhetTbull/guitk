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

<!--* The code is updated with mdpp which is run from proeject root so include paths are relative to project root -->
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
            ui.Button("Ok")

    @ui.on(key="Ok")
    @ui.on(event_type=ui.EventType.EntryReturn)
    def on_ok(self, event: ui.Event):
        """Handle the Ok button click or the Enter key press in the Entry box"""
        print("Hello, ", self.get("name").value)


# run your event loop
if __name__ == "__main__":
    HelloWindow().run()
```

## Creating a Window

## Creating a Layout

## Creating a Button

## Creating a Label
