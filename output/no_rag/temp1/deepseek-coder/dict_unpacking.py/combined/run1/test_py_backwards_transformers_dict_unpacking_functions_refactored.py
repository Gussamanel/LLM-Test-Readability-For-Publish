import typed_ast._ast3 as ast
import dict_unpacking as dict
import typed_ast.ast3 as ast3

def test_unpacking_dict_and_updating_values():
    """
    Test that the transformation of dictionary unpacking works correctly and modifies values as expected.
    """
    # Setup
    module_under_test = module_0.mod()
    dict_unpack_transformer = module_1.DictUnpackingTransformer(module_under_test)

    # Test Inputs
    test_dict = {'a': 1, 'b': 2}

    # Execution
    new_dict = dict_unpack_transformer.transform(test_dict)

    # Assertions
    assert new_dict == {'a': 'modified', 'b': 'modified'}

    # Additional Assertions to check if value modification was successful
    assert 'a' in new_dict and new_dict['a'] == 'modified'
    assert 'b' in new_dict and new_dict['b'] == 'modified'

def test_case_dict_unpacking_transformer():
    INPUT_STRING = "39@U3\r"

    dict_unpacking_transformer = module_1.DictUnpackingTransformer(INPUT_STRING)

    parsed_module = module_2.parse(INPUT_STRING)
    transformed_module = dict_unpacking_transformer.visit_Module(parsed_module)

    assert transformed_module.body[0] == merge_dicts.get_body()

