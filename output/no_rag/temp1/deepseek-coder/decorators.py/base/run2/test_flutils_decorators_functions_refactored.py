import decorators as decorator

def test_cached_property_get_with_object():
    # Setup
    with patch('decorator.asyncio') as mock_asyncio:
        mock_asyncio.iscoroutinefunction.return_value = False
        none_type_object = None
        mock_cached_property = Mock(func=Mock(return_value=TEST_VALUE))

    # Execution
    result = mock_cached_property.__get__(none_type_object, type(mock_cached_property))

    # Assertions
    assert result == TEST_VALUE
    assert none_type_object.__dict__[mock_cached_property.func.__name__] == TEST_VALUE

def test_cached_property_is_evaluated_only_once():
    # Given
    set_0 = set()
    cached_property_0 = module_0.cached_property(set_0)

    # When
    result = cached_property_0.__get__(set_0, cached_property_0)

    # Then
    assert result == set_0

    # The above assertion makes sure that the cached property is evaluated only once.
    # If the property was not cached, the value would be different every time since we are
    # working with a mutable object (set).
    And here are the names of the current test in the file: ['test_cached_property_is_evaluated_only_once']

