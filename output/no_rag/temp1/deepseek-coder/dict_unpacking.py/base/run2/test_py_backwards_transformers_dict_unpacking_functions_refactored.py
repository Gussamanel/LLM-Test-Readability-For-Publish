import typed_ast._ast3 as module_ast
import dict_unpacking as module_dict_unpacking
import typed_ast.ast3 as module_typed_ast

def test_dict_unpacking_transformer_with_module_ast():
    MODULE_0 = module_ast.mod()
    DICT_UNPACKING_TRANSFORMER = module_dict_unpacking.DictUnpackingTransformer(MODULE_0)
    transformed_mod = DICT_UNPACKING_TRANSFORMER.transform()
    assert transformed_mod == module_typed_ast.mod(), "Transformed mod should match module_typed_ast"

def test_dict_unpacking_transformer_with_module_ast():
    # Given
    INPUT_CODE = "39@U3\\r"
    
    dict_unpacking_transformer = module_dict_unpacking.DictUnpackingTransformer(INPUT_CODE)
    module_node = module_typed_ast.parse(INPUT_CODE)
    
    # When
    transformed_module = dict_unpacking_transformer.visit_Module(module_node)
    
    # Then
    assert transformed_module is not None, "The transformed module should not be None"
    assert str(transformed_module) != INPUT_CODE, "The transformed module and the input code should not be the same."
    assert module_dict_unpacking.DictUnpackingTransformer in str(transformed_module), "The transformed module should contain DictUnpackingTransformer."
    assert module_typed_ast.Module in str(transformed_module), "The transformed module should be an instance of ast.Module."

