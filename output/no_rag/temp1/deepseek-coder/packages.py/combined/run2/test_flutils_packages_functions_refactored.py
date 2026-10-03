import pytest
import packages as package

def test_import_versionpart_module():
    # Arrange
    # Defining a constant for the module version
    MODULE_VERSION = 'module_version'

    # Act
    # Importing the module and saving it under the variable 'imported_module'
    imported_module = package._VersionPart()

    # Assert
    # Asserting that the imported module is of the expected type (class)
    assert isinstance(imported_module, type(package._VersionPart))
    # Asserting that the module name is as expected
    assert imported_module.__name__ == MODULE_VERSION

