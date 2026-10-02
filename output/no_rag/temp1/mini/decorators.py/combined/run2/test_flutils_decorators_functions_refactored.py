import pytest

import decorators as decorators_module

def test_cached_property_descriptor_returns_self_for_class_access_and_raises_if_func_missing():
    # Purpose:
    # - Verify that cached_property.__get__ returns the descriptor itself when accessed via the class (obj is None).
    # - Verify that if the descriptor was created without a callable func, using it as an instance will raise an AttributeError
    #   when the code attempts to access self.func.__name__.
    OWNER_NONE = None
    descriptor = decorators_module.cached_property(OWNER_NONE)  # create descriptor with no underlying function

    # class-level access should return the descriptor object itself
    returned = descriptor.__get__(OWNER_NONE, descriptor)
    assert returned is descriptor

    # instance-level access with missing func should raise an AttributeError
    with pytest.raises(AttributeError):
        descriptor.__get__(descriptor, descriptor)

def test_cached_property_caches_computed_value_and_returns_self_when_accessed_on_class():
    # Purpose:
    # Verify that decorators_module.cached_property computes the value once,
    # stores it on the instance __dict__ under the function's name, and that
    # accessing the descriptor via the class (obj is None) returns the descriptor itself.

    # Constants used in the test
    EXPECTED_VALUE = 42
    ATTRIBUTE_NAME = "expensive_computation"

    # --- Setup: define a dummy host class and a function to be used as the cached property ---
    class DummyObject:
        pass

    def expensive_computation(self):
        # This function name is important: cached_property uses func.__name__ as the dict key
        return EXPECTED_VALUE

    descriptor = decorators_module.cached_property(expensive_computation)
    instance = DummyObject()

    # --- Execution: access the descriptor on the instance to trigger computation and caching ---
    computed_value = descriptor.__get__(instance, DummyObject)

    # --- Assertions: returned value, cached value in instance.__dict__, and class access behavior ---
    assert computed_value == EXPECTED_VALUE
    assert instance.__dict__[ATTRIBUTE_NAME] == EXPECTED_VALUE

    # When accessed on the class (obj is None) the descriptor itself should be returned
    assert descriptor.__get__(None, DummyObject) is descriptor

def test_cached_property_raises_when_given_non_callable():
    """Verify cached_property rejects non-callable input by raising TypeError."""
    non_callable_input = set()  # a non-callable value to pass where a function is expected

    with pytest.raises(TypeError):
        decorators_module.cached_property(non_callable_input)

