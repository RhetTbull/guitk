import guitk


class ListWindow(guitk.Window):
    def config(self):
        self.title = "List Box Demo"
        self.layout = [[guitk.ListBox(key="LISTBOX")]]

    def setup(self):
        lines = ["Foo", "Bar", "FooBar", "XYZZY"]
        for line in lines:
            self["LISTBOX"].insert("end", line)

    def handle_event(self, event):
        print(event)


if __name__ == "__main__":
    ListWindow().run()
