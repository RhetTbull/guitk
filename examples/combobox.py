import guitk


class ComboBoxWindow(guitk.Window):
    def config(self):
        self.title = "ComboBox Demo"
        self.layout = [
            [guitk.ComboBox(key="COMBOBOX1", values=["Foo", "Bar", "XYZZY"])],
            [
                guitk.ComboBox(
                    key="COMBOBOX2", values=["Foo", "Bar", "XYZZY"], width=6, readonly=True
                )
            ],
        ]

    def handle_event(self, event):
        print(event)


if __name__ == "__main__":
    ComboBoxWindow().run()
