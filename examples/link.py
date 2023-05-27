""" Demonstrates use of LinkLabel widget """

from guitk import HLayout, LinkLabel, Window


class ClickMe(Window):
    def config(self):
        self.title = "Click me!"

        # you can pass tkinter.ttk options to the widgets
        # e.g. width and anchor
        with HLayout():
            LinkLabel("Click me!", width=20, anchor="center", key="CLICK_ME").font(
                family="Helvetica", size=24, underline=True
            ).style(foreground="blue")
    
        self.padx = 20
        self.pady = 20

    def handle_event(self, event):
        print(event)


if __name__ == "__main__":
    ClickMe().run()
