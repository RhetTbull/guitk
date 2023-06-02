"""Demo showing how to use a custom widget with guitk Widget wrapper class"""

import tkinter as tk

import guitk as ui

# If you need to use a custom widget with guitk, you first need to wrap
# the widget in a guitk Widget class so it can work with guitk events
# and layouts. You can do this with the widget_class_factory function
# which returns a new Widget class for your custom widget. Note that
# widget_class_factory returns the class, not the instance, so you
# will need to instantiate the class (inside a Layout or Containter)
# to use it. Once you have the class, you can use it just like any
# other guitk Widget class.
CustomEntry = ui.widget_class_factory(
    tk.Entry, value_type=tk.StringVar, value_name="textvariable"
)
CustomButton = ui.widget_class_factory(tk.Button, event_type="my_button")

# You can also directly wrap the custom widget in a Widget class which
# returns an instance of the Widget class. This should be done inside
# a Layout or Container just as any other guitk Widget.
# see the example below.

class CustomWidget(ui.Window):
    def config(self):
        with ui.VLayout(valign="top", halign="center"):
            ui.Label(text="Type your name then press Hello or hit Return:")
            CustomEntry(
                key="custom_entry",
                events=True,
                focus=True,
            )
            ui.Label("", key="greeting")
            CustomButton(text="I'm stretched across the window", weightx=1, sticky="ew")
            with ui.HStack():
                CustomButton(text="Hello", key="hello_button")
                ui.Widget(
                widget_class=tk.Button,
                event_type="button2",
                text="Goodbye",
                key="custom_button2",
                )

    def setup(self):
        # bind the <Return> from CustomEntry to a command
        # this isn't necessary for a guitk.Entry because guitk does this for you
        # but it is necessary for a custom widget to handle events other than the default
        entry = self.get("custom_entry")
        entry.bind_event("<Return>")


    @ui.on(key="hello_button")
    @ui.on(key="custom_entry", event_type="<Return>")
    def on_hello(self, event: ui.Event):
        """Say hello after the user presses the Hello button or presses Return in the Entry"""
        self.get("greeting").value = f"Hello {self.get('custom_entry').value}"

    @ui.on(event_type="button2")
    def on_button2(self):
        print("Goodbye")
        self.quit()

    def handle_event(self, event: ui.Event):
        print(event)


if __name__ == "__main__":
    CustomWidget().run()
