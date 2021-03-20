import guitk


class ListWindow(guitk.Window):
    def config(self):
        self.title = "List Box Demo"
        # Note: While guitk tries to match naming conventions of tkinter/ttk, it provides
        # aliases to classes that use PEP 8 CapWords convention:
        # see Listbox and ListBox
        self.layout = [
            [
                guitk.Listbox(key="LISTBOX1", tooltip="I am a Listbox"),
                guitk.ListBox(key="LISTBOX2", tooltip="I am a ListBox"),
            ]
        ]

    def setup(self):
        lines = ["Foo", "Bar", "FooBar", "XYZZY"]
        for line in lines:
            self["LISTBOX1"].append(line)
            self["LISTBOX2"].append(line)

    def handle_event(self, event):
        # CapWords aliases apply to event types as well
        if event.event_type == guitk.EventType.ListboxSelect:
            print(f"event! {event}")
        if event.event_type == guitk.EventType.ListBoxSelect:
            print(f"event! {event}")


if __name__ == "__main__":
    ListWindow().run()
