""" Container classes for guitk """

from guitk.constants import GUITK

from .constants import DEFAULT_PADX, DEFAULT_PADY
from .frame import Container, LayoutMixin
from .layout import get_parent, pop_parent, push_parent
from .widget import Widget


class Stack(Container):
    """A container that stacks widgets vertically when added to a Layout"""

    def __init__(
        self,
        key: str | None = None,
        width: int | None = None,
        height: int | None = None,
        padding: int | None = None,
        disabled: bool | None = False,
        sticky: bool | None = None,
    ):
        super().__init__(
            frametype=GUITK.ELEMENT_FRAME,
            key=key,
            width=width,
            height=height,
            layout=None,
            style=None,
            borderwidth=None,
            padding=padding,
            relief=None,
            disabled=disabled,
            rowspan=None,
            columnspan=None,
            sticky=sticky,
            tooltip=None,
            autoframe=False,
            padx=0,
            pady=0,
        )

    def __enter__(self):
        push_parent(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # reorder the layout to be vertical
        self.layout = [[x] for x in self.layout[0]]
        pop_parent()
        return False


class Row(Container):
    """A container that stacks widgets horizontally when added to a Layout"""

    def __init__(
        self,
        disabled: bool | None = False,
    ):
        super().__init__(
            frametype=GUITK.ELEMENT_FRAME,
            key=None,
            width=None,
            height=None,
            layout=None,
            style=None,
            borderwidth=None,
            padding=0,
            relief=None,
            disabled=disabled,
            rowspan=None,
            columnspan=None,
            sticky=None,
            tooltip=None,
            autoframe=False,
            padx=0,
            pady=0,
        )

    def __enter__(self):
        push_parent(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pop_parent()
        return False
