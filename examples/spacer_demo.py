"""Demo of Spacer and VerticalSpacer widgets"""

from guitk import Label, Layout, Spacer, Stack, VerticalSpacer, Window


class SpacerDemo(Window):
    def config(self):
        self.title = "Spacer Demo"
        self.size = (640, 480)
        with Layout() as layout:
            with Stack():
                Label("Hello")
                VerticalSpacer()
                Label("Always on the bottom")
            Spacer()
            Label("Always on the right", sticky="nw")
        self.layout = layout


if __name__ == "__main__":
    SpacerDemo().run()