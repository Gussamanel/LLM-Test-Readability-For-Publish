import pytest
import typed_ast._ast3 as ast3
import dict_unpacking as dict_unpacking
import typed_ast.ast3 as py_ast3

def test_dict_unpacking_transformer_creation_with_ast_module():
    # Setup: Create an AST module that will be transformed
    source_module = ast3.Module()
    
    # Execution: Initialize the DictUnpackingTransformer with the source module
    transformer = dict_unpacking.DictUnpackingTransformer(source_module)
    
    # Assertion: Verify the transformer was created successfully
    assert transformer is not None
    assert isinstance(transformer, dict_unpacking.DictUnpackingTransformer)

def test_dict_unpacking_transformer_visit_module_returns_transformed_module():
    # Setup: create an instance of the transformer with an arbitrary source string
    source_code = "39@U3\r"
    transformer = dict_unpacking.DictUnpackingTransformer(source_code)

    # Setup: parse the source string into an AST3 module
    parsed_module = py_ast3.parse(source_code)

    # Execution: visit the module with the transformer
    transformed_module = transformer.visit_Module(parsed_module)

    # Assertion: verify the transformer returned the expected module object
    assert transformed_module is not None

