import pytest

import yield_from as yield_from_module
import typed_ast.ast3 as ast3

def test_visit_returns_none_when_node_is_none():
    """Verify that YieldFromTransformer.visit returns None (and does not raise) when given None."""
    # Arrange
    input_node = None  # type: ast3.AST | None
    transformer_config = None
    transformer = yield_from_module.YieldFromTransformer(transformer_config)

    # Act
    result = transformer.visit(input_node)

    # Assert
    assert result is None

def test_yield_from_transformer_initialization_with_none():
    # Purpose:
    # Verify that YieldFromTransformer can be instantiated when given None as its initializer argument.
    # This ensures the constructor accepts a None value and returns a valid transformer object.

    # Constants (inputs for the test)
    TRANSFORMER_INIT_ARG = None

    # Setup: prepare the argument to pass into the constructor
    transformer_init_arg = TRANSFORMER_INIT_ARG

    # Execution: create the transformer instance
    transformer_instance = yield_from_module.YieldFromTransformer(transformer_init_arg)

    # Assertion: ensure an instance was created and is of the expected type
    assert transformer_instance is not None, "YieldFromTransformer constructor returned None"
    assert isinstance(transformer_instance, yield_from_module.YieldFromTransformer), (
        "Constructed object is not an instance of YieldFromTransformer"
    )

def test_yield_from_transformer_visit_handles_while_node_without_assignments_or_expressions():
    # Purpose:
    # Ensure YieldFromTransformer.visit can process a While node that contains
    # simple lists (here filled with None) and returns an AST node (invoking
    # its internal _handle_assignments and _handle_expressions paths
    # and then generic_visit).

    # Constants / setup inputs
    NONE = None
    body_list = [NONE, NONE]            # represents a simple body/orelse placeholder
    while_args = [body_list, body_list] # arguments to ast3.While (kept as in original test)

    # Setup: create transformer and the While node to be visited
    transformer = yield_from_module.YieldFromTransformer(NONE)
    while_node = ast3.While(*while_args)

    # Execution: visit the While node with the transformer
    transformed_node = transformer.visit(while_node)

    # Assertion: the visitor should return an AST node of the same While type
    assert isinstance(transformed_node, ast3.While)

def test_yield_from_transformer_visit_accepts_while_node_with_positional_none_and_extra_attrs():
    # Purpose:
    # Ensure YieldFromTransformer.visit can be called on an ast3.While node that
    # contains positional None values and arbitrary extra keyword attributes.
    # visit() should return an AST node (it runs _handle_assignments,
    # _handle_expressions and then generic_visit).

    # Create the transformer (match original test's initialization).
    transformer = yield_from_module.YieldFromTransformer(None)

    # The original test passed two positional None arguments to ast3.While.
    positional_args = [None, None]

    # An arbitrary extra keyword attribute name and value (value is the transformer).
    EXTRA_ATTR_NAME = "P+>W*v\nDN{M8\x0bLk"
    extra_kwargs = {EXTRA_ATTR_NAME: transformer}

    # Construct the While AST node with positional None values and the extra kwarg.
    while_node = ast3.While(*positional_args, **extra_kwargs)

    # Execute the visit and assert we get an AST node back.
    visited_node = transformer.visit(while_node)
    assert isinstance(visited_node, ast3.AST)

