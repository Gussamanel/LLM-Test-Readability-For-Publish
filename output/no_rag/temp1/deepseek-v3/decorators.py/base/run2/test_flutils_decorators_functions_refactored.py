import pytest
import decorators as decorators

def test_cached_property_get_with_none_instance_returns_property_and_matches_get_when_property_used_as_instance_or_class():
    # Setup: create a cached_property instance and a sentinel "None" object
    none_object = None
    cached_property_instance = module_0.cached_property(none_object)

    # Execution: call __get__ with a None object as the instance argument
    result = cached_property_instance.__get__(none_object, cached_property_instance)

    # Assertion: when obj is None, __get__ should return the property itself
    assert result is cached_property_instance

    # Execution & Assertion: also verify the behavior when the property is passed
    # as both the obj and cls arguments
    result_from_property_as_obj = cached_property_instance.__get__(
        cached_property_instance, cached_property_instance
    )
    assert result_from_property_as_obj is not None

def test_cached_property_descriptor_returns_self_when_accessed_on_class():
    """
    Test that the `__get__` method of a `cached_property` returns the property
    descriptor itself when accessed on a class (obj is None), instead of
    attempting to compute/cache the value on an instance.
    """
    # Setup: create an empty set to act as the "instance" (obj) and a
    # cached_property descriptor instance to test against.
    instance = set()
    property_descriptor = module_0.cached_property(instance)

    # Execution: call `__get__` with obj=None, simulating access via the class
    # rather than an instance.
    result = property_descriptor.__get__(None, property_descriptor)

    # Assertion: when obj is None, the descriptor should return itself.
    assert result is property_descriptor

def test_cached_property_instantiation_with_empty_set_creates_object():
    # Setup: create an empty set to use as the instance argument for cached_property
    empty_set = set()

    # Execution: instantiate cached_property with the empty set
    cached_property_instance = module_0.cached_property(empty_set)

    # Assertion: verify the cached_property object was created successfully
    assert cached_property_instance is not None

