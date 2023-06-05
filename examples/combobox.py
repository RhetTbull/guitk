"""Combobox demo."""

from guitk import Combobox, Label, VLayout, VSpacer, Window


class ComboboxWindow(Window):
    def config(self):
        self.title = "Combobox Demo"
        self.size = (400, 200)
        with VLayout():
            Combobox(key="COMBOBOX1", values=["Foo", "Bar", "XYZZY"], autosize=True)
            Combobox(
                key="COMBOBOX2",
                values=["Foo", "Bar", "XYZZY"],
                width=6,
                readonly=True,
                default="Foo",
            )
            VSpacer()
            Label("", key="STATUS", sticky="EW")

    def handle_event(self, event):
        if event.key in ["COMBOBOX1", "COMBOBOX2"]:
            self["STATUS"].value = f"Selected {event.key} {self[event.key].value}"


if __name__ == "__main__":
    ComboboxWindow().run()
