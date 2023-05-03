"""Demo to show how to use context managers to create widget layout"""

from guitk import (
    Button,
    Entry,
    Event,
    EventType,
    Label,
    Layout,
    ListBox,
    Row,
    Stack,
    Window,
)


class ShoppingList(Window):
    def config(self):
        self.title = "My Shopping List"

        with Layout() as layout:
            with Row():
                # these will be stacked horizontally (side by side)
                Label("Item to buy:")
                Entry(key="item", events=True)
                Button("Add", key="add")
            with Stack():
                # these will be stacked vertically (one on top of the other)
                Label("Shopping list", anchor="center")
                ListBox(key="list")
                Button("Quit", key="quit")

        self.layout = layout

    def handle_event(self, event: Event):
        print(event)
        if event.event_type == EventType.EntryReturn or event.key == "add":
            # add item to the list if user presses Enter in the Entry field
            # or clicks the Add button
            name = self["item"].value
            self["list"].append(name)

            # clear the Entry field
            self["item"].value = ""

        if event.key == "quit":
            self.quit()


if __name__ == "__main__":
    ShoppingList().run()
