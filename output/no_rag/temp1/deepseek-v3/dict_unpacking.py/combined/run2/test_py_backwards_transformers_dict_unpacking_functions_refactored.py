import pytest
import typed_ast._ast3 as ast3_legacy
import dict_unpacking as dict_unpacking
import typed_ast.ast3 as ast3

def test_dict_unpacking_transformer_creation_from_module_factory():
    """
    Test creating a DictUnpackingTransformer using the module returned by the mod() factory.

    This test verifies that:
    1. The 'mod' function from the target module can be called successfully.
    2. A DictUnpackingTransformer instance can be initialized with the resulting module object.
    """
    module_object = dict_unpacking.mod()
    transformer = dict_unpacking.DictUnpackingTransformer(module_object)
    assert transformer is not None

def test_visit_module_inserts_dict_merging_code_at_beginning_into_empty_body():
    # Setup: A DictUnpackingTransformer should be initialized with source code
    # and a parsed AST module representing that same source code.
    SOURCE_CODE = "39@U3\r"
    EXPECTED_INSERTED_BODY = dict_unpacking.merge_dicts.get_body()

    transformer = dict_unpacking.DictUnpackingTransformer(SOURCE_CODE)
    parsed_module = ast3.parse(SOURCE_CODE)

    # Before visiting, the module body should not yet contain the dict merging code.
    assert parsed_module.body[:len(EXPECTED_INSERTED_BODY)] != EXPECTED_INSERTED_BODY

    # Execution: Visit the module, which should insert the dict merging code
    # at position 0 of the module's body and then generic-visit the node.
    result_module = transformer.visit_Module(parsed_module)

    # Assertion: The returned module should be the same node passed in,
    # and its body should now begin with the dict merging code produced by
    # merge_dicts.get_body().
    assert result_module is parsed_module
    assert result_module.body[:len(EXPECTED_INSERTED_BODY)] == EXPECTED_INSERTED_BODY

