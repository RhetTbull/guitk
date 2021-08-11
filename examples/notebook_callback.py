"""Example for guitk.Notebook widget, shows how to use command handlers instead of event loop """

import guitk


class NotebookWindow(guitk.Window):
    def config(self):
        tab1 = [[guitk.Label("Hello World")]]
        tab2 = [[guitk.Label("Tab 2")]]
        self.layout = [
            [
                guitk.Notebook(
                    key="NOTEBOOK",
                    tabs={"Tab 1": tab1, "Tab 2": tab2},
                    command=self.on_tab_change,
                )
            ]
        ]
        self.title = "Notebook"

    def on_tab_change(self):
        nb = self["NOTEBOOK"].widget
        selected_tab = nb.tab(nb.select(), "text")
        print(f"Tab changed to tab: {selected_tab}")


if __name__ == "__main__":
    NotebookWindow().run()
