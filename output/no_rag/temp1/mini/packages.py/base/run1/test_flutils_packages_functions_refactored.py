import pytest

import packages as packages_module

def test_version_part_can_be_instantiated_and_is_correct_type():
    """
    Purpose:
      Verify that the internal _VersionPart class can be instantiated without error
      and that the returned object is an instance of the expected class.
    """
    # Arrange
    CLASS_UNDER_TEST = module_0._VersionPart

    # Act
    version_part_instance = CLASS_UNDER_TEST()

    # Assert
    assert version_part_instance is not None
    assert isinstance(version_part_instance, CLASS_UNDER_TEST)

