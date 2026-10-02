import pytest
import yield_from as yield_from_module
import typed_ast.ast3 as ast3

def test_yield_from_transformer_visit_with_none_node_returns_none():
    """Verify that YieldFromTransformer.visit returns None unchanged when given None."""
    node = None
    transformer = yield_from_module.YieldFromTransformer(node)
    result = transformer.visit(node)
    assert result is node

def test_yield_from_transformer_initializes_with_none_parent():
    # Purpose:
    # Verify that YieldFromTransformer can be constructed when no parent/context is provided.
    # This ensures the transformer handles a None parent argument without raising.

    # Constants / Test data
    PARENT_NONE = None
    TRANSFORMER_CLASS = yield_from_module.YieldFromTransformer

    # Setup
    parent_arg = PARENT_NONE

    # Execution: create an instance of the transformer with a None parent
    transformer_instance = TRANSFORMER_CLASS(parent_arg)

    # Assertion: the instance was created successfully and is of the expected type
    assert transformer_instance is not None
    assert isinstance(transformer_instance, TRANSFORMER_CLASS)

def test_yield_from_transformer_visits_while_node():
    # Purpose:
    # Ensure YieldFromTransformer.visit can be called on a While node and returns an AST node
    # (the transformer should process assignments/expressions and then call generic_visit).

    # Constants / test data
    NONE_VALUE = None
    # Simulate lists used as node fields in the original test (kept simple / None-filled)
    SIMPLE_STMT_LIST = [NONE_VALUE, NONE_VALUE]
    # The original test passed two lists into the While constructor via unpacking
    WHILE_CONSTRUCTOR_ARGS = [SIMPLE_STMT_LIST, SIMPLE_STMT_LIST]

    # Setup: create the transformer and the While node to be visited
    transformer = yield_from_module.YieldFromTransformer(NONE_VALUE)
    while_node = ast3.While(*WHILE_CONSTRUCTOR_ARGS)

    # Execution: run the transformer's visit method on the While node
    transformed_node = transformer.visit(while_node)

    # Assertion: result is an AST While node (i.e., the node type is preserved after visit)
    assert isinstance(transformed_node, ast3.While)

def test_yield_from_transformer_visit_handles_while_with_none_components_and_extra_attribute():
    # Purpose:
    # Ensure YieldFromTransformer.visit can handle an ast3.While node whose
    # key components are None and which carries an unexpected extra attribute.
    # This verifies the visit path (handling assignments/expressions and falling
    # back to generic_visit) does not raise and preserves node structure.

    # --- Constants / setup -------------------------------------------------
    NONE = None
    EXTRA_ATTR_NAME = "unexpected_keyword"  # simulate an unexpected keyword/attribute

    # Instantiate the transformer the same way the original test did (arg was None)
    transformer = yield_from_module.YieldFromTransformer(NONE)

    # Create a While node with the same positional shape as the original test
    # (two positional arguments set to None). This mirrors `While(*[None, None])`.
    while_node = ast3.While(NONE, NONE)

    # Attach an extra attribute to simulate passing an unexpected keyword argument.
    # (Original test used a repeated, unusual string as a kwarg key; here we
    # reproduce the intent with a valid identifier to avoid syntax issues.)
    setattr(while_node, EXTRA_ATTR_NAME, transformer)

    # --- Execute ----------------------------------------------------------
    visited_node = transformer.visit(while_node)

    # --- Assert -----------------------------------------------------------
    # The visitor should return an AST node (specifically a While node) and
    # should preserve the unexpected attribute we attached.
    assert isinstance(visited_node, ast3.While)
    assert getattr(visited_node, EXTRA_ATTR_NAME) is transformer

