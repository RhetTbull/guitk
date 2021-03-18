""" Demonstrates use of BrowseFileButton and BrowseDirectoryButton """
import guitk


class BrowseFile(guitk.Window):
    def config(self):
        self.title = "Select a file"

        # use target_key to have BrowseFileButton/BrowseDirectoryButton update
        # the value of a target widget based on selected file or directory
        self.layout = [
            [
                guitk.Label("File:"),
                guitk.Entry(key="FILENAME"),
                guitk.BrowseFileButton(target_key="FILENAME"),
            ],
            [
                guitk.Label("Directory:"),
                guitk.Entry(key="DIRNAME"),
                guitk.BrowseDirectoryButton(target_key="DIRNAME"),
            ],
        ]

    def handle_event(self, event):
        print(event)


BrowseFile().run()
