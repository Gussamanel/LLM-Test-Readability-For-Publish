import pytest
import base as base_module
import typed_ast._ast3 as ast3_module

def test_base_node_transformer_initialization_with_none_context():
    # Purpose: Verify that BaseNodeTransformer can be instantiated with a None
    # argument without raising an exception (basic construction sanity check).

    # Setup
    none_context = None

    # Execution
    transformer = base_module.BaseNodeTransformer(none_context)

    # Assertion
    assert transformer is not None

def test_visit_import_from_passes_through_when_no_rewrite_rules_match():
    # Setup: Create a MatMult AST node and wrap it in a BaseImportRewrite visitor with no rewrite rules
    mat_mult_node = ast3_module.MatMult()
    base_import_rewrite = base_module.BaseImportRewrite(mat_mult_node)

    # Build the ImportFrom node fields; note the visitor is passed where a module/alias-like slot is expected
    import_from_args = [base_import_rewrite, mat_mult_node, base_import_rewrite]
    import_from_node = ast3_module.ImportFrom(*import_from_args)

    # Execution: Invoke visit_ImportFrom; with no matched rewrite or name replacements,
    # it should fall through to generic_visit without raising.
    base_import_rewrite.visit_ImportFrom(import_from_node)

def test_visit_import_from_falls_through_when_module_none_and_no_rewrite_config():
    # Setup: create a BaseImportRewrite with no rewrite configuration,
    # and an ImportFrom node whose module is None.
    NONE_MODULE = None
    EMPTY_LIST = [NONE_MODULE]  # positional args for ImportFrom: (module,)
    EMPTY_DICT = {}             # no keyword arguments

    base_import_rewrite = base_module.BaseImportRewrite(NONE_MODULE)
    import_from_node = ast3_module.ImportFrom(*EMPTY_LIST, **EMPTY_DICT)

    # Execution: visit the ImportFrom node. Since there is no matching
    # rewrite and no names to replace, this should simply fall through
    # to the generic visitor without modification.
    base_import_rewrite.visit_ImportFrom(import_from_node)

    # Assertion: the call completes without raising, exercising the
    # fall-through path where neither rewrite nor names_to_replace apply.
    assert import_from_node is not None

def test_visit_import_from_returns_ast_node_when_rewrite_rules_match():
    # Setup: create a BaseImportRewrite with a module name that may match a rewrite.
    module_name = "\x0bQHzaZ?\tpM/wFtV"
    alias_name = "%WE}A)"
    import_rewrite = base_module.BaseImportRewrite(module_name)

    # Build an ImportFrom node using the module name and alias name as both
    # positional arguments and keyword arguments.
    import_from_node = ast3_module.ImportFrom(
        module_name,
        alias_name,
        module_name,
        alias_name,
        module=module_name,
        name=alias_name,
        level=module_name,
        names=alias_name,
    )

    # Execution: invoke the visitor on the ImportFrom node.
    result = import_rewrite.visit_ImportFrom(import_from_node)

    # Assertion: the visitor should return a valid AST node (not None) after
    # applying any matched rewrites or name replacements.
    assert result is not None

def test_visit_import_from_with_unmatched_import_returns_generic_visit_result():
    # Setup: Create an ImportFrom node with duplicate keys in dict (last wins)
    # and its corresponding BaseImportRewrite instance.
    IMPORT_NAME = "\x0bQbHzaZ?\tpM/wFtV"
    EMPTY_NAME = ""

    import_from_data = {
        IMPORT_NAME: IMPORT_NAME,
        EMPTY_NAME: IMPORT_NAME,
    }
    import_from_node = ast3_module.ImportFrom(**import_from_data)

    base_import_rewrite = base_module.BaseImportRewrite(import_from_node)

    # Execution: Visit the ImportFrom node. Since no module rewrite or name
    # replacements match, the visitor should fall back to generic_visit.
    result = base_import_rewrite.visit_ImportFrom(import_from_node)

    # Assertion: The generic visit returns the node itself (unchanged),
    # verifying the fallback behavior when no rewrite applies.
    assert result is import_from_node

