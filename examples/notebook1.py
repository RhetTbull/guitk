"""Example for guitk.Notebook widget """

import guitk


class NotebookWindow(guitk.Window):
    def config(self):
        tab1 = [[guitk.Label("Hello World")]]
        tab2 = [[guitk.Label("Tab 2")]]
        self.layout = [
            [guitk.Notebook(key="NOTEBOOK", tabs={"Tab 1": tab1, "Tab 2": tab2})]
        ]
        self.title = "Notebook"

    def handle_event(self, event):
        if event.event_type == guitk.EventType.NotebookTabChanged:
            # The name of the currently selected tab is available in Notebook.current_tab
            print(f"Tab changed to tab: {self['NOTEBOOK'].current_tab}")


if __name__ == "__main__":
    NotebookWindow().run()
