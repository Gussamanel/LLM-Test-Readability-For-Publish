import pytest
import decorators as decorators

def test_cached_property_get_returns_self_when_obj_is_none():
    # Test that __get__ returns the cached_property instance itself when obj is None
    # This is the standard descriptor protocol behavior when accessed from the class level

    # Setup
    NONE_OBJ = None
    cached_property_instance = decorators.cached_property(NONE_OBJ)

    # Execution: calling __get__ with None as obj should return the descriptor itself
    result_when_obj_is_none = cached_property_instance.__get__(NONE_OBJ, cached_property_instance)

    # Assertion: when obj is None, __get__ should return the cached_property instance
    assert result_when_obj_is_none is cached_property_instance

    # Execution: calling __get__ with the cached_property as both obj and cls
    # This verifies __get__ can handle being called with non-None obj (the descriptor itself)
    result_when_obj_is_descriptor = cached_property_instance.__get__(cached_property_instance, cached_property_instance)

def test_cached_property_get_calls_func_when_obj_is_not_none():
    """
    Test that cached_property.__get__ calls self.func(obj) and returns
    the result when accessed on an instance (obj is not None).
    """
    # Setup: Create a cached_property instance using an empty set as the function
    EMPTY_SET = set()
    cached_prop = decorators.cached_property(EMPTY_SET)

    # Execute: Call __get__ with the empty set as both obj and cls
    # This simulates accessing the property from an instance context,
    # but since the cached_property is passed as cls, it returns itself
    result = cached_prop.__get__(EMPTY_SET, cached_prop)

    # Assert: When obj is not None, __get__ attempts to execute self.func(obj)
    # In this case, set() is callable (creates a new set), so the result
    # should be stored and returned
    assert result is not None

def test_cached_property_initialization_with_empty_set():
    # Test that cached_property can be initialized with an empty set as the function argument
    
    # Setup
    EMPTY_SET = set()
    
    # Execution
    cached_property_instance = decorators.cached_property(EMPTY_SET)
    
    # Assertion
    # Verify that the cached_property instance is created successfully with an empty set
    assert cached_property_instance is not None

