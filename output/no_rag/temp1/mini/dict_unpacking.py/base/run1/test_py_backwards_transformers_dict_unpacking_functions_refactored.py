import pytest

import typed_ast._ast3 as typed_ast_private_ast3
import dict_unpacking as dict_unpacking_module
import typed_ast.ast3 as typed_ast_ast3

def test_dict_unpacking_transformer_initializes_with_module_node():
    # Purpose:
    # Ensure the DictUnpackingTransformer can be constructed given a module AST node
    # and that the resulting object is the expected transformer type.

    # Constants / fixtures
    SAMPLE_MODULE_FACTORY = module_0.mod  # factory function that produces a module AST node

    # Setup: create a module AST node to pass into the transformer
    sample_module_node = SAMPLE_MODULE_FACTORY()

    # Execution: construct the transformer with the module node
    transformer = module_1.DictUnpackingTransformer(sample_module_node)

    # Assertions:
    # - The transformer is an instance of the expected class
    assert isinstance(transformer, module_1.DictUnpackingTransformer)

    # - If the transformer stores the original module node on an attribute (common pattern),
    #   verify it refers to the same object we passed in.
    if hasattr(transformer, "module"):
        assert transformer.module is sample_module_node
    elif hasattr(transformer, "tree"):
        # some transformer implementations use 'tree' to hold the AST root
        assert transformer.tree is sample_module_node

def test_visit_module_inserts_merge_nodes_and_returns_module_instance():
    # Purpose:
    # Verify DictUnpackingTransformer.visit_Module runs without error, returns an AST Module,
    # and performs in-place modifications (the Module instance is returned and has a body list
    # that insert_at would operate on).
    #
    # NOTE: The test uses an opaque small source string to exercise transformer initialization
    # and the visit_Module logic (which calls insert_at and then generic_visit).

    # Constants / Setup
    SAMPLE_SOURCE = "39@U3\r"
    transformer = dict_unpacking_module.DictUnpackingTransformer(SAMPLE_SOURCE)
    parsed_module = typed_ast_ast3.parse(SAMPLE_SOURCE)

    # Execution
    result_module = transformer.visit_Module(parsed_module)

    # Assertions
    # - visit_Module should return an AST Module
    assert isinstance(result_module, typed_ast_ast3.Module)
    # - It should return the same module instance (in-place modification)
    assert result_module is parsed_module
    # - The module must have a body attribute that is a list (insert_at operates on this)
    assert hasattr(result_module, "body")
    assert isinstance(result_module.body, list)

