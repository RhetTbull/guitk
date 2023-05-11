""" Demo of Separator and VerticalSeparator widgets """

from guitk import HLayout, Label, Separator, VerticalSeparator, VStack, Window


class SeparatorDemo(Window):
    def config(self):
        self.size = 320, 240
        with HLayout():
            Label("Hello")
            VerticalSeparator()
            Label("World")

            with VStack(width=200, valign="center"):
                Label("Hello", sticky="EW", weightx=1, anchor="center")
                Separator()
                Label("World", sticky="EW", weightx=1, anchor="center")


if __name__ == "__main__":
    SeparatorDemo().run()
