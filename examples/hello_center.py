"""Hello World in center of window"""

from guitk import HLayout, Label, Window


class HelloWorldWindow(Window):
    def config(self):
        self.title = "Hello World"
        self.size = 200, 200
        with HLayout(valign="center", halign="center"):
            Label("Hello World")


if __name__ == "__main__":
    HelloWorldWindow().run()
