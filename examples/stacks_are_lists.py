"""Demo showing how to use stacks as lists"""


from guitk import *


class Demo(Window):
    def config(self):
        with VLayout():
            with HStack():
                with VStack():
                    RadioButton(
                        "VStack", "stack", key="stack", value="VStack", selected=True
                    )
                    RadioButton("HStack", "stack", value="HStack")
                    Button("Add")
                    with HStack():
                        Entry(key="index", default="1", width=3)
                        Button("Insert")

                with VStack(key="VStack") as self.vs:
                    Label("VStack")
                VSeparator()
                with HStack(key="HStack") as self.hs:
                    Label("HStack")
            HSeparator()
            with HStack():
                Label("VStack:", key="vstack_count")
                Label("HStack:", key="hstack_count")

    def setup(self):
        print(self.vs.layout)
        self.update_status_bar()

    @on(key="Add")
    def on_add(self):
        label = Label("Add")
        stack = self["stack"].value
        self[stack].append(label)
        self.update_status_bar()

    @on(key="index")
    @on(key="Insert")
    def on_insert(self):
        idx = int(self["index"].value)
        label = Label("Insert")
        stack = self["stack"].value
        self[stack].insert(idx, label)
        self.update_status_bar()

    def update_status_bar(self):
        """ "Update the status bar"""
        self["vstack_count"].value = f"VStack: {len(self.vs)}"
        self["hstack_count"].value = f"HStack: {len(self.hs)}"


if __name__ == "__main__":
    set_debug(True)
    Demo().run()
