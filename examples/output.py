""" Demonstrates use of guitk.Output widget for capturing stdout/stderr """

import sys

from guitk import (
    Button,
    Checkbutton,
    EventType,
    HLayout,
    HStack,
    Label,
    LabelEntry,
    Output,
    VStack,
    Window,
    on,
)


class OutputDemo(Window):
    def config(self):
        self.title = "Output Demo"
        with HLayout():
            with VStack():
                with HStack(vexpand=False, hexpand=False):
                    LabelEntry("stdout", key="STDOUT")
                    Button("Print", key="PRINT_STDOUT")
                with HStack(vexpand=False, hexpand=False):
                    LabelEntry("stderr", key="STDERR")
                    Button("Print", key="PRINT_STDERR")
            with VStack():
                Output(
                    stderr=False,
                    key="OUTPUT_STDOUT",
                    width=40,
                    height=20,
                    text="This widget will show stdout\n",
                )
                Label(
                    "redirected stdout",
                    sticky="nsew",
                    anchor="center",
                    columnspan=1,
                )
                with HStack():
                    Checkbutton("echo", key="ECHO_STDOUT"),
                    Button("Start", key="START_STDOUT", disabled=True),
                    Button("Stop", key="STOP_STDOUT"),
            with VStack():
                Output(
                    stdout=False,
                    key="OUTPUT_STDERR",
                    width=40,
                    height=20,
                    text="This widget will show stderr\n",
                )
                Label("redirected stderr", sticky="nsew", anchor="center")
                with HStack():
                    Checkbutton("echo", key="ECHO_STDERR")
                    Button("Start", key="START_STDERR", disabled=True)
                    Button("Stop", key="STOP_STDERR")
            with VStack():
                Output(
                    width=40,
                    height=20,
                    key="OUTPUT_BOTH",
                    text="This widget will show both stdout and stderr\n",
                )
                Label(
                    "redirected stdout/stderr",
                    sticky="nsew",
                    anchor="center",
                )

    @on("PRINT_STDOUT")
    @on(key="STDOUT", event_type=EventType.EntryReturn)
    def print_stdout(self, event):
        value = self["STDOUT"].value
        print(value)

    @on("PRINT_STDERR")
    @on(key="STDERR", event_type=EventType.EntryReturn)
    def print_stderr(self, event):
        value = self["STDERR"].value
        print(value, file=sys.stderr)

    @on("ECHO_STDERR")
    def echo_stderr(self, event):
        value = self["ECHO_STDERR"].value
        self["OUTPUT_STDERR"].echo = value

    @on("ECHO_STDOUT")
    def echo_stdout(self, event):
        value = self["ECHO_STDOUT"].value
        self["OUTPUT_STDOUT"].echo = value

    @on("STOP_STDOUT")
    def stop_stdout(self, event):
        self["OUTPUT_STDOUT"].disable_redirect()
        self["START_STDOUT"].widget.state(["!disabled"])
        self["STOP_STDOUT"].widget.state(["disabled"])

    @on("START_STDOUT")
    def start_stdout(self, event):
        self["OUTPUT_STDOUT"].enable_redirect()
        self["START_STDOUT"].widget.state(["disabled"])
        self["STOP_STDOUT"].widget.state(["!disabled"])

    @on("STOP_STDERR")
    def stop_stderr(self, event):
        self["OUTPUT_STDERR"].disable_redirect()
        self["START_STDERR"].widget.state(["!disabled"])
        self["STOP_STDERR"].widget.state(["disabled"])

    @on("START_STDERR")
    def start_stderr(self, event):
        self["OUTPUT_STDERR"].enable_redirect()
        self["START_STDERR"].widget.state(["disabled"])
        self["STOP_STDERR"].widget.state(["!disabled"])


if __name__ == "__main__":
    OutputDemo().run()
