"""Test Button()"""

import guitk as ui

from .runner import TestRunner


class TestButton(ui.Window):
    def config(self):
        with ui.VLayout():
            ui.Label("Button 1 tests @on('Button 1')")
            with ui.HStack():
                ui.Button("Button 1")
                ui.Label("", width=40, key="button1_status")
            ui.Label("Button 2 tests Button(command=...)")
            with ui.HStack():
                ui.Button("Button 2", command=self.button2)
                ui.Label("", width=40, key="button2_status")

    @ui.on("Button 1")
    def button1(self):
        self.get("button1_status").value = "Button 1 pressed"

    def button2(self):
        self.get("button2_status").value = "Button 2 pressed"


def test_button():
    runner = TestRunner(class_=TestButton, description="Test Button()")
    assert not runner.run()
