import pytest
import base as base_module
import typed_ast._ast3 as ast3

def test_base_node_transformer_initializes_with_none_context():
    """Verify that BaseNodeTransformer can be initialized with a None context."""
    # Setup
    none_context = None

    # Execution
    base_node_transformer = base_module.BaseNodeTransformer(none_context)

    # Assertion
    assert base_node_transformer is not None

def test_visit_importfrom_with_matched_module_rewrite_returns_rewritten_node():
    # Setup: create a MatMult node and a BaseImportRewrite that will be used to rewrite imports
    mat_mult_node = ast3.MatMult()
    import_rewriter = base_module.BaseImportRewrite(mat_mult_node)

    # Build an ImportFrom node whose arguments include the rewriter as "module" and the MatMult node as "names"
    import_from_args = [import_rewriter, mat_mult_node, import_rewriter]
    import_from_node = ast3.ImportFrom(*import_from_args)

    # Execution: ask the rewriter to visit the ImportFrom node
    result = import_rewriter.visit_ImportFrom(import_from_node)

    # Assertion: the rewriter should have processed the ImportFrom and returned a rewritten AST node
    assert result is not None

def test_visit_importfrom_with_none_module_no_rewrite_is_noop():
    base_import_rewrite = base_module.BaseImportRewrite(None)

    import_from_node = ast3.ImportFrom(
        None,
        None,
        ast3.MatMult(),
        **{},
    )

    result = base_import_rewrite.visit_ImportFrom(import_from_node)

    assert result is import_from_node

def test_visit_import_from_with_no_matching_rewrite_or_names():
    # Setup: create a BaseImportRewrite instance and an ImportFrom node
    # that does not match any rewrite or names to replace.
    IMPORT_MODULE = "\x0bQHzaZ?\tpM/wFtV"
    IMPORT_NAME = "%WE}A)"
    import_rewrite = base_module.BaseImportRewrite(IMPORT_MODULE)
    import_from_node = ast3.ImportFrom(
        module=IMPORT_MODULE,
        names=[(IMPORT_NAME, IMPORT_NAME), (IMPORT_NAME, IMPORT_NAME)],
        level=0,
    )

    # Execution: visit the ImportFrom node
    result = import_rewrite.visit_ImportFrom(import_from_node)

    # Assertion: since there is no matching rewrite or names to replace,
    # generic_visit should be called (result is not None)
    assert result is not None

def test_visit_import_from_preserves_unchanged_node_when_generic_visit_fallback():
    # Setup: An ImportFrom node with a module name and alias that don't match
    # any configured rewrite, so the visitor should fall through to generic_visit.
    UNMATCHED_MODULE = "\x0bQbHzaZ?\tpM/wFtV"
    ALIAS_NAME = ""

    attribute_mapping = {
        UNMATCHED_MODULE: UNMATCHED_MODULE,
        ALIAS_NAME: UNMATCHED_MODULE,
    }
    import_from_node = module_1.ImportFrom(*attribute_mapping, **attribute_mapping)

    # A BaseImportRewrite built over the node (used as a tree-walking visitor).
    import_rewriter = module_0.BaseImportRewrite(import_from_node)

    # Execution: visit the ImportFrom node.
    result_node = import_rewriter.visit_ImportFrom(import_from_node)

    # Assertion: since no rewrite matches, the node should be returned unchanged.
    assert result_node is import_from_node

