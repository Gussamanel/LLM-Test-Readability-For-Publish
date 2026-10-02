import pytest

import packages as packages_module

def test_version_part_constructor_smoke():
    """Smoke test: constructing the internal _VersionPart does not raise and returns an object."""
    # Constants / setup (kept for clarity)
    PACKAGE_REF = packages_module
    VERSION_PART_FACTORY = module_0._VersionPart

    # Execution
    version_part_instance = VERSION_PART_FACTORY()

    # Assertion: construction succeeded
    assert version_part_instance is not None

