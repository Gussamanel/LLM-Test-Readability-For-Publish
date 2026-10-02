import pytest

import typed_ast.ast3 as typed_ast_ast3

def test_dump_returns_none_when_input_is_none():
    """Verify module_0.dump does not raise and returns None for a None input."""
    # Arrange
    NONE_INPUT = None

    # Act
    result = module_0.dump(NONE_INPUT)

    # Assert
    assert result is None

