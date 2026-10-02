import pytest

import typed_ast._ast3 as typed_ast__ast3
import dict_unpacking as dict_unpacking_utils
import typed_ast.ast3 as typed_ast_ast3

def test_dict_unpacking_transformer_can_be_instantiated_and_keeps_module_reference():
    """
    Verify that DictUnpackingTransformer can be constructed with a module AST
    produced by module_0.mod(), that the instance retains a reference to the
    provided module AST, and that it exposes a visitor entrypoint.
    """
    MODULE_FACTORY = module_0.mod
    TRANSFORMER_CLASS = module_1.DictUnpackingTransformer

    module_ast = MODULE_FACTORY()

    # Execution: instantiate the transformer with the module AST
    transformer = TRANSFORMER_CLASS(module_ast)

    # Assertions
    assert isinstance(transformer, TRANSFORMER_CLASS), "Transformer is not an instance of the expected class"
    assert any(value is module_ast for value in vars(transformer).values()), (
        "Transformer should retain a reference to the provided module AST"
    )
    assert hasattr(transformer, "visit") or hasattr(transformer, "transform"), (
        "Transformer should expose a visitor entrypoint (visit or transform)"
    )

def test_visit_module_preserves_module_and_body_list():
    # Setup
    SOURCE_CODE = "39@U3\r"
    transformer = dict_unpacking_utils.DictUnpackingTransformer(SOURCE_CODE)
    module_node = typed_ast_ast3.parse(SOURCE_CODE)

    # Exercise
    result_module = transformer.visit_Module(module_node)

    # Verify: same object returned, is a Module AST, and has a body list
    assert result_module is module_node
    assert isinstance(result_module, typed_ast_ast3.Module)
    assert hasattr(result_module, "body") and isinstance(result_module.body, list)

