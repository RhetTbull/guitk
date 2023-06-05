"""Example for Notebook widget """

from guitk import EventType, HLayout, HTab, Label, Notebook, Window


class NotebookWindow(Window):
    def config(self):
        with HLayout():
            with Notebook(key="NOTEBOOK"):
                with HTab("Tab 1"):
                    Label("Hello World")
                with HTab("Tab 2"):
                    Label("Tab 2")
        self.title = "Notebook"

    def handle_event(self, event):
        if event.event_type == EventType.NotebookTabChanged:
            # The name of the currently selected tab is available in Notebook.current_tab
            print(f"Tab changed to tab: {self['NOTEBOOK'].current_tab}")


if __name__ == "__main__":
    NotebookWindow().run()
