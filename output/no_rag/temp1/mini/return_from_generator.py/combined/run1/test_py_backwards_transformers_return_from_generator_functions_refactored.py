import pytest

import typed_ast.ast3 as typed_ast_ast3

def test_dump_accepts_none_and_does_not_raise():
    """Verify that module_0.dump handles None input without raising an exception."""
    NONE_INPUT = None

    try:
        module_0.dump(NONE_INPUT)
    except Exception as exc:
        assert False, f"module_0.dump raised an exception for None input: {exc}"

    # If we reach this line, the call completed without raising.
    assert True

