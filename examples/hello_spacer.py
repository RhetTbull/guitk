"""Demo showing use of Spacer()"""

from guitk import Button, Entry, Label, Layout, Spacer, Window


class Hello(Window):
    def config(self):
        self.size = (640, 200)
        with Layout() as layout:
            Label("What's your name?")
            Entry(key="ENTRY_NAME", events=True)
            Spacer()
            Button("Ok")
        self.layout = layout


if __name__ == "__main__":
    Hello().run()
