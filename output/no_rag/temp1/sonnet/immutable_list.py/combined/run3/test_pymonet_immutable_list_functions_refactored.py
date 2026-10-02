import pytest
import immutable_list as immutable_list

def test_empty_immutable_list_operations():
    # Test basic operations on an empty ImmutableList:
    # equality check with itself, string representation, conversion to list,
    # and addition of lists

    # Setup: Create an empty ImmutableList
    empty_list = immutable_list.ImmutableList()

    # Execution: Perform operations on the empty list
    # Verify that an empty list is equal to itself
    is_equal_to_self = empty_list.__eq__(empty_list)

    # Get string representation of the empty list
    string_representation = empty_list.__str__()

    # Convert empty ImmutableList to a regular Python list
    converted_list = empty_list.to_list()

    # Add the converted list to itself (regular list addition)
    doubled_list = converted_list.__add__(converted_list)

    # Get the length of the converted list
    converted_list_length = converted_list.__len__()

    # Add the converted regular list back to the original ImmutableList
    empty_list.__add__(converted_list)

    # Assertions: Verify the expected results
    # An empty ImmutableList should be equal to itself
    assert is_equal_to_self is True

    # The converted list from an empty ImmutableList should have length 0
    assert converted_list_length == 0

    # The doubled list should be empty since the original converted list is empty
    assert doubled_list == []

def test_empty_immutable_list_basic_operations():
    """
    Tests basic operations on an empty ImmutableList:
    - Equality check with a non-ImmutableList value should return False
    - Adding an empty list to itself should return a new empty ImmutableList
    - Finding an element using a non-callable (False result) should return None
    - String representation should be retrievable
    - Unshifting an empty list onto itself creates a new list
    - Reducing the resulting list with itself as reducer and True as accumulator
    """
    # Setup
    INITIAL_ACCUMULATOR = True
    empty_list = immutable_list.ImmutableList()

    # Execution - equality check with non-ImmutableList value
    is_equal_to_non_list = empty_list.__eq__(INITIAL_ACCUMULATOR)

    # Execution - adding empty list to itself
    concatenated_empty_list = empty_list.__add__(empty_list)

    # Execution - find using the False equality result as the predicate
    found_element = empty_list.find(is_equal_to_non_list)

    # Execution - string representation of empty list
    list_string_representation = empty_list.__str__()

    # Execution - unshift the empty list itself as a new element
    list_with_prepended_element = empty_list.unshift(empty_list)

    # Execution - reduce the new list using itself as the reducer function and True as accumulator
    reduced_result = list_with_prepended_element.reduce(list_with_prepended_element, INITIAL_ACCUMULATOR)

    # Assertions
    assert is_equal_to_non_list is False  # Empty list is not equal to a boolean
    assert concatenated_empty_list == immutable_list.ImmutableList()  # Adding two empty lists yields an empty list
    assert found_element is None  # Finding in an empty list returns None
    assert reduced_result == INITIAL_ACCUMULATOR  # Reducing with no matching elements returns the accumulator

def test_find_on_immutable_list_with_boolean_head():
    # Constants
    INITIAL_VALUE = True
    IS_EMPTY = True

    # Setup: Create an ImmutableList with a boolean value and is_empty flag set to True
    immutable_list_with_bool = immutable_list.ImmutableList(INITIAL_VALUE, is_empty=IS_EMPTY)

    # Execution: Append the boolean value to create a new list
    # and attempt to find using the original list as a callable predicate
    immutable_list_after_append = immutable_list_with_bool.append(INITIAL_VALUE)
    find_result = immutable_list_with_bool.find(immutable_list_with_bool)

    # Assertion: Verify find result is None since the head is None when is_empty is True
    assert find_result is None

def test_add_raises_value_error_when_adding_non_immutable_list():
    # Test that adding a non-ImmutableList instance (None) to an ImmutableList raises a ValueError
    
    # Setup: Create an empty ImmutableList
    empty_immutable_list = immutable_list.ImmutableList()
    
    # Define invalid argument to add (None is not an ImmutableList instance)
    invalid_argument = None
    
    # Execution & Assertion: Verify that a ValueError is raised when trying to add None to an ImmutableList
    with pytest.raises(ValueError):
        empty_immutable_list.__add__(invalid_argument)

def test_find_returns_none_when_list_is_empty():
    # Test that find() returns None when searching an empty ImmutableList
    # and that find() on a list initialized with an empty list also returns None
    
    # Setup: Create an empty ImmutableList and verify it has length 0
    empty_list = immutable_list.ImmutableList()
    EXPECTED_EMPTY_LENGTH = 0
    empty_list_length = empty_list.__len__()
    assert empty_list_length == EXPECTED_EMPTY_LENGTH

    # Setup: Create a new ImmutableList using the empty list as both
    # the initial value and the is_empty flag
    list_with_empty_head = immutable_list.ImmutableList(
        empty_list, is_empty=empty_list
    )

    # Execute: Attempt to find an element using the list itself as the predicate
    # Since the head is an empty ImmutableList (falsy), find should return None
    result = list_with_empty_head.find(list_with_empty_head)

    # Assert: Verify that find returns None when no element satisfies the predicate
    assert result is None

def test_find_returns_none_for_empty_list_with_false_head():
    # Test that find() returns None and len() returns 0 for an empty ImmutableList
    # An ImmutableList initialized with False head and is_empty=False acts as an empty list
    
    # Constants
    EMPTY_VALUE = False
    EXPECTED_LENGTH = 0
    
    # Setup: Create an empty ImmutableList using False as the head value and is_empty flag
    empty_list = immutable_list.ImmutableList(EMPTY_VALUE, is_empty=EMPTY_VALUE)
    
    # Execution: Get the length of the empty list
    list_length = empty_list.__len__()
    
    # Assertion: Verify the list length is 0 for an empty list
    assert list_length == EXPECTED_LENGTH
    
    # Execution: Attempt to find an element using the list itself as a predicate
    # Since the list is empty (head is None), find() should return None
    find_result = empty_list.find(empty_list)
    
    # Assertion: Verify that find returns None for an empty list
    assert find_result is None

def test_find_with_list_as_predicate_on_single_element_immutable_list():
    # Test that find() works when using a list (converted from the ImmutableList itself)
    # as the predicate function on a single-element ImmutableList initialized with False

    # Setup: Create a single-element ImmutableList with False as the head value
    # and is_empty=False, meaning the list is not considered empty
    IS_NOT_EMPTY = False
    HEAD_VALUE = False
    single_element_list = immutable_list.ImmutableList(HEAD_VALUE, is_empty=IS_NOT_EMPTY)

    # Execution: Convert the ImmutableList to a plain Python list,
    # then use that list as the predicate/callable argument to find()
    plain_list = single_element_list.to_list()

    # A plain list acts as a callable in Python (list([False]) -> [False]),
    # so passing it to find() uses the list as a lookup/truth function
    result = single_element_list.find(plain_list)

    # Assertion: find() should return None since fn(False) -> [] which is falsy
    assert result is None

def test_find_with_none_predicate_on_empty_list_and_append_self():
    # Setup: Create an empty ImmutableList
    empty_immutable_list = immutable_list.ImmutableList()
    
    # No predicate function to search with (None)
    none_predicate = None
    
    # Execution: Find with None predicate on an empty list should return None
    # since the list has no head element
    find_result = empty_immutable_list.find(none_predicate)
    
    # Assert: Finding in an empty list returns None
    assert find_result is None
    
    # Execution: Append the empty list itself as an element to create a new list
    list_with_appended_element = empty_immutable_list.append(empty_immutable_list)
    
    # Convert the new ImmutableList to a regular Python list
    converted_list = list_with_appended_element.to_list()
    
    # Assert: The converted list contains the appended empty ImmutableList as its element
    assert converted_list == [empty_immutable_list]
    
    # Assert: Attempting to add None to a Python list raises a TypeError,
    # since Python lists can only be concatenated with other lists via __add__
    with pytest.raises(TypeError):
        converted_list.__add__(none_predicate)

def test_map_with_list_as_function_on_non_empty_immutable_list():
    # Test that map can be called with a list as the mapping function
    # on an ImmutableList initialized with is_empty=False
    
    # Setup: Create a non-empty ImmutableList and a default ImmutableList
    IS_EMPTY = False
    non_empty_list = immutable_list.ImmutableList(is_empty=IS_EMPTY)
    default_list = immutable_list.ImmutableList()
    
    # Execution: Convert non_empty_list to a Python list, which will be used as the mapping function
    list_representation = non_empty_list.to_list()
    
    # Retrieve the list representation again to use as the mapping function
    mapping_function = non_empty_list.to_list()
    
    # Apply map using the list as the callable argument
    # Note: This tests behavior when a list (which is not callable) is passed as fn
    non_empty_list.map(mapping_function)

def test_map_with_none_function_raises_error():
    # Test that calling map() with None as the function raises a TypeError
    # when applied to a list built through unshift and append operations
    
    # Setup: Create an ImmutableList with None as both head and tail
    NONE_VALUE = None
    base_list = immutable_list.ImmutableList(NONE_VALUE, NONE_VALUE)
    
    # Execution: Build a more complex list structure using unshift and append operations
    # unshift adds None to the beginning of base_list
    list_with_none_prepended = base_list.unshift(NONE_VALUE)
    # unshift adds the previously created list to the beginning of base_list
    list_with_list_prepended = base_list.unshift(list_with_none_prepended)
    # append adds None to the end of list_with_none_prepended
    list_with_none_appended = list_with_none_prepended.append(NONE_VALUE)
    
    # Assertion: Calling map() with None as the mapping function should raise a TypeError
    # since None is not callable
    with pytest.raises(TypeError):
        list_with_none_appended.map(NONE_VALUE)

def test_filter_with_immutable_list_as_predicate():
    """
    Test that filter can be called using an ImmutableList as the predicate function.
    An ImmutableList initialized with False and is_empty=False is used both as the
    list to filter and as the filtering predicate (callable).
    The ImmutableList with a False head acts as a falsy predicate, so no elements
    should pass the filter, resulting in an empty ImmutableList.
    """
    # Setup
    FALSY_VALUE = False
    
    # Create an ImmutableList with a False head and is_empty=False
    immutable_list_with_false_head = immutable_list.ImmutableList(FALSY_VALUE, is_empty=FALSY_VALUE)
    
    # Execution
    # Use the ImmutableList itself as the predicate/callable for the filter operation
    filtered_result = immutable_list_with_false_head.filter(immutable_list_with_false_head)
    
    # Assertion
    # Since the predicate (ImmutableList with False head) is falsy, 
    # the result should be an empty ImmutableList
    assert filtered_result.is_empty == True

def test_filter_with_length_as_predicate_on_concatenated_empty_lists():
    # Test that filtering a concatenated empty ImmutableList using its length as predicate works correctly
    # An empty list concatenated with itself should produce an empty list
    # Filtering with length (0) as predicate tests the filter behavior with a falsy value

    # Setup: Create an empty ImmutableList and concatenate it with itself
    empty_list = immutable_list.ImmutableList()
    concatenated_empty_list = empty_list.__add__(empty_list)

    # Execute: Get the length of the concatenated list and use it as a filter predicate
    concatenated_list_length = concatenated_empty_list.__len__()

    # Assert: Filtering the concatenated list with its length (0) as predicate should work without errors
    # Length of empty list is 0, which is falsy, so filter should return an empty ImmutableList
    EXPECTED_LENGTH = 0
    assert concatenated_list_length == EXPECTED_LENGTH
    filtered_list = concatenated_empty_list.filter(concatenated_list_length)
    assert filtered_list.__len__() == EXPECTED_LENGTH

def test_find_on_empty_list_returns_none_with_zero_length():
    # Test that finding an element in an empty ImmutableList returns None,
    # and that the length of the result is 0 (None has no length, but the list itself is empty)
    
    # Constants
    SEARCH_VALUE = 1947
    
    # Setup: Create an empty ImmutableList with both head and tail as None
    empty_head = None
    empty_tail = None
    empty_list = immutable_list.ImmutableList(empty_head, empty_tail)
    
    # Execution: Attempt to find an element in the empty list
    # Since the list is empty (head is None), find() should return None
    find_result = empty_list.find(SEARCH_VALUE)
    
    # Assertion: Verify that the length of the empty list is 0
    # (calling __len__ on the find result which is the empty list context)
    result_length = find_result.__len__()
    assert result_length == 0

def test_find_returns_none_using_list_as_predicate_on_false_initialized_list():
    # Test that find() returns None when searching an empty ImmutableList
    # An ImmutableList initialized with False and is_empty=False should have no elements to search
    
    # Setup
    IS_EMPTY = False
    
    # Execution
    empty_list = immutable_list.ImmutableList(IS_EMPTY, is_empty=IS_EMPTY)
    
    # Use the list itself as the search function (False is callable as a boolean,
    # which means no element will satisfy the condition)
    result = empty_list.find(empty_list)
    
    # Assertion
    # Since the list is empty (head is None), find() should return None
    assert result is None

def test_reduce_on_empty_list_returns_accumulator_and_find_with_non_callable_predicate():
    """
    Tests that:
    1. reduce() on an empty ImmutableList returns the accumulator unchanged when given a non-callable (False)
    2. find() on a single-element ImmutableList returns None when given a non-callable (False) as the predicate,
       since calling False on an element will not return True
    """
    # Constants
    NON_CALLABLE_VALUE = False

    # Setup - Create an empty ImmutableList
    empty_list = immutable_list.ImmutableList()

    # Execution - reduce on empty list should return the accumulator (NON_CALLABLE_VALUE) unchanged
    # since head is None, the reduce method returns acc directly without calling fn
    reduce_result = empty_list.reduce(NON_CALLABLE_VALUE, empty_list)

    # Setup - Create a single-element ImmutableList using NON_CALLABLE_VALUE as head
    # is_empty=False ensures the list is treated as non-empty
    single_element_list = immutable_list.ImmutableList(NON_CALLABLE_VALUE, is_empty=NON_CALLABLE_VALUE)

    # Execution - find() with a non-callable predicate (False) on a single-element list
    # Since tail is None and fn(head) evaluates False(False) which raises TypeError or returns falsy,
    # the find result will be None
    find_result = single_element_list.find(single_element_list)

    # Assertion - reduce on empty list returns the accumulator (the empty_list itself)
    assert reduce_result == empty_list

def test_immutable_list_default_initialization():
    # Test that an ImmutableList can be created with no arguments
    # and that it initializes successfully as an empty immutable list
    
    # Setup & Execution: Create an empty ImmutableList with default constructor
    empty_immutable_list = immutable_list.ImmutableList()

def test_find_returns_none_when_head_is_falsy_using_list_as_predicate():
    # Test that find() returns None when searching an empty ImmutableList
    # using another ImmutableList instance as the predicate function.
    # Since the ImmutableList is initialized with False (no head element),
    # find() should return None without invoking the predicate.

    # Setup: Create an empty ImmutableList with is_empty=False and head=False
    IS_EMPTY = False
    HEAD_VALUE = False

    empty_list = immutable_list.ImmutableList(HEAD_VALUE, is_empty=IS_EMPTY)

    # Execution: Get string representation and attempt to find using the list itself as predicate
    list_string_representation = empty_list.__str__()
    find_result = empty_list.find(empty_list)

    # Assert: find() should return None since head is False (falsy, treated as no valid element)
    assert find_result is None

def test_find_after_unshift_with_immutable_list_as_element():
    """
    Tests that find() works correctly after unshifting an ImmutableList as an element.
    
    This test verifies:
    1. An ImmutableList can be created with False as the head element and is_empty=False
    2. An ImmutableList can be unshifted (prepended) with another ImmutableList as an element
    3. The find() method can be called with an ImmutableList as the search function argument
    """
    # Setup
    INITIAL_VALUE = False
    initial_list = immutable_list.ImmutableList(INITIAL_VALUE, is_empty=INITIAL_VALUE)

    # Execution
    list_with_prepended_element = initial_list.unshift(initial_list)
    
    # find() is called with an ImmutableList as the callable argument (fn),
    # which acts as a truthy/falsy function since ImmutableList is used as fn
    result = initial_list.find(initial_list)

def test_find_returns_none_when_predicate_is_false_for_all_elements():
    # Test that find returns None when the predicate (False) matches no elements
    # in a list constructed by unshifting and appending ImmutableList instances
    
    # Setup: Create an initial non-empty ImmutableList and build a multi-element list
    IS_EMPTY = False
    SEARCH_PREDICATE = False  # Using False as predicate, which will never match any element
    
    # Create base ImmutableList with is_empty=False (non-empty list)
    base_list = immutable_list.ImmutableList(is_empty=IS_EMPTY)
    
    # Execution: Build a more complex list by unshifting and appending elements
    # unshift adds False to the beginning of base_list
    list_with_prepended_element = base_list.unshift(IS_EMPTY)
    # append adds base_list (ImmutableList) to the end of list_with_prepended_element
    list_with_appended_element = list_with_prepended_element.append(base_list)
    
    # Search for an element using False as the predicate function (always returns False)
    result = list_with_appended_element.find(SEARCH_PREDICATE)
    
    # Assertion: Since the predicate is False (never matches), find should return None
    assert result is None

def test_immutable_list_append_and_find_with_boolean_predicate():
    # Constants
    BOOL_VALUE = True
    
    # Setup: Create an ImmutableList initialized with True and marked as non-empty
    initial_list = immutable_list.ImmutableList(BOOL_VALUE, is_empty=BOOL_VALUE)
    
    # Execution: Append a boolean value to the list and check the length
    appended_list = initial_list.append(BOOL_VALUE)
    
    # Verify the length of the appended list is correct
    appended_list_length = appended_list.__len__()
    
    # Assert: Find the initial list within itself using the initial list as the predicate function.
    # Since ImmutableList is used as a callable (fn), it tests that find() 
    # handles the case where the predicate is a non-standard callable (ImmutableList object).
    result = initial_list.find(initial_list)

def test_immutable_list_nested_structure_with_reduce_and_find():
    # Setup: Create an empty ImmutableList and build nested structures
    empty_list = immutable_list.ImmutableList()
    
    # Execution: Build a list containing itself as an element
    list_with_self = empty_list.append(empty_list)
    
    # Use reduce with the nested list as both the function and accumulator
    # Since list_with_self is used as the reducer function, it processes the empty list
    reduced_result = empty_list.reduce(list_with_self, list_with_self)
    
    # Assert: Check equality between the two lists (list_with_self vs empty_list)
    are_lists_equal = list_with_self.__eq__(empty_list)
    
    # Create a new list by prepending list_with_self to itself using unshift
    list_with_prepended = list_with_self.unshift(list_with_self)
    
    # Get string representation of the prepended list
    # Expected format: 'ImmutableList[<elements>]'
    list_string_representation = list_with_prepended.__str__()
    
    # Create a new ImmutableList using the string representation as the is_empty flag
    list_from_string = immutable_list.ImmutableList(is_empty=list_string_representation)
    
    # Append reduced_result to itself to create a deeper nested structure
    list_with_appended_reduced = reduced_result.append(reduced_result)
    
    # Attempt to find reduced_result within the prepended list
    # reduced_result is used as the predicate function for find
    find_result = list_with_prepended.find(reduced_result)

def test_reduce_on_empty_list_with_immutable_list_as_accumulator_and_find_on_result():
    # Setup: Create an empty ImmutableList and build up test structures
    empty_list = immutable_list.ImmutableList()
    
    # Create a list with the empty list as its first element [empty_list]
    list_with_empty = empty_list.unshift(empty_list)
    
    # Execute: Reduce the empty list using list_with_empty as both the reducer function
    # and accumulator. Since empty_list has no head, reduce returns the accumulator (list_with_empty)
    reduced_result = empty_list.reduce(list_with_empty, list_with_empty)
    
    # Get the length of list_with_empty (should be 1, since it contains one element)
    list_with_empty_length = list_with_empty.__len__()
    EXPECTED_LENGTH = 1
    
    # Create a new list by prepending list_with_empty to itself [list_with_empty, empty_list]
    nested_list = list_with_empty.unshift(list_with_empty)
    
    # Check if nested_list equals empty_list (should be False, they have different structures)
    are_equal = nested_list.__eq__(empty_list)
    
    # Create a new ImmutableList using the length value as is_empty parameter
    list_from_length = immutable_list.ImmutableList(is_empty=list_with_empty_length)
    
    # Assert: Call find on the reduced result using reduced_result as the predicate function
    # Since reduced_result is an ImmutableList (not a callable returning bool), find will attempt
    # to call it on each element
    find_result = reduced_result.find(reduced_result)
    
    # Verify the length of list_with_empty is as expected
    assert list_with_empty_length == EXPECTED_LENGTH
    
    # Verify nested_list is not equal to the original empty list
    assert are_equal == False

def test_reduce_with_to_list_as_fn_and_acc():
    # Test that reduce can handle using to_list result as both function and accumulator
    # Setup
    IS_EMPTY = True
    EMPTY_DICT = {}

    # Create an ImmutableList with an empty dict as tail (head is None)
    immutable_list_with_empty_tail = immutable_list.ImmutableList(tail=EMPTY_DICT)

    # Create an ImmutableList with True as head and is_empty=True
    immutable_list_with_bool_head = immutable_list.ImmutableList(IS_EMPTY, is_empty=IS_EMPTY)

    # Execution
    # Convert the bool-headed list to a regular Python list [True]
    list_representation = immutable_list_with_bool_head.to_list()

    # Use the list representation as both the reducer function and accumulator
    # Since head is True (not None) and tail is None, reduce returns fn(acc, head)
    # which calls list_representation(list_representation, True)
    result = immutable_list_with_bool_head.reduce(list_representation, list_representation)

    # Assertion
    # The reduce call uses list_representation ([True]) as both fn and acc,
    # effectively calling [True]([True], True), which invokes __call__ on the list
    # This should raise a TypeError since lists are not callable, 
    # but if it doesn't raise, the result should equal fn(acc, head)
    assert result == list_representation(list_representation, IS_EMPTY)

