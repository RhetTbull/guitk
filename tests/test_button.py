"""Test Button()"""

import guitk as ui

from .runner import TestRunner


class TestButton(ui.Window):
    def config(self):
        with ui.VLayout():
            with ui.HStack(halign="center"):
                ui.Label("Press each button to verify the label next to it updates.")
            ui.Label("Button 1 tests @on('Button 1')")
            with ui.HStack():
                ui.Button("Button 1", key="button1")
                ui.Label("", width=40, key="button1_status")
            ui.Label("Button 2 tests Button(command=...)")
            with ui.HStack():
                ui.Button("Button 2", key="button2", command=self.button2)
                ui.Label("", width=40, key="button2_status")
            ui.Label("bind_event()")
            with ui.HStack():
                ui.Button("Button 3", key="button3")
                ui.Label("", width=40, key="button3_status")
            ui.Label("Disabled Button")
            ui.CheckButton("Enable Button 4", key="enable_button4")
            with ui.HStack():
                ui.Button("Button 4", key="button4", disabled=True)
                ui.Label("", width=40, key="button4_status")

    def setup(self):
        self.get("button3").bind_event("<Button-1>", self.button3)

    @ui.on("button1")
    def button1(self):
        self.get("button1_status").value = "Button 1 pressed"

    def button2(self):
        self.get("button2_status").value = "Button 2 pressed"

    def button3(self):
        self.get("button3_status").value = "Button 3 pressed"

    @ui.on("enable_button4")
    def enable_button4(self, event: ui.Event):
        self.get("button4").disabled = not event.widget.value

    @ui.on("button4")
    def button4(self):
        self.get("button4_status").value = "Button 4 pressed"


def test_button():
    runner = TestRunner(class_=TestButton, description="Test Button widget")
    assert not runner.run()
