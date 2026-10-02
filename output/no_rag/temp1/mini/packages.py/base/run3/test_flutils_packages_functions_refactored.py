import pytest

import packages as packages_module

def test_version_part_instantiation_creates_instance():
    """Verify that _VersionPart can be instantiated and yields an instance of the expected class."""
    # Arrange
    VERSION_PART_CLASS = packages_module.module_0._VersionPart

    # Act
    version_part_instance = VERSION_PART_CLASS()

    # Assert
    assert version_part_instance is not None
    assert isinstance(version_part_instance, VERSION_PART_CLASS)

