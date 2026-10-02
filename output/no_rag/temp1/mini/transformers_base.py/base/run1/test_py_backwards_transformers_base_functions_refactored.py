import pytest

import base as base_module
import typed_ast._ast3 as typed_ast_ast3

def test_base_node_transformer_can_initialize_with_none_parent():
    # Purpose:
    # Verify that BaseNodeTransformer can be constructed when given None as the parent
    # (i.e., that initialization does not raise and returns an instance of the expected type).

    # Constants
    NONE_PARENT = None

    # Setup (Arrange)
    parent = NONE_PARENT

    # Execution (Act)
    transformer = base_module.BaseNodeTransformer(parent)

    # Assertion (Assert)
    # - The constructor should return an object (not raise and not return None)
    # - The returned object should be an instance of BaseNodeTransformer
    assert transformer is not None
    assert isinstance(transformer, base_module.BaseNodeTransformer)

def test_visit_importfrom_returns_ast_when_rewrite_matches():
    # Purpose:
    # Verify that BaseImportRewrite.visit_ImportFrom returns an AST node
    # when called with an ImportFrom node that may match a module rewrite
    # or contain names to replace.

    # Setup: create the rewrite target and the BaseImportRewrite instance.
    mat_mult_instance = module_1.MatMult()
    base_import_rewrite = module_0.BaseImportRewrite(mat_mult_instance)

    # Construct the ImportFrom node used as input. The original test passed
    # the rewriter and the mat_mult instance into the ImportFrom constructor.
    import_from_node = module_1.ImportFrom(base_import_rewrite, mat_mult_instance, base_import_rewrite)

    # Execution: call the visitor method under test.
    result = base_import_rewrite.visit_ImportFrom(import_from_node)

    # Assertion: the visitor should return an AST node (ImportFrom, Try, or other AST).
    assert isinstance(result, typed_ast_ast3.AST)

def test_visit_importfrom_with_no_module_and_no_rewrites_returns_same_node():
    """Verify BaseImportRewrite.visit_ImportFrom returns the original node when module is None and there are no rewrites."""
    MODULE_NAME = None
    mat_mult_node = typed_ast_ast3.MatMult()
    import_from_node = typed_ast_ast3.ImportFrom(MODULE_NAME, mat_mult_node)
    base_rewriter = base_module.BaseImportRewrite(MODULE_NAME)

    result_node = base_rewriter.visit_ImportFrom(import_from_node)

    assert result_node is import_from_node

def test_visit_importfrom_falls_back_to_generic_visit_when_no_rewrites_or_name_replacements():
    # Purpose:
    # Verify BaseImportRewrite.visit_ImportFrom correctly handles an ImportFrom node
    # when there is no matched module rewrite and there are no names to replace.
    # In that situation the method should fall back to a generic visit and return
    # an AST node (often the same node or a visited variant).
    
    # Constants / test data
    MODULE_NAME = "\x0bQHzaZ?\tpM/wFtV"
    
    # Setup: create the rewriter configured for MODULE_NAME and an ImportFrom node
    rewriter = base_module.BaseImportRewrite(MODULE_NAME)
    import_from_node = typed_ast_ast3.ImportFrom(module=MODULE_NAME, names=[], level=0)
    
    # Execution: run the visitor on the ImportFrom node
    result_node = rewriter.visit_ImportFrom(import_from_node)
    
    # Assertion: ensure a valid AST node is returned (fallback to generic_visit)
    assert isinstance(result_node, typed_ast_ast3.AST)

def test_visit_importfrom_returns_original_node_when_no_rewrite_matches():
    # Purpose:
    # Verify that BaseImportRewrite.visit_ImportFrom falls back to generic_visit
    # (i.e., returns the original ImportFrom AST node) when there is no module-level
    # rewrite and no individual names to replace.

    # Constants / test data
    MODULE_NAME = "example.module"
    ALIAS_NAME = "some_name"
    AS_NAME = None
    LEVEL = 0

    # Setup: construct a simple ImportFrom node and the BaseImportRewrite visitor.
    # The ImportFrom imports "some_name" from "example.module" at level 0.
    import_node = typed_ast_ast3.ImportFrom(MODULE_NAME, [typed_ast_ast3.alias(ALIAS_NAME, AS_NAME)], LEVEL)
    visitor = base_module.BaseImportRewrite(import_node)

    # Execution: explicitly call the visit_ImportFrom method under test.
    result = visitor.visit_ImportFrom(import_node)

    # Assertion: since no rewrite should match, the visitor should return an AST node
    # representing the ImportFrom (generic_visit path). Check type and preserved content.
    assert isinstance(result, typed_ast_ast3.ImportFrom)
    assert result.module == MODULE_NAME
    assert isinstance(result.names, list) and result.names[0].name == ALIAS_NAME

