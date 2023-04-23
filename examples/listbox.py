"""Demo for Listbox widget."""

import keyword  # used only to generate sample data

import guitk


class ListWindow(guitk.Window):
    def config(self):
        self.title = "List Box Demo"
        # Note: While guitk tries to match naming conventions of tkinter/ttk, it provides
        # aliases to classes that use PEP 8 CapWords convention:
        # see Listbox and ListBox
        self.layout = [
            [
                guitk.Listbox(
                    key="LISTBOX1",
                    tooltip="I am a Listbox with scrollbar",
                    vscrollbar=True,
                ),
                guitk.ListBox(
                    key="LISTBOX2",
                    tooltip="I am a ListBox without scrollbar",
                    width=100,
                ),
            ]
        ]

    def setup(self):
        for line in keyword.kwlist:
            self["LISTBOX1"].append(line)
            self["LISTBOX2"].append(line)

    def handle_event(self, event):
        # CapWords aliases apply to event types as well
        if event.event_type == guitk.EventType.ListboxSelect:
            print(f"event! {event}, {self[event.key].value}")


if __name__ == "__main__":
    ListWindow().run()
