import pytest

import yield_from as yield_from_module
import typed_ast.ast3 as ast3

def test_visit_none_node_returns_ast_or_none_without_error():
    parent_node = None
    yield_from_transformer = yield_from_module.YieldFromTransformer(parent_node)

    node_to_visit = None

    result = yield_from_transformer.visit(node_to_visit)

    assert isinstance(result, (ast3.AST, type(None)))

def test_yield_from_transformer_initialization_with_none_input():
    # Setup: Create a YieldFromTransformer instance with None as argument
    none_input = None
    
    # Execution: Initialize the transformer
    yield_from_transformer = yield_from_module.YieldFromTransformer(none_input)

    # Assertion: Verify the transformer was created successfully
    assert yield_from_transformer is not None

def test_visit_while_node_returns_ast_with_transformer():
    # Setup: create a YieldFromTransformer and a While AST node to visit
    transformer = yield_from_module.YieldFromTransformer(None)
    while_node = ast3.While(test=None, body=[None, None])

    # Execution: visit the While node with the transformer
    result = transformer.visit(while_node)

    # Assertion: visiting a While node should return an AST node
    assert isinstance(result, ast3.AST)

def test_visit_yield_from_transformer_processes_while_node():
    # ARRANGE: Create a transformer instance and a While AST node to verify
    # that visiting a While node with a yield-from transformer performs the
    # assignment/expression handling and generic visit.
    transformer = yield_from_module.YieldFromTransformer(None)

    # ARRANGE: Build a While AST node using positional and keyword arguments.
    while_node_args = [None, None]
    while_node_kwargs = {
        "col_offset": 0,
        "end_col_offset": 0,
        "end_lineno": 1,
    }
    while_node = ast3.While(*while_node_args, **while_node_kwargs)

    # ACT: Visit the While node with the YieldFromTransformer.
    result = transformer.visit(while_node)

    # ASSERT: The visit should return the (possibly transformed) node.
    assert result is not None

