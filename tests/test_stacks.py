"""Test list behavior of HStack and VStack"""


from .runner import TestRunner


def test_linklabel():
    runner = TestRunner(
        path="./examples/stacks_are_lists.py",
        class_="Stacks",
        description="Test the list behavior of HStack and VStack.\n"
        "Verify that widgets can be added, inserted, extended, cleared, popped, deleted, and removed.",
    )
    assert not runner.run()
