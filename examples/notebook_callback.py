"""Example for ui.Notebook widget, shows how to use command handlers instead of event loop """

import guitk as ui


class NotebookWindow(ui.Window):
    def config(self):
        """Configure the window."""

        self.title = "Notebook"

        with ui.HLayout():
            with ui.Notebook(key="NOTEBOOK"):
                with ui.Tab("Tab 1"):
                    ui.Label("Hello World")
                with ui.Tab("Tab 2"):
                    ui.Label("Tab 2")

    @ui.on(event_type=ui.EventType.NotebookTabChanged)
    def on_tab_change(self):
        nb = self["NOTEBOOK"].widget
        selected_tab = nb.tab(nb.select(), "text")
        print(f"Tab changed to tab: {selected_tab}")


if __name__ == "__main__":
    NotebookWindow().run()
