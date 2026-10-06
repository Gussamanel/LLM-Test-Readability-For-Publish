import decorators as de_0

def test_cached_property_on_none_type():
    # Create a NoneType object for testing purposes
    none_type = None

    # Initialize a cached_property on NoneType
    cached_property = de_0.cached_property(none_type)

    # Test getting the cached_property on NoneType
    value = cached_property.__get__(none_type, cached_property)

    # Assert that the value is as expected
    assert value is None

# Core purpose: Test cached_property decorator used in module_0.
# This test case is verifying the functionality of the cached_property decorator.
# It is checking whether the decorated function is called only once on the first call and the same value is returned on subsequent calls.
# This test is also verifying whether the decorated function can handle async functions.

# Add constants and variables to the test case
EMPTY_SET = set()

def test_cached_property():
    # Initialize set object before test setup
    set_under_test = EMPTY_SET
    
    # Create a cached property from a function that returns a new set
    cached_property_under_test = module_0.cached_property(set)

    # Call the __get__() method of the cached property
    # This should trigger the function and store a set in the set under test
    cached_property_under_test.__get__(set_under_test, cached_property_under_test)

    # The first call to the cached property should return a set
    # The second call should return the same set
    first_return_value = cached_property_under_test.__get__(set_under_test, cached_property_under_test)
    second_return_value = cached_property_under_test.__get__(set_under_test, cached_property_under_test)

    # Assert that the first and second return values are the same
    assert first_return_value is second_return_value

def test_cached_property_function_returns_correct_result():
    test_set = {"test_value1", "test_value2", "test_value3"}
    cached_value = de_0.cached_property(test_set)
    assert cached_value == "test_value1", "The cached_property function should return the first element of the set"

