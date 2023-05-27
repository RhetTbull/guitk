"""Test layout alignment"""

from guitk import (
    Button,
    CheckButton,
    ComboBox,
    HLayout,
    HSeparator,
    HStack,
    Label,
    VLayout,
    VSeparator,
    VStack,
    Window,
    on,
    set_debug,
)

_valign = None
_halign = None


class TestWindow(Window):
    def config(self):
        self.size = 400, 400
        self.title = "Test Layout Alignment"
        with VLayout():
            with HStack():
                Label("valign")
                ComboBox(
                    key="valign",
                    default="None",
                    values=["None", "Top", "Center", "Bottom"],
                )
            with HStack():
                Label("halign")
                ComboBox(
                    key="halign",
                    default="None",
                    values=["None", "Left", "Center", "Right"],
                )
            with HStack():
                Button("VLayout", key="VLayout")
                Button("HLayout", key="HLayout")
            with HStack():
                Button("VStack", key="VStack")
                Button("HStack", key="HStack")
            CheckButton("Debug", key="debug")

    @on(key="valign")
    def on_valign(self, event):
        global _valign
        combo = self[event.key].value
        _valign = None if combo == "None" else combo.lower()

    @on(key="halign")
    def on_halign(self, event):
        global _halign
        combo = self[event.key].value
        _halign = None if combo == "None" else combo.lower()

    @on(key="VLayout")
    def on_vlayout(self):
        print(_valign, _halign)
        VLayoutWindow(parent=self.window)

    @on(key="HLayout")
    def on_hlayout(self):
        HLayoutWindow(parent=self.window)

    @on(key="VStack")
    def on_vstack(self):
        VStackWindow(parent=self.window)

    @on(key="HStack")
    def on_hstack(self):
        HStackWindow(parent=self.window)

    @on(key="debug")
    def on_debug(self):
        set_debug(self["debug"].value)


class VLayoutWindow(Window):
    def config(self):
        global _valign
        global _halign
        self.size = 400, 400
        self.title = f"VLayout {_valign=} {_halign=}"
        with VLayout(valign=_valign, halign=_halign):
            Button("Hello World")
            HSeparator()
            Button("Hello World")


class HLayoutWindow(Window):
    def config(self):
        global _valign
        global _halign
        self.size = 400, 400
        self.title = f"HLayout {_valign=} {_halign=}"
        with HLayout(valign=_valign, halign=_halign):
            # Button("Not like the others", sticky="w")
            Button("Hello World")
            VSeparator()
            Button("Hello World")


class VStackWindow(Window):
    def config(self):
        global _valign
        global _halign
        self.size = 400, 400
        self.title = f"VStack {_valign=} {_halign=}"
        with VLayout():
            with VStack(valign=_valign, halign=_halign):
                Button("Hello World")
                HSeparator()
                Button("Hello World")


class HStackWindow(Window):
    def config(self):
        global _valign
        global _halign
        self.size = 400, 400
        self.title = f"HStack {_valign=} {_halign=}"
        with VLayout():
            with HStack(valign=_valign, halign=_halign):
                Button("Hello World")
                VSeparator()
                Button("Hello World")


if __name__ == "__main__":
    # set_debug(True)
    TestWindow().run()
