""" Demo of LabelEntry """

import guitk


class LabelEntryWindow(guitk.Window):
    def config(self):
        self.title = "LabelEntry Example"
        self.layout = [[guitk.LabelEntry("Enter text here")]]


if __name__ == "__main__":
    LabelEntryWindow().run()
