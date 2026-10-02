import packages as pkgs

def test_version_part_returns_correct_values_1():
    # Arrange
    test_input = "v1.2.3"

    # Act
    result = module_0._VersionPart(test_input)

    # Assert
    assert result == pkgs.VersionPart(int(1), int(2), int(3))

