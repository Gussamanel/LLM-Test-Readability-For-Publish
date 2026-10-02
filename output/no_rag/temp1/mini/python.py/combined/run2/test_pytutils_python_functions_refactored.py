import pytest

import python as python_module

def test_pyinfo_initialization_creates_pyinfo_instance():
    # Purpose:
    #   Verify that module_0.PyInfo can be instantiated and that the
    #   created object is an instance of module_0.PyInfo.
    #
    # Arrange
    expected_type = module_0.PyInfo

    # Act
    pyinfo = module_0.PyInfo()

    # Assert
    assert isinstance(pyinfo, expected_type)

