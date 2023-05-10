"""Demo for Scale widget."""

from tkinter import HORIZONTAL

import guitk


class ScaleDemo(guitk.Window):
    def config(self):
        default = 5.0
        self.layout = [
            [
                guitk.Scale(
                    0,
                    100,
                    value=default,
                    orient=HORIZONTAL,
                    target_key="SCALE_LABEL",
                    precision=0,
                )
            ],
            [guitk.Label(text=f"{default:.1f}", key="SCALE_LABEL")],
        ]
        self.padx = 20
        self.pady = 20


if __name__ == "__main__":
    ScaleDemo().run()
