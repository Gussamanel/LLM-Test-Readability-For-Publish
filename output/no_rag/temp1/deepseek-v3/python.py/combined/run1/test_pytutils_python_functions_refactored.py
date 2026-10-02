import pytest
import python as python_module

def test_initialization_of_pyinfo_with_default_constructor():
    """Verify that a PyInfo instance can be created with default arguments."""
    py_info = python_module.PyInfo()

    assert py_info is not None
    assert isinstance(py_info, python_module.PyInfo)

