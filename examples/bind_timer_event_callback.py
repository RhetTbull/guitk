""" Example showing how to use bind_timer_event with a command callback """

import time

import guitk


class TimerWindow(guitk.Window):
    def config(self):
        self.title = "Timer Window"

        self.layout = [
            [guitk.Label("Press Start Timer to fire event after 2000 ms")],
            [guitk.Label("", width=60, key="OUTPUT")],
            [
                guitk.Button("Start Timer", command=self.on_start_timer),
                guitk.Button("Cancel Timer", command=self.on_cancel_timer),
                guitk.Checkbutton("Repeat", key="REPEAT"),
            ],
        ]

    def setup(self):
        # store the id of the running timer so it can be cancelled
        self.data = {"timer_id": None}

    def on_start_timer(self):
        # this simple demo assumes only one timer running at a time
        repeat = self["REPEAT"].value  # value of Repeat Checkbutton
        self.data["timer_id"] = self.bind_timer_event(
            2000, "<<MyTimer>>", repeat=repeat, command=self.on_timer
        )
        self[
            "OUTPUT"
        ].value = f"Timer {self.data['timer_id']} started at {time.time():.2f}"

    def on_cancel_timer(self):
        self.cancel_timer_event(self.data["timer_id"])
        self[
            "OUTPUT"
        ].value = f"Timer {self.data['timer_id']} canceled at {time.time():.2f}"

    def on_timer(self):
        self["OUTPUT"].value = f"Timer went off at {time.time():.2f}!"


if __name__ == "__main__":
    TimerWindow().run()
