import pytest

import python as python_module

def test_create_pyinfo_instance():
    """
    Verify that a PyInfo object can be instantiated and is of the expected type.
    """
    EXPECTED_CLASS = python_module.PyInfo

    # Arrange: keep the class selection explicit
    pyinfo_class = EXPECTED_CLASS

    # Act: construct the object under test
    pyinfo_instance = pyinfo_class()

    # Assert: object created and type matches expectation
    assert pyinfo_instance is not None
    assert isinstance(pyinfo_instance, EXPECTED_CLASS)

