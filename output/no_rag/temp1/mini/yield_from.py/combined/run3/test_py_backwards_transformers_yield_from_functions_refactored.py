import pytest

import yield_from as yield_from_module
import typed_ast.ast3 as typed_ast3

def test_visit_accepts_none_and_returns_none():
    """Verify that YieldFromTransformer.visit accepts None and returns None."""
    transformer = yield_from_module.YieldFromTransformer(None)
    result = transformer.visit(None)
    assert result is None

def test_yield_from_transformer_initialization_with_none():
    # Purpose:
    # Ensure YieldFromTransformer can be constructed with a None input without raising,
    # and that it returns a valid instance of the expected transformer class.
    
    # Constants / Test data
    INPUT_SOURCE = None

    # Setup / Execution: instantiate the transformer with a None input
    transformer = yield_from_module.YieldFromTransformer(INPUT_SOURCE)

    # Assertions: verify an instance was created and is of the correct type
    assert transformer is not None
    assert isinstance(transformer, yield_from_module.YieldFromTransformer)

def test_yield_from_transformer_visit_preserves_while_node_structure():
    # Purpose:
    # Ensure YieldFromTransformer.visit processes a While node (handles assignments and expressions)
    # and returns an AST node (via generic_visit). We use placeholder None values for node parts
    # because this test focuses on control flow through visit(), not semantic correctness of the node.
    
    # ---- Constants / Test data ----
    NONE_VALUE = None
    # A simple placeholder "body/test" consisting of two None entries (mirrors the original test shape)
    LOOP_PLACEHOLDERS = [NONE_VALUE, NONE_VALUE]
    # Arguments to construct the While node (kept as two entries to match the original test)
    WHILE_CONSTRUCTOR_ARGS = [LOOP_PLACEHOLDERS, LOOP_PLACEHOLDERS]

    # ---- Setup ----
    # Create the transformer under test. The original test passed None as its constructor argument.
    transformer = yield_from_module.YieldFromTransformer(NONE_VALUE)
    # Construct a While node using typed_ast3; using placeholder lists to mirror the original test input.
    while_node = typed_ast3.While(*WHILE_CONSTRUCTOR_ARGS)

    # ---- Execution ----
    transformed_node = transformer.visit(while_node)

    # ---- Assertions ----
    # The visit method should return an AST node (not None) and preserve the While node type
    # (visit delegates to generic_visit after handling assignments/expressions).
    assert transformed_node is not None
    assert isinstance(transformed_node, typed_ast3.While)

def test_yield_from_transformer_visits_while_node_preserves_type_and_attrs():
    # Purpose:
    # Verify that YieldFromTransformer.visit can accept a While node,
    # run its internal handlers, and return an AST node of the same kind.
    # Also check that arbitrary keyword attributes provided at construction
    # time are preserved on the node (this mirrors the original test's
    # use of extra kwargs).

    # Constants / test data
    EXTRA_ATTR_NAME = "custom_attr"
    TEST_WHILE_TEST = None
    TEST_WHILE_BODY = None

    # Setup: create transformer and a While node with an extra attribute
    transformer = yield_from_module.YieldFromTransformer(None)
    extra_attrs = {EXTRA_ATTR_NAME: transformer}
    while_node = typed_ast3.While(TEST_WHILE_TEST, TEST_WHILE_BODY, **extra_attrs)

    # Execution: run the transformer's visitor on the While node
    transformed_node = transformer.visit(while_node)

    # Assertions: returned value is a While node and preserves the extra attribute
    assert isinstance(transformed_node, typed_ast3.While)
    assert hasattr(transformed_node, EXTRA_ATTR_NAME)
    assert getattr(transformed_node, EXTRA_ATTR_NAME) is transformer

