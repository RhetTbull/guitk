"""Minimal example of a GUITk Window"""

import guitk as ui


class MinimalWindow(ui.Window):
    def config(self):
        with ui.VLayout():
            ui.Label("Hello World!")


if __name__ == "__main__":
    MinimalWindow().run()
