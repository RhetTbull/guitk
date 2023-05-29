"""Test remove()"""


from .runner import TestRunner


def test_remove():
    runner = TestRunner(
        path="./examples/remove.py",
        class_="Remove",
        description="Test various widget remove() calls.",
    )
    assert not runner.run()
