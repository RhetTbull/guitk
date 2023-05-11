""" Demo of LabelEntry """

from guitk import HLayout, LabelEntry, Window


class LabelEntryWindow(Window):
    def config(self):
        self.title = "LabelEntry Example"
        with HLayout():
            LabelEntry("Enter text here", focus=True)


if __name__ == "__main__":
    LabelEntryWindow().run()
