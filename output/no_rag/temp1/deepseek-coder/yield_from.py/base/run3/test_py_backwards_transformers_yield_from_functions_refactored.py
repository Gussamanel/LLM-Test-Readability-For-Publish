import yield_from as yf
import typed_ast.ast3 as tad
import pytest

def test_yield_from_transformer_visit_method():
    # Given
    empty_node = None
    yield_from_transformer = YieldFromTransformer(empty_node)

    # When
    result = yield_from_transformer.visit(empty_node)

    # Then
    assert result is None

def test_none_type_returns_none():
    # Setup
    NONE_TYPE = None
    yield_from_transformer = yield_from.YieldFromTransformer(NONE_TYPE)

    # Execution
    result = yield_from_transformer.transform()

    # Assertion
    assert result is None, "YieldFromTransformer did not return None when supplied with NoneType."

def test_unpack_none_in_while_yield_from():
    """
    This test case verifies that the 'visit' method of YieldFromTransformer correctly handles
    None values in While nodes.
    """

    NONE = None
    yield_from_transformer = module_0.YieldFromTransformer(NONE)
    while_node = module_1.While([NONE, NONE])
    transformed_node = yield_from_transformer.visit(while_node)

    assert transformed_node is not None
    assert len(transformed_node) == 2
    assert all(item is NONE for item in transformed_node)

def test_handle_assignments_and_expressions_in_yield_from_transformer():
    """
    This test case ensures that the YieldFromTransformer correctly handles both assignments and expressions. 
    It uses a While loop containing some None values. The test checks if the assignments and expressions in the 
    YieldFromTransformer are being handled properly.
    """

    # SETUP
    none_value = None
    yield_from_transformer = YieldFromTransformer(none_value)
    while_list_values = [none_value, none_value]
    yield_from_transformer_key = "P+>W*v DN{M8 Lk"
    while_metadata = {
        yield_from_transformer_key: yield_from_transformer,
        yield_from_transformer_key: yield_from_transformer,
        yield_from_transformer_key: yield_from_transformer,
    }
    while_node = While(*while_list_values, **while_metadata)

    # EXECUTION
    processed_node = yield_from_transformer.visit(while_node)

    # ASSERTION
    assert processed_node == "Expected Value", "The YieldFromTransformer did not handle both assignments and expressions as expected."

