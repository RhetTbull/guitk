"""Demo of GUITk widgets and layouts"""


import contextlib
import pathlib
import sys
import tkinter as tk

import guitk
from guitk import *
from guitk.containers import _Container

SAMPLE_TEXT = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras tempus neque in vehicula hendrerit. 
Nam non posuere ante. Nunc libero libero, tempus eget enim vitae, egestas hendrerit tortor. Vivamus et egestas felis. 
Aliquam erat volutpat. Nulla facilisi. Aliquam hendrerit, nibh nec tempor lobortis, purus nisl vehicula ex, dapibus 
fermentum mauris nibh id nulla. Vivamus non pretium quam. Phasellus elementum commodo nisl. Nullam eu faucibus augue. 
Vivamus pulvinar metus vehicula urna porttitor euismod. """
SAMPLE_TEXT = SAMPLE_TEXT.replace("\n", "")


ALL_WIDGETS = guitk.__all__


def get_docstring(name):
    """Return the docstring of an object with name"""
    try:
        obj = globals()[name]
    except KeyError as e:
        raise ValueError(f"Invalid object name: {e}") from e
    return obj.__doc__ or ""


def list_files(path: str, tree: Treeview):
    """list files in a directory and add to Treeview tree"""
    files = pathlib.Path(path).iterdir()
    pyfiles = []
    for f in files:
        if f.suffix == ".py":
            pyfiles.append(str(f))
            tags = ["pyfile"]
        else:
            tags = []
        tree.widget.insert(
            "",
            "end",
            iid=str(f),
            tags=tags,
            text=str(f),
            values=(str(f), f.stat().st_size),
        )
    tree.widget.selection_set(pyfiles)


class Demo(Window):
    def config(self):
        self.title = "GUTk Demo"
        self.create_layout()
        self.create_menubar()

    def create_layout(self):
        with VLayout():
            with HStack(halign=tk.CENTER):
                Label("This is a demo of GUITk widgets and layouts")
            HSeparator()
            with Notebook(sticky="nsew", weightx=1):
                with VTab("Tab 1"):
                    with HStack():
                        LabelEntry("File:", key="file")
                        BrowseFileButton(target_key="file")
                        LabelEntry("Directory:", key="directory")
                        BrowseDirectoryButton(target_key="directory")
                        Button("Debug Window", key="debug_window")
                    with HStack():
                        LabelEntry("Enter some text:", key="entry", keyrelease=True)
                        Label("You entered:")
                        Label("", key="label_entered")
                    with HStack():
                        LinkLabel("This Label is a link", key="link", sticky="ns").font(
                            underline=True
                        ).style(foreground="blue")
                        CheckButton(
                            "Enable other checkbutton",
                            key="check_enable_other",
                            sticky="ns",
                        )
                        CheckButton(
                            "Other checkbutton",
                            key="check_other",
                            disabled=True,
                            sticky="ns",
                        )
                        Button("Start Timer", key="start_timer", sticky="ns")
                        Label("0", key="timer", width=4, sticky="ns")
                        ComboBox(
                            default="PNG",
                            values=["PNG", "JPEG", "GIF"],
                            width=4,
                            readonly=True,
                        )
                        SpinBox(from_value=0, to_value=5, wrap=True, width=4)
                    with HStack():
                        with LabelFrame("Radio Buttons"):
                            with VStack():
                                Label("These RadioButtons are in a LabelFrame")
                                with HStack():
                                    with VStack(vexpand=False, hexpand=False):
                                        RadioButton(
                                            "Option A", key="option_a", group="group1"
                                        )
                                        RadioButton(
                                            "Option B", key="option_b", group="group1"
                                        )
                                    with VStack(vexpand=False, hexpand=False):
                                        RadioButton(
                                            "Option 1", key="option_1", group="group2"
                                        )
                                        RadioButton(
                                            "Option 2", key="option_2", group="group2"
                                        )
                        with VStack():
                            Label("These Text boxes are in an HStack")
                            with HStack():
                                with VStack():
                                    Label("Text Box", pady=0)
                                    Text(
                                        key="text_box_1",
                                        text=SAMPLE_TEXT,
                                        height=4,
                                        tooltip="Text box",
                                        pady=0,
                                    )
                                with VStack(padding=0):
                                    Label("Text Box With Scrollbar", pady=0)
                                    Text(
                                        key="text_box_2",
                                        text=SAMPLE_TEXT,
                                        height=4,
                                        vscrollbar=True,
                                        tooltip="Text box with scrollbar",
                                        pady=0,
                                    )
                    with HStack():
                        Treeview(
                            key="treeview",
                            headings=["Filename", "Size"],
                            show="headings",
                            tooltip="Treeview; click on headings to sort",
                            vscrollbar=True,
                        ),
                        with VStack(vexpand=False, hexpand=False, halign="center"):
                            Label("Classes and functions in GUITk")
                            ListBox(
                                key="listbox",
                                text=ALL_WIDGETS,
                                height=10,
                                width=160,
                                vscrollbar=True,
                            )
                        with VStack(vexpand=False, hexpand=False, halign="center"):
                            Label("Doc String")
                            Text(key="docstring", height=14, width=30, vscrollbar=True)
                with HTab("Tab 2"):
                    with PanedWindow(key="paned_window", weightx=1):
                        with HPane():
                            Text(text=SAMPLE_TEXT, weightx=1, width=None)
                        with VPane():
                            Text(text=SAMPLE_TEXT, weightx=1, width=None)
            with LabelFrame("Output Redirect", weightx=1, sticky="ew"):
                with HStack():
                    Output(key="output", sticky="nsew", weightx=1, weighty=1)
                    VSeparator()
                    with VStack(vexpand=False, hexpand=False, valign=tk.BOTTOM):
                        Checkbutton("Enable", key="check_enable")
                        Checkbutton("Echo", key="check_echo")
                        Button("stdout")
                        Button("stderr")

    def create_menubar(self):
        """create the menu"""
        with MenuBar():
            with Menu("File"):
                Command("Open", shortcut="Ctrl+O")
                Command("Save")
                Command("Save As")
                Command("Exit", command=self.quit)
            with Menu("Edit"):
                Command("Cut")
                Command("Copy")
                Command("Paste")
            with Menu("SubMenus"):
                with Menu("SubMenu 1"):
                    Command("Command 1")
                    Command("Command 2")
                with Menu("SubMenu 2"):
                    Command("Command 3")
                    Command("Command 4")

    def setup(self):
        """gets called right after __init__"""
        print(f"Setting up: {self.__dict__}")

        # check the Enable checkbutton for enabled output redirect
        self.get("check_enable").widget.invoke()

        # set up the treeview
        self.tree_sort_size_reverse = False
        self.tree_sort_filename_reverse = False
        tree = self.get("treeview")
        list_files(".", self.get("treeview"))

        # bind events for treeview
        tree.bind_heading("Size", "tree_heading_size")
        tree.bind_heading("Filename", "tree_heading_filename")

        # handle Return and double-click events for treeview, but only for python files
        # list_files() will tag python files with tag 'pyfile'
        tree.bind_tag("pyfile", "tree_python_file", sequence="<Return>")
        tree.bind_tag("pyfile", "tree_python_file", sequence="<Double-1>")

        # will store timer id for the timer
        self.timer_id = None

        # set up the listbox
        listbox = self.get("listbox")
        first_item = ALL_WIDGETS[0]
        listbox.widget.selection_set(first_item)
        listbox.widget.see(first_item)

    def teardown(self):
        """gets called right before window is destroyed"""
        print("Tearing down")

    def handle_event(self, event: Event):
        """Gets called for every event"""
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
            print("Enabling output redirect")
            self["output"].enable_redirect()
        else:
            print("Disabling output redirect")
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
    def on_check_enable_other(self):
        self["check_other"].disabled = not self["check_enable_other"].value

    @on(key="start_timer")
    def on_start_timer(self):
        """Start/stop the timer"""
        # cancel the timer if it is running
        if self.timer_id:
            self.cancel_timer_event(self.timer_id)
            self.timer_id = None
            self.get("start_timer").value = "Start Timer"
            return

        # start the timer
        self.timer_id = self.bind_timer_event(1000, "<<MyTimer>>", repeat=True)
        self.get("start_timer").value = "Stop Timer"

    @on(key="<<MyTimer>>")
    def on_timer(self):
        """Increment the timer"""
        self["timer"].value = int(self["timer"].value) + 1

    @on(key="tree_heading_size")
    def on_tree_heading_size(self):
        """Sort treeview on size"""
        self.get("treeview").sort_on_column(
            "Size",
            reverse=self.tree_sort_size_reverse,
            key=lambda x: int(x[0]),
        )
        self.tree_sort_size_reverse = not self.tree_sort_size_reverse

    @on(key="tree_heading_filename")
    def on_tree_heading_filename(self):
        """Sort treeview on filename"""
        self.get("treeview").sort_on_column(
            "Filename",
            reverse=self.tree_sort_filename_reverse,
            key=lambda x: x[0],
        )
        self.tree_sort_filename_reverse = not self.tree_sort_filename_reverse

    @on(key="tree_python_file")
    def on_tree_python_file(self):
        """User hit return on a Python file"""
        print("You picked a Python file")

    @on(key="treeview")
    def on_treeview(self):
        """User clicked on a treeview item"""
        print(f"You clicked on a treeview item: {self.get('treeview').value}")

    @on(key="listbox")
    def on_listbox(self):
        """User clicked on a listbox item, update docstring text box"""
        docstring = None
        with contextlib.suppress(AttributeError):
            docstring = get_docstring(self.get("listbox").value[0])
        docstring = docstring or "doc string not found"
        self.get("docstring").value = docstring


if __name__ == "__main__":
    Demo().run()
