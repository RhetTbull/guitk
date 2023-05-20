"""Demo showing how to add widgets at runtime"""


import guitk as ui


class Demo(ui.Window):
    def config(self):
        with ui.HLayout():
            with ui.VStack() as self.vs:
                ui.Button("Say Hello", key="Hello")
            ui.VSeparator()
            with ui.HStack() as self.hs:
                ui.Button("Say Goodbye", key="Goodbye")

    @ui.on(key="Hello")
    def on_hello(self):
        label = ui.Label("Hello")
        self.vs.add_widget(label)

    @ui.on(key="Goodbye")
    def on_goodbye(self):
        label = ui.Label("Goodbye")
        self.hs.add_widget(label)


if __name__ == "__main__":
    Demo().run()
