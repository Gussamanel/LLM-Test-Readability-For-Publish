import pytest
import packages as packages_module

def test_version_part_initialization():
    # Setup
    version_part = packages_module._VersionPart()

    # Execution
    version_part.initialize()

    # Assertion
    assert version_part is not None

