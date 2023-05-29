"""Demo showing how to replace widgets with other widgets; used for testing and debugging"""

import guitk as ui


class ReplaceDemo(ui.Window):
    def config(self):
        self.size = 600, 600
        self.title = "Replace Demo"
        with ui.VLayout():
            ui.Label(
                "Replace the widgets below by clicking on them",
                anchor="center",
                sticky="ew",
                weightx=1,
            ).font(size=14, underline=True)
            ui.CheckButton(text="VLayout 1", key="vlayout_1")
            ui.CheckButton(text="VLayout 2", key="vlayout_2")
            ui.CheckButton(text="VLayout 3", key="vlayout_3")
            with ui.VStack(expand=False):
                ui.CheckButton(text="VStack 1", key="vstack_1")
                ui.CheckButton(text="VStack 2", key="vstack_2")
                ui.CheckButton(text="VStack 3", key="vstack_3")
            with ui.HStack(expand=False):
                ui.CheckButton(text="HStack 1", key="hstack_1")
                ui.CheckButton(text="HStack 2", key="hstack_2")
                ui.CheckButton(text="HStack 3", key="hstack_3")
            with ui.VGrid(rows=2, expand=False):
                for i in range(8):
                    ui.CheckButton(text=f"VGrid {i}", key=f"vgrid_{i}")
            with ui.HGrid(cols=2, expand=False):
                for i in range(8):
                    ui.CheckButton(text=f"HGrid {i}", key=f"hgrid_{i}")

    @ui.on(event_type=ui.EventType.CheckButton)
    def on_check(self, event: ui.Event):
        """Event handler for the CheckButton widgets"""
        ui.debug(f"on_check: {event.widget.key}")
        event.widget.replace(ui.Label(f"I've replaced {event.widget.key}"))


if __name__ == "__main__":
    ui.set_debug(True)
    ReplaceDemo().run()
