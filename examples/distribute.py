"""Demo distribute property of HStack and VStack"""

from guitk import *


class Demo(Window):
    def config(self):
        self.size = (1000, 400)
        self.title = "Distribute Demo"
        with HLayout(valign="top"):
            with LabelFrame("VStack(distribute=False)", weighty=1, sticky="nsew"):
                with VStack():
                    Button("1")
                    Button("2")
                    Button("3")
            with LabelFrame("VStack(distribute=True)", weighty=1, sticky="nsew"):
                with VStack(distribute=True):
                    Button("1")
                    Button("2")
                    Button("3")
            with VStack():
                with LabelFrame("HStack(distribute=False)", weightx=1, sticky="nsew"):
                    with HStack():
                        Button("1")
                        Button("2")
                        Button("3")
                with LabelFrame("HStack(distribute=True)", weightx=1, sticky="nsew"):
                    with HStack(distribute=True):
                        Button("1")
                        Button("2")
                        Button("3")


if __name__ == "__main__":
    Demo().run()
