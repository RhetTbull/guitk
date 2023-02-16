"""Utilities for the guitk package."""

def _get_docstring(name):
    """Return the docstring of an object with name"""
    try:
        obj = globals()[name]
    except KeyError as e:
        raise ValueError(f"Invalid object name: {e}")
    return obj.__doc__ or ""
