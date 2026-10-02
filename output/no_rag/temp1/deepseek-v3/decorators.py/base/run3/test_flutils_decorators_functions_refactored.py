import pytest
import decorators as decorators_module

def test_cached_property_get_returns_descriptor_for_none_obj_and_uses_func_for_instance():
    # Setup
    none_function = None
    cached_property_instance = decorators_module.cached_property(none_function)

    # When __get__ is called with obj=None, return the descriptor itself
    result = cached_property_instance.__get__(none_function, cached_property_instance)
    assert result is cached_property_instance

    # When __get__ is called with the descriptor as obj, fall back to stored func
    result_2 = cached_property_instance.__get__(cached_property_instance, cached_property_instance)
    assert result_2 == cached_property_instance.func

def test_cached_property_descriptor_short_circuits_on_class_level_access():
    # Setup: create a set instance that will serve as the object owning the cached_property
    target_object = set()

    # Setup: instantiate the cached_property descriptor bound to the set instance
    cached_property_descriptor = decorators_module.cached_property(target_object)

    # Execution: invoke the descriptor's __get__ with obj=None (class-level access),
    # which should short-circuit and return the descriptor itself
    result = cached_property_descriptor.__get__(None, cached_property_descriptor)

    # Assertion: accessing the descriptor on the class (obj is None) returns the descriptor
    assert result is cached_property_descriptor

@pytest.mark.usefixtures("decorators_module")
def test_cached_property_accepts_empty_set_argument():
    empty_set = set()
    cached_property_instance = decorators_module.cached_property(empty_set)
    assert cached_property_instance is not None

