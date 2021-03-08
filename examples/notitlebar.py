import guitk
from idlelib import tooltip


class NoTitleBar(guitk.Window):
    layout = [[guitk.Label("Hello World!")], [guitk.Button("Goodbye")]]

    # def __init__(self, title=None, parent=None, padx=None, pady=None):
    #     super().__init__(title, parent=parent, padx=padx, pady=pady)
    #     self.tk.root.wm_overrideredirect(False)

    def setup(self):
        pass
        # self.window.wm_overrideredirect(1)
        # self.window.update_idletasks()
        # self.window.lift()
        # self.window.attributes("-topmost", 1)
        # self["Goodbye"].element.focus()

    def handle_event(self, event):
        if event.key == "Goodbye":
            self.quit()


if __name__ == "__main__":
    NoTitleBar("",topmost=True).run()
