import pytest
import typed_ast._ast3 as ast3
import dict_unpacking as dict_unpacking
import typed_ast.ast3 as typed_ast3

def test_dict_unpacking_transformer_initialization_with_module_node():
    # Setup
    module_node = ast3.Module()
    
    # Execution
    transformer = dict_unpacking.DictUnpackingTransformer(module_node)
    
    # Assertion
    assert isinstance(transformer, dict_unpacking.DictUnpackingTransformer)

def test_dict_unpacking_transformer_inserts_merge_dicts_body_at_module_start():
    # Setup: source code that the transformer will parse and visit
    source_code = "39@U3\r"
    dict_unpacking_transformer = dict_unpacking.DictUnpackingTransformer(source_code)
    parsed_module = typed_ast3.parse(source_code)

    # Execution: visit the module with the transformer
    transformed_module = dict_unpacking_transformer.visit_Module(parsed_module)

    # Assertion: the merged dict body should be inserted at position 0 of the module
    assert merge_dicts.get_body() in transformed_module.body
    assert transformed_module.body[0] is merge_dicts.get_body()[0]
    assert isinstance(transformed_module, ast3.Module)

