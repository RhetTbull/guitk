"""Demo for Spinbox widget."""


import guitk as ui


class SpinboxDemo(ui.Window):
    """Demo for Spinbox widget."""

    def config(self):
        self.title = "Spinbox Demo"
        self.size = 700, 400
        with ui.VLayout():
            with ui.HStack(halign="center"):
                ui.Label("Demo of different Spinbox options").font(size=14)
            ui.Label(
                "Pick a number between 1 and 10, use the up/down arrows; uses command="
            )
            with ui.HStack():
                # spinbox with command callback
                ui.SpinBox(
                    from_value=1,
                    to_value=10,
                    key="spinbox1",
                    tooltip="Spinbox that updates value with command=",
                    command=self.on_spinbox1_change,
                    focus=True,
                )
                ui.Label("Spinbox 1 value:", key="spinbox1_value")
            ui.Label("Pick a number between 1 and 3 with wrap = True and target_key")
            with ui.HStack():
                # spinbox with target_key, wrap=True
                # value wraps around when it reaches the limit
                # target_key is the key of the widget whose value will be updated
                # also note that SpinBox and Spinbox are equivalent
                ui.Spinbox(
                    from_value=1,
                    to_value=3,
                    wrap=True,
                    target_key="spinbox2_value",
                    key="spinbox2",
                )
                ui.Label("Spinbox 2 value :", padx=0)
                ui.Label("", key="spinbox2_value", padx=0)
            ui.Label("Pick a number between 0.0 and 1.0 with increment = 0.1")
            # spinbox with increment and float values
            ui.SpinBox(
                from_value=0.0,
                to_value=1.0,
                increment=0.1,
                key="spinbox3",
            )
            ui.Label("Pick a color")
            # spinbox with string values
            ui.SpinBox(
                values=("Red", "Green", "Blue", "Yellow", "Orange"), key="spinbox4"
            )
            ui.VSpacer()
            ui.HSeparator()
            with ui.HStack():
                ui.Label("Last Spinbox value:", key="status_last_value")
                ui.Label("Last Spinbox incremented:         ", key="status_increment")
                ui.Label("Last Spinbox decremented:         ", key="status_decrement")

    def handle_event(self, event):
        if event.event_type == ui.EventType.SpinboxUpdate:
            self[
                "status_last_value"
            ].value = f"Last Spinbox value: {event.widget.value}"
        if event.event_type == ui.EventType.SpinboxIncrement:
            self["status_increment"].value = f"Last Spinbox incremented: {event.key}"
        if event.event_type == ui.EventType.SpinboxDecrement:
            self["status_decrement"].value = f"Last Spinbox decremented: {event.key}"

    def on_spinbox1_change(self):
        self["spinbox1_value"].value = f"Spinbox 1 value: {self.get('spinbox1').value}"


if __name__ == "__main__":
    SpinboxDemo().run()
