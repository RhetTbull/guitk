"""Demo showing use of VSpacer()"""

from guitk import Button, Entry, Label, VLayout, VSpacer, Window


class Hello(Window):
    def config(self):
        self.size = (240, 600)
        with VLayout():
            Label("What's your name?")
            Entry(key="ENTRY_NAME")
            VSpacer()
            Button("Ok")


if __name__ == "__main__":
    Hello().run()
