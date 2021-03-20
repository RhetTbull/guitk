import guitk


class RadioButtonDemo(guitk.Window):
    def config(self):
        self.title = "Radio Button Demo"
        self.layout = [
            [guitk.RadioButton("Option 1", "group1", value=1)],
            [guitk.RadioButton("Option 2", "group1", value=2, selected=False)],
            [guitk.RadioButton("Option 3", "group1", value=3, selected=True)],
        ]

    def handle_event(self, event):
        if event.event_type == guitk.EventType.RADIO_BUTTON:
            print(event)


if __name__ == "__main__":
    RadioButtonDemo().run()
