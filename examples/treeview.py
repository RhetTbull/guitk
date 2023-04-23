""" Demonstrates use of guitk.TreeView widget """

import guitk
import pathlib


class ShowMeATree(guitk.Window):
    def config(self):
        self.title = "Tree View"
        self.layout = [
            [
                guitk.Treeview(
                    headings=["Filename", "Size"],
                    key="TREE",
                    vscrollbar=True,
                )
            ]
        ]

    def list_files(self, path, tree):
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

    def setup(self):
        self.data = {
            "tree_sort_size_reverse": False,
            "tree_sort_filename_reverse": False,
        }
        self.list_files(".", self["TREE"].tree)
        self["TREE"].bind_heading("Size", "TREE_SIZE")
        self["TREE"].bind_heading("Filename", "TREE_FILENAME")
        self["TREE"].bind_tag("pyfile", "PYTHON_FILE", sequence="<Return>")

    def handle_event(self, event):
        if event.key == "TREE_SIZE":
            self["TREE"].sort_on_column(
                "Size",
                reverse=self.data["tree_sort_size_reverse"],
                key=lambda x: int(x[0]),
            )
            self.data["tree_sort_size_reverse"] = not self.data[
                "tree_sort_size_reverse"
            ]

        if event.key == "TREE_FILENAME":
            self["TREE"].sort_on_column(
                "Filename", reverse=self.data["tree_sort_filename_reverse"]
            ),
            self.data["tree_sort_filename_reverse"] = not self.data[
                "tree_sort_filename_reverse"
            ]

        if event.event_type == guitk.EventType.TreeviewSelect:
            print(event)
            print(f"You selected file(s): {self[event.key].value}")

        if event.key == "PYTHON_FILE":
            print(f"python file: {self['TREE'].value}")


if __name__ == "__main__":
    ShowMeATree().run()
