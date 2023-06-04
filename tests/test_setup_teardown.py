"""Test setup() and teardown() behavior."""

import pytest

from .class_loader import load_class


def test_setup_teardown(capsys):
    """Test setup() and teardown() behavior."""
    test_class = load_class("./examples/setup_teardown.py", "SetupTeardown")

    test_class().run()
    captured = capsys.readouterr()
    assert (
        captured.out
        == "setup 1\nsetup 2\nsetup 3\nteardown 1\nteardown 2\nteardown 3\n"
    )
