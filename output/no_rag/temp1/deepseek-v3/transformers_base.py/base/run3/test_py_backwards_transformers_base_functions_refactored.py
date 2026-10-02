import pytest
import base as base_module
import typed_ast._ast3 as ast3_module

def test_base_node_transformer_initialization_with_none_argument():
    # Constants
    NONE_VALUE = None

    # Setup
    # Create a BaseNodeTransformer instance by passing None as the argument
    transformer = base_module.BaseNodeTransformer(NONE_VALUE)

    # Assertion
    # Verify that the transformer was created successfully
    assert transformer is not None

def test_visit_importfrom_with_non_matching_module_and_names_returns_unchanged_node():
    # Setup: create a MatMult node and wrap it in a BaseImportRewrite visitor.
    # These nodes are used to construct an ImportFrom node that references
    # a module and names that do not match anything in the rewrite mappings.
    mat_mult_node = ast3_module.MatMult()
    base_import_rewrite_visitor = base_module.BaseImportRewrite(mat_mult_node)

    # Build the ImportFrom node with three positional arguments (mimicking the
    # original test's list-based construction). The first and third arguments
    # are the visitor/MatMult nodes, which are not valid ImportFrom fields but
    # are used here to exercise the visit_ImportFrom code path.
    import_from_args = [
        base_import_rewrite_visitor,
        mat_mult_node,
        base_import_rewrite_visitor,
    ]
    import_from_node = ast3_module.ImportFrom(*import_from_args)

    # Execution: invoke the visitor on the ImportFrom node. Since the module
    # and names do not match any configured rewrite, the method should fall
    # through to generic_visit and return the node (or its generic visit result).
    result = base_import_rewrite_visitor.visit_ImportFrom(import_from_node)

    # Assertion: the visitor should not raise and should return an AST node,
    # confirming the non-matching path of visit_ImportFrom was exercised.
    assert isinstance(result, ast3_module.AST)

def test_visit_import_from_without_matching_rewrite_returns_unchanged_node():
    # Setup: create a BaseImportRewrite with no matching module rewrites
    base_import_rewrite = base_module.BaseImportRewrite(None)

    # Create an ast.ImportFrom node with module=None and no names
    import_from_node = ast3_module.ImportFrom(module=None, names=[], level=0)

    # Execution: visit the ImportFrom node
    result = base_import_rewrite.visit_ImportFrom(import_from_node)

    # Assertion: since no rewrite matched and no names to replace, the original node is returned unchanged
    assert result is import_from_node

def test_visit_importfrom_with_unmatched_module_and_no_names_to_replace_returns_unchanged_node():
    # Setup: a BaseImportRewrite with a module string that will not match any rewrite rule
    module_name = "\x0bQHzaZ?\tpM/wFtV"
    base_import_rewrite = base_module.BaseImportRewrite(module_name)

    # Setup: an ImportFrom node whose module and names do not match any rewrite
    import_name = "%WE}A)"
    import_from_kwargs = {
        module_name: import_name,
        import_name: import_name,
        import_name: import_name,
        module_name: import_name,
    }
    import_from_node = ast3_module.ImportFrom(*import_from_kwargs, **import_from_kwargs)

    # Execution: visiting the ImportFrom should fall through to the generic visit
    result = base_import_rewrite.visit_ImportFrom(import_from_node)

    # Assertion: no rewrite should be applied, so the original node is returned unchanged
    assert result is import_from_node

def test_visit_import_from_with_unmatched_module_returns_original_node():
    # Setup: create an ImportFrom node whose module name does not match any rewrite
    # configuration on the BaseImportRewrite instance, so visit_ImportFrom should
    # fall through to generic_visit and return the original node.
    UNMATCHED_MODULE_NAME = "\x0bQbHzaZ?\tpM/wFtV"
    EMPTY_MODULE_NAME = ""

    # Build keyword arguments for ImportFrom using a dict; note keys collide,
    # leaving only the last distinct key ("") in the resulting kwargs.
    import_from_kwargs = {
        UNMATCHED_MODULE_NAME: UNMATCHED_MODULE_NAME,
        EMPTY_MODULE_NAME: UNMATCHED_MODULE_NAME,
        UNMATCHED_MODULE_NAME: UNMATCHED_MODULE_NAME,
        EMPTY_MODULE_NAME: UNMATCHED_MODULE_NAME,
        UNMATCHED_MODULE_NAME: UNMATCHED_MODULE_NAME,
    }
    import_from_node = ast3_module.ImportFrom(*import_from_kwargs, **import_from_kwargs)

    # Create the rewrite visitor that will process the ImportFrom node.
    import_rewrite = base_module.BaseImportRewrite(import_from_node)

    # Execution: attempt to rewrite the ImportFrom node.
    result_node = import_rewrite.visit_ImportFrom(import_from_node)

    # Assertion: with no matching rewrite and no names to replace, the visitor
    # should return the original node unchanged (via generic_visit).
    assert result_node is import_from_node

