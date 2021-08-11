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
            nb = self["NOTEBOOK"].widget
            selected_tab = nb.tab(nb.select(), "text")
            print(f"Tab changed to tab: {selected_tab}")


if __name__ == "__main__":
    NotebookWindow().run()
