import pytest

import typed_ast._ast3 as ast3_internal
import dict_unpacking as dict_unpacking_utils
import typed_ast.ast3 as ast3

def test_dict_unpacking_transformer_initializes_with_module():
    """
    Purpose:
    - Verify that DictUnpackingTransformer can be constructed with a module AST produced
      by module_0.mod() without raising, and that the resulting object is an instance
      of the expected transformer class and exposes expected visitor-like behavior.

    Setup:
    - Create the module AST using the factory from module_0.
    - Capture the transformer class from module_1 for clarity.
    """
    # Constants / fixtures
    MODULE_FACTORY = module_0.mod
    TRANSFORMER_CLASS = module_1.DictUnpackingTransformer

    # --- Setup ---
    input_module = MODULE_FACTORY()

    # --- Execution ---
    transformer = TRANSFORMER_CLASS(input_module)

    # --- Assertions ---
    # The transformer should be an instance of the expected class.
    assert isinstance(transformer, TRANSFORMER_CLASS)

    # The transformer should not be None and should expose visitor-like behavior.
    # Many AST transformers provide a 'visit' method (or similar). Ensure at least one exists.
    assert transformer is not None
    assert any(hasattr(transformer, name) for name in ("visit", "visit_Module", "transform")), (
        "Transformer should expose a visitor/transform method (e.g., 'visit', 'visit_Module' or 'transform')."
    )

def test_visit_module_returns_original_module_after_insertion():
    # Core purpose:
    # Verify that DictUnpackingTransformer.visit_Module returns the original Module node
    # after performing its in-place insertion of merged dicts at the start of the body.
    # Setup: prepare source, transformer and parsed AST node
    SOURCE_CODE = "39@U3\r"
    transformer = dict_unpacking_utils.DictUnpackingTransformer(SOURCE_CODE)
    parsed_module = ast3.parse(SOURCE_CODE)

    # Execution: run the visit_Module method which is expected to mutate and return the node
    visited_module = transformer.visit_Module(parsed_module)

    # Assertions: the returned node should be the same object as the parsed module
    # and should be an AST Module from typed_ast.ast3
    assert visited_module is parsed_module, "visit_Module should return the original Module node after processing"
    assert isinstance(parsed_module, ast3.Module), "parsed object should be an ast Module"
    assert isinstance(visited_module, ast3.Module), "visited result should be an ast Module"

