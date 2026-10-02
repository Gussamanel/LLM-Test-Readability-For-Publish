import pytest

import python as python_module

def test_pyinfo_default_construction_creates_pyinfo_instance():
    """Verify that PyInfo can be instantiated using its default constructor."""
    # Arrange
    PyInfoClass = python_module.PyInfo

    # Act
    instance = PyInfoClass()

    # Assert
    assert instance is not None, "PyInfo() returned None instead of an instance"
    assert isinstance(instance, PyInfoClass), "Created object is not an instance of PyInfo"

