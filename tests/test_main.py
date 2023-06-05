"""Test "all widgets" demo in __main__.py."""


from guitk.__main__ import Demo

from .runner import TestRunner


def test_main():
    runner = TestRunner(
        class_=Demo, description="Test the 'all widgets' demo in __main__.py"
    )
    assert not runner.run()
