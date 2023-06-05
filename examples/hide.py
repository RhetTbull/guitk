"""Simple demo showing how to show/hide a widget"""

import guitk as gui


class Demo(gui.Window):
    def config(self):
        self.size = 300, 600
        with gui.VLayout():
            gui.Label("Hello", key="hello", weightx=1, sticky="ew", anchor="e")
            gui.Label("World")
            gui.Button("Hide", key="show_hide")

    def setup(self):
        self.hidden = False

    @gui.on(key="show_hide")
    def on_show_hide(self, event: gui.Event):
        """Hide/show the hello label"""

        # All guitk widgets have a widget attribute that is the tkinter widget
        # guitk uses the grid() method to place widgets in the window
        # so you can use the tkinter grid_remove() and grid() methods to hide/show the underlying widget
        if self.hidden:
            self["hello"].widget.grid()
            self["show_hide"].value = "Hide"
        else:
            self["hello"].widget.grid_remove()
            self["show_hide"].value = "Show"
        self.hidden = not self.hidden


if __name__ == "__main__":
    Demo().run()
