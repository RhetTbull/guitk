""" Example for guitk showing how to use lists of lists for creating GUI layout """

import guitk


class LayoutDemo(guitk.Window):

    layout = [
        [guitk.Label("Row 1"), guitk.Label("What's your name?")],
        [guitk.Label("Row 2"), guitk.Entry()],
        [guitk.Label("Row 3"), guitk.Button("Ok")],
    ]

    def handle_event(self, event):
        if event.key == "Ok":
            print("Ok!")


if __name__ == "__main__":
    LayoutDemo("Layouts are Lists of Lists", padx=5, pady=5).run()
