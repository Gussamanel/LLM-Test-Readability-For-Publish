import pytest
import python as py_module

def test_py_info_initialization_creates_valid_instance():
    # Purpose: Verify that a PyInfo object can be instantiated without errors,
    # confirming the PyInfo class is importable and has a default constructor.

    # Setup & Execution: Create a new PyInfo instance.
    py_info = py_module.PyInfo()

    # Assertion: Ensure the created object is a valid instance of PyInfo.
    assert isinstance(py_info, py_module.PyInfo)

