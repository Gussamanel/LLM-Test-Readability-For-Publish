import pytest
import typed_ast.ast3 as ast3

def test_dump_none_value_handles_none_without_exception():
    none_value = None
    module_0.dump(none_value)

