import pytest

import decorators as decorators_module

def test_cached_property_get_with_none_object_returns_descriptor_self():
    # Purpose: Verify that accessing a cached_property via descriptor protocol
    # (i.e., calling __get__) with obj set to None returns the cached_property
    # instance itself, regardless of the cls argument used.

    # Setup
    obj_none = None
    cached_property_instance = decorators_module.cached_property(obj_none)

    # Execution & Assertion
    # When obj is None, __get__ should return the descriptor instance itself.
    result_with_none_obj_and_self_cls = cached_property_instance.__get__(
        obj_none, cached_property_instance
    )
    assert result_with_none_obj_and_self_cls is cached_property_instance

    # Also verify the same behavior when cls is a different class while obj is None.
    class DummyClass:
        pass

    result_with_none_obj_and_dummy_cls = cached_property_instance.__get__(
        obj_none, DummyClass
    )
    assert result_with_none_obj_and_dummy_cls is cached_property_instance

def test_cached_property_get_returns_cached_value_when_function_takes_no_args():
    # Setup: create a target object and a cached_property wrapper for a zero-arg function
    target_object = set()
    cached_property_descriptor = decorators_module.cached_property(target_object)

    # Execution: invoke the descriptor's __get__ to fetch and cache the computed value
    retrieved_value = cached_property_descriptor.__get__(target_object, cached_property_descriptor)

    # Assertion: the returned value matches the target object and is stored in its __dict__
    assert retrieved_value is target_object
    assert target_object.__dict__[target_object.__class__.__name__] is target_object

def test_cached_property_initialization_with_empty_set_object():
    # Setup: create an empty set to be used as the wrapped object for cached_property
    empty_set = set()

    # Execution: instantiate cached_property with the empty set as its argument
    cached_property_instance = decorators_module.cached_property(empty_set)

    # Assertion: verify that the cached_property instance is created successfully
    assert cached_property_instance is not None

