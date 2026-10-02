import pytest

import typed_ast.ast3 as ast3

def test_dump_returns_none_for_none_input():
    """Verify module_0.dump accepts None and returns None without raising."""
    result = module_0.dump(None)
    assert result is None

