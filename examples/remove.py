"""Demo that shows various ways to remove widgets"""

import guitk as ui


class Demo(ui.Window):
    def config(self):
        self.title = "Remove Widgets"
        self.size = (600, 400)
        with ui.HLayout():
            with ui.VStack():
                ui.Button("Widget.destroy")
                ui.Button("VStack.remove(key)")
                ui.Button("VStack.remove(widget)")
                ui.Button("Window.remove_widget(key)")
                ui.Button("Window.remove_widget(widget)")
            ui.VSeparator
            with ui.VStack() as self.widget_stack:
                ui.Label("Widget.destroy", key="widget_destroy")
                ui.Label("VStack.remove(key)", key="vstack_remove_key")
                ui.Label("VStack.remove(widget)", key="vstack_remove_widget")
                ui.Label("Window.remove_widget(key)", key="window_remove_key")
                ui.Label("Window.remove_widget(widget)", key="window_remove_widget")

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

    @ui.on(key="Window.remove_widget(key)")
    def window_remove_key(self):
        self.remove_widget("window_remove_key")

    @ui.on(key="Window.remove_widget(widget)")
    def window_remove_widget(self):
        for widget in self.widgets:
            if widget.key == "window_remove_widget":
                self.remove_widget(widget)
                break

if __name__ == "__main__":
    Demo().run()