"""Test PanedWindow widget"""


from .runner import TestRunner


def test_align():
    runner = TestRunner(
        path="./examples/panedwindow.py",
        class_="PanedDemo",
        description="Test PanedWindow widget. "
        "Verify both horizontal and vertical panes are aligned correctly and can be resized.",
    )
    assert not runner.run()
