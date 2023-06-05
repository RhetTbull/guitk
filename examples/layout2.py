""" Example for guitk showing how to use list comprehensions to create a GUI """

import guitk as ui


class LayoutDemo(ui.Window):
    def config(self):
        self.title = "List Comprehension"
        # use loop to generate 4x4 grid of buttons with tooltips
        # use the tooltip named argument to add tooltip text to any element
        with ui.HLayout():
            with ui.HGrid(cols=4):
                for row in range(4):
                    for col in range(4):
                        ui.Button(
                            f"{row}, {col}",
                            padx=0,
                            pady=0,
                            tooltip=f"Tooltip: {row},{col}",
                        )

    @ui.on(event_type=ui.EventType.ButtonPress)
    def on_button_press(self, event: ui.Event):
        if event.event_type == ui.EventType.ButtonPress:
            # print the key for the button that was pressed
            print(self[event.key].value)


if __name__ == "__main__":
    LayoutDemo().run()
