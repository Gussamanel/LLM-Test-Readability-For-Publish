import pytest

import base as base_module
import typed_ast._ast3 as typed_ast_ast3

def test_base_node_transformer_accepts_none_constructor_arg():
    """Ensure BaseNodeTransformer can be constructed with None and returns the correct type."""
    CONSTRUCTOR_ARG = None

    transformer = base_module.BaseNodeTransformer(CONSTRUCTOR_ARG)

    assert transformer is not None
    assert isinstance(transformer, base_module.BaseNodeTransformer)

def test_visit_importfrom_applies_rewrite_and_returns_ast_node():
    # Purpose:
    # Verify that BaseImportRewrite.visit_ImportFrom can be invoked with an ImportFrom node
    # that references a MatMult-related object and that it returns a typed_ast AST node
    # (i.e., the visit did not raise and returned a valid AST-compatible object).

    # --- Setup ---
    # Create a MatMult helper and a BaseImportRewrite instance that uses it.
    MAT_MULT_INSTANCE = module_1.MatMult()
    base_import_rewriter = module_0.BaseImportRewrite(MAT_MULT_INSTANCE)

    # Construct the ImportFrom node arguments. The original test passed three objects;
    # keep the same structure to reproduce the same code paths.
    IMPORT_FROM_ARGS = [base_import_rewriter, MAT_MULT_INSTANCE, base_import_rewriter]
    import_from_node = module_1.ImportFrom(*IMPORT_FROM_ARGS)

    # --- Execution ---
    result_node = base_import_rewriter.visit_ImportFrom(import_from_node)

    # --- Assertion ---
    # The visitor should return an AST node (one of the allowed return types).
    assert isinstance(result_node, typed_ast_ast3.AST)

def test_visit_importfrom_with_none_module_and_no_matched_rewrite_returns_ast_node():
    # Purpose:
    # Verify that BaseImportRewrite.visit_ImportFrom can be invoked with an ImportFrom node
    # that has no module specified and a MatMult name. When there is no matched rewrite
    # and no names to replace, the method should fall back to a generic visit and
    # return an AST node (not raise).

    # Constants / test inputs
    MODULE_VALUE = None
    REWRITE_CONTEXT = None

    # Setup: create the nodes and the rewriter under test
    mat_mult_node = module_1.MatMult()
    base_rewriter = module_0.BaseImportRewrite(REWRITE_CONTEXT)

    # Construct ImportFrom node in the same manner as the original test (using unpacking)
    import_from_args = [MODULE_VALUE, mat_mult_node]
    import_from_kwargs = {}
    import_from_node = module_1.ImportFrom(*import_from_args, **import_from_kwargs)

    # Execute: call the method under test
    result = base_rewriter.visit_ImportFrom(import_from_node)

    # Assert: ensure we got back an AST node (function returns ast.AST subclasses)
    assert isinstance(result, typed_ast_ast3.AST)

def test_visit_importfrom_unmatched_module_and_names_returns_ast_node():
    # Purpose:
    # Ensure BaseImportRewrite.visit_ImportFrom returns an AST node when given an
    # ImportFrom node constructed with unusual mapping inputs (no matched rewrite).
    #
    # The original test used a mapping with repeated and unusual string keys/values
    # and passed it as both positional and keyword unpackings. This reproduces that
    # shape while making variable names and structure clearer.

    # Setup: constants and rewriter instance
    ORIGINAL_MODULE_NAME = "\x0bQHzaZ?\tpM/wFtV"
    ALIAS_NAME = "%WE}A)"
    rewriter = base_module.BaseImportRewrite(ORIGINAL_MODULE_NAME)

    # Create a mapping with repeated entries to simulate the original test inputs.
    # Note: duplicate keys in a literal will collapse; this mirrors the original test's intent.
    mapping = {
        ORIGINAL_MODULE_NAME: ALIAS_NAME,
        ALIAS_NAME: ALIAS_NAME,
        ALIAS_NAME: ALIAS_NAME,
        ORIGINAL_MODULE_NAME: ALIAS_NAME,
    }

    # Execution: construct an ImportFrom node using both positional and keyword unpacking,
    # then run the visitor.
    import_from_node = typed_ast_ast3.ImportFrom(*mapping, **mapping)
    result_node = rewriter.visit_ImportFrom(import_from_node)

    # Assertion: the visitor should return an AST node (either the original node or a transformed one).
    assert isinstance(result_node, typed_ast_ast3.AST)

def test_visit_import_from_returns_same_node_when_no_rewrite_or_name_replacements():
    # Purpose:
    # Verify that BaseImportRewrite.visit_ImportFrom returns the original ImportFrom node
    # (via generic_visit) when there is no module rewrite match and there are no names to replace.

    # Setup: create an ImportFrom node with a non-matching module name and empty names list.
    MODULE_NAME = "\x0bQbHzaZ?\tpM/wFtV"
    IMPORT_LEVEL = 0
    import_from_node = typed_ast_ast3.ImportFrom(MODULE_NAME, [], IMPORT_LEVEL)

    # Create the rewriter instance that will be exercised.
    base_rewriter = base_module.BaseImportRewrite(import_from_node)

    # Execution: call the visit_ImportFrom method under test.
    result_node = base_rewriter.visit_ImportFrom(import_from_node)

    # Assertion: when there is no rewrite and no names to replace, the node should be returned unchanged.
    assert isinstance(result_node, typed_ast_ast3.ImportFrom)
    assert result_node is import_from_node

