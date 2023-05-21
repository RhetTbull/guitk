"""Simple ToDo list application using guitk"""

import guitk as ui


class ToDoWindow(ui.Window):
    def config(self):
        self.size = 300, 600
        with ui.VLayout():
            ui.Label("ToDo List", anchor="center", sticky="ew", weightx=1)
            with ui.VStack() as self.vs_todo:
                # start with a new Entry widget for a new ToDo item
                ui.Entry(key="todo_0", events=True, focus=True)
            with ui.HStack(halign="right"):
                ui.Button("+", key="add")

    def setup(self):
        # this is where we would load the todo list from a file
        # to restore state from a previous session
        self.todo_count = 0

    @ui.on(key="add")
    def on_add(self, event: ui.Event):
        """Event handler for the add button"""
        key = f"todo_{self.todo_count}"
        self.vs_todo.append(ui.Entry(key=key, events=True))
        self[key].focus()

    @ui.on(event_type=ui.EventType.EntryReturn)
    def on_return(self, event: ui.Event):
        """Event handler for the return key in the Entry widget"""
        if not event.widget.value:
            # empty string, so do nothing
            return

        # replace the Entry widget with a CheckButton
        event.widget.replace(
            ui.CheckButton(
                text=event.widget.value,
                key=f"todo_{self.todo_count}",
            )
        )
        self.todo_count += 1

    @ui.on(event_type=ui.EventType.CheckButton)
    def on_check(self, event: ui.Event):
        """Event handler for the CheckButton widget"""
        if event.widget.value:
            # checkbox is checked, so mark as done
            event.widget.font(overstrike=True)
        else:
            # checkbox is unchecked, so mark as not done
            event.widget.font(overstrike=False)


if __name__ == "__main__":
    # ui.set_debug(True)
    ToDoWindow().run()
