"""Test Image widget."""

from .runner import TestRunner


def test_image():
    """Test Image()"""
    runner = TestRunner(
        path="./examples/image.py",
        class_="ImageDemo",
        description="Test Image widget as well as Label and Button widgets with images.",
    )
    assert not runner.run()
