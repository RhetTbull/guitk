"""Demo for Scale widget."""

import tkinter as tk

from guitk import HLayout, Label, Scale, VStack, Window


class ScaleDemo(Window):
    def config(self):
        default = 5.0
        self.title = "Scale Demo"
        self.size = 300, 200
        with HLayout(valign="center"):
            with VStack(valign="bottom"):
                Scale(
                    0,
                    100,
                    value=default,
                    orient=tk.HORIZONTAL,
                    target_key="SCALE_LABEL1", # key to the target widget whose value will be updated
                    precision=0,
                )
                Label(text=f"{default:.1f}", key="SCALE_LABEL1")
            with VStack(valign="bottom"):
                Scale(
                    0,
                    100,
                    value=default,
                    orient=tk.VERTICAL,
                    target_key="SCALE_LABEL2",
                    precision=1,
                )
                Label(text=f"{default:.1f}", key="SCALE_LABEL2")
        self.padx = 20
        self.pady = 20


if __name__ == "__main__":
    ScaleDemo().run()
