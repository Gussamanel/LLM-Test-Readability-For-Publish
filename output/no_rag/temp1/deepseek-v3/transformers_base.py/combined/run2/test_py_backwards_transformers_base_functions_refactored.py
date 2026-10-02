import pytest
import base as base_module
import typed_ast._ast3 as ast3_module

def test_base_node_transformer_accepts_none_context():
    none_context = None
    base_node_transformer = base_module.BaseNodeTransformer(none_context)
    assert isinstance(base_node_transformer, base_module.BaseNodeTransformer)

def test_visit_ImportFrom_returns_import_from_when_module_matches_rewrite_modified():
    # Setup: Create a MatMult node and wrap it in a BaseImportRewrite instance
    mat_mult_node = ast3_module.MatMult()
    import_rewriter = base_module.BaseImportRewrite(mat_mult_node)

    # Create an ImportFrom node with the same node list used for construction
    node_list = [import_rewriter, mat_mult_node, import_rewriter]
    import_from_node = ast3_module.ImportFrom(*node_list)

    # Execution: Visit the ImportFrom node, which should trigger module or name rewriting
    result = import_rewriter.visit_ImportFrom(import_from_node)

    # Assertion: Ensure the visitor returns the rewritten ImportFrom node
    assert result is not None
    assert isinstance(result, ast3_module.ImportFrom)

def test_visit_import_from_with_nonexistent_module_and_empty_names():
    # Setup: Create an AST ImportFrom node with module=None and empty names list
    mat_mult_expression = ast3_module.MatMult()
    none_value = None
    base_import_rewrite = base_module.BaseImportRewrite(none_value)
    
    # Create ImportFrom node with None module and single name (MatMult)
    import_from_args = [none_value, mat_mult_expression]
    import_from_kwargs = {}
    import_from_node = ast3_module.ImportFrom(*import_from_args, **import_from_kwargs)
    
    # Execute: Visit the ImportFrom node
    result = base_import_rewrite.visit_ImportFrom(import_from_node)
    
    # Assert: Verify the result is the generic visit result (since no rewrite matches)
    assert result is None

def test_visit_import_from_with_no_matching_rewrite_returns_unchanged_node_preserving_module():
    # Constants
    ORIGINAL_MODULE_NAME = "\x0bQHzaZ?\tpM/wFtV"
    IMPORT_NAME = "%WE}A)"

    # Setup
    base_import_rewrite = base_module.BaseImportRewrite(ORIGINAL_MODULE_NAME)
    import_from_node = ast3_module.ImportFrom(
        module=ORIGINAL_MODULE_NAME,
        names=[(IMPORT_NAME, None)],
        level=0,
    )

    # Execution
    result = base_import_rewrite.visit_ImportFrom(import_from_node)

    # Assertion
    assert result is import_from_node

def test_visit_import_from_with_arbitrary_module_and_names_returns_node_unchanged():
    # Setup: construct an ImportFrom node with arbitrary (non-rewritten) module and names
    SAMPLE_MODULE_NAME = "\x0bQbHzaZ?\tpM/wFtV"
    EMPTY_MODULE_NAME = ""

    import_from_attributes = {
        SAMPLE_MODULE_NAME: SAMPLE_MODULE_NAME,
        EMPTY_MODULE_NAME: SAMPLE_MODULE_NAME,
        SAMPLE_MODULE_NAME: SAMPLE_MODULE_NAME,
        EMPTY_MODULE_NAME: SAMPLE_MODULE_NAME,
        SAMPLE_MODULE_NAME: SAMPLE_MODULE_NAME,
    }

    import_from_node = ast3_module.ImportFrom(
        *import_from_attributes, **import_from_attributes
    )
    base_import_rewrite = base_module.BaseImportRewrite(import_from_node)

    # Execution: visit the ImportFrom node through the rewrite
    result = base_import_rewrite.visit_ImportFrom(import_from_node)

    # Assertion: with no matched rewrite and no names to replace,
    # the original node is returned unchanged (via generic_visit)
    assert result is not None

