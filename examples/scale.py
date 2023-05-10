"""Demo for Scale widget."""

from tkinter import HORIZONTAL

from guitk import Label, Scale, VerticalLayout, Window


class ScaleDemo(Window):
    def config(self):
        default = 5.0
        with VerticalLayout():
            Scale(
                0,
                100,
                value=default,
                orient=HORIZONTAL,
                target_key="SCALE_LABEL",
                precision=0,
            )
            Label(text=f"{default:.1f}", key="SCALE_LABEL")
        self.padx = 20
        self.pady = 20


if __name__ == "__main__":
    ScaleDemo().run()
