import guitk


class ComboboxWindow(guitk.Window):
    def config(self):
        self.title = "Combobox Demo"
        self.layout = [
            [
                guitk.Combobox(
                    key="COMBOBOX1", values=["Foo", "Bar", "XYZZY"], autosize=True
                )
            ],
            [
                guitk.Combobox(
                    key="COMBOBOX2",
                    values=["Foo", "Bar", "XYZZY"],
                    width=6,
                    readonly=True,
                )
            ],
        ]

    def handle_event(self, event):
        if event.key in ["COMBOBOX1", "COMBOBOX2"]:
            print(event, self[event.key].value)


if __name__ == "__main__":
    ComboboxWindow().run()
