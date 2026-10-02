import pytest

import python as python_module

def test_pyinfo_instantiation_returns_expected_type():
    """Verify module_0.PyInfo can be instantiated and returns the expected type."""
    EXPECTED_CLASS = module_0.PyInfo

    # Exercise
    py_info = EXPECTED_CLASS()

    # Verify
    assert py_info is not None, "PyInfo() returned None instead of an instance"
    assert isinstance(
        py_info, EXPECTED_CLASS
    ), f"Expected instance of {EXPECTED_CLASS.__name__}, got {type(py_info).__name__}"

