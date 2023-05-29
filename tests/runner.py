"""Test runner for guitk"""

from __future__ import annotations

import guitk as ui

from .class_loader import load_class


class TestRunner(ui.Window):
    """Runs a test class (which should be a subclass of ui.Window)"""

    def __init__(
        self,
        class_: str | type,
        path: str | None = None,
        description: str | None = None,
    ):
        self.class_ = class_
        self.path = path
        self.description = description

        if type(class_) == str:
            self.class_name = class_
            self.class_ = load_class(path, class_)
        else:
            self.class_name = class_.__name__
        super().__init__()

    def config(self):
        with ui.VLayout():
            ui.Label(
                f"Running test: {self.path}::{self.class_name}"
                if self.path
                else f"Running test: {self.class_name}"
            )
            ui.Label(f"{self.description}")
            ui.VSpacer()
            ui.Button(f"Run test: {self.class_name}", key="run")
            ui.VSpacer()
            with ui.HStack():
                ui.Button("Pass")
                ui.LabelEntry("Fail reason", key="fail_reason")
                ui.Button("Fail")

    @ui.on(key="run")
    def run_test(self):
        """Run the test"""
        self.class_(parent=self.window)

    @ui.on(key="Pass")
    def pass_test(self):
        """Pass the test and quit"""
        return self.quit(None)

    @ui.on(event_type=ui.EventType.DeleteWindow)
    @ui.on(key="Fail")
    def fail_test(self):
        """Fail the test if user presses Fail or closes the window"""
        return self.quit(self.get("fail_reason").value or "No reason given")
