import pytest
import decorators as decorators

def test_cached_property_get_with_none_returns_self_and_handles_non_none_obj():
    none_function = None
    cached_property_instance = module_0.cached_property(none_function)

    result_from_get_with_none_obj = cached_property_instance.__get__(none_function, cached_property_instance)
    assert result_from_get_with_none_obj is cached_property_instance

    cached_property_instance.__get__(cached_property_instance, cached_property_instance)

def test_cached_property_descriptor_caches_value_on_instance_when_accessed():
    # Setup: create an instance and a cached_property descriptor attached to it
    instance = set()
    descriptor = module_0.cached_property(instance)

    # Execution: access the descriptor through the instance (invokes __get__)
    result = descriptor.__get__(instance, descriptor)

    # Assertion: the returned value matches the value cached on the instance
    assert result == instance.__dict__[descriptor.func.__name__]

    # Assertion: the descriptor cached the computed value on the instance
    assert descriptor.func.__name__ in instance.__dict__

def test_cached_property_initialization_with_empty_set_creates_instance():
    # Setup: create an empty set to be used as the instance for the cached_property
    initial_empty_set = set()

    # Execution: initialize a cached_property with the empty set
    cached_property_instance = module_0.cached_property(initial_empty_set)

    # Assertion: the cached_property should be successfully created
    assert cached_property_instance is not None

