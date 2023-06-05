"""Example of how to use Panedwindow class"""

from guitk import (
    Button,
    HLabelPane,
    HLayout,
    HPane,
    Label,
    LabelEntry,
    PanedWindow,
    VLabelPane,
    VPane,
    VSeparator,
    VStack,
    Window,
)


class PanedDemo(Window):
    def config(self):
        self.title = "Panedwindow Demo"

        with HLayout():
            with VStack():
                Label("Horizontal PanedWindow", anchor="center", sticky="ew")
                with PanedWindow(
                    orient="horizontal", weightx=1, weighty=1, sticky="nsew"
                ):
                    with HPane():
                        LabelEntry("HPane")
                        Button("Hello")
                    with HLabelPane("Pane 2"):
                        LabelEntry("LabelPane")
                        Button("Hello")
                    with VPane():
                        LabelEntry("VerticalPane")
                        Button("Hello")
                    with VLabelPane("Pane 4"):
                        LabelEntry("VLabelPane")
                        Button("Hello")
            VSeparator()
            with VStack():
                Label("Vertical PanedWindow", anchor="center", sticky="ew")
                with PanedWindow(
                    orient="vertical", weightx=1, weighty=1, sticky="nsew"
                ):
                    with HPane():
                        LabelEntry("HPane")
                        Button("Hello")
                    with HLabelPane("Pane 2"):
                        LabelEntry("LabelPane")
                        Button("Hello")
                    with VPane():
                        LabelEntry("VPane")
                        Button("Hello")
                    with VLabelPane("Pane 4"):
                        LabelEntry("VLabelPane")
                        Button("Hello")


if __name__ == "__main__":
    PanedDemo().run()
