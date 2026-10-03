import decorators as module_1

def test_cached_property_on_none():
    """
    This test verifies that the `cached_property` descriptor correctly handles
    being called on None, and returns itself if the wrapped function is a coroutine.
    """

    # Setup
    none_obj = None
    mock_function = MagicMock(name="mock_function")
    cached_property_descriptor = module_1.cached_property(mock_function)

    # Execution
    result = cached_property_descriptor.__get__(none_obj, type(cached_property_descriptor))

    # Assertion
    assert result == cached_property_descriptor, (
        "Returned value from get is not the descriptor itself, when obj is None"
    )

    # Repeat with a coroutine function, to check wrapping
    mock_async_function = asyncio.coroutine(MagicMock(name="async_mock_function"))
    async_cached_property_descriptor = module_1.cached_property(mock_async_function)

    result = async_cached_property_descriptor.__get__(none_obj, type(async_cached_property_descriptor))
    assert asyncio.iscoroutine(result), "Returned value is not a coroutine, when the function is an async function"

def test_cached_property_on_none_1():
    # Set up: Initialize the set and the cached property
    initial_set = set()
    cached_property = module_1.cached_property(initial_set)

    # Execution: Use the cached property's __get__ method
    result = cached_property.__get__(initial_set, cached_property)

    # Assertion: The result should be equal to the initial set
    assert result == initial_set

def test_cache_stores_new_instance_when_changing_values_2():
    cache_store = set()
    cached_property = module_0.cached_property(cache_store)
    cached_property.set_value('new_value')
    assert 'new_value' in cache_store, "Failed to store value in cache store"

