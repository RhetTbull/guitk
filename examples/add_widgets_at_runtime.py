"""Demo showing how to add widgets at runtime"""

import tkinter as tk

from guitk import (
    Button,
    HLayout,
    HStack,
    Label,
    VSeparator,
    VStack,
    Window,
    on,
)


class Demo(Window):
    def config(self):
        with HLayout():
            with VStack() as self.vs:
                Button("Say Hello", key="Hello")
            VSeparator()
            with HStack() as self.hs:
                Button("Say Goodbye", key="Goodbye")

    @on(key="Hello")
    def on_hello(self):
        label = Label("Hello")
        self.vs.add_widget(label)

    @on(key="Goodbye")
    def on_goodbye(self):
        label = Label("Goodbye")
        self.hs.add_widget(label)


if __name__ == "__main__":
    Demo().run()
