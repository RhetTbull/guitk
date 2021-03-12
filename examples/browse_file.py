import guitk


class BrowseFile(guitk.Window):
    layout = [
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


BrowseFile("Select a file", padx=5, pady=5).run()
