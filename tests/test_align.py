"""Test valign, halign"""


from .runner import TestRunner


def test_align():
    runner = TestRunner(
        path="./examples/align.py",
        class_="Align",
        description="Test alignment. In the test window, adjust alignment and verify behavior.",
    )
    assert not runner.run()
