import pytest
import decorators as decorators_module

def test_cached_property_returns_self_when_accessed_on_class_and_raises_when_func_none():
    # Purpose:
    # - Ensure the cached_property descriptor returns itself when accessed on a class (obj is None).
    # - Ensure that if the descriptor was constructed with func=None, accessing it on an instance
    #   raises an AttributeError (attempting to read self.func.__name__ fails).
    OBJ_NONE = None
    FUNC_IS_NONE = None
    descriptor = decorators_module.cached_property(FUNC_IS_NONE)

    # Accessing the descriptor via the class (obj is None) should return the descriptor itself
    result_for_class_access = descriptor.__get__(OBJ_NONE, descriptor)
    assert result_for_class_access is descriptor

    # Accessing the descriptor on an instance when func is None should raise AttributeError
    with pytest.raises(AttributeError):
        descriptor.__get__(descriptor, descriptor)

def test_cached_property_get_raises_attribute_error_for_non_callable_func():
    # Purpose:
    # Verify that cached_property.__get__ raises an AttributeError when the
    # underlying "func" object does not have a __name__ attribute (i.e., is not a proper function).
    #
    # This mirrors the situation where cached_property was constructed with a non-callable
    # or non-function object, and __get__ attempts to access self.func.__name__.

    # Constants / Setup
    NON_FUNCTIONAL_OBJECT = set()  # object that is not a function and has no __name__
    cached_prop_decorator = decorators_module.cached_property(NON_FUNCTIONAL_OBJECT)

    # Execution & Assertion: calling __get__ should raise AttributeError because
    # cached_prop_decorator.func (the set) has no __name__ attribute.
    with pytest.raises(AttributeError):
        cached_prop_decorator.__get__(NON_FUNCTIONAL_OBJECT, cached_prop_decorator)

def test_cached_property_raises_type_error_for_non_callable_input():
    # Verify that cached_property enforces being used with a callable by raising TypeError
    # when provided a non-callable argument.
    NON_CALLABLE_OBJECT = set()
    with pytest.raises(TypeError):
        decorators_module.cached_property(NON_CALLABLE_OBJECT)

