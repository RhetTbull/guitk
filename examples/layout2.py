""" Example for guitk showing how to use list comprehensions to create a GUI """

import guitk


class LayoutDemo(guitk.Window):
    def config(self):
        self.title = "List Comprehension"
        # use list comprehension to generate 4x4 grid of buttons with tooltips
        # use the tooltip named argument to add tooltip text to any element
        self.layout = [
            [
                guitk.Button(
                    f"{row}, {col}", padx=0, pady=0, tooltip=f"Tooltip: {row},{col}"
                )
                for col in range(4)
            ]
            for row in range(4)
        ]

    # Interact with the Window using an event Loop
    def handle_event(self, event):
        if event.event_type == guitk.EventType.ButtonPress:
            # print the key for the button that was pressed
            print(self[event.key].value)


if __name__ == "__main__":
    LayoutDemo().run()
