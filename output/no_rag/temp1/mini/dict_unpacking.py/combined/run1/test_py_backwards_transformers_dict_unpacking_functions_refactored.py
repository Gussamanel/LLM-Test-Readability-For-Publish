import pytest
import typed_ast._ast3 as typed_ast__ast3
import dict_unpacking as dict_unpacking_module
import typed_ast.ast3 as typed_ast_ast3

def test_dict_unpacking_transformer_initializes_with_ast_module():
    """Constructing DictUnpackingTransformer with an AST module should succeed and retain that module."""
    # Arrange: create an AST module instance from the provided factory
    AST_MODULE_FACTORY = module_0.mod
    ast_module = AST_MODULE_FACTORY()

    # Act: initialize the transformer with the AST module
    transformer = dict_unpacking_module.DictUnpackingTransformer(ast_module)

    # Assert: instance is created and is of the expected type
    assert transformer is not None
    assert isinstance(transformer, dict_unpacking_module.DictUnpackingTransformer)

    # If the transformer exposes an attribute named 'module', it should be the same object we passed in
    sentinel = object()
    stored_module = getattr(transformer, "module", sentinel)
    assert stored_module is ast_module, "Transformer did not retain the module passed to its constructor"

def test_visit_module_preserves_body_and_returns_typed_ast_module():
    """Verify that visit_Module returns a typed_ast Module and preserves or extends the module body."""
    SOURCE_CODE = "39@U3\r"

    transformer = dict_unpacking_module.DictUnpackingTransformer(SOURCE_CODE)
    original_module = typed_ast_ast3.parse(SOURCE_CODE)
    original_body_length = len(original_module.body)

    transformed_module = transformer.visit_Module(original_module)

    assert isinstance(transformed_module, typed_ast_ast3.Module)
    assert hasattr(transformed_module, "body") and isinstance(transformed_module.body, list)
    assert len(transformed_module.body) >= original_body_length

