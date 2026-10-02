import pytest
import packages as pkg

def test_version_part_instantiation_without_arguments():
    # Core purpose: Verify that a VersionPart object can be instantiated without errors.
    # Setup: No specific preconditions required; import packages are available via pkg.
    # Execution
    version_part = pkg._VersionPart()

    # Assertion
    assert version_part is not None

