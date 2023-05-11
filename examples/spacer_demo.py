"""Demo of Spacer and VerticalSpacer widgets"""

from guitk import Label, Layout, Spacer, VerticalSpacer, VStack, Window


class SpacerDemo(Window):
    def config(self):
        self.title = "Spacer Demo"
        self.size = (640, 480)
        with Layout():
            with VStack():
                Label("Top left")
                VerticalSpacer()
                Label("Bottom left")
            Spacer()
            Label("Center")
            Spacer()
            with VStack():
                Label("Top right", sticky="e")
                VerticalSpacer()
                Label("Bottom right", sticky="e")


if __name__ == "__main__":
    SpacerDemo().run()
