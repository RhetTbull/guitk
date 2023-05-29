"""Demo VGrid and HGrid containers"""

from guitk import *


class Grid(Window):
    def config(self):
        self.title = "Grid Demo"
        with VLayout():
            with VGrid(3, vspacing=0, hspacing=(0, 20)) as self.vgrid:
                for i in range(11):
                    Button(f"VGrid {i}")
            HSeparator()
            with HGrid(3, vspacing=5, hspacing=(0, 5)) as self.hgrid:
                for i in range(11):
                    Button(f"HGrid {i}")
            HSeparator()
            with HStack(expand=False):
                Button("Add")
                Button("Remove")
            HSeparator()
            Label("", key="status")

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

    @on(event_type=EventType.ButtonPress)
    def on_button_press(self, event):
        """Update status label"""
        self.get("status").value = f"Button {event.widget.value} pressed"


if __name__ == "__main__":
    Grid().run()
