"""Test VGrid, HGrid containers"""


from .runner import TestRunner


def test_grid():
    runner = TestRunner(
        path="./examples/grid.py",
        class_="Grid",
        description="Test VGrid and HGrid containers. "
        "Click Add and Remove buttons to add/remove widgets and verify grid behavior is correct.",
    )
    assert not runner.run()
