"""@on decorator for defining event handlers """

from __future__ import annotations

from functools import wraps
from typing import Callable, Hashable

from .events import EventType
from .types import CommandType, DecoratedType


def on(
    key: Hashable | None = None,
    event_type: EventType | None = None,
) -> CommandType:
    """Decorator to declare that the method is an event handler.

    The decorated method will be called when a widget with the given `key`
    emits an event or an event of the given `event_type` is emitted.

    Example:
        ```python
        # Handle the press of buttons with key "OK"
        @on(key="OK")
        def ok_button(self) -> None:
            ...

        # Handle the press of any button
        @on(event_type=EventType.ButtonPressed)
        def any_button(self) -> None:
            ...

        # Handle the press of buttons with key "OK" or "Cancel"
        @on(key="OK", event_type=EventType.ButtonPressed)
        @on(key="Cancel", event_type=EventType.ButtonPressed)
        def ok_or_cancel_button(self) -> None:
            ...

        # Handle any event
        @on(event_type=EventType.Any)
        def any_event(self) -> None:
            ...
        ```

    Args:
        key (Hashable, optional): Key of the event to handle. Defaults to None.
        event_type (EventType, optional): Type of the event to handle. Defaults to None.

    Note: Either `key` or `event_type` must be specified and both can be specified.
    """
    # Inspired by the implementation of the `on` decorator in textual
    # https://github.com/Textualize/textual

    # Event handlers registered with the `on` decorator are stored in the
    # `_guitk_event_handlers` attribute of the decorated method and are bound
    # by Window._bind_event_handlers() then called by Window._handle_commands()

    if not key and not event_type:
        raise ValueError("Either key or event_type (or both) must be specified")

    def decorate(method: Callable[..., DecoratedType]):
        if not hasattr(method, "_guitk_event_handlers"):
            method._guitk_event_handlers = []
        getattr(method, "_guitk_event_handlers").append((key, event_type))

        @wraps(method)
        def wrapper(*args, **kwargs) -> DecoratedType:
            """Store key, event_type, return callable unaltered."""
            return method(*args, **kwargs)

        return wrapper

    return decorate
