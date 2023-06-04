"""Demo showing how to run code at setup and teardown time in guitk."""

import guitk as ui

# If your Window class has a setup() method, it will be called before the window is shown.
# If you have registered any handlers for EventType.Setup, they will be called after the setup()
# method is called, in the order they were registered.
# If your Window class has a teardown() method, it will be called immediately before the window
# is destroyed (user has called quit() or closed the window). If you have registered any handlers
# for EventType.Teardown, they will be called after the teardown() method is called, in the order
# they were registered.


class SetupTeardown(ui.Window):
    def config(self):
        self.title = "Setup and Teardown Demo"
        self.size = 200, 200

        with ui.VLayout(halign="center", valign="center"):
            ui.Label("", key="label")

    def setup(self):
        """Setup is called before the window is shown and before any @on handlers are called"""
        print("setup 1")
        self.countdown = 3
        self.bind_timer_event(1000, "<<Countdown>>", repeat=True, command=self.on_timer)
        self["label"].value = f"Quitting in {self.countdown} seconds"

    @ui.on(event_type=ui.EventType.Setup)
    def on_setup(self, event):
        """EventType.Setup handled after self.setup() is called"""
        print("setup 2")

    @ui.on(event_type=ui.EventType.Setup)
    def on_setup_again(self, event):
        """EventType.Setup handled in order of registration"""
        print("setup 3")

    def teardown(self):
        """Teardown is called immediately before the window is destroyed and before any @on handlers for teardown are called"""
        print("teardown 1")

    @ui.on(event_type=ui.EventType.Teardown)
    def on_teardown(self, event):
        """EventType.Teardown handled after self.teardown() is called and before the window is destroyed"""
        print("teardown 2")

    @ui.on(event_type=ui.EventType.Teardown)
    def on_teardown_again(self, event):
        """EventType.Teardown handled in order of registration"""
        print("teardown 3")

    def on_timer(self):
        """Update timer label and quit if countdown is zero"""
        self.countdown -= 1

        self[
            "label"
        ].value = (
            f"Quitting in {self.countdown} second{'s' if self.countdown != 1 else ''}"
        )
        if self.countdown == 0:
            self.quit("auto quit")


if __name__ == "__main__":
    # ui.set_debug(True)
    SetupTeardown().run()
