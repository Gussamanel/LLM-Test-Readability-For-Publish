import pytest

import decorators as decorators_module

def test_cached_property_descriptor_protocol_and_missing_func_raises():
    """Verify cached_property descriptor protocol and error behavior when no function is provided.

    1) When accessed via the descriptor protocol with obj=None, __get__ should return the descriptor itself.
    2) If the descriptor was constructed without a callable (func is None), attempting to access it on an instance
       should raise an AttributeError.
    """
    # Arrange
    NO_FUNC = None
    cached_prop = decorators_module.cached_property(NO_FUNC)

    # Act & Assert: accessing via descriptor protocol (obj is None) returns the descriptor
    returned_descriptor = cached_prop.__get__(None, type(cached_prop))
    assert returned_descriptor is cached_prop

    # Act & Assert: accessing on an instance when func is None raises AttributeError
    with pytest.raises(AttributeError):
        # Using the descriptor itself as the "instance" simulates instance access and triggers the error path
        cached_prop.__get__(cached_prop, type(cached_prop))

def test_cached_property_get_raises_attribute_error_for_non_dict_object():
    # Purpose:
    # Verify that calling the cached_property descriptor's __get__ on an object
    # that lacks a __dict__ (e.g., a built-in set) raises AttributeError.
    # This exercises the branch where the descriptor attempts to write into obj.__dict__.

    # Constants / Setup
    NON_CALLABLE_VALUE = set()                 # used both as the "func" passed to the decorator and as the target object
    TARGET_OBJECT = NON_CALLABLE_VALUE
    cached_prop = decorators_module.cached_property(NON_CALLABLE_VALUE)

    # Execution + Assertion:
    # The descriptor implementation tries to access obj.__dict__ before calling the function,
    # so using a set (which has no __dict__) should raise AttributeError.
    with pytest.raises(AttributeError):
        cached_prop.__get__(TARGET_OBJECT, cached_prop)

def test_cached_property_handles_non_callable_input_and_returns_object():
    # Purpose:
    # Verify that decorators_module.cached_property can be invoked with a non-callable input
    # (an empty set) and returns an object rather than raising an exception.

    # Constants / Setup
    EMPTY_INPUT = set()
    non_callable_input = EMPTY_INPUT

    # Execution
    cached_property_obj = decorators_module.cached_property(non_callable_input)

    # Assertion: ensure something was returned (no exception raised)
    assert cached_property_obj is not None

