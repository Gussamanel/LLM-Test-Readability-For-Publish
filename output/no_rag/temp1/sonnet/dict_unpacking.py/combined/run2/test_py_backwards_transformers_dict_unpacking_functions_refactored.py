import pytest
import typed_ast._ast3 as typed_ast_internal
import dict_unpacking as dict_unpacking
import typed_ast.ast3 as ast3

def test_dict_unpacking_transformer_initialization():
    # Test that DictUnpackingTransformer can be successfully initialized with a module object
    
    # Setup: Create a module instance to be used as the target for transformation
    target_module = typed_ast_internal.mod()
    
    # Execute: Initialize the DictUnpackingTransformer with the created module
    transformer = dict_unpacking.DictUnpackingTransformer(target_module)

def test_visit_module_with_simple_string_transforms_module():
    # Test that DictUnpackingTransformer correctly visits and transforms a Module node
    # by inserting merge_dicts body at position 0 and applying generic_visit

    # Constants
    SOURCE_CODE = "39@U3\r"

    # Setup: Create the transformer with source code and parse the source into an AST module
    transformer = dict_unpacking.DictUnpackingTransformer(SOURCE_CODE)
    parsed_module = ast3.parse(SOURCE_CODE)

    # Execute: Visit and transform the parsed module node
    transformed_module = transformer.visit_Module(parsed_module)

    # Assert: Verify the result is an AST Module node after transformation
    assert isinstance(transformed_module, typed_ast_internal.Module)

