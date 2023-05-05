"""Demo of Spacer and VerticalSpacer widgets"""

from guitk import Label, Layout, Spacer, Stack, VerticalSpacer, Window


class SpacerDemo(Window):
    def config(self):
        self.title = "Spacer Demo"
        self.size = (640, 480)
        with Layout() as layout:
            with Stack():
                Label("Top left")
                VerticalSpacer()
                Label("Bottom left")
            Spacer()
            Label("Center")
            Spacer()
            with Stack():
                Label("Top right", sticky="e")
                VerticalSpacer()
                Label("Bottom right", sticky="e")
        self.layout = layout


if __name__ == "__main__":
    SpacerDemo().run()