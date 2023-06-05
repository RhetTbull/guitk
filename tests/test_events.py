"""Test event handling"""

from textwrap import dedent

import pytest

import guitk as ui


class Events(ui.Window):
    def config(self):
        self.geometry = "600x400"
        with ui.VLayout():
            ui.Label(
                "Wait until the window closes itself. Buttons will be pressed automatically."
            )
            ui.Button(
                "command bound in Button.__init__",
                key="button1",
                command=lambda: print("button1 pressed"),
            )
            ui.Button("@on(key=<<button2>>)", key="button2")
            ui.Button("bind_command(key=<<button3>>)", key="button3")
            ui.Button(
                '@ui.on(key="button4", event_type=ui.EventType.ButtonPress)',
                key="button4",
            )

    def setup(self):
        self._return_value = ""
        self.bind_command(key="button3", command=lambda: print("button3 pressed"))
        self.bind_command(
            event_type=ui.EventType.ButtonPress,
            command=lambda: print("button pressed (from bind_command)"),
        )
        self.bind_timer_event(
            1000, "<<button1_press>>", command=lambda: self["button1"].widget.invoke()
        )
        self.bind_timer_event(
            1500, "<<button2_press>>", command=lambda: self["button2"].widget.invoke()
        )
        self.bind_timer_event(
            2000, "<<button3_press>>", command=lambda: self["button3"].widget.invoke()
        )
        self.bind_timer_event(
            2500, "<<button4_press>>", command=lambda: self["button4"].widget.invoke()
        )
        self.bind_timer_event(3000, "<<quit>>", command=lambda: self.quit())

    @ui.on(event_type=ui.EventType.ButtonPress)
    def on_button_press(self):
        print("button pressed (from @on decorator)")

    @ui.on(key="button2")
    def on_button2(self):
        print("button2 pressed")

    @ui.on(key="button4", event_type=ui.EventType.ButtonPress)
    def on_button4(self):
        print("button4 pressed")

    def handle_event(self, event):
        if event.event_type == ui.EventType.ButtonPress:
            print(f"button {event.key} pressed (from handle_event)")

    @ui.on(event_type=ui.EventType.Any)
    def on_any(self, event):
        if event.event_type == ui.EventType.ButtonPress:
            print(
                f"button {event.key} pressed (@on(event_type=ui.EventType.Any) decorator)"
            )


def test_events(capsys):
    Events().run()
    captured = capsys.readouterr()
    assert (
        captured.out.strip()
        == dedent(
            """
        button1 pressed
        button pressed (from @on decorator)
        button button1 pressed (@on(event_type=ui.EventType.Any) decorator)
        button pressed (from bind_command)
        button button1 pressed (from handle_event)
        button pressed (from @on decorator)
        button2 pressed
        button button2 pressed (@on(event_type=ui.EventType.Any) decorator)
        button pressed (from bind_command)
        button button2 pressed (from handle_event)
        button pressed (from @on decorator)
        button button3 pressed (@on(event_type=ui.EventType.Any) decorator)
        button3 pressed
        button pressed (from bind_command)
        button button3 pressed (from handle_event)
        button pressed (from @on decorator)
        button4 pressed
        button button4 pressed (@on(event_type=ui.EventType.Any) decorator)
        button pressed (from bind_command)
        button button4 pressed (from handle_event)
        """
        ).strip()
    )
