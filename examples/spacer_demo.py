"""Demo of HSpacer and VSpacer widgets"""

from guitk import Label, Layout, HSpacer, VSpacer, VStack, Window


class SpacerDemo(Window):
    def config(self):
        self.title = "Spacer Demo"
        self.size = (640, 480)
        with Layout():
            with VStack():
                Label("Top left")
                VSpacer()
                Label("Bottom left")
            HSpacer()
            Label("Center")
            HSpacer()
            with VStack():
                Label("Top right", sticky="e")
                VSpacer()
                Label("Bottom right", sticky="e")


if __name__ == "__main__":
    SpacerDemo().run()
