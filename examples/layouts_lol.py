""" Example for guitk showing how to use lists of lists for creating GUI layout """

# This demo shows how to use lists of lists to create a GUI layout.
# The preferred way to create a GUI layout is to use the layout manager
# classes as context managers in your config() method.  However, if you
# prefer, you can create a list of lists to define your layout.
# Each inner list is a row (or HStack)

import guitk


class LayoutDemo(guitk.Window):
    def config(self):
        self.title = "Layouts are Lists of Lists"
        self.layout = [
            [guitk.Label("HStack 1"), guitk.Label("What's your name?")],
            [guitk.Label("HStack 2"), guitk.Entry()],
            [guitk.Label("HStack 3"), guitk.Button("Ok")],
        ]

    def handle_event(self, event):
        if event.key == "Ok":
            print("Ok!")


if __name__ == "__main__":
    LayoutDemo().run()
