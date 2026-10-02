import pytest
import decorators as decorators

def test_cached_property_get_returns_self_when_obj_is_none():
    # Test that __get__ returns the cached_property instance itself when obj is None
    # This is standard descriptor protocol behavior - returning self when accessed on the class

    # Setup
    NONE_OBJ = None

    # Create a cached_property instance with None as the function
    cached_property_instance = decorators.cached_property(NONE_OBJ)

    # Execution: Call __get__ with None as obj, which should return the descriptor itself
    result = cached_property_instance.__get__(NONE_OBJ, cached_property_instance)

    # Assert: When obj is None, __get__ should return the cached_property instance (self)
    assert result is cached_property_instance

    # Execution: Call __get__ with the cached_property instance as obj
    # This verifies __get__ handles being called with a non-None obj (the descriptor itself)
    cached_property_instance.__get__(cached_property_instance, cached_property_instance)

def test_cached_property_get_returns_descriptor_when_accessed_from_class():
    """
    Test that cached_property.__get__ returns self (the descriptor)
    when accessed from the class level (obj is None/falsy).
    
    When __get__ is called with obj=None, it means the property is being
    accessed from the class rather than an instance, and the descriptor
    itself should be returned.
    """
    # Setup: Create a simple function and wrap it with cached_property
    def sample_func():
        pass

    cached_prop = decorators.cached_property(sample_func)

    # Execute: Call __get__ with obj=None to simulate class-level access
    result = cached_prop.__get__(None, type(cached_prop))

    # Assert: When obj is None, __get__ should return the descriptor itself
    assert result is cached_prop

def test_cached_property_initialization_with_empty_set():
    # Test that cached_property can be initialized with an empty set as the wrapped object
    
    # Setup
    EMPTY_SET = set()
    
    # Execution
    cached_property_instance = decorators.cached_property(EMPTY_SET)
    
    # Assert: Verify that the cached_property instance is created successfully
    assert cached_property_instance is not None

