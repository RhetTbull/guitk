"""Demo and test GUITk menus."""

from textwrap import dedent

import guitk as ui


class MenuDemo(ui.Window):
    def config(self):
        self.title = "Menu Demo"
        self.size = (800, 200)
        self.instructions = dedent(
            """
        Verify the 'File|Save' command is {} then check the 'Enable Save Command' checkbutton
        Then verify the 'Edit' menu is {} and check the 'Enable Edit Menu' checkbutton
        Next verify there is a menu separator after 'Open Recent'
        Finally, verify that the 'Ctrl+O' shortcut key generates a MenuCommand event for File|Open"""
        ).strip()

        with ui.VLayout():
            ui.Label(
                self.instructions.format("disabled", "disabled"),
                key="instructions",
            )
            ui.Checkbutton("Enable Save Command")
            ui.Checkbutton("Enable Edit Menu")
            ui.Label("Select a menu command or shortcut key to see the event here")
            ui.Text("", key="event", height=2, sticky="ew", weightx=1)

        with ui.MenuBar():
            with ui.Menu("File"):
                ui.Command("Open...", shortcut="Ctrl+O")
                with ui.SubMenu("Open Recent"):
                    ui.Command("File 1")
                    ui.Command("File 2")
                    ui.Command("File 3")
                ui.MenuSeparator()
                ui.Command("Save", key="File|Save", disabled=True)
                ui.Command("Save As")
            with ui.Menu("Edit", key="Edit", disabled=True):
                ui.Command("Cut", shortcut="Ctrl+X")
                ui.Command("Copy", shortcut="Ctrl+C")
                ui.Command("Paste", shortcut="Ctrl+V")

    @ui.on("Enable Save Command")
    def enable_save(self):
        self["File|Save"].disabled = not self["Enable Save Command"].value
        self.update_instructions()

    @ui.on("Enable Edit Menu")
    def enable_edit(self):
        self["Edit"].disabled = not self["Enable Edit Menu"].value
        self.update_instructions()

    @ui.on(event_type=ui.EventType.MenuCommand)
    def menu_command(self, event: ui.Event):
        self["event"].value = f"{event}"

    def update_instructions(self):
        """Update the instructions label"""

        def enabled(value: bool) -> str:
            """Return 'enabled' or 'disabled' based on value"""
            return "enabled" if value else "disabled"

        self["instructions"].value = self.instructions.format(
            enabled(self["Enable Save Command"].value),
            enabled(self["Enable Edit Menu"].value),
        )

    def handle_event(self, event: ui.Event):
        print(f"handle_event: {event}")


if __name__ == "__main__":
    MenuDemo().run()
