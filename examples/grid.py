"""Demo VGrid and HGrid containers"""

from guitk import *


class Demo(Window):
    def config(self):
        self.title = "Grid Demo"
        with VLayout():
            with VGrid(3) as self.vgrid:
                for i in range(11):
                    Button(f"VGrid {i}")
            HSeparator()
            with HGrid(3) as self.hgrid:
                for i in range(11):
                    Button(f"HGrid {i}")
            HSeparator()
            with HStack(expand=False):
                Button("Add")
                Button("Remove")

    @on("Add")
    def on_add(self):
        """Add a widget"""
        button_count = len(self.vgrid)
        self.vgrid.append(Button(f"VGrid {button_count}"))
        self.hgrid.append(Button(f"HGrid {button_count}"))

    @on("Remove")
    def on_remove(self):
        """Remove a widget"""
        if len(self.vgrid):
            self.vgrid.pop()
        if len(self.hgrid):
            self.hgrid.pop()


if __name__ == "__main__":
    Demo().run()
