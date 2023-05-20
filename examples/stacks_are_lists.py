"""Demo showing how to use stacks as lists"""


from guitk import *


class Demo(Window):
    def config(self):
        with VLayout():
            with HStack():
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
            HSeparator()
            with HStack():
                Label("VStack:", key="vstack_count")
                Label("HStack:", key="hstack_count")

    def add_control_widgets(self):
        """Create the control widgets"""
        RadioButton("VStack", "stack", key="stack", value="VStack", selected=True)
        RadioButton("HStack", "stack", value="HStack")
        Button("Add")
        with HStack():
            Entry(key="index", default="1", width=3)
            Button("Insert")
        with HStack():
            Entry(key="extend", default="2", width=3)
            Button("Extend")
        Button("Clear")

    def setup(self):
        print(self.vs.layout)
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

    @debug_watch
    @on(key="Clear")
    def on_clear(self):
        print(self.vs.layout)
        stack = self["stack"].value
        self[stack].clear()
        print(self.vs.layout)

    def handle_event(self, event: Event):
        self.update_status_bar()

    def update_status_bar(self):
        """ "Update the status bar"""
        self["vstack_count"].value = f"VStack: {len(self.vs)}"
        self["hstack_count"].value = f"HStack: {len(self.hs)}"


if __name__ == "__main__":
    set_debug(True)
    Demo().run()
