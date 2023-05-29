"""Demo of GUITk widgets and layouts"""

import sys
import tkinter as tk

from guitk import (
    BrowseDirectoryButton,
    BrowseFileButton,
    Button,
    Checkbutton,
    CheckButton,
    DebugWindow,
    Entry,
    Event,
    EventType,
    HLayout,
    HSeparator,
    HStack,
    Label,
    LabelEntry,
    LinkLabel,
    Notebook,
    Output,
    Tab,
    VerticalTab,
    VLayout,
    VSeparator,
    VStack,
    Window,
    on,
)


class Demo(Window):
    def config(self):
        with VLayout():
            with HStack(halign=tk.CENTER):
                Label("This is a demo of GUITk widgets and layouts")
            HSeparator()
            with Notebook(sticky="nsew", weightx=1):
                with VerticalTab("Tab 1"):
                    with HStack():
                        LabelEntry("File:", key="file")
                        BrowseFileButton(target_key="file")
                        LabelEntry("Directory:", key="directory")
                        BrowseDirectoryButton(target_key="directory")
                        Button("Debug Window", key="debug_window")
                    with HStack():
                        LabelEntry("Enter some text:", key="entry", events=True)
                        Label("You entered:")
                        Label("", key="label_entered")
                    with HStack():
                        LinkLabel("This Label is a link", key="link").font(
                            underline=True
                        ).style(foreground="blue")
                        CheckButton(
                            "Enable other checkbutton", key="check_enable_other"
                        )
                        CheckButton(
                            "Other checkbutton", key="check_other", disabled=True
                        )
                with Tab("Tab 2"):
                    ...
            with HStack():
                Output(key="output", sticky="nsew", weightx=1, weighty=1)
                VSeparator()
                with VStack(valign=tk.BOTTOM, expand=False):
                    Checkbutton("Enable", key="check_enable")
                    Checkbutton("Echo", key="check_echo")
                    Button("stdout")
                    Button("stderr")

    def setup(self):
        ...
        # self["output"].enable_redirect()

    def handle_event(self, event: Event):
        print(event)

    @on(key="debug_window")
    def on_debug_window(self):
        DebugWindow(parent=self.window)

    @on(key="entry")
    def on_entry(self):
        self["label_entered"].value = self["entry"].value

    @on(key="check_enable")
    def on_check_enable(self):
        if self["check_enable"].value:
            self["output"].enable_redirect()
        else:
            self["output"].disable_redirect()

    @on(key="check_echo")
    def on_check_echo(self):
        self["output"].echo = self["check_echo"].value

    @on(key="stdout")
    def on_stdout(self):
        print("This is stdout")

    @on(key="stderr")
    def on_stderr(self):
        print("This is stderr", file=sys.stderr)

    @on(key="link")
    def on_link(self):
        print("You clicked the link")

    @on(key="check_enable_other")
    def on_check_enable(self):
        self["check_other"].disabled = not self["check_enable_other"].value


if __name__ == "__main__":
    Demo().run()
