"""Simple ToDo list application using guitk"""

from tkinter import ttk

import guitk as gtk


class ToDoWindow(gtk.Window):
    def config(self):
        self.size = 300, 600
        with gtk.VLayout():
            gtk.Label("ToDo List", anchor="center", sticky="ew", weightx=1)
            with gtk.VStack() as self.vs_todo:
                # start with a new Entry widget for a new ToDo item
                gtk.Entry(key="todo_0", events=True, focus=True)
            with gtk.HStack(halign="right"):
                gtk.Button("+", key="add")

    def setup(self):
        # this is where we would load the todo list from a file
        # to restore state from a previous session
        self.todo_count = 0

        # create a style for the checkbutton
        self.done_style = "Done.TCheckbutton"
        self._done_style = ttk.Style()
        self._done_style.configure(self.done_style, foreground="gray")

    @gtk.on(key="add")
    def on_add(self, event: gtk.Event):
        """Event handler for the add button"""
        key = f"todo_{self.todo_count}"
        self.vs_todo.add_widget(gtk.Entry(key=key, events=True))
        self[key].focus()

    @gtk.on(event_type=gtk.EventType.EntryReturn)
    def on_return(self, event: gtk.Event):
        """Event handler for the return key in the Entry widget"""
        if not event.widget.value:
            # empty string, so do nothing
            return

        # replace the Entry widget with a CheckButton
        event.widget.widget.grid_forget()
        self.vs_todo.add_widget(
            gtk.CheckButton(
                text=event.widget.value,
                key=f"todo_{self.todo_count}",
            )
        )
        self.todo_count += 1
        event.widget.widget.destroy()

    @gtk.on(event_type=gtk.EventType.CheckButton)
    def on_check(self, event: gtk.Event):
        """Event handler for the CheckButton widget"""
        if event.widget.value:
            # checkbox is checked, so mark as done
            event.widget.widget.configure(style=self.done_style)
        else:
            # checkbox is unchecked, so mark as not done
            event.widget.widget.configure(style="")


if __name__ == "__main__":
    ToDoWindow().run()
