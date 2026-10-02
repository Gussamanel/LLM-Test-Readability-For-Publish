import pytest
import immutable_list as immutable_list_module

def test_immutable_list_equality_representation_and_concatenation_behavior():
    # Setup
    immutable_list = immutable_list_module.ImmutableList()
    
    # Assertion: An empty list should be equal to itself
    assert immutable_list == immutable_list
    
    # Assertion: String representation of an empty list
    assert str(immutable_list) == 'ImmutableList[]'
    
    # Execution: Convert to list and verify empty result
    empty_list = immutable_list.to_list()
    assert empty_list == []
    
    # Setup: Create a list with one element for concatenation tests
    single_element_list = immutable_list_module.ImmutableList()
    single_element_list = single_element_list.__add__(immutable_list_module.ImmutableList(5))
    
    # Execution: Concatenate a list with an empty list
    concatenated_list = single_element_list.__add__(immutable_list)
    
    # Assertion: Length of concatenated list should be 1
    assert concatenated_list.__len__() == 1
    
    # Execution: Concatenate with a list of multiple elements
    multi_element_list = immutable_list_module.ImmutableList(1, immutable_list_module.ImmutableList(2))
    result_list = single_element_list.__add__(multi_element_list)
    
    # Assertion: Length of result list should be 3
    assert result_list.__len__() == 3
    
    # Assertion: Verify the content of the result list
    assert result_list.to_list() == [5, 1, 2]

def test_immutable_list_empty_chain_operations_behavior():
    # Setup: create an empty ImmutableList and a non-list value for comparison
    expected_find_result = True
    empty_immutable_list = immutable_list_module.ImmutableList()

    # Execution & Verification of equality against a non-ImmutableList value
    # An ImmutableList should not be equal to a plain boolean
    is_equal_to_bool = empty_immutable_list.__eq__(expected_find_result)
    assert is_equal_to_bool is False

    # Execution: add an ImmutableList to itself
    # Concatenating two empty lists should still behave correctly without error
    concatenated_list = empty_immutable_list.__add__(empty_immutable_list)

    # Execution: find an element using the previous equality result as predicate value
    # Since the list is empty, find should return None regardless of the predicate
    found_element = empty_immutable_list.find(is_equal_to_bool)
    assert found_element is None

    # Execution: check the string representation of the empty list
    string_representation = empty_immutable_list.__str__()
    assert string_representation == 'ImmutableList[]'

    # Execution: prepend the (empty) list to itself
    # unshift should return a new ImmutableList without mutating the original
    unshifted_list = empty_immutable_list.unshift(empty_immutable_list)
    assert isinstance(unshifted_list, immutable_list_module.ImmutableList)

    # Execution: reduce over the unshifted list with the reducer returning the accumulator
    # The result should be the initial accumulator value
    reduced_result = unshifted_list.reduce(lambda acc, _: acc, expected_find_result)
    assert reduced_result is expected_find_result

def test_find_with_always_true_predicate_on_single_element_list():
    # Setup: create an ImmutableList containing a single True value
    is_true = True
    single_element_list = immutable_list_module.ImmutableList(is_true, is_empty=is_true)

    # Execution: append another element and find the first element matching the predicate
    list_with_appended_element = single_element_list.append(is_true)
    found_element = single_element_list.find(lambda x: True)

    # Assertion: the found element should be the head of the list (True)
    assert found_element == is_true

def test_add_non_immutable_list_raises_value_error_with_invalid_operand():
    # Setup
    empty_immutable_list = immutable_list_module.ImmutableList()
    invalid_operand = None  # Non-ImmutableList instance to trigger validation error

    # Execution & Assertion
    with pytest.raises(ValueError) as exc_info:
        empty_immutable_list.__add__(invalid_operand)

    # Verify the error message clearly indicates the invalid operand type
    assert str(exc_info.value) == (
        'ImmutableList: you can not add any other instace than ImmutableList'
    )

def test_find_on_empty_nested_immutable_list_returns_none():
    # Setup: create an empty ImmutableList with another empty ImmutableList as head
    empty_list = immutable_list_module.ImmutableList()
    FOUND_VALUE = None
    empty_head_list = immutable_list_module.ImmutableList(
        empty_list, is_empty=empty_list
    )

    # Execution: search for any element using a predicate that always returns True
    result = empty_head_list.find(lambda _element: True)

    # Assertion: an empty head yields no found element
    assert result == FOUND_VALUE

def test_find_on_empty_immutable_list_with_empty_flag_returns_none():
    # Setup: create an empty ImmutableList by passing an empty flag
    IS_EMPTY = True
    empty_list = immutable_list_module.ImmutableList(IS_EMPTY, is_empty=IS_EMPTY)

    # Execution: compute the length of the empty list and attempt a find
    list_length = empty_list.__len__()
    find_result = empty_list.find(empty_list)

    # Assertion: an empty list has length 0 and find should return None
    assert list_length == 0
    assert find_result is None

def test_find_on_empty_lists_returns_none():
    is_empty = True
    empty_list = immutable_list_module.ImmutableList(is_empty, is_empty=is_empty)
    expected_result = None

    elements = empty_list.to_list()
    result = empty_list.find(elements)

    assert result == expected_result

def test_find_with_none_predicate_on_appended_empty_list_returns_none():
    # Constants
    EMPTY_LIST_HEAD = None
    expected_find_result = None

    # Setup: create an empty ImmutableList and a None predicate
    empty_list = immutable_list_module.ImmutableList()

    # Execution: find with a None predicate on an empty list should return None
    find_result = empty_list.find(EMPTY_LIST_HEAD)

    # Execution: append the list to itself and convert the result to a Python list
    doubled_list = empty_list.append(empty_list)
    doubled_list_as_python_list = doubled_list.to_list()

    # Execution: attempt to add None to the resulting Python list via __add__
    doubled_list_as_python_list.__add__(EMPTY_LIST_HEAD)

    # Assertion: find on an empty list with any predicate returns None
    assert find_result == expected_find_result

def test_immutable_list_map_with_own_elements_preserves_contents():
    # Setup: create an immutable list with a single False value
    NON_EMPTY_LIST_VALUE = False
    immutable_list_with_false = immutable_list_module.ImmutableList(is_empty=NON_EMPTY_LIST_VALUE)

    # Extract the internal elements as a Python list to use as a mapping function argument
    list_elements = immutable_list_with_false.to_list()

    # Capture the original contents for comparison
    original_list_elements = immutable_list_with_false.to_list()

    # Execution: apply map using the extracted elements, effectively re-mapping the list with itself
    immutable_list_with_false.map(list_elements)

    # Assertion: verify the map operation produces a list equivalent to the original contents
    # (mapping a single-element list with itself yields the same element)
    assert immutable_list_with_false.to_list() == original_list_elements

def test_map_none_on_immutable_list_with_none_head_and_tail():
    # Setup: create an ImmutableList where both head and tail are None
    none_value = None
    immutable_list = immutable_list_module.ImmutableList(none_value, none_value)

    # Create a new ImmutableList by prepending none_value and another list
    unshifted_with_none = immutable_list.unshift(none_value)
    unshifted_with_list = immutable_list.unshift(unshifted_with_none)

    # Create a new ImmutableList by appending none_value to the unshifted list
    appended_list = unshifted_with_none.append(none_value)

    # Execution & Assertion: mapping None over the appended list should not raise an error
    result = appended_list.map(none_value)
    assert result is not None

def test_filter_on_single_false_element_list_returns_value_when_predicate_is_true():
    # Setup: create an ImmutableList with one element (False) and a predicate that always returns True
    element_value = False
    immutable_list = immutable_list_module.ImmutableList(element_value, is_empty=False)

    def predicate_always_true(_):
        return True

    # Execution: apply the filter with the always-true predicate
    filtered_list = immutable_list.filter(predicate_always_true)

    # Assertion: the original single element should be preserved in the filtered list
    assert filtered_list.head == element_value
    assert filtered_list.is_empty is False

def test_len_of_concatenated_empty_lists_is_zero():
    # Setup: create an empty ImmutableList and concatenate it with itself
    empty_list = immutable_list_module.ImmutableList()
    concatenated_list = empty_list.__add__(empty_list)

    # Execution: compute the length of the resulting list
    concatenated_length = concatenated_list.__len__()

    # Assertion: the length of two concatenated empty lists is zero
    assert concatenated_length == 0

    # Also ensures filter with a length-based predicate runs without error
    concatenated_list.filter(concatenated_length)

def test_find_on_empty_list_returns_none_and_zero_for_absent_value():
    # Setup: an ImmutableList constructed with both head and tail equal to None (empty list).
    EMPTY_HEAD = None
    EMPTY_TAIL = None
    SEARCH_VALUE = 1947
    empty_immutable_list = immutable_list_module.ImmutableList(EMPTY_HEAD, EMPTY_TAIL)

    # Execution: find a value that does not exist in the empty list.
    found_element = empty_immutable_list.find(SEARCH_VALUE)

    # Assertion: find returns None and the list length is 0.
    assert found_element is None
    assert found_element.__len__() == 0

def test_find_on_empty_immutable_list_using_self_as_predicate_returns_none():
    # Setup: create an empty ImmutableList instance
    is_empty = False
    empty_list = immutable_list_module.ImmutableList(is_empty, is_empty=is_empty)

    # Execution: call find with the empty list itself as the predicate function
    result = empty_list.find(empty_list)

    # Assertion: find on an empty list should return None
    assert result is None

def test_find_with_identity_predicate_on_single_false_element_returns_none():
    # Setup - Create an ImmutableList with a False value in the head
    initial_value = False
    immutable_list_with_false_value = immutable_list_module.ImmutableList(
        initial_value, is_empty=False
    )
    
    # Execution - Call find method with a function that returns the value itself
    result = immutable_list_with_false_value.find(
        lambda x: x  # Simple identity function that returns the input value
    )
    
    # Assertion - Verify that find returns None when the only element is False
    # (since False is falsy, the predicate function returns False)
    assert result is None

def test_immutable_list_constructed_with_no_arguments_is_instance():
    # Setup: create a new immutable list without providing any initial elements
    initial_elements = None

    # Execution: instantiate the immutable list with default construction
    immutable_list = immutable_list_module.ImmutableList() if initial_elements is None else immutable_list_module.ImmutableList(initial_elements)

    # Assertion: verify the immutable list object is created successfully
    assert isinstance(immutable_list, immutable_list_module.ImmutableList)

def test_find_on_empty_immutable_list_via_str_conversion_returns_none():
    # Setup: create an empty ImmutableList by passing False as the head value
    # and is_empty=True, so the list has no elements.
    EMPTY_HEAD_VALUE = False
    IS_EMPTY = True
    empty_list = immutable_list_module.ImmutableList(EMPTY_HEAD_VALUE, is_empty=IS_EMPTY)

    # Execution: convert the empty list to its string representation
    # and invoke find() with the list itself as the predicate.
    list_string_representation = empty_list.__str__()
    find_result = empty_list.find(empty_list)

    # Assertion: finding in an empty list should return None since there are no elements.
    assert find_result is None

def test_find_on_non_empty_list_with_itself_after_unshift_returns_self():
    # Setup: create an empty ImmutableList and unshift itself onto it
    # so the list becomes non-empty with one element (the list itself)
    is_empty = False
    empty_list = immutable_list_module.ImmutableList(is_empty, is_empty)

    # Execution: prepend the list to itself, then search for an element
    # using the list itself as the predicate function
    non_empty_list = empty_list.unshift(empty_list)
    found_element = empty_list.find(non_empty_list)

    # Assertion: verify the returned element is the inner list used as predicate
    assert found_element is empty_list

def test_find_with_false_as_predicate_raises_type_error():
    ELEMENT = False
    original_list = immutable_list_module.ImmutableList(is_empty=ELEMENT)
    list_with_unshifted_element = original_list.unshift(ELEMENT)
    combined_list = list_with_unshifted_element.append(original_list)
    combined_list.find(ELEMENT)

def test_append_true_to_single_element_true_list_increases_length_and_find_returns_none_for_list_input():
    # Setup: a single-element immutable list containing True
    element = True
    initial_list = immutable_list_module.ImmutableList(element, is_empty=True)

    # Execution: append True and query length, then find an element matching the original list
    appended_list = initial_list.append(element)
    appended_length = appended_list.__len__()
    found_element = initial_list.find(initial_list)

    # Assertion: appending increases length to 2 and find returns None (fn is not callable on a list)
    assert appended_length == 2
    assert found_element is None

def test_immutable_list_nested_operations_with_self_reduction():
    empty_list = immutable_list_module.ImmutableList()

    list_with_self = empty_list.append(empty_list)

    reduced_result = empty_list.reduce(list_with_self, list_with_self)

    is_equal = list_with_self.__eq__(empty_list)
    assert is_equal is False

    list_with_prepended_self = list_with_self.unshift(list_with_self)

    list_str = list_with_prepended_self.__str__()

    list_from_string = immutable_list_module.ImmutableList(is_empty=list_str)

    appended_reduced = reduced_result.append(reduced_result)

    list_with_prepended_self.find(reduced_result)

def test_unshift_self_reduce_and_find_truthy_element_in_nested_immutable_list():
    # Setup: create an empty ImmutableList and build nested lists via unshift.
    empty_list = immutable_list_module.ImmutableList()
    list_with_self_unshifted = empty_list.unshift(empty_list)

    # Execution: reduce using the unshifted list as both reducer and accumulator.
    reduced_result = empty_list.reduce(list_with_self_unshifted, list_with_self_unshifted)
    length_of_unshifted_list = list_with_self_unshifted.__len__()

    # Create another list by unshifting the previously built list onto itself.
    list_with_nested_unshift = list_with_self_unshifted.unshift(list_with_self_unshifted)
    # Execution: check equality between the doubly-nested list and the original empty list.
    is_equal_to_empty_list = list_with_nested_unshift.__eq__(empty_list)

    # Setup: create a new list using the length value (non-zero) as is_empty hint.
    list_from_length = immutable_list_module.ImmutableList(is_empty=length_of_unshifted_list)

    # Execution: find the first element satisfying the reducer itself as predicate.
    found_element = reduced_result.find(reduced_result)

    # Assertions: verify the structural and logical outcomes.
    assert length_of_unshifted_list == 1
    assert is_equal_to_empty_list is False
    assert found_element is not None

def test_reduce_on_list_from_empty_tail_with_flattened_self_as_elements():
    # Setup
    LIST_HEAD_VALUE = True
    EMPTY_TAIL = {}
    non_empty_list = immutable_list_module.ImmutableList(tail=EMPTY_TAIL)
    list_with_head_and_empty_flag = immutable_list_module.ImmutableList(
        LIST_HEAD_VALUE, is_empty=LIST_HEAD_VALUE
    )
    elements_as_list = list_with_head_and_empty_flag.to_list()

    # Execution
    result = non_empty_list.reduce(elements_as_list, elements_as_list)

    # Assertion
    assert result == elements_as_list

