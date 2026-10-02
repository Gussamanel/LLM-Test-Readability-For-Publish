import pytest
import decorators as decorators

def test_cached_property_get_returns_self_when_obj_is_none():
    # Test that __get__ returns the cached_property descriptor itself
    # when called with obj=None (descriptor protocol behavior for class-level access)
    
    # Setup: Create a cached_property with None as the function (simulating descriptor creation)
    NONE_FUNC = None
    cached_property_descriptor = decorators.cached_property(NONE_FUNC)
    
    # Execution: Call __get__ with obj=None, which should return the descriptor itself
    result_from_none_obj = cached_property_descriptor.__get__(NONE_FUNC, cached_property_descriptor)
    
    # Assertion: When obj is None, __get__ should return self (the descriptor)
    assert result_from_none_obj is cached_property_descriptor
    
    # Execution: Call __get__ with the descriptor as both obj and cls
    # This verifies the descriptor can handle being passed as an object
    result_from_descriptor_obj = cached_property_descriptor.__get__(cached_property_descriptor, cached_property_descriptor)
    
    # Assertion: When obj is not None, __get__ should not return self
    assert result_from_descriptor_obj is not cached_property_descriptor

def test_cached_property_get_with_none_obj_returns_self():
    """
    Test that accessing a cached_property descriptor with obj=None returns the descriptor itself.
    When __get__ is called with obj=None (class-level access), the descriptor should
    return itself rather than attempting to compute/cache any value.
    """
    # Setup: Create an empty set to use as the function (callable) for cached_property
    # and use another empty set instance as the 'obj' argument
    EMPTY_SET = set()
    cached_prop = decorators.cached_property(EMPTY_SET)

    # Execution & Assertion: When __get__ is called with obj=None (class-level access),
    # the descriptor returns itself, so we verify the descriptor is returned
    result = cached_prop.__get__(None, cached_prop)

    # When obj is None, __get__ should return the descriptor itself
    assert result is cached_prop

def test_cached_property_initialization_with_empty_set():
    # Test that cached_property can be initialized with an empty set as the function argument
    
    # Setup
    EMPTY_SET = set()
    
    # Execution
    cached_property_instance = decorators.cached_property(EMPTY_SET)
    
    # Assertion
    # Verify that the cached_property instance is created successfully with an empty set
    assert cached_property_instance is not None

