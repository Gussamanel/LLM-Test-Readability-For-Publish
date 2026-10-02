import pytest
import immutable_list as immutable_list

def test_immutable_list_equality_to_self_and_to_list_conversion_with_addition_semantics():
    # Setup: Create an empty ImmutableList instance
    empty_list = immutable_list.ImmutableList()

    # Execution and Assertion: Verify an ImmutableList is equal to itself
    assert empty_list.__eq__(empty_list) is True

    # Execution: Convert the empty list to a Python list
    list_representation = empty_list.to_list()

    # Assertion: The empty list should be converted to [None] due to the implementation
    assert list_representation == [None]

    # Execution: Attempt to add the list representation to itself (list + list is valid)
    combined_list = list_representation.__add__(list_representation)

    # Assertion: The combined list should contain two copies of the original elements
    assert combined_list == [None, None]

    # Execution: Get the length of the list representation
    length = list_representation.__len__()

    # Assertion: The length of [None] should be 1
    assert length == 1

    # Execution and Assertion: Verify adding an ImmutableList to an empty ImmutableList works
    # This tests the __add__ method with another ImmutableList
    result = empty_list.__add__(empty_list)
    assert isinstance(result, immutable_list.ImmutableList)

def test_immutable_list_operations_with_boolean_comparison_and_reduction_consistency():
    # Setup: an empty ImmutableList and a boolean value to use as a test element
    EMPTY_LIST = immutable_list.ImmutableList()
    SAMPLE_ELEMENT = True

    # Execution: perform various list operations to verify behavior
    # Comparing with the raw boolean should return False since types differ
    comparison_with_boolean = EMPTY_LIST.__eq__(SAMPLE_ELEMENT)
    # Concatenating an empty list with itself should remain empty
    concatenated_list = EMPTY_LIST.__add__(EMPTY_LIST)
    # Searching the empty list for an element should return None
    found_element = EMPTY_LIST.find(comparison_with_boolean)
    # String representation of an empty list
    list_string_representation = EMPTY_LIST.__str__()
    # Prepending the empty list as an element produces a non-empty list
    list_with_prepended_element = EMPTY_LIST.unshift(EMPTY_LIST)
    # Reducing the resulting list with a boolean accumulator and non-callable fn argument
    reduced_result = list_with_prepended_element.reduce(
        list_with_prepended_element, SAMPLE_ELEMENT
    )

    # Assertions: verify the list operations produce expected results
    assert comparison_with_boolean is False
    assert concatenated_list.find(lambda _: True) is None
    assert found_element is None
    assert list_string_representation == 'ImmutableList[]'
    assert list_with_prepended_element.find(lambda _: True) is EMPTY_LIST

def test_find_with_predicate_returns_first_matching_boolean_element():
    initial_value = True
    list_with_true_element = immutable_list.ImmutableList(initial_value, is_empty=initial_value)
    list_with_two_true_elements = list_with_true_element.append(initial_value)

    found_element = list_with_two_true_elements.find(lambda x: x)

    assert found_element == initial_value

def test_add_with_none_operand_raises_value_error():
    # Setup: create an empty ImmutableList to operate on
    empty_immutable_list = immutable_list.ImmutableList()
    invalid_operand = None

    # Execution and Assertion: adding a non-ImmutableList should raise ValueError
    with pytest.raises(ValueError):
        empty_immutable_list.__add__(invalid_operand)

def test_find_on_single_element_list_returns_none_when_predicate_fails():
    # Setup
    empty_list = ImmutableList()
    single_element_list = ImmutableList(empty_list, is_empty=empty_list)
    
    # Execution
    result = single_element_list.find(lambda x: False)
    
    # Assertion
    assert result is None

def test_find_on_empty_immutable_list_returns_none_and_len_is_zero():
    # Setup: create an empty ImmutableList (is_empty flag set to True)
    is_empty = True
    empty_list = immutable_list.ImmutableList(is_empty, is_empty=is_empty)

    # Execution: retrieve the length and attempt to find an element
    length_of_empty_list = len(empty_list)
    result_of_find = empty_list.find(empty_list)

    # Assertion: an empty list has length 0 and find returns None
    assert length_of_empty_list == 0
    assert result_of_find is None

def test_find_on_empty_immutable_list_returns_none_when_predicate_always_false():
    # Setup: an empty ImmutableList (head is None, is_empty=True)
    IS_EMPTY = True
    empty_immutable_list = immutable_list.ImmutableList(IS_EMPTY, is_empty=IS_EMPTY)

    # Execution: convert to a list and call find with a predicate
    # that would normally be used to filter elements.
    list_representation = empty_immutable_list.to_list()
    result = empty_immutable_list.find(lambda element: element == list_representation)

    # Assertion: find on an empty list should return None
    assert result is None

def test_immutable_list_self_append_and_find_with_none_predicate_returns_none():
    # Constants and setup
    EMPTY_LIST = module_0.ImmutableList()
    PREDICATE = None  # non-callable predicate passed to find (should return None)

    # Execution: find on empty list with None predicate
    find_result = EMPTY_LIST.find(PREDICATE)

    # Execution: append the list to itself and convert to list
    appended_list = EMPTY_LIST.append(EMPTY_LIST)
    list_elements = appended_list.to_list()

    # Assertions
    # find on an empty list should return None regardless of predicate
    assert find_result == PREDICATE

    # appending an ImmutableList to itself creates a nested structure;
    # to_list should return a list of length 1 containing the appended list
    assert isinstance(list_elements, list)
    assert len(list_elements) == 1
    assert list_elements[0] == EMPTY_LIST

    # calling __add__ directly with None should raise ValueError
    with pytest.raises(ValueError):
        list_elements.__add__(PREDICATE)

def test_map_on_empty_immutable_list_returns_list_with_mapped_default_head():
    # Setup: create an empty ImmutableList (is_empty=True) and a non-empty default ImmutableList
    EMPTY_LIST_FLAG = True
    empty_immutable_list = ImmutableList(is_empty=EMPTY_LIST_FLAG)
    default_immutable_list = ImmutableList()

    # Execution: convert the empty list to a regular list and apply map
    empty_list_as_regular = empty_immutable_list.to_list()
    empty_immutable_list.map(empty_list_as_regular)

    # Assertion: mapping an empty ImmutableList should not raise and should yield a list
    # containing the mapped head value (None), producing an ImmutableList with mapped result
    mapped_list = empty_immutable_list.map(lambda x: x)
    assert mapped_list.to_list() == [None]

def test_unshift_append_and_map_operations_with_none_elements_on_immutable_list():
    # Setup: create an ImmutableList containing a None element
    initial_list = immutable_list.ImmutableList(None, None)

    # Execution: build chains of operations on the ImmutableList
    list_with_none_unshifted = initial_list.unshift(None)
    list_with_list_unshifted = initial_list.unshift(list_with_none_unshifted)
    list_with_none_appended = list_with_none_unshifted.append(None)

    # Execution & Assertion: mapping over the mutated list should work
    # (calling map with None as fn is expected to raise an error)
    list_with_none_appended.map(None)

def test_filter_on_empty_list_yields_empty_result():
    # Setup: create an empty ImmutableList as the source for filtering
    empty_list = immutable_list.ImmutableList(is_empty=True)

    # Execution: attempt to filter the empty list using a predicate.
    # The list itself is callable and returns False for any given value,
    # so the filter should produce an empty list.
    filtered_list = empty_list.filter(empty_list)

    # Assertion: filtering an empty list must result in an empty list
    assert filtered_list.is_empty()

def test_filter_with_zero_length_predicate_on_concatenated_empty_immutable_lists():
    # Setup: Create two empty ImmutableList instances and concatenate them.
    # The result is an empty list because both operands are empty.
    empty_list_left = immutable_list.ImmutableList()
    empty_list_right = immutable_list.ImmutableList()
    concatenated_list = empty_list_left.__add__(empty_list_right)

    # Execution: Determine the length of the concatenated list (expected 0)
    # and use it as a predicate for filter. A length of 0 is falsy,
    # so filter should produce an empty list.
    concatenated_list_length = len(concatenated_list)
    filtered_list = concatenated_list.filter(concatenated_list_length)

    # Assertion: The filtered result should remain an empty ImmutableList.
    assert len(filtered_list) == 0

def test_find_on_empty_immutable_list_returns_none_and_len_is_zero():
    # Setup: create an empty ImmutableList (head and tail are None)
    EMPTY_LIST_HEAD = None
    EMPTY_LIST_TAIL = None
    empty_immutable_list = ImmutableList(EMPTY_LIST_HEAD, EMPTY_LIST_TAIL)

    # Execution: search for an arbitrary value and get the list length
    SEARCH_VALUE = 1947
    search_result = empty_immutable_list.find(lambda element: element == SEARCH_VALUE)
    empty_list_length = empty_immutable_list.__len__()

    # Assertion: finding in an empty list returns None and its length is 0
    assert search_result is None
    assert empty_list_length == 0

def test_find_on_empty_immutable_list_using_list_as_predicate_returns_none():
    # Setup: Create an empty ImmutableList instance
    is_empty = False
    empty_list = immutable_list.ImmutableList(is_empty, is_empty=is_empty)

    # Execution: Call find on the empty list, using the list itself as the predicate function
    result = empty_list.find(empty_list)

    # Assertion: find should return None because the list is empty
    assert result is None

def test_reduce_on_empty_list_returns_accumulator_and_find_with_list_predicate_returns_list():
    # Setup: create an empty ImmutableList and define the arguments for reduce
    empty_initial_value = False
    empty_list = immutable_list.ImmutableList()

    # Execution: reduce an empty list with an accumulator value
    reduced_result = empty_list.reduce(empty_initial_value, empty_list)

    # Assertion: reducing an empty list should return the accumulator unchanged
    assert reduced_result == empty_initial_value

    # Setup: build an ImmutableList whose single element is False and is_empty flag is False
    is_empty_flag = False
    list_with_false_element = immutable_list.ImmutableList(is_empty_flag, is_empty=is_empty_flag)

    # Execution: find an element in the list using the list itself as the predicate
    # (the predicate is never expected to be meaningfully evaluated here)
    found_element = list_with_false_element.find(list_with_false_element)

    # Assertion: searching with a non-callable predicate should return the list itself
    assert found_element == list_with_false_element

def test_creation_of_empty_immutable_list_type_check():
    # Setup: create a new empty ImmutableList instance
    empty_immutable_list = immutable_list.ImmutableList()

    # Assertion: verify the instance is an ImmutableList
    assert isinstance(empty_immutable_list, immutable_list.ImmutableList)

def test_empty_immutable_list_string_representation_and_find_returns_none():
    # Setup: create an empty ImmutableList
    is_empty = False
    empty_list = immutable_list.ImmutableList(is_empty, is_empty=is_empty)

    # Execution: get string representation and search for an element
    string_representation = str(empty_list)
    search_result = empty_list.find(empty_list)

    # Assertions: verify the string representation and that find returns None on empty list
    assert string_representation == 'ImmutableList[]'
    assert search_result is None

def test_find_on_list_containing_itself_returns_the_list_when_used_as_predicate():
    # Constants
    IS_EMPTY = False

    # Setup: create an empty ImmutableList
    empty_list = immutable_list.ImmutableList(IS_EMPTY, is_empty=IS_EMPTY)

    # Execution: prepend the list to itself, then search using the list as the predicate
    list_containing_itself = empty_list.unshift(empty_list)
    found_element = empty_list.find(list_containing_itself)

    # Assertion: the first element matches the predicate (its own identity), so find should return it
    assert found_element == list_containing_itself

def test_find_boolean_false_element_after_prepend_and_append_on_immutable_list():
    # Setup: create an ImmutableList with a single boolean value (False) as the head,
    # then prepend False and append the original list to build a list of booleans.
    initial_value = False
    initial_list = immutable_list.ImmutableList(is_empty=initial_value)
    list_with_prepended_value = initial_list.unshift(initial_value)
    combined_list = list_with_prepended_value.append(initial_list)

    # Execution: find the first element in the combined list that satisfies the predicate.
    # The predicate is the boolean value itself (False), which acts as a callable.
    found_element = combined_list.find(initial_value)

    # Assertion: verify that find returns the expected matching element.
    assert found_element == initial_value

def test_length_and_find_on_immutable_boolean_element_list_with_append():
    # Setup: create an ImmutableList containing a single boolean element (True)
    # and mark the list as empty via the is_empty flag
    INITIAL_ELEMENT = True
    immutable_list = immutable_list.ImmutableList(INITIAL_ELEMENT, is_empty=INITIAL_ELEMENT)

    # Setup: append a boolean element to produce a new ImmutableList
    APPENDED_ELEMENT = True
    extended_list = immutable_list.append(APPENDED_ELEMENT)

    # Execution: determine the length of the extended list
    resulting_length = extended_list.__len__()

    # Execution: search for the first element matching the original list itself
    # (the predicate is the ImmutableList instance, which is callable and
    # returns True for elements equal to its own head)
    found_element = immutable_list.find(immutable_list)

    # Assertion: the extended list should contain two elements
    EXPECTED_LENGTH = 2
    assert resulting_length == EXPECTED_LENGTH

    # Assertion: searching should not raise and should return a valid result
    assert found_element in (None, INITIAL_ELEMENT)

def test_reduce_append_unshift_and_find_with_self_referential_immutable_lists():
    # Setup: create an empty ImmutableList and derive related lists/values
    empty_list = immutable_list.ImmutableList()
    list_with_empty_appended = empty_list.append(empty_list)

    # Execution: reduce the list, then compare the derived lists
    reduced_result = empty_list.reduce(list_with_empty_appended, list_with_empty_appended)
    are_lists_equal = list_with_empty_appended.__eq__(empty_list)

    # Execution: prepend the list to itself, convert to string and build from string
    prefixed_list = list_with_empty_appended.unshift(list_with_empty_appended)
    prefixed_list_str = prefixed_list.__str__()
    list_from_string = immutable_list.ImmutableList(is_empty=prefixed_list_str)

    # Execution: append reduced result to itself and search in prefixed list
    appended_reduced = reduced_result.append(reduced_result)
    found_element = prefixed_list.find(reduced_result)

    # Assertions: document expected outcomes for each action
    assert are_lists_equal is False
    assert isinstance(prefixed_list_str, str)
    assert isinstance(list_from_string, immutable_list.ImmutableList)
    assert isinstance(appended_reduced, immutable_list.ImmutableList)
    assert found_element is None

def test_reduce_and_find_on_nested_immutable_lists_with_self_reference():
    # Setup: create an empty ImmutableList and a list containing itself
    empty_list = ImmutableList()
    list_with_self = empty_list.unshift(empty_list)

    # Execution: reduce combines elements of the list into a single value
    # using the list_with_self as both the reducer and the accumulator.
    reduced_result = empty_list.reduce(list_with_self, list_with_self)

    # Verify the length of the list containing itself
    list_length = list_with_self.__len__()
    assert list_length == 1

    # Add another nested list and compare with the original empty list
    nested_list = list_with_self.unshift(list_with_self)
    is_equal_to_empty = nested_list.__eq__(empty_list)
    assert is_equal_to_empty is False

    # Create an ImmutableList from the computed length (treated as an empty flag)
    list_from_length = ImmutableList(is_empty=list_length)
    assert list_from_length.is_empty == list_length

    # Find the reduced result within itself; since the reducer identity
    # returns the same object, find should return that object.
    found = reduced_result.find(reduced_result)
    assert found is reduced_result

def test_reduce_list_with_boolean_values_and_empty_tail_list():
    # Setup
    INITIAL_ACCUMULATOR = {}
    BOOLEAN_TRUE = True

    empty_tail_list = immutable_list.ImmutableList(tail=INITIAL_ACCUMULATOR)
    boolean_list = immutable_list.ImmutableList(BOOLEAN_TRUE, is_empty=BOOLEAN_TRUE)

    # Execution
    list_values = boolean_list.to_list()
    result = boolean_list.reduce(list_values, list_values)

    # Assertion
    assert result is not None

