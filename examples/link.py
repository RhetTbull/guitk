import guitk
from tkinter import ttk


class ClickMe(guitk.Window):
    layout = [[guitk.LinkLabel("Click me!", key="CLICK_ME", underline_font=True)]]

    def setup(self):
        # configure the Click Me label to be blue
        style = ttk.Style()
        style.configure("Blue.TLabel", foreground="blue")
        self["CLICK_ME"].element.configure(style="Blue.TLabel")

    def handle_event(self, event):
        print(event)


if __name__ == "__main__":
    ClickMe("Click me!", padx=20, pady=20).run()
