import pytest
import decorators as decorators

def test_cached_property_get_returns_self_when_obj_is_none():
    # Test that __get__ returns the cached_property descriptor itself
    # when called with obj=None (descriptor protocol behavior for class-level access)
    
    # Setup: Create a cached_property with None as the function
    NONE_FUNC = None
    cached_property_instance = decorators.cached_property(NONE_FUNC)
    
    # Execution: Call __get__ with obj=None, which should return the descriptor itself
    result = cached_property_instance.__get__(NONE_FUNC, cached_property_instance)
    
    # Assertion: When obj is None, __get__ should return the cached_property instance (self)
    assert result is cached_property_instance
    
    # Verify same behavior when both obj and cls are the cached_property instance
    result_with_self_as_obj = cached_property_instance.__get__(cached_property_instance, cached_property_instance)
    assert result_with_self_as_obj is not None

def test_cached_property_get_raises_error_when_func_is_not_callable():
    """
    Test that cached_property.__get__ raises an error when the wrapped
    func is not callable (e.g., an empty set).

    When __get__ is called with a non-None obj, it will attempt to call
    self.func(obj). Since an empty set is not callable, this should raise
    a TypeError. Additionally, if the property tries to store the result
    in obj's __dict__ and obj doesn't support item assignment, a KeyError
    may be raised instead.
    """
    # Setup: Create an empty set to act as the callable (func) for cached_property
    EMPTY_SET_FUNC = set()

    # Create a cached_property descriptor wrapping the empty set
    cached_property_descriptor = decorators.cached_property(EMPTY_SET_FUNC)

    # Execution & Assertion: Access the property using __get__ with the set as obj
    # Since obj (EMPTY_SET_FUNC) is not None, it will try to call self.func(obj)
    # which will raise a TypeError since set is not callable with an argument
    with pytest.raises((TypeError, KeyError)):
        cached_property_descriptor.__get__(EMPTY_SET_FUNC, cached_property_descriptor)

def test_cached_property_initialized_with_empty_set():
    # Test that cached_property can be initialized with an empty set as the function argument
    
    # Setup
    EMPTY_SET = set()
    
    # Execution
    cached_property_instance = decorators.cached_property(EMPTY_SET)

