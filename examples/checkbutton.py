"""Checkbutton Demo"""

import guitk


class CheckbuttonDemo(guitk.Window):
    def config(self):
        self.title = "Check Button Demo"
        with guitk.VLayout():
            guitk.Checkbutton("Checkbutton 1", key="check1", command=self.toggle_check2)
            guitk.Checkbutton("Checkbutton 2", key="check2", disabled=True)

    def toggle_check2(self):
        self["check2"].disabled = not self["check1"].value

    def handle_event(self, event):
        if event.event_type == guitk.EventType.Checkbutton:
            widget = self[event.key]
            print(f"{event.key} is {widget.value}")


if __name__ == "__main__":
    CheckbuttonDemo().run()
