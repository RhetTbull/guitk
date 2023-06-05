"""Test Spinbox widget"""


from .runner import TestRunner


def test_spinbox():
    runner = TestRunner(
        path="./examples/spinbox.py",
        class_="SpinboxDemo",
        description="Test the list behavior of Spinbox widget.\n"
        "Verify that Spinbox behavior is correct.",
    )
    assert not runner.run()
