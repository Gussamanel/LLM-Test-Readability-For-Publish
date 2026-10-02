import pytest

import yield_from as yield_from_module
import typed_ast.ast3 as typed_ast_ast3

def test_visit_returns_none_when_node_is_none():
    """YieldFromTransformer.visit(None) should return None and not raise."""
    # Arrange
    input_node = None
    transformer = yield_from_module.YieldFromTransformer(None)

    # Act
    transformed_node = transformer.visit(input_node)

    # Assert
    assert transformed_node is None

def test_yield_from_transformer_initializes_with_none():
    """
    Purpose:
    - Ensure that YieldFromTransformer can be constructed with a None argument
      and that an instance of the expected type is returned.
    """

    # Setup: define the constant input used to initialize the transformer
    TRANSFORMER_INIT_ARG = None

    # Execution: construct the transformer instance under test
    transformer_instance = module_0.YieldFromTransformer(TRANSFORMER_INIT_ARG)

    # Assertion: verify the transformer was created and is of the expected type
    assert transformer_instance is not None, "Expected a transformer instance to be created"
    assert isinstance(transformer_instance, module_0.YieldFromTransformer), (
        "Expected instance of module_0.YieldFromTransformer"
    )

def test_visit_preserves_while_node_structure_with_none_context():
    # Purpose: ensure YieldFromTransformer.visit can be invoked with a While node
    # when the transformer was constructed with a None context, and that it
    # returns a While node (i.e., structure is preserved and no crash/None).
    DUMMY_CONTEXT = None
    DUMMY_ELEMENT = DUMMY_CONTEXT
    DUMMY_LIST = [DUMMY_ELEMENT, DUMMY_ELEMENT]
    WHILE_NODE_ARGS = [DUMMY_LIST, DUMMY_LIST]

    transformer = yield_from_module.YieldFromTransformer(DUMMY_CONTEXT)
    while_node = typed_ast_ast3.While(*WHILE_NODE_ARGS)

    transformed_node = transformer.visit(while_node)

    assert transformed_node is not None
    assert isinstance(transformed_node, typed_ast_ast3.While)

def test_yield_from_transformer_visits_while_node_with_none_context():
    # Purpose:
    # - Verify that YieldFromTransformer.visit can be called on a While node
    #   when the transformer is created with a None context.
    # - The test sets up a While node using positional and keyword arguments,
    #   runs the visitor, and asserts that a node is returned.

    # ---- Constants / test data ----
    DEFAULT_CONTEXT = None
    # Using the same string used in the original test to preserve input shape.
    ARBITRARY_KEY = "P+>W*v\nDN{M8\x0bLk"

    # ---- Setup ----
    # Create the transformer under test with the None context.
    transformer = yield_from_module.YieldFromTransformer(DEFAULT_CONTEXT)

    # Prepare positional arguments (two None values, as in the original test).
    while_positional_args = [DEFAULT_CONTEXT, DEFAULT_CONTEXT]

    # Prepare keyword arguments: map the arbitrary key to the transformer object
    # (kept to mirror the original test's shape).
    while_keyword_args = {ARBITRARY_KEY: transformer}

    # Construct the While AST node using the prepared args/kwargs.
    while_node = typed_ast_ast3.While(*while_positional_args, **while_keyword_args)

    # ---- Execution ----
    visited_node = transformer.visit(while_node)

    # ---- Assertion ----
    # The visit method should return an AST node (not None). We assert that
    # a node is returned; in typical cases it will be a While node.
    assert visited_node is not None

