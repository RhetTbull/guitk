"""Demo that shows various ways to remove widgets"""

import guitk as ui


class Remove(ui.Window):
    def config(self):
        self.title = "Remove Widgets"
        self.size = (1000, 400)
        with ui.HLayout() as self.layout:
            with ui.VStack():
                ui.Button("Widget.destroy")
                ui.Button("VStack.remove(key)")
                ui.Button("VStack.remove(widget)")
                ui.Button("HLayout.remove(key)")
                ui.Button("HLayout.remove(widget)")
                ui.Button("Window.remove(key)")
                ui.Button("Window.remove(widget)")
            ui.VSeparator()
            with ui.VStack() as self.widget_stack:
                ui.Label("Widget.destroy", key="widget_destroy")
                ui.Label("VStack.remove(key)", key="vstack_remove_key")
                ui.Label("VStack.remove(widget)", key="vstack_remove_widget")
                ui.Label("Window.remove(key)", key="window_remove_key")
                ui.Label("Window.remove(widget)", key="window_remove_widget")
            ui.VSeparator()
            ui.Label("HLayout.remove(key)", key="layout_remove_key", sticky="n")
            ui.Label("HLayout.remove(widget)", key="layout_remove_widget")

    @ui.on(key="Widget.destroy")
    def widget_destroy(self):
        for widget in self.widgets:
            if widget.key == "widget_destroy":
                widget.destroy()
                break

    @ui.on(key="VStack.remove(key)")
    def vstack_remove_key(self):
        self.widget_stack.remove("vstack_remove_key")

    @ui.on(key="VStack.remove(widget)")
    def vstack_remove_widget(self):
        for widget in self.widgets:
            if widget.key == "vstack_remove_widget":
                self.widget_stack.remove(widget)
                break

    @ui.on(key="HLayout.remove(key)")
    def layout_remove_key(self):
        self.layout.remove("layout_remove_key")

    @ui.on(key="HLayout.remove(widget)")
    def layout_remove_widget(self):
        for widget in self.widgets:
            if widget.key == "layout_remove_widget":
                self.layout.remove(widget)
                break

    @ui.on(key="Window.remove(key)")
    def window_remove_key(self):
        self.remove("window_remove_key")

    @ui.on(key="Window.remove(widget)")
    def window_remove_widget(self):
        for widget in self.widgets:
            if widget.key == "window_remove_widget":
                self.remove(widget)
                break


if __name__ == "__main__":
    ui.set_debug(True)
    Remove().run()
