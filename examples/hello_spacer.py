"""Demo showing use of HSpacer()"""

from guitk import Button, Entry, Label, Layout, HSpacer, Window


class Hello(Window):
    def config(self):
        self.size = (640, 200)
        with Layout(valign="center") as layout:
            Label("What's your name?")
            Entry(key="ENTRY_NAME", events=True)
            HSpacer()
            Button("Ok")


if __name__ == "__main__":
    Hello().run()
