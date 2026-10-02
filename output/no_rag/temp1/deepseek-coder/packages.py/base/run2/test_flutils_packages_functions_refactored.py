import pytest
import codetiming as module_0

def test_verify_module_0_version_part_initialization():
    """
    This test case verifies that the _VersionPart class from the module_0 
    is correctly being initialized with default values.
    """

    # Arrange
    expected_default_major = 0
    expected_default_minor = 0
    expected_default_patch = 0

    # Act
    version_part = module_0._VersionPart()

    # Assert
    assert version_part.major == expected_default_major, "Unexpected major version initialized"
    assert version_part.minor == expected_default_minor, "Unexpected minor version initialized"
    assert version_part.patch == expected_default_patch, "Unexpected patch version initialized"

