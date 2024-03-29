""" Demonstrates use of debug window """

import sys

import guitk as ui


class MyWindow(ui.Window):
    def config(self):
        self.title = "Demo Window"
        with ui.VLayout():
            ui.Label("Type some text then click a button.")
            ui.Entry(key="INPUT")
            ui.Button("STDOUT"), ui.Button("STDERR")

    def setup(self):
        # launch a debug window
        # don't need to use .run() as event loop already running in the parent window
        ui.DebugWindow(parent=self.window, output_width=100, output_height=30)

    def handle_event(self, event):
        value = self["INPUT"].value
        if event.key == "STDOUT":
            print(value)

        if event.key == "STDERR":
            print(value, file=sys.stderr)


if __name__ == "__main__":
    MyWindow().run()
