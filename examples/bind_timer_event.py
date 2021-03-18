""" Example showing how to use bind_timer_event """

import time
import tkinter as tk

import guitk


class TimerWindow(guitk.Window):
    def config(self):
        self.title = "Timer Window"

        self.layout = [
            [guitk.Label("Press Start Timer to fire event after 2000 ms")],
            [guitk.Label("", width=60, key="OUTPUT")],
            [
                guitk.Button("Start Timer"),
                guitk.Button("Cancel Timer"),
                guitk.CheckButton("Repeat", key="REPEAT"),
            ],
        ]

    def setup(self):
        # store the id of the running timer so it can be cancelled
        self.data = {"timer_id": None}

    # Interact with the Window using an event Loop
    def handle_event(self, event):
        if event.key == "Quit":
            self.quit()

        if event.key == "Start Timer":
            # this simple demo assumes only one timer running at a time
            repeat = event.values["REPEAT"]  # value of Repeat CheckButton
            self.data["timer_id"] = self.bind_timer_event(
                2000, "<<MyTimer>>", repeat=repeat
            )
            self[
                "OUTPUT"
            ].value = f"Timer {self.data['timer_id']} started at {time.time():.2f}"

        if event.key == "<<MyTimer>>":
            self["OUTPUT"].value = f"Timer went off at {time.time():.2f}!"

        if event.key == "Cancel Timer":
            self.cancel_timer_event(self.data["timer_id"])
            self[
                "OUTPUT"
            ].value = f"Timer {self.data['timer_id']} canceled at {time.time():.2f}"


if __name__ == "__main__":
    # add some padding around GUI elements to make it prettier
    TimerWindow().run()
