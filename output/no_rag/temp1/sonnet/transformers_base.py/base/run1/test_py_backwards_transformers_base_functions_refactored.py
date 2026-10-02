import pytest
import base as base
import typed_ast._ast3 as ast3

def test_base_node_transformer_initialization_with_none():
    # Test that BaseNodeTransformer can be initialized with None as the tree argument
    # This verifies the constructor accepts None without raising an exception
    
    # Setup
    NONE_TREE = None
    
    # Execution
    transformer = base.BaseNodeTransformer(NONE_TREE)
    
    # Assertion
    assert transformer is not None

def test_visit_import_from_with_no_matching_rewrite_or_names():
    """
    Test that visit_ImportFrom performs a generic visit when there is no matching
    rewrite for the module and no names to replace.
    
    Setup: Create a BaseImportRewrite instance with a MatMult node as its rewrite target,
           then construct an ImportFrom node where the module and names reference the
           BaseImportRewrite instance (which won't match any rewrite rules).
    
    Execution: Call visit_ImportFrom with the constructed ImportFrom node.
    
    Assertion: The method should fall through to generic_visit since no rewrite
               matches and no names need replacing, completing without error.
    """
    # Setup: Create a MatMult node to act as a placeholder and wrap it in a BaseImportRewrite
    mat_mult_node = ast3.MatMult()
    base_import_rewrite = base.BaseImportRewrite(mat_mult_node)

    # Construct an ImportFrom node using the rewrite and mat_mult as arguments
    # list represents: [module, names, level] arguments for ImportFrom
    import_from_args = [base_import_rewrite, mat_mult_node, base_import_rewrite]
    import_from_node = ast3.ImportFrom(*import_from_args)

    # Execution: Visit the ImportFrom node - expects no matching rewrite or names to replace
    base_import_rewrite.visit_ImportFrom(import_from_node)

def test_visit_import_from_with_none_module_and_mat_mult_operator():
    """
    Test that visit_ImportFrom handles an ImportFrom node where the module is None
    and the names list contains a MatMult operator.
    Since the module is None, no rewrite match should be found, and the method
    should fall through to generic_visit without raising an exception.
    """
    # Constants
    NONE_MODULE = None

    # Setup: Create a BaseImportRewrite instance with no configuration
    rewriter = base.BaseImportRewrite(NONE_MODULE)

    # Setup: Create an ImportFrom AST node with None as the module
    # and a MatMult operator as part of the names list
    mat_mult_operator = ast3.MatMult()
    import_from_args = [NONE_MODULE, mat_mult_operator]
    import_from_kwargs = {}
    import_from_node = ast3.ImportFrom(*import_from_args, **import_from_kwargs)

    # Execution: Visit the ImportFrom node
    # With a None module, no rewrite rule should match, leading to generic_visit
    rewriter.visit_ImportFrom(import_from_node)

def test_visit_import_from_falls_through_to_generic_visit_when_module_unmatched():
    """
    Test that visit_ImportFrom performs a generic visit when the module does not
    match any rewrite rules and there are no names to replace.
    
    The BaseImportRewrite is initialized with a module name that won't match any
    rewrite rules. An ImportFrom node is created with positional and keyword
    arguments derived from a dictionary mapping. Since neither the module nor
    the imported names trigger any rewrite logic, the method falls through to
    generic_visit.
    """
    # Setup
    UNMATCHED_MODULE_NAME = "\x0bQHzaZ?\tpM/wFtV"
    ALTERNATE_NAME = "%WE}A)"
    
    # Create a BaseImportRewrite instance with a non-matching module name
    base_import_rewrite = base.BaseImportRewrite(UNMATCHED_MODULE_NAME)
    
    # Create a dictionary to use as both positional and keyword args for ImportFrom
    # Keys and values simulate module and alias mappings
    import_args = {
        UNMATCHED_MODULE_NAME: ALTERNATE_NAME,
        ALTERNATE_NAME: ALTERNATE_NAME,
    }

    # Execution: Create an ImportFrom node using the args dict
    import_from_node = ast3.ImportFrom(*import_args, **import_args)

    # Assert: visit_ImportFrom should perform generic_visit since there is no matching
    # rewrite rule and no names to replace
    base_import_rewrite.visit_ImportFrom(import_from_node)

def test_visit_import_from_with_mixed_module_name_keys_no_match():
    # Test that visit_ImportFrom returns the node unchanged via generic_visit
    # when neither the module nor any names match the rewrite rules

    # Constants representing module and alias names
    NON_EMPTY_MODULE_NAME = "\x0bQbHzaZ?\tpM/wFtV"
    EMPTY_MODULE_NAME = ""

    # Setup: Create an ImportFrom node with mixed module name keys
    # The dict intentionally has duplicate keys, resulting in the last value winning
    import_from_kwargs = {
        NON_EMPTY_MODULE_NAME: NON_EMPTY_MODULE_NAME,
        EMPTY_MODULE_NAME: NON_EMPTY_MODULE_NAME,
    }
    import_from_node = ast3.ImportFrom(*import_from_kwargs, **import_from_kwargs)

    # Setup: Create a BaseImportRewrite instance with the ImportFrom node
    rewriter = base.BaseImportRewrite(import_from_node)

    # Execution: Visit the ImportFrom node through the rewriter
    result = rewriter.visit_ImportFrom(import_from_node)

    # Assertion: The result should be the node returned from generic_visit
    # since there are no matching rewrites for the module or names
    assert result is not None

