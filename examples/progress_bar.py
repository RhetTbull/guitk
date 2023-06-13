"""Example of various types of progress bars """

import tkinter as tk

import guitk as ui


class ProgressWindow(ui.Window):
    def config(self):
        # create some progress bars with different modes and orientations
        # default mode is determinate

        self.title = "Show Some Progress!"

        with ui.VLayout():
            with ui.HStack():
                ui.Label("mode=determinate")
                ui.ProgressBar(key="progress1", tooltip="determinate", value=0)
            with ui.HStack():
                ui.Label("mode=indeterminate")
                ui.ProgressBar(
                    key="progress2",
                    tooltip="indeterminate",
                    mode=ui.PROGRESS_INDETERMINATE,
                    maximum=100,
                )
            with ui.HStack():
                ui.Button(text="Start", key="START")
                ui.Button(text="Stop", key="STOP", disabled=True)
            with ui.HStack():
                ui.ProgressBar(
                    key="progress3", tooltip="vertical", value=100.0, orient=tk.VERTICAL
                )
            with ui.HStack():
                ui.ProgressBar(key="progress4", maximum=100, tooltip="step")
                ui.Button(text="Step", key="STEP")
                ui.Scale(
                    0,
                    100,
                    key="SCALE",
                    orient=tk.HORIZONTAL,
                    value=5,
                    target_key="SCALE_LABEL",
                    precision=0,
                )
                ui.Label(text="5.0", key="SCALE_LABEL")
            ui.VSpacer()
            ui.HSeparator()
            ui.Label("", key="status", weightx=1, sticky="ew")

    def setup(self):
        self._demo_timer_id = None
        self._demo_done = False

    def handle_event(self, event):
        # Update status label with progress bar values
        # and stop the demo when progress1 reaches 100
        self["status"].value = (
            f"progress1: {self['progress1'].value}, "
            f"progress2: {self['progress2'].value}, "
            f"progress3: {self['progress3'].value}, "
            f"progress4: {self['progress4'].value}"
        )

        if not self._demo_done and self["progress1"].value >= 100:
            self._demo_done = True
            print("Done")
            self.cancel_timer_event(self._demo_timer_id)
            self["progress2"].progressbar.stop()
            self["progress2"].value = 0
            self["START"].disabled = False
            self["STOP"].disabled = True

    @ui.on("STOP")
    def on_stop(self, event):
        print("Stopping")
        self.cancel_timer_event(self._demo_timer_id)
        self["progress2"].progressbar.stop()
        self["progress2"].value = 0
        self["START"].disabled = False
        self["STOP"].disabled = True

    @ui.on("START")
    def on_start(self, event):
        print("Starting")
        self._demo_timer_id = self.bind_timer_event(500, "<<Start>>", repeat=True)
        self._demo_done = False
        self["progress2"].widget.start()
        self["START"].disabled = True
        self["STOP"].disabled = False
        self["progress1"].value = 0
        self["progress3"].value = 100

    @ui.on("<<Start>>")
    def on_start_event(self, event):
        print("Updating progress")
        self["progress1"].value += 10
        self["progress3"].value -= 10

    @ui.on("STEP")
    def on_step(self, event):
        step = self["SCALE"].value
        self["progress4"].widget.step(step)


# run your event loop
if __name__ == "__main__":
    ProgressWindow().run()
