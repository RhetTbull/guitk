"""Test Combobox()"""

import guitk as ui

from .runner import TestRunner


class TestCombobox(ui.Window):
    def config(self):
        with ui.VLayout():
            ui.Label("Select the color 'green'")
            ui.Combobox("combo1", "red", values=["red", "green", "blue"], readonly=True)
            ui.Label("Type 'apple' in the combobox and press Return")
            ui.Combobox(
                "combo2", "apricot", values=["apricot", "apple", "pear"], disabled=True
            )
            ui.Label("Type 'pear' in the combobox")
            ui.Combobox(
                "combo3",
                "apricot",
                values=["apricot", "apple", "pear"],
                keyrelease=True,
                disabled=True,
            )
            ui.Label("Press the 'Done' button to finish the test")
            ui.Button("Done", disabled=True)

    @ui.on("combo1", event_type=ui.EventType.ComboboxSelected)
    def on_combo1(self, event: ui.Event):
        if event.widget.value == "green":
            self.get("combo2").disabled = False

    @ui.on("combo2", event_type=ui.EventType.ComboboxReturn)
    def on_combo2(self, event: ui.Event):
        if event.widget.value == "apple":
            self.get("combo3").disabled = False

    @ui.on("combo3", event_type=ui.EventType.KeyRelease)
    def on_combo3(self, event: ui.Event):
        if event.widget.value == "pear":
            self.get("Done").disabled = False

    @ui.on("Done")
    def on_done(self, event: ui.Event):
        self.quit()


def test_button():
    runner = TestRunner(class_=TestCombobox, description="Test Combobox widget")
    assert not runner.run()
