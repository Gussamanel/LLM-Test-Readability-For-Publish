import pytest

import base as base_module
import typed_ast._ast3 as typed_ast_ast3

def test_base_node_transformer_initializes_with_none_argument():
    """Verify that BaseNodeTransformer can be instantiated when given None as its initial argument."""
    # Setup
    initial_arg = None

    # Execution
    transformer_instance = base_module.BaseNodeTransformer(initial_arg)

    # Assertions
    assert transformer_instance is not None
    assert isinstance(transformer_instance, base_module.BaseNodeTransformer)

def test_base_import_rewrite_visit_importfrom_applies_module_rewrite():
    # Purpose:
    # Verify that BaseImportRewrite.visit_ImportFrom can be invoked with an ImportFrom node
    # that (in the original scenario) should trigger a module-level rewrite. The test
    # ensures the method completes without raising and returns an AST node (ImportFrom, Try, etc.).
    #
    # Setup
    # Create the objects used to build the ImportFrom node and the BaseImportRewrite instance.
    mat_mult_instance = module_1.MatMult()
    base_import_rewrite = module_0.BaseImportRewrite(mat_mult_instance)

    # Constant arguments list used to construct the ImportFrom node (mirrors original test shape).
    IMPORTFROM_ARGS = [base_import_rewrite, mat_mult_instance, base_import_rewrite]

    # Build the ImportFrom AST-like node using the prepared arguments.
    import_from_node = module_1.ImportFrom(*IMPORTFROM_ARGS)

    # Exercise
    # Call the visitor method under test.
    result = base_import_rewrite.visit_ImportFrom(import_from_node)

    # Assertion
    # The visit should return an AST node (such as ImportFrom or Try) and not raise an exception.
    assert isinstance(result, typed_ast_ast3.AST)

def test_base_import_rewrite_visit_importfrom_with_none_module_and_matmult_returns_ast():
    # Purpose:
    # Verify that BaseImportRewrite.visit_ImportFrom can handle an ImportFrom
    # node whose module is None and which contains a MatMult name, and that
    # it returns an AST node (either the original node or a rewritten node).
    #
    # Setup: create the MatMult name node, an ImportFrom node with module=None,
    # and an instance of BaseImportRewrite.
    MODULE_NAME_NONE = None
    matmult_name_node = module_1.MatMult()
    import_from_args = [MODULE_NAME_NONE, matmult_name_node]
    import_from_kwargs = {}

    import_rewriter = module_0.BaseImportRewrite(MODULE_NAME_NONE)
    import_from_node = module_1.ImportFrom(*import_from_args, **import_from_kwargs)

    # Execution: run the visitor on the ImportFrom node.
    result_node = import_rewriter.visit_ImportFrom(import_from_node)

    # Assertion: the visitor should return an AST node (not None).
    # We don't assert a specific rewrite behavior here — only that the result
    # is an AST instance (consistent with generic_visit returning an AST).
    assert result_node is not None
    assert isinstance(result_node, typed_ast_ast3.AST)

def test_visit_import_from_handles_module_and_name_rewrites():
    # Purpose:
    # Verify BaseImportRewrite.visit_ImportFrom can be invoked on an ImportFrom
    # node constructed from a mapping of module/name strings and returns an AST node.
    # This is intended to exercise the code paths that check for module-based
    # rewrites and name-based rewrites in visit_ImportFrom.

    # Constants: strings used for the ImportFrom node construction
    MODULE_NAME = "\x0bQHzaZ?\tpM/wFtV"
    ALIAS_NAME = "%WE}A)"

    # Setup: create the rewrite visitor and the dict used to build the ImportFrom node.
    # The original test used duplicated keys in the dict literal; keep the same mapping
    # shape to preserve behavior.
    rewrite_visitor = base_module.BaseImportRewrite(MODULE_NAME)
    mapping = {MODULE_NAME: ALIAS_NAME, ALIAS_NAME: ALIAS_NAME, ALIAS_NAME: ALIAS_NAME, MODULE_NAME: ALIAS_NAME}

    # Construct the ImportFrom node the same way the original test did.
    import_from_node = typed_ast_ast3.ImportFrom(*mapping, **mapping)

    # Execution: invoke the visitor on the ImportFrom node.
    result = rewrite_visitor.visit_ImportFrom(import_from_node)

    # Assertion: the visitor should return an AST node (could be ImportFrom, Try, or generic AST).
    assert isinstance(result, typed_ast_ast3.AST)

def test_visit_ImportFrom_with_nonstandard_module_and_duplicate_keys_calls_generic_visit():
    # Purpose:
    # Verify that BaseImportRewrite.visit_ImportFrom returns an AST node when given an
    # ImportFrom constructed from a mapping with duplicate keys and nonstandard module names.
    # This exercises the code path where no module rewrite or name replacements are applied
    # and the implementation should fall back to a generic AST visit (or return a valid AST).
    #
    # Note: the original test constructed a dict with repeated keys and passed it both as
    # positional and keyword expansions to ImportFrom. We preserve that construction here
    # to keep the test semantically equivalent.

    # --- Setup ---
    MODULE_NAME = "\x0bQbHzaZ?\tpM/wFtV"
    EMPTY_NAME = ""
    # duplicate-like mapping (duplicates in a literal would collapse to last-value for each key)
    PARAM_MAP = {MODULE_NAME: MODULE_NAME, EMPTY_NAME: MODULE_NAME}

    # Construct an ImportFrom node using the same pattern as the original test.
    import_from_node = typed_ast_ast3.ImportFrom(*PARAM_MAP, **PARAM_MAP)

    # Instantiate the rewriter with the node (mirrors original creation)
    rewriter = base_module.BaseImportRewrite(import_from_node)

    # --- Exercise ---
    result_node = rewriter.visit_ImportFrom(import_from_node)

    # --- Assertion ---
    # The result should be an AST node (either the original node, a replaced node, or another AST)
    assert isinstance(result_node, typed_ast_ast3.AST)

