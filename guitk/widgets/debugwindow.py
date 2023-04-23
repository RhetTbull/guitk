""" Debug Window that can be used to display debug information """

from .tk_text import Output
from .ttk_button import Button
from .ttk_entry import Entry
from .ttk_label import Label
from .window import Window


class DebugWindow(Window):
    """Debug window that captures stdout/stderr"""

    def __init__(self, output_width=80, output_height=20, **kwargs):
        self._output_width = output_width
        self._output_height = output_height
        super().__init__(**kwargs)

    def config(self):
        self.title = "Debug"
        self.padx = self.pady = 2
        self.layout = [
            [
                Label("Filter"),
                Entry(key="FILTER_TEXT", width=40),
                Button("Filter", key="FILTER"),
            ],
            [
                Output(
                    width=self._output_width,
                    height=self._output_height,
                    key="OUTPUT",
                    events=True,
                )
            ],
        ]

    def handle_event(self, event):
        if event.key in ["FILTER", "OUTPUT"]:
            filter = self["FILTER_TEXT"].value
            if filter:
                lines = self["OUTPUT"].value.split("\n")
                lines = [l for l in lines if filter in l]
                self["OUTPUT"].value = "\n".join(lines) + "\n"

