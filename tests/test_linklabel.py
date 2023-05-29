"""Test LinkLabel widget as well as font() and style()"""


from .runner import TestRunner


def test_remove():
    runner = TestRunner(
        path="./examples/link.py",
        class_="ClickMe",
        description="Test various LinkLabel and font(), style(). "
        "Link should be clickable and in large, underline blue font.",
    )
    assert not runner.run()
