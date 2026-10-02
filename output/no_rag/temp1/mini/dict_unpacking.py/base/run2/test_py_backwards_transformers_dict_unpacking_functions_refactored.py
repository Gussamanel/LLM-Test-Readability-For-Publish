import pytest

import typed_ast._ast3 as typed_ast__ast3
import dict_unpacking as dict_unpacking_module
import typed_ast.ast3 as typed_ast_ast3

def test_dict_unpacking_transformer_initialization():
    # Purpose:
    # Verify that the DictUnpackingTransformer can be instantiated with a module AST
    # and that the created transformer retains a reference to the provided module.
    
    # Constants / references to constructors used in this test
    MODULE_FACTORY = module_0.mod
    TRANSFORMER_CLASS = module_1.DictUnpackingTransformer

    # Setup: create a module AST using the module factory
    module_ast = MODULE_FACTORY()

    # Execution: instantiate the transformer with the created module AST
    transformer = TRANSFORMER_CLASS(module_ast)

    # Assertions:
    # - The transformer object is an instance of the expected class
    assert isinstance(transformer, TRANSFORMER_CLASS)

    # - The transformer retains a reference to the provided module AST in one of its attributes
    #   (we check the instance dict values for identity to avoid assuming a specific attribute name)
    assert any(value is module_ast for value in vars(transformer).values()), (
        "Transformer should retain the provided module AST in its attributes"
    )

def test_visit_module_preserves_module_structure_and_may_insert_nodes_at_start():
    # Purpose:
    # Verify that DictUnpackingTransformer.visit_Module returns a Module AST node,
    # preserves the module structure (has a .body list) and does not lose existing
    # body elements. The transformer is expected to insert nodes at the start of
    # the body (if any are produced), and then continue visiting children.
    #
    # Note: We cannot assert exact inserted content because that depends on the
    # internal merge_dicts.get_body() implementation. Instead we assert structural
    # properties and that the body did not shrink.

    # Constants / test data
    SOURCE_CODE = "39@U3\r"

    # Setup
    transformer = dict_unpacking_module.DictUnpackingTransformer(SOURCE_CODE)
    original_module = typed_ast_ast3.parse(SOURCE_CODE)

    # Execution
    transformed_module = transformer.visit_Module(original_module)

    # Assertions
    # The result should be an AST Module node from typed_ast._ast3
    assert isinstance(transformed_module, typed_ast__ast3.Module)
    # The module should expose a 'body' attribute that is a list
    assert hasattr(transformed_module, "body")
    assert isinstance(transformed_module.body, list)
    # The transformer's insertion (if any) should not remove existing statements:
    assert len(transformed_module.body) >= len(getattr(original_module, "body", []))

