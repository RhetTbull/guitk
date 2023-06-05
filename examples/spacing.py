"""Demo container spacing."""

# Horizontal and vertical spacing can be specified for HStack and VStack using
# the `hspacing` and `vspacing` keyword arguments. The value of these arguments
# can be either an integer or a tuple of two integers. If an integer is
# specified, it is used as the spacing between all widgets. If a tuple is
# specified, the first integer is left or top spacing and the second integer is
# right or bottom spacing.
# A widget can override the default Stack spacing by specifying its own `padx`
# and `pady` values. The `padx` and `pady` values can also be a single integer
# or a tuple of two integers.

from guitk import *


class Demo(Window):
    def config(self):
        self.title = "Spacing Demo"
        self.size = 640, 480
        self.padx = 0
        self.pady = 0
        with VLayout():
            with VStack():
                Label("vspacing=20")
                with VStack(vspacing=20):
                    Button("Hello")
                    Button("World")
            HSeparator()
            with VStack():
                Label("vspacing=0")
                with VStack(vspacing=0):
                    Button("Hello")
                    Button("World")
            HSeparator()
            with VStack():
                Label("hspacing=(0, 30), vspacing=(30, 0)")
                with HStack(hspacing=(0, 30), vspacing=(30, 0)):
                    Button("Hello")
                    Button("World")
            HSeparator()
            with VStack():
                Label("hspacing=0")
                with HStack(hspacing=0):
                    Button("Hello")
                    Button("World")
                    Button(
                        "But wait, this button has it's own spacing (padx=40)", padx=40
                    )


if __name__ == "__main__":
    Demo().run()
