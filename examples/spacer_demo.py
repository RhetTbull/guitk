"""Demo of HSpacer and VSpacer widgets"""

from guitk import HLayout, HSpacer, Label, VSpacer, VStack, Window, set_debug


class SpacerDemo(Window):
    def config(self):
        self.title = "Spacer Demo"
        self.size = (640, 480)
        with HLayout():
            with VStack():
                Label("Top left")
                VSpacer()
                Label("Center left")
                VSpacer()
                Label("Bottom left")
            HSpacer()
            with VStack(halign="center"):
                Label("Top Center")
                VSpacer()
                Label("Center", anchor="center")
                VSpacer()
                Label("Bottom center", anchor="center")
            HSpacer()
            with VStack(halign="right"):
                Label("Top right")
                VSpacer()
                Label("Center right")
                VSpacer()
                Label("Bottom right")


if __name__ == "__main__":
    # set_debug(True)
    SpacerDemo().run()
