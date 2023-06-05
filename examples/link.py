""" Demonstrates use of LinkLabel widget """

from guitk import Label, LinkLabel, VLayout, Window, on


class ClickMe(Window):
    def config(self):
        self.title = "Click me!"

        # you can pass tkinter.ttk options to the widgets
        # e.g. width and anchor
        with VLayout(halign="center"):
            LinkLabel("Click me!", key="click_me").font(
                family="Helvetica", size=24, underline=True
            ).style(foreground="blue")
            Label("", key="status")

        self.padx = 20
        self.pady = 20

    @on(key="click_me")
    def click_me(self):
        self["status"].value = "You clicked me!"

    def handle_event(self, event):
        print(event)


if __name__ == "__main__":
    ClickMe().run()
