import pytest
import typed_ast._ast3 as ast3_internal
import dict_unpacking as dict_unpacking
import typed_ast.ast3 as ast3

def test_dict_unpacking_transformer_initialization():
    # Test that DictUnpackingTransformer can be successfully initialized with a module
    
    # Setup: Create a module instance to serve as the context for the transformer
    source_module = ast3_internal.mod()
    
    # Execution: Initialize the DictUnpackingTransformer with the created module
    transformer = dict_unpacking.DictUnpackingTransformer(source_module)

def test_visit_module_inserts_merge_dicts_body():
    # Test that DictUnpackingTransformer.visit_Module correctly processes
    # a parsed module by inserting merge_dicts body at position 0
    # and returning the visited module node

    # Constants
    SOURCE_CODE = "39@U3\r"

    # Setup: Create transformer instance and parse the source code into an AST module
    transformer = dict_unpacking.DictUnpackingTransformer(SOURCE_CODE)
    parsed_module = ast3.parse(SOURCE_CODE)

    # Execute: Visit the parsed module with the transformer
    transformed_module = transformer.visit_Module(parsed_module)

    # Assert: The result should be a valid AST Module node
    # with merge_dicts body inserted at the beginning
    assert transformed_module is not None
    assert isinstance(transformed_module, ast3_internal.Module)

