import python as py

def test_import_version_from_py_info_class():
    # Given
    py_import = py.module_0.PyInfo()   # create an instance of PyInfo class from module_0

    # Constants
    EXPECTED_VERSION = "1.0.0"

    # When
    actual_version = py_import.version()   # call the version method from the PyInfo class

    # Then
    assert actual_version == EXPECTED_VERSION, f"Expected version to be {EXPECTED_VERSION} but was {actual_version}"

    # Module_0 should import Python info correctly and return the expected version number

