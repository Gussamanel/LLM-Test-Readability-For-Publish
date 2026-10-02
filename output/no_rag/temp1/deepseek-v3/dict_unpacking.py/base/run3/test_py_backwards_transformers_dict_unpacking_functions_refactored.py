import pytest
import typed_ast._ast3 as ast3_internal
import dict_unpacking as dict_unpacking_module
import typed_ast.ast3 as ast3

def test_dict_unpacking_transformer_creation_with_module():
    module_node = ast3.Module(body=[], type_ignores=[])
    transformer = dict_unpacking_module.DictUnpackingTransformer(module_node)
    assert transformer is not None
    assert transformer.module == module_node

def test_dict_unpacking_transform_inserts_merged_dict_body_at_module_start():
    # Setup: build AST for a module containing a single string expression
    source_code = "39@U3\r"
    dict_unpacking_transformer = dict_unpacking_module.DictUnpackingTransformer(source_code)
    module_node = ast3.parse(source_code)

    # Execution: apply the transformer to the parsed module
    transformed_module = dict_unpacking_transformer.visit_Module(module_node)

    # Assertion: the transformer returns a module node and injects merged dict body at the start
    assert isinstance(transformed_module, ast3_internal.Module)
    assert transformed_module.body[0] == dict_unpacking_module.merge_dicts.get_body()[0]

