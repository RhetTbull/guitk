"""Test replace()"""


from .runner import TestRunner


def test_replace():
    runner = TestRunner(
        path="./examples/replace.py",
        class_="Replace",
        description="Test various widget replace() calls.",
    )
    assert not runner.run()
