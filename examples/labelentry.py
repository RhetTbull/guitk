""" Demo of LabelEntry """

from guitk import LabelEntry, Layout, Window


class LabelEntryWindow(Window):
    def config(self):
        self.title = "LabelEntry Example"
        with Layout() as layout:
            LabelEntry("Enter text here", focus=True)
        self.layout = layout


if __name__ == "__main__":
    LabelEntryWindow().run()
