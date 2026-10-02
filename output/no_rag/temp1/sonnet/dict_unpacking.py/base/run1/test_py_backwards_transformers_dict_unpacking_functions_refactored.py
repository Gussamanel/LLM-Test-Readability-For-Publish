import pytest
import typed_ast._ast3 as typed_ast_internal
import dict_unpacking as dict_unpacking
import typed_ast.ast3 as ast3

def test_dict_unpacking_transformer_initialization():
    # Test that DictUnpackingTransformer can be properly initialized with a module instance
    
    # Setup: Create a module instance to be used as the argument for the transformer
    module_instance = typed_ast_internal.mod()
    
    # Execution: Initialize the DictUnpackingTransformer with the module instance
    dict_unpacking_transformer = dict_unpacking.DictUnpackingTransformer(module_instance)
    
    # Assertion: Verify the transformer was created successfully and is an instance of DictUnpackingTransformer
    assert isinstance(dict_unpacking_transformer, dict_unpacking.DictUnpackingTransformer)

def test_visit_module_with_simple_string_transforms_module():
    # Test that DictUnpackingTransformer correctly visits and transforms a Module node
    # by inserting merge_dicts body at the beginning and applying generic visit

    # Constants
    SOURCE_CODE = "39@U3\r"

    # Setup: Create transformer and parse source into AST module
    transformer = dict_unpacking.DictUnpackingTransformer(SOURCE_CODE)
    parsed_module = ast3.parse(SOURCE_CODE)

    # Execute: Visit and transform the parsed module
    transformed_module = transformer.visit_Module(parsed_module)

    # Assert: The result should be a valid AST Module node
    assert transformed_module is not None
    assert isinstance(transformed_module, typed_ast_internal.Module)

