import guitk


class ClickMe(guitk.Window):
    layout = [[guitk.LinkLabel("Click me!")]]

    def handle_event(self, event):
        print(event)

if __name__ == "__main__":
    ClickMe("Click me!",padx=20, pady=20).run()
