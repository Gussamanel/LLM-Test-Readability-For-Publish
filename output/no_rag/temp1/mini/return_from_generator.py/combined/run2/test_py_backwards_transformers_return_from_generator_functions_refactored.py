import pytest

import typed_ast.ast3 as typed_ast_ast3

def test_dump_handles_none_without_raising():
    """Verify that the module's `dump` function accepts None and does not raise."""
    INPUT_NONE = None

    # Ensure the target provides the expected callable
    target_module = module_0
    assert hasattr(target_module, "dump") and callable(getattr(target_module, "dump")), \
        "The target module must provide a callable `dump`."

    # Execution: call dump with None (should not raise)
    target_module.dump(INPUT_NONE)

    # If no exception was raised above, the test passes.
    assert True

