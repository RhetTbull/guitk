"""Test Menus"""


from .runner import TestRunner


def test_replace():
    runner = TestRunner(
        path="./examples/menu.py",
        class_="MenuDemo",
        description="Test behavior of menus.",
    )
    assert not runner.run()
