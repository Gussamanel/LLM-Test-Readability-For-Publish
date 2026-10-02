import pytest

import yield_from as yield_from_module
import typed_ast.ast3 as typed_ast_ast3

def test_yieldfrom_transformer_visit_composes_handlers_and_delegates_to_generic_visit(monkeypatch):
    """Verify YieldFromTransformer.visit:
       - calls _handle_assignments(node)
       - then calls _handle_expressions(node)
       - then calls generic_visit with the node returned by the handlers
       - and returns the value from generic_visit
    """
    # Test data
    INPUT_NODE = None
    GENERIC_VISIT_SENTINEL = object()

    # Create transformer instance
    transformer = yield_from_module.YieldFromTransformer(INPUT_NODE)

    # Record calls and their arguments
    call_log = {}

    def fake_handle_assignments(node):
        call_log['assign_called_with'] = node
        return node

    def fake_handle_expressions(node):
        call_log['expr_called_with'] = node
        return node

    def fake_generic_visit(node):
        call_log['generic_called_with'] = node
        return GENERIC_VISIT_SENTINEL

    # Replace real methods with fakes
    monkeypatch.setattr(transformer, '_handle_assignments', fake_handle_assignments)
    monkeypatch.setattr(transformer, '_handle_expressions', fake_handle_expressions)
    monkeypatch.setattr(transformer, 'generic_visit', fake_generic_visit)

    # Execute
    result = transformer.visit(INPUT_NODE)

    # Assertions
    assert call_log.get('assign_called_with') is INPUT_NODE
    assert call_log.get('expr_called_with') is INPUT_NODE
    assert call_log.get('generic_called_with') is INPUT_NODE
    assert result is GENERIC_VISIT_SENTINEL

def test_yield_from_transformer_initializes_with_none_config():
    # Purpose:
    # Verify that YieldFromTransformer can be instantiated when given a None configuration.
    # This ensures the constructor handles a missing/None config without raising.

    # Setup: define constants used for initialization
    DEFAULT_CONFIG = None

    # Execution: create the transformer using the provided (None) configuration
    transformer = yield_from_module.YieldFromTransformer(DEFAULT_CONFIG)

    # Assertion: the constructor returned an object of the expected type and did not return None
    assert transformer is not None
    assert isinstance(transformer, yield_from_module.YieldFromTransformer)

def test_yield_from_transformer_visit_handles_while_node_with_nested_none_lists():
    # Purpose:
    # Verify that YieldFromTransformer.visit can accept a typed_ast.ast3.While node
    # constructed from nested lists containing None and returns an AST node (no exceptions).
    #
    # Notes:
    # - yield_from_module.YieldFromTransformer corresponds to the transformer under test.
    # - typed_ast_ast3.While constructs a While AST node; we pass simple nested structures
    #   to exercise the visit path that handles assignments and expressions.

    # --------------------
    # Setup
    # --------------------
    TRANSFORMER_INITIAL_ARG = None  # argument passed to YieldFromTransformer in original test
    NONE_ELEMENT = None
    # Construct a simple "test" expression and "body" using repeated None elements,
    # matching the structure used in the original test case.
    test_expression = [NONE_ELEMENT, NONE_ELEMENT]
    body_block = [test_expression, test_expression]

    transformer = yield_from_module.YieldFromTransformer(TRANSFORMER_INITIAL_ARG)
    initial_while_node = typed_ast_ast3.While(*body_block)

    # --------------------
    # Execute
    # --------------------
    transformed_node = transformer.visit(initial_while_node)

    # --------------------
    # Assert
    # --------------------
    # The visit method should return an AST node; in this case we expect a While node
    # (or at least an AST node of the same high-level type).
    assert isinstance(transformed_node, typed_ast_ast3.While)

def test_yield_from_transformer_visits_while_node_and_returns_while():
    # Purpose:
    # Ensure YieldFromTransformer.visit processes a While node by running
    # its internal handlers (_handle_assignments and _handle_expressions)
    # and then delegating to generic_visit, returning an AST node.
    #
    # The visit implementation sequence is:
    #   node = self._handle_assignments(node)
    #   node = self._handle_expressions(node)
    #   return self.generic_visit(node)

    # ---------- Setup ----------
    NONE = None
    DUMMY_KEY = "P+>W*v\nDN{M8\x0bLk"  # arbitrary string used as a keyword name in the original test
    transformer = yield_from_module.YieldFromTransformer(NONE)

    # positional args mirror the original test's [None, None]
    positional_args = [NONE, NONE]

    # original test used the same string key repeated; a dict will retain the last mapping.
    # Keep a single mapping for clarity.
    keyword_args = {DUMMY_KEY: transformer}

    # Construct the While node using the positional and keyword arguments
    while_node = typed_ast_ast3.While(*positional_args, **keyword_args)

    # ---------- Execution ----------
    transformed_node = transformer.visit(while_node)

    # ---------- Assertion ----------
    # The visitor should return an AST node (in this case, a While node).
    assert isinstance(transformed_node, typed_ast_ast3.While)

