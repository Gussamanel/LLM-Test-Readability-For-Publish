import pytest

import decorators as decorators_module

def test_cached_property_get_behavior_with_none_func():
    # Verify cached_property.__get__ behavior when the underlying function is None:
    # - When accessed on the class (obj is None) it should return the descriptor itself.
    # - When accessed on an instance it should raise AttributeError because self.func is None.
    NO_FUNCTION = None
    descriptor = decorators_module.cached_property(NO_FUNCTION)

    # Class access: obj is None -> descriptor should be returned unchanged.
    returned_when_class_accessed = descriptor.__get__(None, type(descriptor))
    assert returned_when_class_accessed is descriptor

    # Instance access: with func == None, resolving should raise AttributeError.
    with pytest.raises(AttributeError):
        descriptor.__get__(descriptor, type(descriptor))

def test_cached_property_raises_when_initialized_with_non_callable():
    # This test verifies that cached_property raises a TypeError when it is
    # created with a non-callable object as the underlying "func".
    # Setup: define a non-callable and an object instance that has a __dict__.
    NON_CALLABLE_FUNC = set()  # deliberately not a function/callable
    class DummyObject:
        pass
    target_instance = DummyObject()
    target_class = DummyObject

    # Create the cached_property wrapper using the non-callable.
    cached_prop = decorators_module.cached_property(NON_CALLABLE_FUNC)

    # Execution & Assertion: calling __get__ should attempt to call the non-callable
    # and therefore raise a TypeError.
    with pytest.raises(TypeError):
        cached_prop.__get__(target_instance, target_class)

def test_cached_property_descriptor_creation_from_object():
    """Verify that decorators_module.cached_property returns a descriptor-like object when given a non-callable."""
    # Setup: create a sample target object to be wrapped by cached_property
    ORIGINAL_TARGET = set()
    wrapped_target = ORIGINAL_TARGET

    # Execution: construct the cached_property wrapper around the target object
    cached_prop = decorators_module.cached_property(wrapped_target)

    # Assertions:
    # - The constructor should return a non-None value.
    # - The returned value should behave like a descriptor (provide __get__).
    assert cached_prop is not None
    assert hasattr(cached_prop, "__get__")

    # If the implementation stores the original target on an attribute (commonly "func"),
    # ensure that attribute references the exact object we passed in.
    if hasattr(cached_prop, "func"):
        assert getattr(cached_prop, "func") is ORIGINAL_TARGET

