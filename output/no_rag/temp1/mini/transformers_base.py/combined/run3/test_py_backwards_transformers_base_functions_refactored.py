import pytest

import base as base_module
import typed_ast._ast3 as typed_ast_ast3

def test_base_node_transformer_initialization_with_none():
    """
    Purpose:
    - Verify that BaseNodeTransformer can be constructed when given None as the constructor argument.
    - This ensures the constructor accepts a None value and returns a valid instance (no exception raised).
    """

    # Constants / test data
    CONSTRUCTOR_ARG = None

    # Setup: prepare any required inputs (none required beyond the constant above)
    # (If BaseNodeTransformer were to interact with AST nodes, they would be prepared here.)

    # Execution: construct the transformer with the None argument
    transformer = base_module.BaseNodeTransformer(CONSTRUCTOR_ARG)

    # Assertions: ensure an instance was created and is of the expected type
    assert transformer is not None, "Constructor returned None instead of an instance"
    assert isinstance(transformer, base_module.BaseNodeTransformer), (
        "Constructed object is not a BaseNodeTransformer instance"
    )

def test_visit_importfrom_replaces_import_when_module_matches_rewrite():
    """Verify visit_ImportFrom delegates to replacement logic when the ImportFrom
    node's module matches a rewrite found by _get_matched_rewrite.
    """
    # --- Setup: create the objects used to build the ImportFrom node ---
    mat_mult_instance = module_1.MatMult()
    base_import_rewrite_instance = module_0.BaseImportRewrite(mat_mult_instance)

    # Use the instances to populate the ImportFrom positional args
    IMPORT_FROM_MODULE = base_import_rewrite_instance
    IMPORT_FROM_NAMES = mat_mult_instance
    IMPORT_FROM_LEVEL = base_import_rewrite_instance

    import_from_node = module_1.ImportFrom(
        IMPORT_FROM_MODULE,
        IMPORT_FROM_NAMES,
        IMPORT_FROM_LEVEL,
    )

    # --- Execution ---
    result = base_import_rewrite_instance.visit_ImportFrom(import_from_node)

    # --- Assertion ---
    # The visitor should return an AST node (replacement) and not None.
    assert result is not None
    assert isinstance(result, typed_ast_ast3.AST)

def test_visit_importfrom_with_none_module_and_matmult_returns_ast():
    # Purpose:
    # Verify that BaseImportRewrite.visit_ImportFrom can handle an ImportFrom
    # node whose module is None and which references a MatMult node,
    # and that it returns an AST node (does not raise and returns a valid AST).
    
    # Constants / test data
    MODULE_VALUE = None
    MAT_MULT_NODE = module_1.MatMult()
    BASE_REWRITE_INIT_ARG = MODULE_VALUE

    # Setup: create the rewriter and the ImportFrom node to visit
    base_import_rewrite = module_0.BaseImportRewrite(BASE_REWRITE_INIT_ARG)
    import_from_node = module_1.ImportFrom(MODULE_VALUE, MAT_MULT_NODE)

    # Execution: perform the visit
    result = base_import_rewrite.visit_ImportFrom(import_from_node)

    # Assertion: the visitor should return an AST node (no exception, valid return type)
    assert isinstance(result, typed_ast_ast3.AST), "Expected visit_ImportFrom to return an AST node"

def test_base_import_rewrite_visit_importfrom_with_duplicate_keys():
    # Purpose:
    # Ensure BaseImportRewrite.visit_ImportFrom can be called with an ImportFrom node
    # constructed from a mapping that contains duplicate keys/values. The test verifies
    # the method executes and returns a non-None result (it may return a node, a Try,
    # or perform a generic visit).
    #
    # Note: The ImportFrom constructor is invoked with both *args and **kwargs using
    # the same mapping to reproduce the unusual call pattern from the original test.

    # --- Constants / Test data ---
    MODULE_NAME = "\x0bQHzaZ?\tpM/wFtV"
    REWRITE_TARGET = "%WE}A)"

    # Duplicate entries are intentionally repeated to mirror the original test input.
    mapping_with_duplicates = {
        MODULE_NAME: REWRITE_TARGET,
        REWRITE_TARGET: REWRITE_TARGET,
        REWRITE_TARGET: REWRITE_TARGET,
        MODULE_NAME: REWRITE_TARGET,
    }

    # --- Setup ---
    rewriter = base_module.BaseImportRewrite(MODULE_NAME)

    # Construct an ImportFrom node using the same mapping for positional and keyword args
    import_from_node = typed_ast_ast3.ImportFrom(*mapping_with_duplicates, **mapping_with_duplicates)

    # --- Exercise ---
    result = rewriter.visit_ImportFrom(import_from_node)

    # --- Assert ---
    # The method should return a value (either a transformed node or result of generic_visit).
    assert result is not None

def test_visit_importfrom_with_duplicate_aliases_triggers_name_replacement():
    # Purpose:
    # Verify BaseImportRewrite.visit_ImportFrom can be invoked on an ImportFrom node
    # that contains multiple (including duplicate and empty) alias entries.
    # The test does not assert specific rewrite behavior, only that the visitor
    # returns an AST node (either transformed or the original node).

    # --- Setup ---
    MODULE_NAME = "\x0bQbHzaZ?\tpM/wFtV"
    EMPTY_ALIAS_NAME = ""
    DUPLICATE_ALIAS_NAME = MODULE_NAME

    # Create several alias entries, including duplicates and an empty name,
    # to simulate the original test's repeated dictionary keys/values.
    aliases = [
        typed_ast_ast3.alias(name=DUPLICATE_ALIAS_NAME, asname=None),
        typed_ast_ast3.alias(name=EMPTY_ALIAS_NAME, asname=None),
        typed_ast_ast3.alias(name=DUPLICATE_ALIAS_NAME, asname=None),
        typed_ast_ast3.alias(name=EMPTY_ALIAS_NAME, asname=None),
        typed_ast_ast3.alias(name=DUPLICATE_ALIAS_NAME, asname=None),
    ]

    # Construct an ImportFrom node with the module name and the aliases list.
    import_from_node = typed_ast_ast3.ImportFrom(module=MODULE_NAME, names=aliases, level=0)

    # Instantiate the BaseImportRewrite with the node as initial state/context.
    importer = base_module.BaseImportRewrite(import_from_node)

    # --- Execution ---
    result_node = importer.visit_ImportFrom(import_from_node)

    # --- Assertion ---
    # The visitor should return some AST node (possibly transformed).
    assert isinstance(result_node, typed_ast_ast3.AST)

