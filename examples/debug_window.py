""" Demonstrates use of debug window """

import sys

import guitk


class MyWindow(guitk.Window):
    def config(self):
        self.title = "Demo Window"
        self.layout = [
            [guitk.Label("Type some text then click a button.")],
            [guitk.Entry(key="INPUT")],
            [guitk.Button("STDOUT"), guitk.Button("STDERR")],
        ]

    def setup(self):
        # launch a debug window
        # don't need to use .run() as event loop already running in the parent window
        guitk.DebugWindow(parent=self.window, output_width=100, output_height=30)

    def handle_event(self, event):
        value = self["INPUT"].value
        if event.key == "STDOUT":
            print(value)

        if event.key == "STDERR":
            print(value, file=sys.stderr)


if __name__ == "__main__":
    MyWindow().run()
