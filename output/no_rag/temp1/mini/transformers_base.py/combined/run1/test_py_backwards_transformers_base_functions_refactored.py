import pytest

import base as base_module
import typed_ast._ast3 as ast3

def test_base_node_transformer_instantiation_with_none():
    """Ensure BaseNodeTransformer can be instantiated when no base transformer is provided."""
    NO_BASE = None

    transformer = base_module.BaseNodeTransformer(NO_BASE)

    assert transformer is not None
    assert isinstance(transformer, base_module.BaseNodeTransformer)

def test_visit_importfrom_returns_ast_node_after_rewrite_or_generic_visit():
    # This test verifies that BaseImportRewrite.visit_ImportFrom returns an AST node.
    # The method under test may (1) replace the entire import-from when the module matches,
    # (2) replace specific names within the import-from, or (3) fall back to generic_visit.
    # In all cases the return value should be an AST node (ast3.AST or subclass).

    # Constants
    EXPECTED_RETURN_BASE_CLASS = ast3.AST

    # --------------------
    # Setup
    # --------------------
    # Create the MatMult helper used by the rewriter
    mat_mult_instance = module_1.MatMult()

    # Create the BaseImportRewrite instance under test, injecting the MatMult instance
    base_import_rewriter = module_0.BaseImportRewrite(mat_mult_instance)

    # Prepare arguments used to construct the ImportFrom node. We preserve the original
    # call pattern: (base_import_rewriter, mat_mult_instance, base_import_rewriter)
    import_from_args = [base_import_rewriter, mat_mult_instance, base_import_rewriter]
    import_from_node = module_1.ImportFrom(*import_from_args)

    # --------------------
    # Execution
    # --------------------
    result_node = base_import_rewriter.visit_ImportFrom(import_from_node)

    # --------------------
    # Assertion
    # --------------------
    # The visit method must return an AST node (it may return a replaced ImportFrom, a Try,
    # or a generic AST node). Confirm the result is not None and is an instance of ast3.AST.
    assert result_node is not None
    assert isinstance(result_node, EXPECTED_RETURN_BASE_CLASS)

def test_visit_importfrom_with_no_module_and_unmatched_names_uses_generic_visit():
    # Purpose:
    # Verify that BaseImportRewrite.visit_ImportFrom falls back to generic_visit
    # when there is no module rewrite match and no names to replace.

    # Constants / test data
    MODULE_NONE = None
    KWARGS = {}

    # Setup: create a MatMult node, a BaseImportRewrite instance and an ImportFrom node
    mat_mult_node = module_1.MatMult()
    rewriter = module_0.BaseImportRewrite(MODULE_NONE)
    import_from_node = module_1.ImportFrom(MODULE_NONE, mat_mult_node, **KWARGS)

    # Execution: invoke the method under test
    result = rewriter.visit_ImportFrom(import_from_node)

    # Assertion: result should equal the generic_visit outcome (fallback behavior)
    expected = rewriter.generic_visit(import_from_node)
    assert result == expected

def test_visit_importfrom_triggers_module_rewrite_returns_ast():
    # Purpose:
    # Ensure BaseImportRewrite.visit_ImportFrom triggers the "module rewrite" branch
    # when the ImportFrom.node.module matches a configured rewrite target.
    # The visitor should return an AST node (a replacement), not the original node.

    # --- Setup ---
    TARGET_MODULE = "\x0bQHzaZ?\tpM/wFtV"
    ALIAS_NAME = "%WE}A)"

    # Create a simple alias used in the ImportFrom node
    alias_node = ast3.alias(name=ALIAS_NAME, asname=None)

    # Construct an ImportFrom node whose module matches TARGET_MODULE.
    # This should cause BaseImportRewrite._get_matched_rewrite to return a rewrite.
    import_from_node = ast3.ImportFrom(module=TARGET_MODULE, names=[alias_node], level=0)

    # Instantiate the visitor configured to rewrite imports for TARGET_MODULE.
    visitor = base_module.BaseImportRewrite(TARGET_MODULE)

    # --- Execution ---
    result_node = visitor.visit_ImportFrom(import_from_node)

    # --- Assertion ---
    # Expect some AST result (could be a replaced ImportFrom, a Try, or other AST).
    assert isinstance(result_node, ast3.AST)
    # Expect that a replacement occurred (i.e., not the exact same node instance).
    assert result_node is not import_from_node

def test_visit_importfrom_no_rewrites_or_names_returns_same_node():
    # Purpose:
    # Verify that BaseImportRewrite.visit_ImportFrom returns the original node
    # when there is no module rewrite matched and there are no names to replace.
    #
    # This ensures the fallback to generic_visit behavior (no modifications).

    # Constants / setup data
    MODULE_NAME = "\x0bQbHzaZ?\tpM/wFtV"  # arbitrary module name unlikely to match any rewrite
    NAMES_LIST = []  # empty names list -> no names_to_replace

    # Setup: construct an ImportFrom AST node with no names and level 0
    import_from_node = ast3.ImportFrom(MODULE_NAME, NAMES_LIST, 0)

    # Instantiate the transformer. Passing the node as in the original test call
    transformer = base_module.BaseImportRewrite(import_from_node)

    # Execution: invoke the specific visitor method under test
    result_node = transformer.visit_ImportFrom(import_from_node)

    # Assertion: with no matching rewrite and no names to replace, the node should be unchanged
    assert result_node is import_from_node

