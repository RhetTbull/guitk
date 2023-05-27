"""Demo of the Radiobutton widget."""

import guitk as ui


class RadiobuttonDemo(ui.Window):
    def config(self):
        self.title = "Radio Button Demo"
        self.size = 200, 200
        with ui.VLayout():
            ui.Radiobutton("Option 1", "group1", value=1)
            ui.Radiobutton("Option 2", "group1", value=2, selected=False)
            ui.Radiobutton("Option 3", "group1", value=3, selected=True)

    def handle_event(self, event):
        if event.event_type == ui.EventType.Radiobutton:
            print(f"Option {event.widget.value} selected")


if __name__ == "__main__":
    RadiobuttonDemo().run()
