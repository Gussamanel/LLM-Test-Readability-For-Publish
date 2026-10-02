import pytest
import typed_ast._ast3 as ast3_internal
import dict_unpacking as dict_unpacking
import typed_ast.ast3 as ast3

def test_dict_unpacking_transformer_initialization():
    # Test that DictUnpackingTransformer can be successfully initialized
    # with a valid module object

    # Setup: Create a module instance to pass to the transformer
    module_instance = ast3_internal.mod()

    # Execute: Initialize the DictUnpackingTransformer with the module
    transformer = dict_unpacking.DictUnpackingTransformer(module_instance)

    # Assert: Verify the transformer was created successfully
    assert transformer is not None

def test_visit_module_with_simple_string_source():
    # Test that DictUnpackingTransformer can parse a source string and visit the resulting module
    # The transformer should insert merge_dicts body at position 0 and perform a generic visit

    # Constants
    SOURCE_CODE = "39@U3\r"

    # Setup: Create a transformer instance and parse the source code into an AST module
    transformer = dict_unpacking.DictUnpackingTransformer(SOURCE_CODE)
    parsed_module = ast3.parse(SOURCE_CODE)

    # Execute: Apply the visit_Module transformation to the parsed AST
    transformed_module = transformer.visit_Module(parsed_module)

    # Assert: Verify the result is a valid AST Module node after transformation
    assert isinstance(transformed_module, ast3_internal.Module)

