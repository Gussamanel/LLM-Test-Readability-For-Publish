import pytest
import decorators as decorators

def test_cached_property_get_returns_self_when_obj_is_none():
    # Test that __get__ returns the cached_property descriptor itself
    # when called with None as the object (descriptor protocol behavior)
    
    # Setup: Create a cached_property with None as the function
    NONE_FUNC = None
    cached_property_descriptor = decorators.cached_property(NONE_FUNC)
    
    # Execution: Call __get__ with None as obj, which should return the descriptor itself
    result_with_none_obj = cached_property_descriptor.__get__(NONE_FUNC, cached_property_descriptor)
    
    # Assert: When obj is None, __get__ should return the descriptor instance itself
    assert result_with_none_obj is cached_property_descriptor
    
    # Execution: Call __get__ with the descriptor as obj (non-None case)
    # This verifies __get__ handles a non-None obj (even if it's the descriptor itself)
    result_with_descriptor_obj = cached_property_descriptor.__get__(cached_property_descriptor, cached_property_descriptor)

def test_cached_property_get_returns_self_when_accessed_from_class():
    # Test that __get__ returns the cached_property descriptor itself
    # when accessed from the class level (obj is None)

    # Setup: Create a simple function and wrap it with cached_property
    def sample_func(self):
        return 42

    cached_property_descriptor = decorators.cached_property(sample_func)

    # Execute: When __get__ is called with obj=None (class-level access),
    # it should return the descriptor itself
    result = cached_property_descriptor.__get__(None, type(cached_property_descriptor))

    # Assert: The result should be the cached_property descriptor itself
    assert result is cached_property_descriptor

def test_cached_property_initialized_with_empty_set():
    # Test that cached_property can be initialized with an empty set as the function argument
    
    # Setup
    EMPTY_SET = set()
    
    # Execution
    cached_property_instance = decorators.cached_property(EMPTY_SET)
    
    # Assertion
    # Verify that the cached_property instance is created successfully with an empty set
    assert cached_property_instance is not None

