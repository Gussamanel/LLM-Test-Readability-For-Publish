import pytest

import decorators as decorators_module

def test_cached_property_returns_self_on_class_access_and_raises_when_func_is_none():
    # Constants / setup
    FUNC_NONE = None
    descriptor = decorators_module.cached_property(FUNC_NONE)

    # Execution & assertion: accessing the descriptor via the class (obj is None)
    # should return the descriptor itself (per descriptor protocol).
    result_when_accessed_on_class = descriptor.__get__(None, descriptor)
    assert result_when_accessed_on_class is descriptor

    # Execution & assertion: accessing the descriptor via an object that is the
    # descriptor instance itself should attempt to call the wrapped function.
    # Since the wrapped function is None, attribute access or call will raise.
    with pytest.raises(AttributeError):
        descriptor.__get__(descriptor, descriptor)

def test_cached_property_caches_computed_value_in_instance_dict():
    # Purpose:
    # Verify that the cached_property descriptor calls the wrapped function,
    # stores the returned value in the instance __dict__ under the function's name,
    # and returns that value.

    # Constants / Setup
    EXPECTED_VALUE = "computed_value"
    PROPERTY_NAME = "my_prop"

    # Create a simple callable that will be wrapped by the descriptor.
    # Ensure it has a predictable __name__ used as the cache key.
    def compute(self):
        return EXPECTED_VALUE
    compute.__name__ = PROPERTY_NAME

    # Create the descriptor using the module's cached_property factory.
    descriptor = decorators_module.cached_property(compute)

    # Create a plain object instance to act as the descriptor owner.
    instance = type("DummyOwner", (), {})()

    # Execution: invoke the descriptor as the attribute getter on the instance.
    returned_value = descriptor.__get__(instance, type(instance))

    # Assertions: the returned value matches and the instance __dict__ is updated.
    assert returned_value == EXPECTED_VALUE
    assert PROPERTY_NAME in instance.__dict__
    assert instance.__dict__[PROPERTY_NAME] == EXPECTED_VALUE

def test_cached_property_accepts_empty_set_and_returns_descriptor():
    # Purpose:
    # Ensure that decorators_module.cached_property can be invoked with an empty set
    # and that it returns a non-None descriptor-like object.

    # Constants / Setup
    EMPTY_INPUT_SET = set()
    source_value = EMPTY_INPUT_SET

    # Execution
    cached_prop_result = decorators_module.cached_property(source_value)

    # Assertions
    # - The call should produce a result (not None).
    # - The result should resemble a descriptor or callable (common for cached_property implementations).
    assert cached_prop_result is not None
    assert hasattr(cached_prop_result, "__get__") or callable(cached_prop_result)

