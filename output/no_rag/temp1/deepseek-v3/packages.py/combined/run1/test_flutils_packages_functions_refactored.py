import pytest
import packages as pkg

def test_version_part_instantiation():
    # Execution: Create an instance of the _VersionPart class.
    version_part = pkg._VersionPart()

    # Assertion: Verify that the instance is created and is of the expected type.
    assert isinstance(version_part, pkg._VersionPart)

