""" Demonstrates use of guitk.Output widget for capturing stdout/stderr """

import guitk
import sys


class OutputDemo(guitk.Window):
    def config(self):
        self.title = "Output Demo"

        self.layout = [
            [
                guitk.Frame(
                    layout=[
                        [
                            guitk.Label("stdout"),
                            guitk.Entry(key="STDOUT"),
                            guitk.Button("Print", key="PRINT_STDOUT"),
                        ],
                        [
                            guitk.Label("stderr"),
                            guitk.Entry(key="STDERR"),
                            guitk.Button("Print", key="PRINT_STDERR"),
                        ],
                    ]
                )
            ],
            [
                guitk.Frame(
                    layout=[
                        [
                            guitk.Output(
                                stderr=False, key="OUTPUT_STDOUT", width=40, height=20
                            )
                        ],
                        [
                            guitk.Label(
                                "stdout", sticky="nsew", anchor="center", columnspan=1
                            )
                        ],
                        [
                            guitk.Checkbutton("echo", key="ECHO_STDOUT"),
                            guitk.Button("Start", key="START_STDOUT", disabled=True),
                            guitk.Button("Stop", key="STOP_STDOUT"),
                        ],
                    ]
                ),
                guitk.Frame(
                    layout=[
                        [
                            guitk.Output(
                                stdout=False, key="OUTPUT_STDERR", width=40, height=20
                            )
                        ],
                        [guitk.Label("stderr", sticky="nsew", anchor="center")],
                        [
                            guitk.Checkbutton("echo", key="ECHO_STDERR"),
                            guitk.Button("Start", key="START_STDERR", disabled=True),
                            guitk.Button("Stop", key="STOP_STDERR"),
                        ],
                    ]
                ),
                guitk.Frame(
                    layout=[
                        [guitk.Output(width=40, height=20, key="OUTPUT_BOTH")],
                        [guitk.Label("stdout/stderr", sticky="nsew", anchor="center")],
                        [guitk.Frame(layout=[[None]])],
                    ]
                ),
            ],
        ]

    def handle_event(self, event):
        if event.key == "PRINT_STDOUT":
            value = event.values["STDOUT"]
            print(value)

        if event.key == "PRINT_STDERR":
            value = event.values["STDERR"]
            print(value, file=sys.stderr)

        if event.key == "ECHO_STDERR":
            value = event.values["ECHO_STDERR"]
            self["OUTPUT_STDERR"].echo = value

        if event.key == "ECHO_STDOUT":
            value = event.values["ECHO_STDOUT"]
            self["OUTPUT_STDOUT"].echo = value

        if event.key == "STOP_STDOUT":
            self["OUTPUT_STDOUT"].disable_redirect()
            self["START_STDOUT"].widget.state(["!disabled"])
            self["STOP_STDOUT"].widget.state(["disabled"])

        if event.key == "START_STDOUT":
            self["OUTPUT_STDOUT"].enable_redirect()
            self["START_STDOUT"].widget.state(["disabled"])
            self["STOP_STDOUT"].widget.state(["!disabled"])

        if event.key == "STOP_STDERR":
            self["OUTPUT_STDERR"].disable_redirect()
            self["START_STDERR"].widget.state(["!disabled"])
            self["STOP_STDERR"].widget.state(["disabled"])

        if event.key == "START_STDERR":
            self["OUTPUT_STDERR"].enable_redirect()
            self["START_STDERR"].widget.state(["disabled"])
            self["STOP_STDERR"].widget.state(["!disabled"])


if __name__ == "__main__":
    OutputDemo().run()
