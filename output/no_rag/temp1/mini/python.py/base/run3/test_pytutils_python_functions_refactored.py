import pytest

import python as python_module

def test_create_pyinfo_returns_instance():
    """Verify that calling the PyInfo constructor returns a valid instance."""
    EXPECTED_CLASS = python_module.PyInfo

    # Execution: create a PyInfo instance
    pyinfo = python_module.PyInfo()

    # Assertions:
    assert pyinfo is not None, "PyInfo() returned None instead of an object"
    assert isinstance(pyinfo, EXPECTED_CLASS), f"Expected instance of {EXPECTED_CLASS.__name__}, got {type(pyinfo).__name__}"

