import packages as pkgs

def test_version_part_conversion_to_string():
    # Constants
    VERSION_PART = pkgs.module_0._VersionPart()
    NON_ZERO_DIGITS = [1, 2, 3]
    NO_OF_DIGITS_IN_VERSION_PART = 3

    # Setup
    VERSION_PART.from_version_part_to(NON_ZERO_DIGITS)

    # Execution
    version_part_str = VERSION_PART.to_str()

    # Assertion
    assert len(version_part_str) == NO_OF_DIGITS_IN_VERSION_PART, \
        f"Expected version part length to be {NO_OF_DIGITS_IN_VERSION_PART}, but got {len(version_part_str)}"

