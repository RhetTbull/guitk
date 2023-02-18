""" Demonstrates use of guitk.Output widget for capturing stdout/stderr """

import sys

from guitk import Button, Checkbutton, Entry, Frame, Label, Output, Window


class OutputDemo(Window):
    def config(self):
        self.title = "Output Demo"

        self.layout = [
            [
                Frame(
                    [
                        [
                            Label("stdout"),
                            Entry(key="STDOUT"),
                            Button("Print", key="PRINT_STDOUT"),
                        ],
                        [
                            Label("stderr"),
                            Entry(key="STDERR"),
                            Button("Print", key="PRINT_STDERR"),
                        ],
                    ]
                )
            ],
            [
                Frame(
                    [
                        [
                            Output(
                                stderr=False,
                                key="OUTPUT_STDOUT",
                                width=40,
                                height=20,
                                text="This widget will show stdout\n",
                            )
                        ],
                        [
                            Label(
                                "redirected stdout",
                                sticky="nsew",
                                anchor="center",
                                columnspan=1,
                            )
                        ],
                        [
                            Checkbutton("echo", key="ECHO_STDOUT"),
                            Button("Start", key="START_STDOUT", disabled=True),
                            Button("Stop", key="STOP_STDOUT"),
                        ],
                    ]
                ),
                Frame(
                    [
                        [
                            Output(
                                stdout=False,
                                key="OUTPUT_STDERR",
                                width=40,
                                height=20,
                                text="This widget will show stderr\n",
                            )
                        ],
                        [Label("redirected stderr", sticky="nsew", anchor="center")],
                        [
                            Checkbutton("echo", key="ECHO_STDERR"),
                            Button("Start", key="START_STDERR", disabled=True),
                            Button("Stop", key="STOP_STDERR"),
                        ],
                    ]
                ),
                Frame(
                    [
                        [
                            Output(
                                width=40,
                                height=20,
                                key="OUTPUT_BOTH",
                                text="This widget will show both stdout and stderr\n",
                            )
                        ],
                        [
                            Label(
                                "redirected stdout/stderr",
                                sticky="nsew",
                                anchor="center",
                            )
                        ],
                        [Frame(layout=[[None]])],
                    ]
                ),
            ],
        ]

    def handle_event(self, event):
        if event.key == "PRINT_STDOUT":
            value = self["STDOUT"].value
            print(value)

        if event.key == "PRINT_STDERR":
            value = self["STDERR"].value
            print(value, file=sys.stderr)

        if event.key == "ECHO_STDERR":
            value = self["ECHO_STDERR"].value
            self["OUTPUT_STDERR"].echo = value

        if event.key == "ECHO_STDOUT":
            value = self["ECHO_STDOUT"].value
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
