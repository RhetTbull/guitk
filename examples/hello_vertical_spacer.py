"""Demo showing use of VerticalSpacer()"""

from guitk import Button, Entry, Label, VerticalLayout, VerticalSpacer, Window


class Hello(Window):
    def config(self):
        self.size = (240, 600)
        with VerticalLayout() as layout:
            Label("What's your name?")
            Entry(key="ENTRY_NAME", events=True)
            VerticalSpacer()
            Button("Ok")
        self.layout = layout


if __name__ == "__main__":
    Hello().run()
