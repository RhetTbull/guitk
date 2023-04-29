"""Demo to show how to use context managers to create widget layout"""

import guitk


class ShoppingList(guitk.Window):
    def config(self):
        self.title = "My Shopping List"

        with guitk.Layout() as layout:
            with guitk.Row() as row:
                # these will be stacked horizontally (side by side)
                guitk.Label("Item to buy:")
                guitk.Entry(key="item", events=True)
                guitk.Button("Add", key="add")
            with guitk.Stack() as stack:
                # these will be stacked vertically (one on top of the other)
                guitk.Label("Shopping list", anchor="center")
                guitk.ListBox(key="list")
                guitk.Button("Quit", key="quit")

        self.layout = layout

    def handle_event(self, event: guitk.Event):
        print(event)
        if (
            event.key == "item" and event.event.keysym == "Return"
        ) or event.key == "add":
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
