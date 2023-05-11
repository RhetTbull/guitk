"""Example for Notebook, showing how to use add, insert """

from guitk import (
    Button,
    Event,
    EventType,
    HStack,
    Label,
    Notebook,
    Tab,
    VerticalTab,
    VLayout,
    Window,
)


class NotebookWindow(Window):
    def config(self):
        # tabs can be added to the Notebook later, here tabs are added in setup() after the notebook is created
        with VLayout():
            Notebook(key="NOTEBOOK", sticky="nsew")
            with HStack():
                Button("Add", key="ADD")
                Button("Insert", key="INSERT")
        self.title = "Notebook"
        self.tab_count = 0

    def setup(self):
        # add a couple tabs to the notebook
        self.tab_count += 1
        with VerticalTab(f"Tab {self.tab_count}") as tab1:
            Label(f"Tab {self.tab_count}")
            Label("Hello World", anchor="center")

        self.tab_count += 1
        with Tab(f"Tab {self.tab_count}") as tab2:
            Label("Tab 2")

        self["NOTEBOOK"].add(tab1)
        self["NOTEBOOK"].add(tab2)

    def handle_event(self, event: Event):
        if event.key == "ADD":
            self.tab_count += 1
            with Tab(f"Tab {self.tab_count}") as tab:
                Label(f"Tab {self.tab_count}")

            self["NOTEBOOK"].add(tab)

        if event.key == "INSERT":
            self.tab_count += 1
            with Tab(f"Tab {self.tab_count}") as tab:
                Label(f"Tab {self.tab_count}")
            self["NOTEBOOK"].insert(0, tab)

        if event.event_type == EventType.NotebookTabChanged:
            # The name of the currently selected tab is available in Notebook.current_tab
            print(f"Tab changed to tab: {self['NOTEBOOK'].current_tab}")


if __name__ == "__main__":
    NotebookWindow().run()
