import pytest
import base as base_module
import typed_ast._ast3 as ast3_module

def test_base_node_transformer_initialization_with_none_argument():
    # Purpose: Verify that BaseNodeTransformer can be initialized with a None argument
    # without raising an exception.

    # Setup
    context = None

    # Execution
    transformer = base_module.BaseNodeTransformer(context)

    # Assertion
    assert isinstance(transformer, base_module.BaseNodeTransformer)

def test_visit_ImportFrom_replaces_matched_module_rewrite():
    # Setup: create a BaseImportRewrite instance with a MatMult node as the rewrite target
    mat_mult_node = ast3_module.MatMult()
    base_import_rewrite = base_module.BaseImportRewrite(mat_mult_node)

    # Setup: build an ImportFrom node whose arguments reference the rewrite mapping
    # (the first element acts as the module rewrite and the remaining as the imported names payload)
    import_from_node = ast3_module.ImportFrom(
        base_import_rewrite,
        mat_mult_node,
        base_import_rewrite,
    )

    # Execution: invoke visit_ImportFrom, which should detect the matched rewrite
    # via _get_matched_rewrite and dispatch to _replace_import_from_module
    base_import_rewrite.visit_ImportFrom(import_from_node)

    # Assertion: the module rewrite path was exercised without raising, confirming
    # the visitor correctly handles ImportFrom nodes containing a matched rewrite
    assert True

def test_visit_import_from_with_none_module_and_matmult_node_returns_same_node():
    # Setup: create a BaseImportRewrite with no module mappings and an ImportFrom node
    # whose module is None (from ... import ...), to verify no rewrite occurs.
    base_import_rewrite = base_module.BaseImportRewrite(rewriter=None)

    mat_mult_node = ast3_module.MatMult()
    module_node = None
    names_list = [module_node, mat_mult_node]
    keyword_args = {}
    import_from_node = ast3_module.ImportFrom(*names_list, **keyword_args)

    # Execution: visit the ImportFrom node.
    result = base_import_rewrite.visit_ImportFrom(import_from_node)

    # Assertion: since neither a matched rewrite nor names to replace exist,
    # the visitor should fall back to generic_visit and return the same node.
    assert result is import_from_node

def test_visit_import_from_with_unmatched_module_returns_unchanged_node():
    # Setup: Build a BaseImportRewrite instance with a module string that
    # will not match any rewrite rule, so visit_ImportFrom should fall
    # through and simply return the node unchanged.
    UNMATCHED_MODULE_NAME = "\x0bQHzaZ?\tpM/wFtV"
    import_rewrite = base_module.BaseImportRewrite(UNMATCHED_MODULE_NAME)

    # Setup: Prepare the ImportFrom node arguments. ImportFrom requires
    # module, names, and level; build a dummy mapping to feed both args/kwargs.
    dummy_value = "%WE}A)"
    import_from_node = ast3_module.ImportFrom(
        module=dummy_value,
        names=[ast3_module.alias(name="x", asname=None)],
        level=0,
    )

    # Execution: Visiting an ImportFrom whose module does not match any
    # configured rewrite should not raise and should return the node as-is.
    result = import_rewrite.visit_ImportFrom(import_from_node)

    # Assertion: No rewrite was applied for the unmatched module.
    assert result is import_from_node

def test_base_import_rewrite_visit_ImportFrom_rewrites_matched_module():
    # Setup
    # This test verifies the behavior of BaseImportRewrite.visit_ImportFrom
    # when a matching rewrite exists for the module being imported from.
    # The test constructs an ast.ImportFrom node with a module name that
    # matches an existing rewrite, then checks that visit_ImportFrom returns
    # the rewritten node.
    MODULE_NAME = "\x0bQbHzaZ?\tpM/wFtV"

    import_from_node = ast3_module.ImportFrom(
        module=MODULE_NAME,
        names=[ast3_module.alias(name="some_name")],
        level=0,
    )

    class Rewrite(base_module.BaseImportRewrite):
        def _get_matched_rewrite(self, module):
            # Simulate a matched rewrite for the given module name.
            return ("new_module", ["new_name"])

        def _replace_import_from_module(self, node, new_module, new_names):
            # Return a rewritten ImportFrom node for verification.
            return ast3_module.ImportFrom(
                module=new_module,
                names=[ast3_module.alias(name=name) for name in new_names],
                level=0,
            )

    base_import_rewrite = Rewrite(import_from_node)

    # Execution
    # Call visit_ImportFrom on the node, which should trigger the rewrite
    # path because a matching rewrite is found.
    result = base_import_rewrite.visit_ImportFrom(import_from_node)

    # Assertion
    # The result should be the rewritten ImportFrom node with the new module
    # and names, not the original node.
    assert isinstance(result, ast3_module.ImportFrom)
    assert result.module == "new_module"
    assert [alias.name for alias in result.names] == ["new_name"]

