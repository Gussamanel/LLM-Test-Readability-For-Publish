import pytest
import decorators as decorators_module

def test_cached_property_get_with_none_instance_returns_descriptor():
    # Setup: Create a cached_property with a placeholder function and a None object.
    NONE_OBJECT = None
    cached_property_descriptor = decorators_module.cached_property(NONE_OBJECT)

    # Execution: Call __get__ with None as the instance.
    result_from_none_instance = cached_property_descriptor.__get__(
        NONE_OBJECT, cached_property_descriptor
    )

    # Execution: Call __get__ with the descriptor as the instance.
    cached_property_descriptor.__get__(
        cached_property_descriptor, cached_property_descriptor
    )

    # Assertion: When obj is None, the descriptor should return itself.
    assert result_from_none_instance is cached_property_descriptor

def test_cached_property_get_with_set_as_instance_creates_dict():
    # SETUP
    empty_set = set()
    cached_property = decorators_module.cached_property(empty_set)

    # EXECUTION
    cached_property.__get__(empty_set, cached_property)

    # ASSERTION
    assert empty_set.__dict__ is not None

def test_cached_property_creation_with_empty_set_as_data_source():
    # Setup: create an empty set to be used as the underlying data for the cached property
    data_source = set()

    # Execution: initialize a cached_property instance wrapping the empty set
    cached_property_instance = decorators_module.cached_property(data_source)

    # Assertion: verify the cached_property was created and wraps the expected set
    assert cached_property_instance is not None
    assert isinstance(cached_property_instance, decorators_module.cached_property)

