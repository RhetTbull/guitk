""" Demo of LabelEntry """

from guitk import LabelEntry, Layout, Window


class LabelEntryWindow(Window):
    def config(self):
        self.title = "LabelEntry Example"
        with Layout():
            LabelEntry("Enter text here", focus=True)


if __name__ == "__main__":
    LabelEntryWindow().run()
