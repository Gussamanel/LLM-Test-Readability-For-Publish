import pytest

import python as python_module

def test_pyinfo_instantiation_creates_instance():
    """Ensure module_0.PyInfo() constructs successfully and returns the expected type."""
    PYINFO_CLASS = module_0.PyInfo  # class under test

    # Instantiate using the default constructor
    pyinfo_instance = PYINFO_CLASS()

    # Verify an object was created and is an instance of the expected class
    assert pyinfo_instance is not None, "PyInfo() returned None instead of an instance"
    assert isinstance(pyinfo_instance, PYINFO_CLASS), f"Expected instance of {PYINFO_CLASS}, got {type(pyinfo_instance)}"

