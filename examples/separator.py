""" Demo of HSeparator and VSeparator widgets """

from guitk import HLayout, HSeparator, Label, VSeparator, VStack, Window


class SeparatorDemo(Window):
    def config(self):
        self.size = 320, 240
        with HLayout():
            Label("Hello")
            VSeparator()
            Label("World")

            with VStack(width=200, valign="center"):
                Label("Hello", sticky="EW", weightx=1, anchor="center")
                HSeparator()
                Label("World", sticky="EW", weightx=1, anchor="center")


if __name__ == "__main__":
    SeparatorDemo().run()
