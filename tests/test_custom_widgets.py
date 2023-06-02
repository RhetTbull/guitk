"""Test custom widgets created with Widget() and widget_class_factory()"""


from .runner import TestRunner


def test_linklabel():
    runner = TestRunner(
        path="./examples/custom_widget.py",
        class_="CustomWidget",
        description="Test widgets created with widget_class_factory() and Widget(). "
        "Verify that the custom Entry and Buttons work as expected."
    )
    assert not runner.run()
