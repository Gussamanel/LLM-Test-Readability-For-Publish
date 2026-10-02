import pytest
import decorators as decorators

def test_cached_property_get_returns_self_when_obj_is_none():
    # Test that __get__ returns the cached_property instance itself when obj is None
    # This is the standard descriptor protocol behavior when accessed from the class
    
    # Setup
    NONE_FUNC = None
    cached_property_instance = decorators.cached_property(NONE_FUNC)
    
    # Execute: accessing descriptor with None obj should return the descriptor itself
    result = cached_property_instance.__get__(None, cached_property_instance)
    
    # Assert: when obj is None, __get__ should return the cached_property instance
    assert result is cached_property_instance

def test_cached_property_get_returns_self_when_obj_is_none():
    """
    Test that __get__ returns the cached_property descriptor itself
    when accessed on the class (obj is None), which is the standard
    descriptor protocol behavior for class-level access.
    """
    # Setup: Create an empty set to use as the function and a cached_property instance
    EMPTY_SET_AS_FUNC = set()
    cached_property_instance = decorators.cached_property(EMPTY_SET_AS_FUNC)

    # Assert: Verify that when __get__ is called with obj=None (class-level access),
    # the descriptor returns itself
    none_result = cached_property_instance.__get__(None, cached_property_instance)
    assert none_result is cached_property_instance

def test_cached_property_initialization_with_empty_set():
    # Test that cached_property can be initialized with an empty set as the underlying function
    # This verifies that cached_property accepts a set object during instantiation
    
    # Setup
    EMPTY_SET = set()
    
    # Execution
    cached_property_instance = decorators.cached_property(EMPTY_SET)

