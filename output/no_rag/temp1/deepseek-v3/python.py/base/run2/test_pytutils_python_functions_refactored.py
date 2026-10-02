import pytest
import python as python_module

def test_pyinfo_can_be_instantiated():
    # Execution
    py_info = python_module.PyInfo()

    # Assertion
    # Core purpose: verify that PyInfo can be instantiated without errors.
    assert py_info is not None

