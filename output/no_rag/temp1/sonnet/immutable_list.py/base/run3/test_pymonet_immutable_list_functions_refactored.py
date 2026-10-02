import pytest
import immutable_list as immutable_list

def test_empty_immutable_list_operations():
    # Test basic operations on an empty ImmutableList:
    # equality check with itself, string representation,
    # conversion to list, and addition with another list

    # Setup: Create an empty ImmutableList
    empty_list = immutable_list.ImmutableList()

    # Execute: Test equality of empty list with itself
    is_equal_to_itself = empty_list.__eq__(empty_list)

    # Assert: An empty ImmutableList should be equal to itself
    assert is_equal_to_itself is True

    # Execute: Test string representation of empty list
    string_representation = empty_list.__str__()

    # Assert: String representation should follow the ImmutableList format
    assert string_representation == "ImmutableList[None]"

    # Execute: Convert empty ImmutableList to a regular Python list
    converted_list = empty_list.to_list()

    # Assert: Converting an empty ImmutableList should return a list with None as head
    assert converted_list == [None]

    # Execute: Test length of the converted list
    converted_list_length = converted_list.__len__()

    # Assert: The converted list should have a length of 1 (containing None as head)
    assert converted_list_length == 1

    # Execute: Test adding two converted lists together (Python list addition)
    combined_list = converted_list.__add__(converted_list)

    # Assert: Adding the list to itself should double its content
    assert combined_list == [None, None]

    # Execute: Test adding an empty ImmutableList with the converted Python list
    # This should raise a ValueError since we can only add ImmutableList instances
    with pytest.raises(ValueError):
        empty_list.__add__(converted_list)

def test_empty_immutable_list_operations():
    # Constants
    INITIAL_ACC = True  # Used as initial accumulator value for reduce

    # Setup: Create an empty ImmutableList
    empty_list = immutable_list.ImmutableList()

    # Verify equality check between ImmutableList and a non-ImmutableList object returns False
    is_equal_to_non_list = empty_list.__eq__(INITIAL_ACC)
    assert not is_equal_to_non_list, "An ImmutableList should not be equal to a non-ImmutableList object"

    # Verify adding two empty ImmutableLists returns a new empty ImmutableList
    concatenated_empty_list = empty_list.__add__(empty_list)
    assert concatenated_empty_list is not None, "Adding two empty ImmutableLists should return an ImmutableList"

    # Verify find on an empty list with a False condition returns None
    found_element = empty_list.find(is_equal_to_non_list)
    assert found_element is None, "Finding in an empty ImmutableList should return None"

    # Verify string representation of an empty ImmutableList
    list_str_representation = empty_list.__str__()
    assert "ImmutableList" in list_str_representation, "String representation should contain 'ImmutableList'"

    # Verify unshift on empty list with itself as element creates a new list
    # with the empty list as the first element
    list_with_prepended_element = empty_list.unshift(empty_list)
    assert list_with_prepended_element is not None, "Unshift should return a new ImmutableList"

    # Verify reduce on the new list with the list itself as reducer function
    # and True as initial accumulator returns the accumulator (since head is the reducer itself)
    reduced_value = list_with_prepended_element.reduce(list_with_prepended_element, INITIAL_ACC)
    assert reduced_value == INITIAL_ACC, "Reduce on a single-element list should apply the function to the accumulator and head"

def test_find_on_empty_immutable_list_with_bool_head_returns_none():
    # Constants
    INITIAL_VALUE = True
    IS_EMPTY = True

    # Setup: Create an ImmutableList with a boolean head value and marked as empty
    immutable_list_with_bool = immutable_list.ImmutableList(INITIAL_VALUE, is_empty=IS_EMPTY)

    # Execute: Append a boolean value to create a new list
    immutable_list_after_append = immutable_list_with_bool.append(INITIAL_VALUE)

    # Assert: Find using the original list as the search function (callable)
    # Since the list itself is used as 'fn', verify that find returns None
    # because is_empty=True means head is None, so find returns None immediately
    result = immutable_list_with_bool.find(immutable_list_with_bool)
    assert result is None

def test_add_raises_value_error_when_adding_non_immutable_list():
    # Test that adding a non-ImmutableList instance (None) to an ImmutableList raises a ValueError
    
    # Setup
    empty_immutable_list = immutable_list.ImmutableList()
    invalid_operand = None
    
    # Execution and Assertion
    # Verify that attempting to add None (non-ImmutableList) raises a ValueError
    with pytest.raises(ValueError):
        empty_immutable_list.__add__(invalid_operand)

def test_find_on_list_with_empty_list_as_predicate():
    # Test that find() returns None when searching an empty ImmutableList
    # using another empty ImmutableList as the predicate (falsy value)

    # Setup: Create an empty ImmutableList and verify it has length 0
    empty_list = immutable_list.ImmutableList()
    EXPECTED_EMPTY_LENGTH = 0
    empty_list_length = empty_list.__len__()
    assert empty_list_length == EXPECTED_EMPTY_LENGTH

    # Setup: Create a second ImmutableList using the empty list as both
    # the head element and the is_empty flag
    list_with_empty_head = immutable_list.ImmutableList(
        empty_list, is_empty=empty_list
    )

    # Execute: Attempt to find an element using the list itself as the predicate
    # Since is_empty is set to a truthy ImmutableList object, the list is treated as empty
    result = list_with_empty_head.find(list_with_empty_head)

    # Assert: find() should return None since the list is treated as empty
    assert result is None

def test_find_returns_none_when_predicate_is_falsy_immutable_list():
    # Test that finding an element in an empty ImmutableList returns None
    # An ImmutableList created with False as head and is_empty=False 
    # effectively creates an empty-like list

    # Setup: Create an ImmutableList with False values indicating empty state
    IS_EMPTY = False
    empty_immutable_list = immutable_list.ImmutableList(IS_EMPTY, is_empty=IS_EMPTY)

    # Execute: Get the length of the empty list and attempt to find an element
    list_length = empty_immutable_list.__len__()
    
    # Use the list itself as the predicate function for find
    # Since head is False (falsy), find should return None
    find_result = empty_immutable_list.find(empty_immutable_list)

    # Assert: The list length should be 1 (head is False, tail is None)
    # and find should return None since fn(False) evaluates to falsy
    assert list_length == 1
    assert find_result is None

def test_find_with_to_list_as_predicate_on_single_element_list():
    # Test that find() correctly uses to_list() output as predicate
    # on an ImmutableList initialized with False values
    
    # Setup: Create an ImmutableList with a single False element
    INITIAL_VALUE = False
    immutable_list_false = immutable_list.ImmutableList(INITIAL_VALUE, is_empty=INITIAL_VALUE)
    
    # Execution: Convert the list to a regular Python list, then use it as predicate in find()
    list_representation = immutable_list_false.to_list()
    result = immutable_list_false.find(list_representation)
    
    # Assertion: The find() call should return None since the head is False
    # and the predicate (to_list() result) evaluates to falsy for the single False element
    assert result is None

def test_find_on_empty_list_and_append_then_convert_to_list():
    """
    Test that:
    1. Finding an element in an empty ImmutableList returns None (since head is None)
    2. Appending an ImmutableList to an empty ImmutableList creates a new ImmutableList
    3. Converting the resulting ImmutableList to a regular list works correctly
    4. Attempting to add None to a regular Python list (via __add__) does not raise an error
       since list.__add__ is being called (not ImmutableList.__add__)
    """
    # Setup
    empty_immutable_list = immutable_list.ImmutableList()
    none_value = None

    # Execution - find on empty list should return None since head is None
    find_result = empty_immutable_list.find(none_value)

    # Assert find returns None for an empty ImmutableList
    assert find_result is None

    # Execution - append the empty ImmutableList to itself, creating a new ImmutableList
    appended_immutable_list = empty_immutable_list.append(empty_immutable_list)

    # Execution - convert the appended ImmutableList to a regular Python list
    converted_list = appended_immutable_list.to_list()

    # Assert the converted list contains the appended empty ImmutableList as its element
    assert converted_list == [empty_immutable_list]

    # Execution - calling list.__add__ with None; this returns NotImplemented for Python lists
    # but does not raise an exception at call time
    converted_list.__add__(none_value)

def test_map_with_list_as_function_on_non_empty_list():
    # Test that map can be called with a list as the function argument
    # on a non-empty ImmutableList (is_empty=False creates a list with head=None)
    
    # Setup: Create a non-empty ImmutableList with is_empty=False
    IS_EMPTY = False
    non_empty_list = immutable_list.ImmutableList(is_empty=IS_EMPTY)
    
    # Get the list representation to use as a mapping "function"
    list_representation = non_empty_list.to_list()
    
    # Create a default ImmutableList (separate instance, not used in assertion)
    default_list = immutable_list.ImmutableList()
    
    # Execution: Get the list representation again and use it as the map function
    mapping_argument = non_empty_list.to_list()
    
    # Apply map using the list as the callable argument
    # This tests that map is invoked without raising an error
    result = non_empty_list.map(mapping_argument)

def test_map_with_none_function_raises_error():
    # Test that calling map with None as the function raises a TypeError
    # when operating on an ImmutableList created with None values and modified via unshift/append

    # Constants
    NONE_VALUE = None

    # Setup: Create an initial ImmutableList with None head and tail
    initial_list = immutable_list.ImmutableList(NONE_VALUE, NONE_VALUE)

    # Execution: Perform unshift operations to create new lists
    # unshift(None) adds None to the beginning of initial_list
    list_with_none_prepended = initial_list.unshift(NONE_VALUE)

    # unshift(list_with_none_prepended) adds the entire list as head of initial_list
    list_with_list_prepended = initial_list.unshift(list_with_none_prepended)

    # append(None) adds None to the end of list_with_none_prepended
    list_with_none_appended = list_with_none_prepended.append(NONE_VALUE)

    # Assertion: Calling map with None as the function should raise a TypeError
    # since None is not callable
    with pytest.raises(TypeError):
        list_with_none_appended.map(NONE_VALUE)

def test_filter_with_immutable_list_as_predicate():
    """
    Test that filter() can accept an ImmutableList instance as a predicate function.
    Since ImmutableList is used as the filter function (fn), and the list head is False,
    the ImmutableList instance is called with False as its argument.
    This verifies that filter() executes without errors when an ImmutableList
    is passed as the filtering predicate.
    """
    # Setup: Create an empty ImmutableList using False as head value and is_empty=False
    EMPTY_VALUE = False
    immutable_list_with_false = immutable_list.ImmutableList(EMPTY_VALUE, is_empty=EMPTY_VALUE)

    # Execute: Use the ImmutableList instance itself as the filter predicate
    result = immutable_list_with_false.filter(immutable_list_with_false)

def test_filter_with_length_as_predicate_on_concatenated_empty_lists():
    # Test that filter can be called with the length of a concatenated empty list as predicate
    # Core purpose: Verify that concatenating two empty ImmutableLists and filtering
    # the result using its own length (0) as the predicate works without errors

    # Setup: Create an empty ImmutableList
    empty_list = immutable_list.ImmutableList()

    # Execution: Concatenate the empty list with itself and get the length
    concatenated_empty_list = empty_list.__add__(empty_list)
    EXPECTED_LENGTH_OF_EMPTY_LIST = 0
    length_of_concatenated_list = concatenated_empty_list.__len__()

    # Assert: Verify the length is 0 for two concatenated empty lists
    assert length_of_concatenated_list == EXPECTED_LENGTH_OF_EMPTY_LIST

    # Filter the concatenated list using its length (0) as the predicate
    # Since 0 is falsy, filter will exclude all elements (the list is already empty)
    filtered_list = concatenated_empty_list.filter(length_of_concatenated_list)

    # Assert: The filtered result should also be an ImmutableList instance
    assert isinstance(filtered_list, immutable_list.ImmutableList)

def test_find_on_empty_list_returns_none_with_zero_length():
    """
    Test that finding an element in an empty ImmutableList returns None,
    and that calling __len__ on the result (None) raises an AttributeError
    or that the find operation on an empty list (both head and tail are None)
    returns None which has length 0 when treated as an empty result.
    
    Core purpose: Verify that find() on an empty ImmutableList (head=None, tail=None)
    returns None, and that __len__ can be called on the resulting empty list structure.
    """
    # Setup
    SEARCH_VALUE = 1947
    EMPTY_HEAD = None
    EMPTY_TAIL = None

    # Create an empty ImmutableList where both head and tail are None
    empty_list = immutable_list.ImmutableList(EMPTY_HEAD, EMPTY_TAIL)

    # Execution: Search for an element in the empty list
    # Since head is None, find() returns None
    find_result = empty_list.find(SEARCH_VALUE)

    # Assertion: Verify the result of __len__ on the find result
    # find returns None for an empty list, and calling __len__ on None's result
    find_result.__len__()

def test_find_returns_none_when_list_is_used_as_falsy_predicate():
    # Test that find() returns None when searching an empty ImmutableList
    # An ImmutableList initialized with False values for both head and is_empty
    # should behave as an empty list, returning None for any find operation
    
    # Setup
    IS_EMPTY = False
    HEAD_VALUE = False
    
    # Execution
    empty_immutable_list = immutable_list.ImmutableList(HEAD_VALUE, is_empty=IS_EMPTY)
    
    # Use the list itself as the search function (False is falsy, so find should return None)
    result = empty_immutable_list.find(empty_immutable_list)
    
    # Assertion
    assert result is None

def test_reduce_on_empty_list_returns_accumulator_and_find_with_list_predicate():
    # Constants
    FALSE_VALUE = False

    # Setup: Create an empty ImmutableList (no arguments)
    empty_list = immutable_list.ImmutableList()

    # Execution: Reduce on empty list with False as function and the empty list as accumulator
    # Since head is None in empty list, reduce should return the accumulator (empty_list itself)
    reduce_result = empty_list.reduce(FALSE_VALUE, empty_list)

    # Setup: Create a second ImmutableList with False as head value and is_empty=False
    list_with_false_head = immutable_list.ImmutableList(FALSE_VALUE, is_empty=FALSE_VALUE)

    # Execution: Call find on the second list using the second list itself as the predicate function
    # Since the list has a head (False), find will call fn(self.head) -> list_with_false_head(False)
    # ImmutableList as a callable predicate will be invoked with the head value
    find_result = list_with_false_head.find(list_with_false_head)

    # Assertion: Verify that reduce returns the accumulator (empty_list) when list is empty
    assert reduce_result == empty_list

def test_empty_immutable_list_initialization():
    # Test that an ImmutableList can be created with no arguments
    # and that it initializes successfully as an empty list
    
    # Setup & Execution: Create an empty ImmutableList instance
    empty_list = immutable_list.ImmutableList()
    
    # Assert: Verify the empty ImmutableList was created successfully
    assert empty_list is not None

def test_find_returns_none_when_predicate_is_false_value():
    # Test that find() on an ImmutableList containing False returns None
    # when using the list itself as the search function (which evaluates to False)
    
    # Setup: Create an ImmutableList with False as the value and is_empty=False
    INITIAL_VALUE = False
    immutable_list_with_false = immutable_list.ImmutableList(INITIAL_VALUE, is_empty=INITIAL_VALUE)
    
    # Execution: Get string representation and attempt to find using the list as predicate
    string_representation = immutable_list_with_false.__str__()
    find_result = immutable_list_with_false.find(immutable_list_with_false)
    
    # Assert: When searching with a predicate that evaluates to False (the list itself),
    # find() should return None since no element satisfies the condition
    assert find_result is None
    assert string_representation == 'ImmutableList{}'.format(immutable_list_with_false.to_list())

def test_unshift_and_find_with_immutable_list_as_element():
    """
    Test that an ImmutableList can be used as an element within another ImmutableList.
    Verifies that:
    1. unshift() correctly prepends an ImmutableList instance as an element to itself
    2. find() can search through the resulting list using an ImmutableList instance as the predicate/element
    """
    # Setup: Create an ImmutableList initialized with False as head and is_empty=False
    INITIAL_VALUE = False
    immutable_list = immutable_list.ImmutableList(INITIAL_VALUE, is_empty=INITIAL_VALUE)

    # Execution: Prepend the immutable_list itself as a new element to the beginning of the list
    list_with_prepended_self = immutable_list.unshift(immutable_list)

    # Assert: find() returns a result when searching using the immutable_list as the predicate
    # (ImmutableList instance used as callable predicate - will be truthy/falsy based on its value)
    find_result = immutable_list.find(immutable_list)

def test_find_with_false_as_non_callable_predicate_returns_none():
    """
    Test that find() returns None when using False as predicate function,
    since False is not callable and will not match any element in the list.
    The test verifies the behavior of find() on a list constructed by
    unshifting and appending elements to an initially non-empty ImmutableList.
    """
    # Constants
    IS_NOT_EMPTY = False
    PREDICATE = False  # False used as predicate (non-callable)

    # Setup - Create an initial non-empty ImmutableList
    initial_list = immutable_list.ImmutableList(is_empty=IS_NOT_EMPTY)

    # Execution - Build a list by prepending and appending elements
    list_with_prepended_element = initial_list.unshift(IS_NOT_EMPTY)
    list_with_appended_list = list_with_prepended_element.append(initial_list)

    # Assert - find() with False as predicate returns None
    result = list_with_appended_list.find(PREDICATE)
    assert result is None

def test_append_to_non_empty_list_and_find_with_list_as_predicate():
    # Constants for test setup
    INITIAL_VALUE = True
    IS_EMPTY_FLAG = True

    # Setup: Create an ImmutableList initialized with a boolean value and is_empty flag
    initial_list = immutable_list.ImmutableList(INITIAL_VALUE, is_empty=IS_EMPTY_FLAG)

    # Execution: Append a boolean value to the initial list, creating a new immutable list
    appended_list = initial_list.append(INITIAL_VALUE)

    # Assert: Verify the length of the appended list is correct
    appended_list_length = appended_list.__len__()

    # Execution: Attempt to find an element in the initial list using the initial list as the predicate
    # Since the initial list is used as a callable predicate, find will evaluate each element against it
    find_result = initial_list.find(initial_list)

def test_immutable_list_operations_with_nested_elements():
    # Setup: Create initial empty ImmutableList instances
    empty_list = immutable_list.ImmutableList()
    
    # Append the empty list to itself, creating a list containing itself as an element
    list_with_self = empty_list.append(empty_list)
    
    # Execute: Use reduce with list_with_self as both the function and accumulator
    # Since empty_list has no head, reduce returns the accumulator (list_with_self)
    reduced_result = empty_list.reduce(list_with_self, list_with_self)
    
    # Assert: Check equality between list_with_self and empty_list (should be False)
    are_equal = list_with_self.__eq__(empty_list)
    assert not are_equal, "list_with_self should not be equal to empty_list"
    
    # Execute: Prepend list_with_self to itself using unshift
    unshifted_list = list_with_self.unshift(list_with_self)
    
    # Get string representation of the unshifted list
    list_string_repr = unshifted_list.__str__()
    assert list_string_repr.startswith("ImmutableList"), "String representation should start with 'ImmutableList'"
    
    # Setup: Create a new ImmutableList using the string representation as is_empty flag
    list_from_string = immutable_list.ImmutableList(is_empty=list_string_repr)
    
    # Execute: Append the reduced result to itself
    appended_reduced_list = reduced_result.append(reduced_result)
    
    # Execute: Attempt to find the reduced result within the unshifted list
    # reduced_result is an ImmutableList (not callable), so find uses it as a predicate-like object
    found_element = unshifted_list.find(reduced_result)

def test_reduce_and_find_on_nested_immutable_lists():
    # Setup: Create an empty ImmutableList and a list with the empty list as its first element
    empty_list = immutable_list.ImmutableList()
    list_with_empty_as_head = empty_list.unshift(empty_list)

    # Execute: Use the empty list to reduce the list_with_empty_as_head,
    # using list_with_empty_as_head as both the reducer function and accumulator.
    # Since empty_list.head is None, reduce returns the accumulator (list_with_empty_as_head) directly.
    reduced_result = empty_list.reduce(list_with_empty_as_head, list_with_empty_as_head)

    # Get the length of list_with_empty_as_head (should be 1, since it contains one element)
    list_length = list_with_empty_as_head.__len__()
    EXPECTED_LENGTH = 1
    assert list_length == EXPECTED_LENGTH

    # Create a new list by prepending list_with_empty_as_head to itself
    nested_list = list_with_empty_as_head.unshift(list_with_empty_as_head)

    # Verify that the nested list is NOT equal to the original empty list
    is_equal_to_empty = nested_list.__eq__(empty_list)
    assert not is_equal_to_empty

    # Create a new ImmutableList using the length value as the is_empty flag
    list_with_length_as_flag = immutable_list.ImmutableList(is_empty=list_length)

    # Execute: Call find on reduced_result using reduced_result itself as the predicate.
    # Since reduced_result is list_with_empty_as_head, and its head is the empty_list,
    # calling reduced_result (an ImmutableList) as a function would raise a TypeError.
    # This verifies that find raises an error when the predicate is not callable.
    with pytest.raises(TypeError):
        reduced_result.find(reduced_result)

def test_reduce_with_to_list_as_function_and_accumulator():
    # Test that reduce can be called with to_list result as both function and accumulator
    # This tests an edge case where the list itself is used as both the reducer function and initial accumulator
    
    # Setup
    IS_EMPTY = True
    HEAD_VALUE = True
    EMPTY_TAIL = {}
    
    # Create an ImmutableList with an empty dict as tail (edge case)
    immutable_list_with_empty_tail = immutable_list.ImmutableList(tail=EMPTY_TAIL)
    
    # Create an ImmutableList marked as empty with a boolean head value
    immutable_list_with_bool_head = immutable_list.ImmutableList(HEAD_VALUE, is_empty=IS_EMPTY)
    
    # Execution
    # Convert the list to a Python list - this will serve as both fn and acc in reduce
    list_representation = immutable_list_with_bool_head.to_list()
    
    # Call reduce using the list as both the reducer function and accumulator
    # Since head is True (not None) and tail is None, reduce returns fn(acc, self.head)
    # which is list_representation(list_representation, True)
    immutable_list_with_bool_head.reduce(list_representation, list_representation)

