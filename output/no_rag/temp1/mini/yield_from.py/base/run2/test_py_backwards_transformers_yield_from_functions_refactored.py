import pytest

import yield_from as yield_from_module
import typed_ast.ast3 as typed_ast_ast3

def test_yield_from_transformer_visit_handles_none_node():
    # Purpose:
    # Verify that YieldFromTransformer.visit can be called with a None node
    # and that it handles this gracefully (no exception) and returns None.

    # Constants / Test data
    INPUT_NODE = None

    # Setup: create the transformer (initial state provided as None)
    transformer = yield_from_module.YieldFromTransformer(INPUT_NODE)

    # Execution: invoke visit with a None node to exercise internal handlers
    result = transformer.visit(INPUT_NODE)

    # Assertion: expecting no transformation and no exception; result should be None
    assert result is None

def test_yield_from_transformer_construction_with_none_context():
    """
    Ensure YieldFromTransformer can be constructed when provided a None context.
    Verifies the constructor accepts None and returns a valid instance without raising.
    """
    # Setup
    context_none = None
    TransformerClass = yield_from_module.YieldFromTransformer

    # Execution
    transformer_instance = TransformerClass(context_none)

    # Assertions
    assert transformer_instance is not None
    assert isinstance(transformer_instance, TransformerClass)
    if hasattr(transformer_instance, "context"):
        assert getattr(transformer_instance, "context") is None

def test_yield_from_transformer_visit_handles_while_node_with_none_elements():
    # Purpose:
    # Verify that YieldFromTransformer.visit can process a While node whose
    # components contain None values (nested lists), ensuring internal handlers
    # are invoked and an AST node (or subclass) is returned.

    # --- Constants / Setup ---
    NONE = None
    INNER_LIST = [NONE, NONE]          # Represents a list with None elements
    OUTER_LIST = [INNER_LIST, INNER_LIST]  # Arguments to construct the While node

    # Instantiate the transformer under test. Passing NONE mirrors original usage.
    transformer = yield_from_module.YieldFromTransformer(NONE)

    # Construct a While node using the nested lists. This mirrors the original test's shape.
    while_node = typed_ast_ast3.While(*OUTER_LIST)

    # --- Execution ---
    visited_node = transformer.visit(while_node)

    # --- Assertion ---
    # The visit method should return an AST node (possibly transformed). At minimum,
    # it should not return None and should be an instance of the typed_ast AST base.
    assert isinstance(visited_node, typed_ast_ast3.AST)

def test_yield_from_transformer_visits_and_returns_while_node():
    # Purpose:
    # Verify that YieldFromTransformer.visit can be called on a typed_ast.ast3.While node
    # and returns an AST node (the transformer delegates to its handlers and then generic_visit).

    # ---- Setup ----
    # Constant inputs used to construct the While node and the transformer.
    TRANSFORMER_INIT_ARG = None
    WHILE_POS_ARGS = [None, None]
    # Use the same literal key string as the original test to reproduce the call shape.
    WHILE_KEYWORD_NAME = "P+>W*v\nDN{M8\x0bLk"

    # Instantiate the transformer under test.
    transformer = yield_from_module.YieldFromTransformer(TRANSFORMER_INIT_ARG)

    # Build keyword arguments for the While AST node. The keyword value is the transformer
    # instance (matches original test structure where the dict mapped the string to the transformer).
    while_kwargs = {WHILE_KEYWORD_NAME: transformer}

    # Construct the While AST node using positional and keyword arguments.
    while_node = typed_ast_ast3.While(*WHILE_POS_ARGS, **while_kwargs)

    # ---- Execution ----
    # Invoke the transformer's visit method on the While node.
    result_node = transformer.visit(while_node)

    # ---- Assertion ----
    # The visit call should return an AST node. In this test we assert it is a While node.
    assert isinstance(result_node, typed_ast_ast3.While)
    # Also assert the result is not None to be explicit about a valid return value.
    assert result_node is not None

