""" Demo/test all widgets """

import pathlib
import sys
from enum import Enum, auto

from .widgets import *
from .widgets import __all__ as ALL_WIDGETS
from .widgets import _get_docstring
from .widgets.events import EventType

dummy_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras tempus neque in vehicula hendrerit. Nam non posuere ante. Nunc libero libero, tempus eget enim vitae, egestas hendrerit tortor. Vivamus et egestas felis. Aliquam erat volutpat. Nulla facilisi. Aliquam hendrerit, nibh nec tempor lobortis, purus nisl vehicula ex, dapibus fermentum mauris nibh id nulla. Vivamus non pretium quam. Phasellus elementum commodo nisl. Nullam eu faucibus augue. Vivamus pulvinar metus vehicula urna porttitor euismod. "


def _list_files(path, tree):
    """list files in a directory and add to Treeview tree"""
    files = pathlib.Path(path).iterdir()
    pyfiles = []
    for f in files:
        if f.suffix == ".py":
            pyfiles.append(str(f))
            tags = ["pyfile"]
        else:
            tags = []
        tree.insert(
            "",
            "end",
            iid=str(f),
            tags=tags,
            text=str(f),
            values=(str(f), f.stat().st_size),
        )
    tree.selection_set(pyfiles)


class ModalWindow(Window):
    def config(self):
        self.layout = [[LabelEntry("Enter some text")]]
        self.modal = True


class ProgressWindow(Window):
    class GUI(Enum):
        ProgressBar = auto()
        ButtonStart = auto()
        ButtonStop = auto()

    def config(self):
        GUI = self.GUI
        self.layout = [
            [Progressbar(key=GUI.ProgressBar)],
            [Button("Start", key=GUI.ButtonStart), Button("Stop", key=GUI.ButtonStop)],
        ]
        self.modal = True

    def setup(self):
        self._demo_timer_id = None

    def handle_event(self, event):
        GUI = self.GUI
        if event.key == GUI.ButtonStart:
            self._demo_timer_id = self.bind_timer_event(500, "<<Start>>", repeat=True)

        if event.key == "<<Start>>":
            self[GUI.ProgressBar].value += 10

        if event.key == GUI.ButtonStop:
            self[GUI.ProgressBar].progressbar.stop()
            self.cancel_timer_event(self._demo_timer_id)


class DemoWindow(Window):
    """Demo guitk widgets"""

    # constants
    class GUI(Enum):
        FileEntry = auto()
        DirectoryEntry = auto()
        TextEntry = auto()
        TextLabel = auto()
        DebugWindow = auto()
        LinkLabel = auto()
        EnableCheckbutton = auto()
        OtherCheckbutton = auto()
        TimerButton = auto()
        TimerLabel = auto()
        Output = auto()
        RadioButtons1 = auto()
        RadioButtons2 = auto()
        Text = auto()
        ScrolledText = auto()
        ButtonStdOut = auto()
        ButtonStdErr = auto()
        OutputEchoCheckbutton = auto()
        OutputEnableCheckbutton = auto()
        TreeView = auto()
        ListBox = auto()
        TextDocStrings = auto()
        ComboBox = auto()
        TreeHeadingSize = auto()
        TreeHeadingFilename = auto()
        TreePythonFile = auto()
        ButtonModalWindow = auto()
        ButtonProgressWindow = auto()

    def config(self):
        GUI = self.GUI  # shortcut for constants
        self.title = "guitk Demo Window"
        self.padx = 2
        self.pady = 2
        self.menu = {
            Menu("File"): [
                Command("New File", shortcut="Cmd+N", separator=True),
                Command("Open...", shortcut="Ctrl+O"),
                {
                    Menu("Open Recent...", separator=True): [
                        Command("Recent File 1"),
                        Command("Recent File 2"),
                    ]
                },
                Command("Save", disabled=True),
                Command("Save As"),
            ],
            Menu("Edit"): [Command("Copy", shortcut="Cmd+C"), Command("Paste")],
            Menu("Debug"): [
                Command(
                    "Open Debug Window",
                    shortcut="Alt+Ctrl+X",
                    command=self.on_debug_window,
                )
            ],
            Menu("Help"): [Command("About")],
        }

        tab1 = [
            [  # row 1
                Label("File", tooltip="Label"),
                Entry(
                    key=GUI.FileEntry,
                    tooltip="Entry; will be populated by BrowseFileButton",
                ),
                BrowseFileButton(target_key=GUI.FileEntry, tooltip="BrowseFileButton"),
                Label("Directory", tooltip="Label"),
                Entry(
                    key=GUI.DirectoryEntry,
                    tooltip="Entry; will be populated by BrowseDirectoryButton",
                ),
                BrowseDirectoryButton(
                    target_key=GUI.DirectoryEntry, tooltip="BrowseDirectoryButton"
                ),
                Button(
                    "Debug Window",
                    key=GUI.DebugWindow,
                    sticky="e",
                    tooltip="Open a DebugWindow",
                ),
            ],
            [  # row 2
                LabelEntry(
                    "Enter some text",
                    key=GUI.TextEntry,
                    events=True,
                    tooltip="LabelEntry",
                ),
                Label("You entered: ", tooltip="Label; updated as you type in Entry"),
                Label("", key=GUI.TextLabel),
            ],
            [  # row 3
                LinkLabel(
                    "This Label is a link",
                    key=GUI.LinkLabel,
                    underline_font=True,
                    tooltip="LinkLabel",
                ),
                None,
                Checkbutton(
                    "Enable other checkbutton",
                    key=GUI.EnableCheckbutton,
                    tooltip="Checkbutton",
                ),
                Checkbutton(
                    "Other checkbutton",
                    key=GUI.OtherCheckbutton,
                    disabled=True,
                    tooltip="Checkbutton",
                ),
                Button(
                    "Start Timer",
                    key=GUI.TimerButton,
                    tooltip="Button; activates Window.bind_timer_event()",
                ),
                Label(
                    "0",
                    key=GUI.TimerLabel,
                    width=5,
                    tooltip="Label; updates with event generated by bind_timer_event",
                ),
                Label("Combobox", tooltip="Label"),
                Combobox(
                    key=GUI.ComboBox,
                    values=["JPEG", "PNG", "HEIC"],
                    autosize=True,
                    readonly=True,
                    tooltip="Combobox",
                ),
            ],
            [  # row 4
                # column 1
                LabelFrame(
                    text="Radio Buttons",
                    layout=[
                        [
                            Label(
                                "These Radiobuttons are in a LabelFrame",
                                tooltip="Label",
                            )
                        ],
                        [
                            Radiobutton(
                                "Option A", GUI.RadioButtons1, tooltip="Radiobutton"
                            ),
                            Radiobutton(
                                "Option 1",
                                GUI.RadioButtons2,
                                value=1,
                                tooltip="Radiobutton",
                            ),
                        ],
                        [
                            Radiobutton(
                                "Option B", GUI.RadioButtons1, tooltip="Radiobutton"
                            ),
                            Radiobutton(
                                "Option 2",
                                GUI.RadioButtons2,
                                value=2,
                                tooltip="Radiobutton",
                            ),
                        ],
                    ],
                    sticky="n",
                    tooltip="LabelFrame",
                ),
                # column 2
                Frame(
                    layout=[
                        [
                            Label(
                                "These Text boxes are in a Frame with autoframe=False so columns line up",
                                columnspan=2,
                                tooltip="Label",
                            )
                        ],
                        [
                            Label("Text box", tooltip="Label"),
                            Label("Text box with scrollbar", tooltip="Label"),
                        ],
                        [
                            Text(
                                key=GUI.Text, height=4, text=dummy_text, tooltip="Text"
                            ),
                            Text(
                                key=GUI.ScrolledText,
                                height=4,
                                text=dummy_text,
                                tooltip="Text with scrollbar",
                                vscrollbar=True,
                            ),
                        ],
                    ],
                    autoframe=False,
                ),
            ],
            # row 5
            [
                Treeview(
                    key=GUI.TreeView,
                    headings=["Filename", "Size"],
                    show="headings",
                    tooltip="Treeview; click on headings to sort",
                    vscrollbar=True,
                ),
                Frame(
                    layout=[
                        [
                            Label("Classes in guitk", tooltip="Label"),
                            Label(
                                "Doc String", key=GUI.TextDocStrings, tooltip="Label"
                            ),
                        ],
                        [
                            Listbox(
                                key=GUI.ListBox,
                                height=10,
                                width=150,
                                text=ALL_WIDGETS,
                                tooltip="Listbox",
                                vscrollbar=True,
                            ),
                            Text(
                                key=GUI.TextDocStrings,
                                height=14,
                                width=30,
                                tooltip="Text",
                            ),
                        ],
                    ],
                    autoframe=False,
                ),
            ],
        ]

        tab2 = [
            [
                Frame(
                    layout=[
                        [
                            Button("Modal Window", key=GUI.ButtonModalWindow),
                            Button("Progress Bar", key=GUI.ButtonProgressWindow),
                        ]
                    ],
                    padding=3,
                )
            ]
        ]

        self.layout = [
            [Notebook(tabs={"Tab 1": tab1, "Tab 2": tab2})],
            [
                Output(
                    key=GUI.Output, echo=True, width=100, height=10, tooltip="Output"
                ),
                Frame(
                    layout=[
                        [
                            Checkbutton(
                                "Enable",
                                key=GUI.OutputEnableCheckbutton,
                                tooltip="Checkbutton",
                            )
                        ],
                        [
                            Checkbutton(
                                "Echo",
                                key=GUI.OutputEchoCheckbutton,
                                tooltip="Checkbutton",
                            )
                        ],
                        [
                            Button(
                                "stdout",
                                key=GUI.ButtonStdOut,
                                tooltip="Button; print to stdout",
                            )
                        ],
                        [
                            Button(
                                "stderr",
                                key=GUI.ButtonStdErr,
                                tooltip="Button; print to stderr",
                            )
                        ],
                    ]
                ),
            ],
        ]

    def setup(self):
        """gets called right after __init__"""
        # a place to store some data later
        GUI = self.GUI
        self.data = {
            "timer_id": None,
            "tree_sort_size_reverse": False,
            "tree_sort_filename_reverse": False,
        }

        # check the Enable checkbutton for enabled output redirect
        self[GUI.OutputEnableCheckbutton].widget.invoke()

        _list_files(".", self[GUI.TreeView].tree)
        self[GUI.TreeView].bind_heading("Size", GUI.TreeHeadingSize)
        self[GUI.TreeView].bind_heading("Filename", GUI.TreeHeadingFilename)
        self[GUI.TreeView].bind_tag("pyfile", GUI.TreePythonFile, sequence="<Return>")
        print("Done with setup")

    def teardown(self):
        """gets called right before window is destroyed"""
        print(f"Tearing down")

    def on_debug_window(self):
        DebugWindow(parent=self.window)

    def handle_event(self, event):
        print(event)
        GUI = self.GUI
        if event.event_type == EventType.BrowseFile:
            print(f"You chose file {self[GUI.FileEntry].value}")

        if event.event_type == EventType.BrowseDirectory:
            print(f"You chose directory {self[GUI.DirectoryEntry].value}")

        if event.key == GUI.TextEntry:
            self[GUI.TextLabel].value = self[GUI.TextEntry].value
            print(f"You typed: '{self[GUI.TextEntry].value}'")

        if event.key == GUI.LinkLabel:
            print(f"You clicked the link!")

        if event.key == GUI.EnableCheckbutton:
            if self[GUI.EnableCheckbutton].value:
                # checkbutton is checked
                self[GUI.OtherCheckbutton].widget.state(["!disabled"])
                print("Enabling other Checkbutton")
            else:
                # checkbutton is not checked
                self[GUI.OtherCheckbutton].widget.state(["disabled"])
                print("Disabling other Checkbutton")

        if event.key == GUI.TimerButton:
            if self.data["timer_id"] is None:
                # timer not running, start a timer
                print("Starting timer")
                self.data["timer_id"] = self.bind_timer_event(
                    1000, "<<MyTimer>>", repeat=True
                )
                self[GUI.TimerButton].value = "Stop Timer"
            else:
                # timer is running, stop it
                print("Stopping timer")
                self.cancel_timer_event(self.data["timer_id"])
                self[GUI.TimerButton].value = "Start Timer"
                self.data["timer_id"] = None

        if event.key == "<<MyTimer>>":
            timer = self[GUI.TimerLabel].value
            self[GUI.TimerLabel].value = int(timer) + 1

        if event.key == GUI.OutputEnableCheckbutton:
            if self[GUI.OutputEnableCheckbutton].value:
                print("Enabling output redirect")
                self[GUI.Output].enable_redirect()
            else:
                print("Disabling output redirect")
                self[GUI.Output].disable_redirect()

        if event.key == GUI.OutputEchoCheckbutton:
            if self[GUI.OutputEchoCheckbutton].value:
                print("Enabling output redirect echo")
                self[GUI.Output].echo = True
            else:
                print("Disabling output redirect echo")
                self[GUI.Output].echo = False

        if event.key == GUI.ButtonStdOut:
            print("This text went to stdout")

        if event.key == GUI.ButtonStdErr:
            print("This text went to stderr", file=sys.stderr)

        if event.key == GUI.RadioButtons1:
            print(f"Radiobuttons1 value is {self[GUI.RadioButtons1].value}")

        if event.key == GUI.RadioButtons2:
            print(f"Radiobuttons2 value is {self[GUI.RadioButtons2].value}")

        if event.key == GUI.TreeHeadingSize:
            self[GUI.TreeView].sort_on_column(
                "Size",
                reverse=self.data["tree_sort_size_reverse"],
                key=lambda x: int(x[0]),
            )
            self.data["tree_sort_size_reverse"] = not self.data[
                "tree_sort_size_reverse"
            ]

        if event.key == GUI.TreeHeadingFilename:
            self[GUI.TreeView].sort_on_column(
                "Filename", reverse=self.data["tree_sort_filename_reverse"]
            ),
            self.data["tree_sort_filename_reverse"] = not self.data[
                "tree_sort_filename_reverse"
            ]

        if event.event_type == EventType.TreeviewSelect:
            print(f"You selected file(s): {self[GUI.TreeView].value}")

        if event.key == GUI.TreePythonFile:
            print(f"You hit Return on a python file: {self[GUI.TreeView].value}")

        if event.key == GUI.ListBox:
            print(f"You selected {self[GUI.ListBox].value}")
            docstring = None
            try:
                docstring = _get_docstring(self[GUI.ListBox].value[0])
            except AttributeError:
                pass
            docstring = docstring or "doc string not found"
            self[GUI.TextDocStrings].value = docstring

        if event.key == GUI.ComboBox:
            print(f"Combobox: {self[GUI.ComboBox].value}")

        if event.key == GUI.DebugWindow:
            # open debug window
            DebugWindow(parent=self.window)

        if event.key == GUI.ButtonModalWindow:
            ModalWindow(parent=self.window)

        if event.key == GUI.ButtonProgressWindow:
            ProgressWindow(parent=self.window)


if __name__ == "__main__":
    """Run demo window showing all widgets"""
    DemoWindow().run()
