import pytest

import typed_ast._ast3 as typed_ast__ast3_module
import dict_unpacking as dict_unpacking_module
import typed_ast.ast3 as typed_ast_ast3_module

def test_dict_unpacking_transformer_initialization_creates_transformer_instance():
    """
    Verify that DictUnpackingTransformer can be instantiated with a typed_ast module
    and that the resulting object is an instance of the expected transformer class.
    """
    # Arrange
    MODULE_CREATOR = typed_ast__ast3_module.mod
    TRANSFORMER_CLASS = dict_unpacking_module.DictUnpackingTransformer
    sample_ast_module = MODULE_CREATOR()

    # Act
    transformer_instance = TRANSFORMER_CLASS(sample_ast_module)

    # Assert
    assert transformer_instance is not None
    assert isinstance(transformer_instance, TRANSFORMER_CLASS)

def test_dict_unpacking_transformer_visit_module_returns_module_with_body():
    # This test verifies that DictUnpackingTransformer.visit_Module accepts a parsed AST Module,
    # performs its transformation (inserting merge_dicts body items) and returns an AST Module
    # whose 'body' attribute is a list. We do not validate the exact inserted nodes here,
    # only that the transformation yields a Module with a proper body structure.
    
    # Constants / Setup
    SOURCE_CODE = "39@U3\r"
    transformer = dict_unpacking_module.DictUnpackingTransformer(SOURCE_CODE)
    parsed_module = typed_ast_ast3_module.parse(SOURCE_CODE)
    
    # Execution
    transformed_module = transformer.visit_Module(parsed_module)
    
    # Assertions: ensure we received an AST Module and it has a list-like body
    assert isinstance(transformed_module, typed_ast__ast3_module.Module)
    assert hasattr(transformed_module, "body")
    assert isinstance(transformed_module.body, list)

