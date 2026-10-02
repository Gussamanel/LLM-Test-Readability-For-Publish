import pytest
import yield_from as yield_from_module
import typed_ast.ast3 as ast3

def test_visit_none_node_returns_none_safely():
    # Setup: create a transformer with a None argument
    none_arg = None
    transformer = yield_from_module.YieldFromTransformer(none_arg)

    # Execution: visit a None node (not a valid AST node)
    # The visit method internally calls _handle_assignments, _handle_expressions,
    # and generic_visit on the provided node.
    result = transformer.visit(none_arg)

    # Assertion: visiting None should complete without raising and return None
    assert result is None

def test_yield_from_transformer_initialization_with_none_argument():
    """
    Test that YieldFromTransformer can be initialized with None as an argument.
    
    This test verifies that the YieldFromTransformer class accepts None as 
    a parameter during instantiation without raising any exceptions.
    """
    # Setup: Define the input argument as None
    input_argument = None
    
    # Execution: Instantiate the transformer with None
    transformer_instance = yield_from_module.YieldFromTransformer(input_argument)
    
    # Assertion: Verify that the transformer was created successfully
    assert transformer_instance is not None

def test_yield_from_transformer_processes_while_loop_with_none_children():
    # Setup: Create a While AST node whose two required child attributes
    # are populated with the same list of None values, then wrap it in
    # the transformer under test.
    children = [None, None]
    test_body_and_orelse = [children, children]

    none_placeholder = None
    while_node = ast3.While(*test_body_and_orelse)

    yield_from_transformer = yield_from_module.YieldFromTransformer(none_placeholder)

    # Execution: Visit the While node to ensure the transformer's
    # generic_visit path handles a node with None-valued children.
    result = yield_from_transformer.visit(while_node)

    # Assertion: The transformer should return an AST node rather than
    # raising an error.
    assert isinstance(result, ast3.AST)

def test_yield_from_transformer_handles_while_with_non_string_keywords_gracefully():
    # Setup
    # Non-string keyword arguments in a While node are invalid at runtime,
    # but the transformer should still accept and process the node gracefully.
    dummy_context = None
    transformer = yield_from_module.YieldFromTransformer(dummy_context)

    # While(*args, **kwargs) expects string keys; using a non-string key
    # exercises the generic_visit path without crashing.
    invalid_keyword_name = "P+>W*v\nDN{M8\x0bLk"
    while_args = [dummy_context, dummy_context]
    while_kwargs = {
        invalid_keyword_name: transformer,
        invalid_keyword_name: transformer,
        invalid_keyword_name: transformer,
    }
    while_node = ast3.While(*while_args, **while_kwargs)

    # Execution
    result = transformer.visit(while_node)

    # Assertion
    # The transformer should return an AST node (generic_visit result)
    # rather than raising an exception.
    assert isinstance(result, ast3.AST)

