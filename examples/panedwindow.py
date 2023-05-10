"""Example of how to use Panedwindow class"""

from guitk import (
    Button,
    LabelEntry,
    LabelPane,
    Layout,
    Pane,
    PanedWindow,
    VerticalLabelPane,
    VerticalPane,
    VerticalSeparator,
    Window,
)


class PanedDemo(Window):
    def config(self):
        self.title = "Panedwindow Demo"

        with Layout():
            with PanedWindow(orient="horizontal", weightx=1, weighty=1, sticky="nsew"):
                with Pane():
                    LabelEntry("Pane")
                    Button("Hello")
                with LabelPane("Pane 2"):
                    LabelEntry("LabelPane")
                    Button("Hello")
                with VerticalPane():
                    LabelEntry("VerticalPane")
                    Button("Hello")
                with VerticalLabelPane("Pane 4"):
                    LabelEntry("VerticalLabelPane")
                    Button("Hello")
            VerticalSeparator()
            with PanedWindow(orient="vertical", weightx=1, weighty=1, sticky="nsew"):
                with Pane():
                    LabelEntry("Pane")
                    Button("Hello")
                with LabelPane("Pane 2"):
                    LabelEntry("LabelPane")
                    Button("Hello")
                with VerticalPane():
                    LabelEntry("VerticalPane")
                    Button("Hello")
                with VerticalLabelPane("Pane 4"):
                    LabelEntry("VerticalLabelPane")
                    Button("Hello")


if __name__ == "__main__":
    PanedDemo().run()
