"""Demo showing use of VSpacer()"""

from guitk import Button, Entry, Label, VLayout, VSpacer, Window


class Hello(Window):
    def config(self):
        self.size = (240, 600)
        with VLayout() as layout:
            Label("What's your name?")
            Entry(key="ENTRY_NAME", events=True)
            VSpacer()
            Button("Ok")
        self.layout = layout


if __name__ == "__main__":
    Hello().run()
