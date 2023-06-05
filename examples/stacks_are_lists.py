"""Demo showing how to use stacks as lists to add or remove widgets from a stack"""


import contextlib

from guitk import *


class Stacks(Window):
    def config(self):
        self.title = "Stacks are Lists"
        with VLayout():
            with HStack(expand=True):
                with VStack():
                    self.add_control_widgets()
                VSeparator()
                with VStack():
                    Label("VStack").font(weight="bold", underline=True)
                    with VStack(key="VStack") as self.vs:
                        ...
                VSeparator()
                with VStack():
                    Label("HStack").font(weight="bold", underline=True)
                    with HStack(key="HStack") as self.hs:
                        ...
                VSeparator()
                with VStack(expand=True):
                    Label("Popped").font(weight="bold", underline=True)
                    with VStack() as self.vs_popped:
                        ...
            HSeparator()
            with HStack(expand=False):
                Label("VStack:", key="vstack_count")
                Label("HStack:", key="hstack_count")
            HSeparator()
            Output(echo=True, weightx=1, sticky="nsew")

    def add_control_widgets(self):
        """Create the control widgets; must be called inside the Layout or Container context"""
        RadioButton("VStack", "stack", key="stack", value="VStack", selected=True)
        RadioButton("HStack", "stack", value="HStack")
        Button("Add")
        with HStack():
            Entry(
                key="index",
                default="1",
                width=3,
            )
            Button("Insert")
        with HStack():
            Entry(key="extend", default="2", width=3)
            Button("Extend")
        Button("Clear")
        with HStack():
            Entry(key="pop", default="0", width=3)
            Button("Pop")
            Entry(key="del", default="0", width=3)
            Button("Del")
        with HStack():
            Entry(key="remove", default="", width=10)
            Button("Remove")
        Button("Widgets", key="widgets", tooltip="Print list of widgets to Output")

    def setup(self):
        # place to store popped widgets
        self.popped = {}
        self.update_status_bar()

    @on(key="Add")
    def on_add(self):
        label = Label("Add")
        stack = self["stack"].value
        self[stack].append(label)

    @on(key="index")
    @on(key="Insert")
    def on_insert(self):
        idx = int(self["index"].value)
        label = Label("Insert")
        stack = self["stack"].value
        self[stack].insert(idx, label)

    @on(key="extend")
    @on(key="Extend")
    def on_extend(self):
        count = int(self["extend"].value)
        labels = [Label("Extend") for _ in range(count)]
        stack = self["stack"].value
        self[stack].extend(labels)

    @on(key="Clear")
    def on_clear(self):
        stack = self["stack"].value
        self[stack].clear()

    @on(key="pop")
    @on(key="Pop")
    def on_pop(self):
        idx = int(self["pop"].value)
        stack = self["stack"].value
        widget = self[stack].pop(idx)

        # add the popped widget to the ListBox and store it
        key = f"id_{id(widget)}"
        name = f"{stack} {widget.widget_type} {widget.key}"
        self.popped[key] = stack, widget
        self.vs_popped.append(Button(name, key=f"popped: {key}"))

    @on(key="del")
    @on(key="Del")
    def on_del(self):
        idx = int(self["pop"].value)
        stack = self["stack"].value
        with contextlib.suppress(IndexError):
            del self[stack][idx]

    @on(event_type=EventType.ButtonPress)
    def on_popped(self, event: Event):
        """Event handler for the popped widgets"""
        if not str(event.key).startswith("popped:"):
            return

        # popped widget was clicked, so add it back to the stack
        # and remove the button from the popped stack
        widget_name = str(event.key)[8:]
        stack, widget = self.popped[widget_name]
        print(widget_name, stack, widget, widget.widget)
        self[stack].append(widget)
        event.widget.destroy()

    @on(key="remove")
    @on(key="Remove")
    def on_remove(self):
        key = self["remove"].value
        stack = self["stack"].value
        self[stack].remove(key)

    @on(key="widgets")
    def on_widgets(self):
        """Print the list of widgets to the Output widget"""
        stack = self["stack"].value
        print(self[stack].widgets)

    def handle_event(self, event: Event):
        self.update_status_bar()

    def update_status_bar(self):
        """ "Update the status bar"""
        self["vstack_count"].value = f"VStack: {len(self.vs)}"
        self["hstack_count"].value = f"HStack: {len(self.hs)}"


if __name__ == "__main__":
    # set_debug(True)
    Stacks().run()
