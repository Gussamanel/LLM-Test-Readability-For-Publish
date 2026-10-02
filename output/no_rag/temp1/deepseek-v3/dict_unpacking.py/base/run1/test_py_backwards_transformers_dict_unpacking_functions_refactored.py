import pytest
import typed_ast._ast3 as ast3_typed
import dict_unpacking as dict_unpacking
import typed_ast.ast3 as ast3

def test_dict_unpacking_transformer_stores_provided_empty_ast_module():
    # Setup: create an empty AST module and the transformer over it
    empty_module = ast3.Module(body=[], type_ignores=[])
    dict_unpacking_transformer = dict_unpacking.DictUnpackingTransformer(empty_module)

    # Execution: verify initialization retains the given module
    # Assertion: the transformer is constructed with the provided module
    assert dict_unpacking_transformer.module is empty_module

def test_dict_unpacking_transformer_visit_module_inserts_merged_dicts_and_returns_same_node():
    source_code = "39@U3\r"
    expected_insert_index = 0

    dict_unpacking_transformer = dict_unpacking.DictUnpackingTransformer(source_code)
    parsed_module = ast3.parse(source_code)

    original_module_body_length = len(parsed_module.body)

    transformed_module = dict_unpacking_transformer.visit_Module(parsed_module)

    assert transformed_module is parsed_module

    inserted_statements = parsed_module.body[:1]
    assert len(inserted_statements) == 1
    assert len(parsed_module.body) == original_module_body_length + 1
    assert inserted_statements[0] is not None

