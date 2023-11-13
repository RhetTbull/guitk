"""Demo grid container with scrollbars"""

from guitk import *


class Grid(Window):
    def config(self):
        self.title = "Grid Demo"
        with VLayout():
            with HGrid(
                4,
                vspacing=0,
                hspacing=(0, 20),
                vscrollbar=True,
                autohide_scrollbars=True,
            ) as self.vgrid:
                for i in range(25):
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
        self.vgrid.append(Button(f"HGrid {button_count}"))

    @on("Remove")
    def on_remove(self):
        """Remove a widget"""
        if len(self.vgrid):
            self.vgrid.pop()

    @on(event_type=EventType.ButtonPress)
    def on_button_press(self, event):
        """Update status label"""
        self.get("status").value = f"Button {event.widget.value} pressed"


if __name__ == "__main__":
    Grid().run()
