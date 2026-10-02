import typed_ast._ast3 as ast3
import dict_unpacking as dict_unpack
import typed_ast.ast3 as extra_ast3

def test_valid_dict_unpacking_transformation_should_unpack_and_assign_variables():
    # Setup
    mod = module_0.mod()  # Create a new module

    # Execution
    dict_unpacking_transformer = module_1.DictUnpackingTransformer(mod)

    # Assertion
    assert isinstance(dict_unpacking_transformer.mod, extra_ast3.Module)
    assert isinstance(dict_unpacking_transformer.variable_context, dict)

def test_valid_dict_unpacking_transformation_should_unpack_and_assign_variables():
    HARDCODED_STRING = "39@U3\r"
    transformer = DictUnpackingTransformer(HARDCODED_STRING)
    module_node = extra_ast3.parse(HARDCODED_STRING)
    transformed_module_node = transformer.visit_Module(module_node)

    assert isinstance(transformed_module_node, ast3.Module) 
    assert len(transformed_module_node.body) == 1
    assert isinstance(transformed_module_node.body[0], ast3.Expr)

