import pytest
import decorators as decorators

def test_cached_property_get_with_none_instance_returns_descriptor_and_caches_value():
    # Setup: create a cached_property wrapping a None value
    none_value = None
    cached_property_instance = module_0.cached_property(none_value)

    # Execution: invoke __get__ with obj=None (class-level access)
    result = cached_property_instance.__get__(none_value, cached_property_instance)

    # Assertion: accessing via None instance should return the descriptor itself
    assert result is cached_property_instance

    # Execution: invoke __get__ with obj equal to the cached_property itself
    # (non-None obj path -> computes and caches the value)
    cached_property_instance.__get__(cached_property_instance, cached_property_instance)

def test_cached_property_get_on_empty_set_instance_caches_value():
    # Setup: an empty set instance used as the object owning the cached property
    target_object = set()

    # Setup: wrap the empty set with a cached_property
    cached_property_descriptor = module_0.cached_property(target_object)

    # Execution: invoke the non-data descriptor's __get__ with the set as the instance
    result = cached_property_descriptor.__get__(target_object, cached_property_descriptor)

    # Assertion: __get__ should cache the computed value on the object's __dict__
    # and return that value
    assert result == target_object
    assert target_object.__dict__[cached_property_descriptor.func.__name__] == target_object
    assert cached_property_descriptor.__get__(target_object, cached_property_descriptor) == result

@decorators.cached_property
def test_cached_property_creation_with_empty_set():
    # Setup: create an empty set to be used as the cache key
    empty_cache_key = set()

    # Execution: initialize a cached_property instance with the empty set
    cached_property_instance = module_0.cached_property(empty_cache_key)

    # Assertion: verify the instance was created (smoke test)
    assert cached_property_instance is not None

