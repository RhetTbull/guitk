import guitk


class LayoutDemo(guitk.Window):

    # use list comprehension to generate 4x4 grid of buttons with tooltips
    layout = [
        [
            guitk.Button(f"{row}, {col}", padx=0, pady=0, tooltip=f"Tooltip: {row},{col}")
            for col in range(4)
        ]
        for row in range(4)
    ]

    # Interact with the Window using an event Loop
    def handle_event(self, event):
        if event.event == guitk.EventType.BUTTON_PRESS:
            # print the key for the button that was pressed
            print(event.values[event.key])


if __name__ == "__main__":
    LayoutDemo("List Comprehension", padx=5, pady=5).run()
