"""Run GUITk examples"""

import ast
import pathlib
import subprocess
import sys

import guitk as ui

_global_examples_dir = pathlib.Path("./examples")


def get_docstring(file: pathlib.Path) -> str:
    """Get the docstring from a python file using the AST"""
    with file.open("r") as f:
        tree = ast.parse(f.read())
    return ast.get_docstring(tree)


def get_examples(examples_dir: pathlib.Path):
    """Get examples from the examples directory"""
    example_files = pathlib.Path(examples_dir).glob("*.py")
    example_files = sorted(
        [f for f in example_files if f.name != pathlib.Path(__file__).name]
    )
    return {
        file.stem: {"path": file, "docstring": get_docstring(file)}
        for file in example_files
    }


class ExampleBrowser(ui.Window):
    """Browse and run GUITk examples"""

    def config(self):
        global _global_examples_dir

        self.title = "GUITk Examples Browser"
        self.examples = get_examples(_global_examples_dir)
        with ui.VLayout():
            for name, example in self.examples.items():
                with ui.HGrid(cols=2):
                    ui.Button(name, command=self.run_example(example["path"]))
                    ui.Label(example["docstring"])

    def run_example(self, path: pathlib.Path):
        """Run an example"""

        def run():
            subprocess.run([sys.executable, path])

        return run


if __name__ == "__main__":
    if len(sys.argv) > 1:
        _global_examples_dir = pathlib.Path(sys.argv[1])
    ExampleBrowser().run()
