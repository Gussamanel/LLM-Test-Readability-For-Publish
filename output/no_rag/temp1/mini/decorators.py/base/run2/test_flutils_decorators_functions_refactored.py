import pytest

import decorators as decorators_module

def test_cached_property_get_returns_self_on_class_access_and_raises_on_instance_when_func_missing():
    """When accessed on a class (obj is None) cached_property.__get__ returns the descriptor itself.
    When constructed without a function (func is None), accessing it on an instance raises AttributeError.
    """
    func = None
    descriptor = decorators_module.cached_property(func)

    # class-level access (obj is None) should return the descriptor itself
    returned = descriptor.__get__(None, type(descriptor))
    assert returned is descriptor

    # instance-level access should raise because func is missing
    with pytest.raises(AttributeError):
        descriptor.__get__(descriptor, type(descriptor))

def test_cached_property_get_raises_when_func_has_no_name_attribute():
    # Purpose:
    # Ensure cached_property.__get__ raises AttributeError when the descriptor was
    # constructed with a non-callable object that does not have a __name__ attribute.
    #
    # This covers the branch where __get__ tries to access self.func.__name__ before calling it.

    # Setup: create a non-callable object (a set) and construct the descriptor with it.
    NON_CALLABLE_OBJ = set()
    descriptor = decorators_module.cached_property(NON_CALLABLE_OBJ)

    # Execution & Assertion: calling __get__ should raise AttributeError because
    # the non-callable object does not define __name__.
    with pytest.raises(AttributeError):
        descriptor.__get__(NON_CALLABLE_OBJ, descriptor)

def test_cached_property_handles_non_callable_input():
    """Verify calling decorators_module.cached_property with a non-callable
    value (here, an empty set) does not raise and returns a value.
    """
    # Setup
    non_callable_input = set()

    # Execution
    cached_property_result = decorators_module.cached_property(non_callable_input)

    # Assertion
    assert cached_property_result is not None

