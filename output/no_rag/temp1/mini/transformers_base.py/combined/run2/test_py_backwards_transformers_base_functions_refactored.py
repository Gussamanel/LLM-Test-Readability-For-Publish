import pytest

import base as base_module
import typed_ast._ast3 as typed_ast_ast3

def test_base_node_transformer_initializes_with_none_parent():
    # Purpose:
    # Verify that BaseNodeTransformer can be constructed when provided a None parent.
    # This ensures the class handles a missing/optional parent transformer gracefully.

    # Constants / Test data
    NONE_PARENT = None

    # Setup (Arrange)
    parent_transformer = NONE_PARENT

    # Execution (Act)
    transformer = base_module.BaseNodeTransformer(parent_transformer)

    # Assertion (Assert)
    # - The constructor should return a non-None object
    # - The object should be an instance of BaseNodeTransformer
    assert transformer is not None
    assert isinstance(transformer, base_module.BaseNodeTransformer)

def test_visit_importfrom_returns_ast_node_when_processing_matmult_and_rewrites():
    # Purpose:
    # Ensure BaseImportRewrite.visit_ImportFrom can handle an ImportFrom node
    # composed of a mix of rewrite helpers and target-module helpers and returns
    # an AST node without raising exceptions.

    # Arrange: create a MatMult helper and the BaseImportRewrite under test.
    mat_mult = module_1.MatMult()
    base_import_rewrite = module_0.BaseImportRewrite(mat_mult)

    # Construct an ImportFrom node using a mix of rewrite helpers and the target helper.
    import_from_args = [base_import_rewrite, mat_mult, base_import_rewrite]
    import_from_node = module_1.ImportFrom(*import_from_args)

    # Act: run the visitor method.
    result_node = base_import_rewrite.visit_ImportFrom(import_from_node)

    # Assert: the result is an AST node (typed_ast AST base type).
    assert isinstance(result_node, typed_ast_ast3.AST)

def test_visit_importfrom_returns_ast_when_no_module_rewrite_matches():
    # Purpose:
    # Verify that BaseImportRewrite.visit_ImportFrom processes an ImportFrom node
    # and returns an AST-derived object when there is no module-level rewrite match.
    # The test constructs a minimal ImportFrom node and ensures the visitor returns
    # an AST node (it may be the original node or a transformed node).

    # --- Setup ---
    MODULE_NAME = None
    mat_mult_node = module_1.MatMult()
    base_rewriter = module_0.BaseImportRewrite(MODULE_NAME)

    # Create an ImportFrom node with the module set to None and the names/second arg
    # set to the MatMult-like node. This mirrors the original test shape.
    import_from_node = module_1.ImportFrom(MODULE_NAME, mat_mult_node)

    # --- Execution ---
    result = base_rewriter.visit_ImportFrom(import_from_node)

    # --- Assertion ---
    # The visitor should return an AST node (could be the same node or a transformed one).
    assert isinstance(result, typed_ast_ast3.AST)

def test_visit_import_from_handles_duplicate_name_mappings():
    # Core purpose:
    # Verify that BaseImportRewrite.visit_ImportFrom can accept an ImportFrom node
    # constructed from a mapping that contains duplicate keys/values and that it
    # returns an AST node (and does not raise).
    #
    # Arrange: define constants and build the rewriter and the ImportFrom node.
    MODULE_NAME = "\x0bQHzaZ?\tpM/wFtV"
    ALIAS_NAME = "%WE}A)"
    # Intentionally include duplicate keys/values to mirror the original test input shape.
    NAMES_MAPPING = {
        MODULE_NAME: ALIAS_NAME,
        ALIAS_NAME: ALIAS_NAME,
        ALIAS_NAME: ALIAS_NAME,
        MODULE_NAME: ALIAS_NAME,
    }

    rewriter = base_module.BaseImportRewrite(MODULE_NAME)
    # Construct an ImportFrom node using the same pattern as the original test:
    # unpacking the dict as positional args (iterates keys) and as keyword args.
    import_from_node = typed_ast_ast3.ImportFrom(*NAMES_MAPPING, **NAMES_MAPPING)

    # Act: invoke the visitor
    result_node = rewriter.visit_ImportFrom(import_from_node)

    # Assert: ensure a valid AST node is returned and nothing raised
    assert result_node is not None
    assert isinstance(result_node, typed_ast_ast3.AST)

def test_visit_importfrom_returns_ast_when_no_rewrite_and_no_name_replacements():
    # Purpose:
    # - Verify BaseImportRewrite.visit_ImportFrom returns a valid AST node
    #   (falls back to generic_visit) when there is no module rewrite match
    #   and no names-to-replace are found.
    #
    # Setup:
    # - Create a synthetic ImportFrom node with a module name and a single alias.
    # - Instantiate BaseImportRewrite with the created node as context.
    MODULE_NAME = "some_random_module_name"
    ALIAS_NAME = "some_name"
    import_from_node = typed_ast_ast3.ImportFrom(
        module=MODULE_NAME,
        names=[typed_ast_ast3.alias(name=ALIAS_NAME, asname=None)],
        level=0,
    )

    base_rewriter = base_module.BaseImportRewrite(import_from_node)

    # Execution:
    result = base_rewriter.visit_ImportFrom(import_from_node)

    # Assertion:
    # - The returned value should be an AST node.
    # - If it's an ImportFrom node, ensure it preserves the module and alias name.
    assert isinstance(result, typed_ast_ast3.AST)
    if isinstance(result, typed_ast_ast3.ImportFrom):
        assert result.module == MODULE_NAME
        assert result.names and result.names[0].name == ALIAS_NAME

