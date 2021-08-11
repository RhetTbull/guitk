"""Example for guitk.Notebook, showing how to use add, insert """

import guitk


class NotebookWindow(guitk.Window):
    def config(self):
        # tabs can be added to the Notebook later, here tabs are added in setup() after the notebook is created
        self.layout = [
            [guitk.Notebook(key="NOTEBOOK")],
            [guitk.Button("Add", key="ADD"), guitk.Button("Insert", key="INSERT")],
        ]
        self.title = "Notebook"
        self.tab_count = 0

    def setup(self):
        # add a couple tabs to the notebook
        self.tab_count += 1
        self["NOTEBOOK"].add(
            text=f"Tab {self.tab_count}", layout=[[guitk.Label("Hello World")]]
        )
        self.tab_count += 1
        self["NOTEBOOK"].add(
            text=f"Tab {self.tab_count}",
            layout=[[guitk.Label(f"Tab {self.tab_count}")]],
        )

    def handle_event(self, event):
        if event.key == "ADD":
            self.tab_count += 1
            self["NOTEBOOK"].add(
                text=f"Tab {self.tab_count}",
                layout=[[guitk.Label(f"Tab {self.tab_count}")]],
            )

        if event.key == "INSERT":
            self.tab_count += 1
            self["NOTEBOOK"].insert(
                0,
                text=f"Tab {self.tab_count}",
                layout=[[guitk.Label(f"Tab {self.tab_count}")]],
            )


if __name__ == "__main__":
    NotebookWindow().run()
