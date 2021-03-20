import guitk


class RadiobuttonDemo(guitk.Window):
    def config(self):
        self.title = "Radio Button Demo"
        self.layout = [
            [guitk.Radiobutton("Option 1", "group1", value=1)],
            [guitk.Radiobutton("Option 2", "group1", value=2, selected=False)],
            [guitk.Radiobutton("Option 3", "group1", value=3, selected=True)],
        ]

    def handle_event(self, event):
        if event.event_type == guitk.EventType.Radiobutton:
            print(event)


if __name__ == "__main__":
    RadiobuttonDemo().run()
