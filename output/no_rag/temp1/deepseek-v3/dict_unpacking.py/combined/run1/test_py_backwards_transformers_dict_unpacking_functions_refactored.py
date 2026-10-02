import pytest
import typed_ast._ast3 as ast3_module
import dict_unpacking as dict_unpacking_module
import typed_ast.ast3 as ast3_module_2

def test_dict_unpacking_transformer_instantiates_with_ast_module():
    # Setup: create an AST module node to be transformed
    ast_module = dict_unpacking_module.mod()

    # Execution: initialize the transformer with the AST module
    transformer = ast_module_2.DictUnpackingTransformer(ast_module)

    # Assertion: verify the transformer was created successfully
    assert transformer is not None

def test_visit_module_returns_same_ast_module_node():
    # Setup: Create a transformer with a dummy source string and parse the string into an AST module
    source_code = "39@U3\r"
    dict_unpacking_transformer = dict_unpacking_module.DictUnpackingTransformer(source_code)
    ast_module = ast3_module_2.parse(source_code)

    # Execution: Visit the parsed module to trigger the transformer logic
    result_module = dict_unpacking_transformer.visit_Module(ast_module)

    # Assertion: Ensure the visit_Module returns the generic_visit result (the same node)
    assert result_module is ast_module

