import pytest

import packages as packages_module

def test_version_part_default_initialization():
    version_part_instance = packages_module._VersionPart()
    assert version_part_instance is not None

