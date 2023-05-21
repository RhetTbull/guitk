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

    def setup(self):
        print(self.vs._layout)

    @ui.on(key="Hello")
    def on_hello(self):
        label = ui.Label("Hello")
        self.vs.append(label)
        ui.debug(f"{len(self.vs)=}")

    @ui.on(key="Goodbye")
    def on_goodbye(self):
        label = ui.Label("Goodbye")
        self.hs.append(label)
        ui.debug(f"{len(self.hs)=}")


if __name__ == "__main__":
    ui.set_debug(True)
    Demo().run()
