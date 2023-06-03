"""Test list behavior of Spacer()"""


from .runner import TestRunner


def test_linklabel():
    runner = TestRunner(
        path="./examples/spacer_demo.py",
        class_="SpacerDemo",
        description="Test the behavior of VSpacer/HSpacer.\n"
        "Verify that widgets reposition themselves as you resize the window.",
    )
    assert not runner.run()
