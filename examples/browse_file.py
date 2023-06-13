""" Demonstrates use of BrowseFileButton and BrowseDirectoryButton """
import guitk as ui


class BrowseFile(ui.Window):
    def config(self):
        self.title = "Select a file"

        # use target_key to have BrowseFileButton/BrowseDirectoryButton update
        # the value of a target widget based on selected file or directory
        with ui.VLayout():
            with ui.HStack():
                ui.Label("File:")
                ui.Entry(key="FILENAME")
                ui.BrowseFileButton(target_key="FILENAME")

            with ui.HStack():
                ui.Label("Directory:")
                ui.Entry(key="DIRNAME")
                ui.BrowseDirectoryButton(target_key="DIRNAME")

    def handle_event(self, event):
        print(event)


if __name__ == "__main__":
    BrowseFile().run()
