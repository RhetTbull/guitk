"""Example of various types of progress bars """

import guitk
from tkinter import VERTICAL, HORIZONTAL

# subclass guitk.Window as the starting point for your app's main window
class ProgressWindow(guitk.Window):
    def config(self):
        # define a layout for the window
        # you must have a class variable named `layout` or you'll get an empty window

        # create some progress bars with different modes and orientations
        progress1 = guitk.ProgressBar(key="progress1", tooltip="determinate", value=0)
        progress2 = guitk.ProgressBar(
            key="progress2",
            tooltip="indeterminate",
            mode="indeterminate",
            maximum=100,
        )
        progress3 = guitk.ProgressBar(
            key="progress3",
            tooltip="vertical",
            value=100.0,
            orient=VERTICAL,
        )
        progress4 = guitk.ProgressBar(key="progress4", maximum=100, tooltip="step")
        self.layout = [
            [
                guitk.Frame(
                    layout=[
                        [guitk.Label("mode=determinate"), progress1],
                        [guitk.Label("mode=indeterminate"), progress2],
                        [
                            guitk.Button(text="Start", key="START"),
                            guitk.Button(text="Stop", key="STOP", disabled=True),
                        ],
                    ]
                ),
                progress3,
            ],
            [progress4],
            [
                guitk.Button(text="Step", key="STEP"),
                guitk.Scale(
                    key="SCALE",
                    orient=HORIZONTAL,
                    from_=0,
                    to=100,
                    value=5,
                    target_key="SCALE_LABEL",
                    precision=0,
                ),
                guitk.Label(text="5.0", key="SCALE_LABEL"),
            ],
        ]
        self.title = "Show Some Progress!"

    def setup(self):
        self._demo_timer_id = None
        self._demo_done = False

    # define your event loop
    # every guitk.Window will call self.handle_event to handle GUI events
    # event is a guitk.Event object
    def handle_event(self, event):
        print(
            # f"progress1: {self['progress1'].value}"
            f"progress1: {self['progress1'].value}, progress2: {self['progress2'].value}, progress3: {self['progress3'].value}, progress4: {self['progress4'].value}"
        )

        if event.key == "STOP":
            print("Stopped")
            self.cancel_timer_event(self._demo_timer_id)
            self["progress2"].progressbar.stop()
            self["progress2"].value = 0
            self["START"].disabled = False
            self["STOP"].disabled = True

        if event.key == "START":
            self._demo_timer_id = self.bind_timer_event(500, "<<Start>>", repeat=True)
            self["progress2"].widget.start()
            self["START"].disabled = True
            self["STOP"].disabled = False

        if event.key == "<<Start>>":
            print("Updating progress")
            self["progress1"].value += 10
            self["progress3"].value -= 10

        if not self._demo_done and self["progress1"].value >= 100:
            self._demo_done = True
            print("Done")
            self.cancel_timer_event(self._demo_timer_id)
            self["progress2"].progressbar.stop()
            self["progress2"].value = 0
            self["START"].disabled = True
            self["STOP"].disabled = True

        if event.key == "STEP":
            step = self["SCALE"].value
            self["progress4"].widget.step(step)


# run your event loop
if __name__ == "__main__":
    ProgressWindow().run()
