""" Example showing how to use bind_timer_event """

import time

import guitk as ui


class TimerWindow(ui.Window):
    def config(self):
        self.title = "Timer Window"

        with ui.VLayout():
            ui.Label("Press Start Timer to fire event after 2000 ms")
            ui.Label("", width=60, key="OUTPUT")
            with ui.HStack(valign="center"):
                ui.Button("Start Timer")
                ui.Button("Cancel Timer")
                ui.Checkbutton("Repeat", key="REPEAT")

    def setup(self):
        # store the id of the running timer so it can be cancelled
        self.data = {"timer_id": None}

    @ui.on(key="Start Timer")
    def start_timer(self):
        # this simple demo assumes only one timer running at a time
        repeat = self["REPEAT"].value
        self.data["timer_id"] = self.bind_timer_event(
            2000, "<<MyTimer>>", repeat=repeat
        )
        self[
            "OUTPUT"
        ].value = f"Timer {self.data['timer_id']} started at {time.time():.2f}"

    @ui.on(key="<<MyTimer>>")
    def on_timer(self):
        self["OUTPUT"].value = f"Timer went off at {time.time():.2f}!"

    @ui.on(key="Cancel Timer")
    def cancel_timer(self):
        self.cancel_timer_event(self.data["timer_id"])
        self[
            "OUTPUT"
        ].value = f"Timer {self.data['timer_id']} canceled at {time.time():.2f}"


if __name__ == "__main__":
    TimerWindow().run()
