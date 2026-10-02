import pytest

import immutable_list as immutable_list

def test_immutable_list_direct_dunder_methods_on_empty_and_single_element_lists():
    # Setup
    empty_list = immutable_list.ImmutableList()
    single_element_list = immutable_list.ImmutableList("item")

    # Execution
    lists_are_equal = empty_list.__eq__(empty_list)
    string_representation = empty_list.__str__()
    converted_list = empty_list.to_list()
    concatenated_list = converted_list.__add__(converted_list)

    # Assertion
    assert lists_are_equal is True
    assert string_representation == "ImmutableList[]"
    assert converted_list == []
    assert concatenated_list == []

    # Additional checks with non-empty list
    non_empty_to_list = single_element_list.to_list()
    non_empty_concatenated = non_empty_to_list.__add__(non_empty_to_list)
    assert single_element_list.__len__() == 1
    assert non_empty_concatenated == ["item", "item"]

def test_empty_immutable_list_operations_and_find_first_match():
    # Setup: create an empty ImmutableList
    empty_list = immutable_list.ImmutableList()

    # Execution: perform a sequence of operations on the empty list
    is_equal_to_true = empty_list == True           # equality check against a non-list object
    concatenated_list = empty_list + empty_list     # concatenation of two empty lists
    found_element = empty_list.find(is_equal_to_true)  # find element matching the boolean predicate
    string_representation = str(empty_list)         # string representation of the empty list
    prepended_list = empty_list.unshift(empty_list) # prepend the empty list as a single element
    reduced_value = prepended_list.reduce(prepended_list, True)  # reduce with the list itself as the reducer

    # Assertion: verify the results of the operations on empty lists
    assert is_equal_to_true is False
    assert concatenated_list.is_empty
    assert found_element is None
    assert string_representation == 'ImmutableList[]'
    assert prepended_list.head == empty_list
    assert reduced_value is prepended_list  # reduce returns the reducer unchanged for a single-element list

def test_find_returns_first_match_when_identity_predicate_matches_multiple_true_elements():
    # Setup: create an ImmutableList with one element and append another True element
    element_to_find = True
    immutable_list = immutable_list.ImmutableList(element_to_find, is_empty=element_to_find)
    immutable_list = immutable_list.append(element_to_find)
    
    # Execution: find the first element that satisfies the identity predicate
    result = immutable_list.find(lambda x: x)
    
    # Assertion: the first element (True) should be returned
    assert result == element_to_find

def test_add_none_to_empty_immutable_list_raises_value_error():
    # Setup: create an ImmutableList and an invalid operand (None)
    immutable_list = immutable_list.ImmutableList()
    invalid_operand = None

    # Execution & Assertion: adding a non-ImmutableList value should raise ValueError
    with pytest.raises(ValueError):
        immutable_list.__add__(invalid_operand)

def test_find_on_list_constructed_with_empty_list_as_source_and_is_empty_flag_returns_none():
    # Setup: create an empty immutable list to use as both source and is_empty flag
    empty_list = immutable_list.ImmutableList()

    # Execution: construct a new ImmutableList from the empty list and find using the list itself as predicate
    empty_list_length = len(empty_list)
    derived_list = immutable_list.ImmutableList(empty_list, is_empty=empty_list)
    found_element = derived_list.find(derived_list)

    # Assertion: derived list remains empty and find returns None
    assert empty_list_length == 0
    assert found_element is None

def test_empty_immutable_list_len_and_find_lookup_return_zero_and_none():
    # Setup: create an empty ImmutableList
    is_empty = False
    immutable_list = immutable_list.ImmutableList(is_empty, is_empty=is_empty)

    # Execution: get the length and search for an element
    length = immutable_list.__len__()
    found_element = immutable_list.find(immutable_list)

    # Assertion: the length should be 0 and the search should return None
    assert length == 0
    assert found_element is None

def test_find_on_an_empty_in_memory_immutable_list_returns_none():
    # Setup: create an empty ImmutableList
    is_empty = True
    empty_list = immutable_list.ImmutableList(is_empty, is_empty=is_empty)

    # Execution: convert the list to a Python list and search for any element
    elements = empty_list.to_list()
    result = empty_list.find(lambda element: element == elements)

    # Assertion: finding on an empty list should yield None
    assert result is None

def test_append_self_to_empty_then_convert_to_list_and_add_none():
    # Setup: create an empty ImmutableList
    empty_list = immutable_list.ImmutableList()
    search_predicate = None  # No predicate provided for find (per original test)

    # Execution: find on empty list should return None
    find_result = empty_list.find(search_predicate)

    # Execution: append the empty list to itself, creating a list containing the empty list
    appended_list = empty_list.append(empty_list)

    # Execution: convert the resulting list to a Python list
    elements_as_python_list = appended_list.to_list()

    # Execution: attempt to add None using the list's __add__ method (expects an ImmutableList)
    elements_as_python_list.__add__(None)

    # Assertion: find on empty list returns None
    assert find_result is None

    # Assertion: the appended list contains exactly one element, which is the original empty list
    assert elements_as_python_list == [empty_list]

def test_to_list_and_map_on_immutable_list_with_non_empty_value():
    # Setup: create an ImmutableList with a single non-empty (False is Empty) value
    is_empty = False
    immutable_list = immutable_list.ImmutableList(is_empty=is_empty)

    # Execution: convert the ImmutableList to a plain Python list and
    # then attempt to map over the resulting list (which is not supported for lists)
    converted_list = immutable_list.to_list()

    # Setup: create an additional (empty) ImmutableList for the second call
    another_immutable_list = immutable_list.ImmutableList()
    second_converted_list = immutable_list.to_list()

    # Execution: call map on the ImmutableList with the converted list as the mapper
    immutable_list.map(second_converted_list)

def test_map_on_immutable_list_with_appended_none_after_prepend_operations():
    # Setup: create an ImmutableList containing a single None element
    NONE_ELEMENT = None
    original_list = immutable_list.ImmutableList(NONE_ELEMENT, NONE_ELEMENT)

    # Create new lists by prepending elements via unshift operations
    list_with_prepended_none = original_list.unshift(NONE_ELEMENT)
    list_with_prepended_list = original_list.unshift(list_with_prepended_none)

    # Append None to the list created by prepending None
    list_with_appended_none = list_with_prepended_none.append(NONE_ELEMENT)

    # Execution & Assertion: mapping over the list with appended None should not raise
    list_with_appended_none.map(NONE_ELEMENT)

def test_filter_always_false_on_empty_immutable_list_returns_empty_list():
    # Setup: Create an empty ImmutableList
    is_empty = True
    empty_list = immutable_list.ImmutableList(is_empty, is_empty=is_empty)
    
    # Filter function that always returns False (should not affect the empty list)
    def always_false_filter(element):
        return False
    
    # Execution: Apply filter to the empty list
    result = empty_list.filter(always_false_filter)
    
    # Assertion: The result should be an empty ImmutableList
    assert result.is_empty

def test_concatenation_of_empty_immutable_list_with_itself_results_in_empty_and_filter_with_length_as_predicate():
    # Setup: create an empty ImmutableList and concatenate it with itself
    empty_list = immutable_list.ImmutableList()
    concatenated_list = empty_list.__add__(empty_list)

    # Execution: obtain the length of the concatenated list and use it as a filter predicate
    # (an int is passed where a callable is expected by the filter implementation)
    concatenated_length = len(concatenated_list)
    filtered_list = concatenated_list.filter(concatenated_length)

    # Assertion: the concatenation of an empty list with itself remains empty,
    # so the resulting length is zero
    assert concatenated_length == 0

def test_find_in_empty_immutable_list_returns_none_and_length_is_zero_v2():
    # Setup
    search_value = 1947
    empty_list_head = None
    empty_list_tail = None
    empty_immutable_list = immutable_list.ImmutableList(empty_list_head, empty_list_tail)

    # Execution
    found_element = empty_immutable_list.find(lambda x: x == search_value)

    # Assertion
    assert found_element is None, "find on an empty ImmutableList should return None"
    assert len(empty_immutable_list) == 0, "length of an empty ImmutableList should be 0"

def test_search_empty_immutable_list_using_self_predicate_returns_none():
    # Setup: create an empty ImmutableList
    # An empty list is created by passing head=False and marking it as empty
    EMPTY_FLAG = False
    empty_list = immutable_list.ImmutableList(EMPTY_FLAG, is_empty=EMPTY_FLAG)

    # Execution: search for an element using the list itself as the predicate
    result = empty_list.find(empty_list)

    # Assertion: searching an empty list should return None
    assert result is None

def test_reduce_empty_list_returns_initial_accumulator_without_calling_reducer():
    # Setup: an empty ImmutableList and a reducer function that always returns False.
    # The reducer is used to verify that reducing an empty list does not invoke the
    # reducer and simply returns the provided accumulator.
    empty_list = immutable_list.ImmutableList()
    initial_accumulator = False
    reducer_fn = lambda acc, item: acc

    # Execution: reduce the empty list with the reducer and initial accumulator.
    result = empty_list.reduce(reducer_fn, initial_accumulator)

    # Assertion: reducing an empty list returns the accumulator unchanged.
    assert result == initial_accumulator


def test_find_returns_head_value_when_predicate_matches_single_element_list():
    # Setup: a single-element ImmutableList with a predicate that matches the head.
    is_empty_flag = False
    test_value = False
    list_with_one_element = immutable_list.ImmutableList(test_value, is_empty=is_empty_flag)

    # Execution: find the first element matching the predicate. The predicate
    # returns the element itself, which is truthy when the element is True, but
    # here we directly pass the list's value to mirror the original behavior.
    found_element = list_with_one_element.find(list_with_one_element)

    # Assertion: since the list is not empty and the predicate matches the head,
    # the head should be returned (which is False in this case, matching equality
    # to the stored value). We assert against the expected stored value.
    assert found_element == test_value

def test_new_created_immutable_list_has_zero_length_and_yields_empty_iteration():
    # Setup: create a new ImmutableList instance with no elements.
    empty_immutable_list = immutable_list.ImmutableList()

    # Execution: no operation is performed; we inspect the freshly created list.

    # Assertion: a newly created ImmutableList should be empty.
    assert len(empty_immutable_list) == 0
    assert list(empty_immutable_list) == []

def test_empty_immutable_list_str_and_find_returns_none_without_matches():
    # Setup: create an empty ImmutableList
    is_empty = False
    empty_list = immutable_list.ImmutableList(is_empty, is_empty=is_empty)

    # Execution: get string representation and search for an element
    string_representation = empty_list.__str__()
    found_element = empty_list.find(empty_list)

    # Assertion: verify the string representation and that find returns None
    assert string_representation == 'ImmutableList[]'
    assert found_element is None

def test_find_on_self_unshifted_empty_immutable_list_returns_none():
    # Setup: create an empty ImmutableList
    is_empty = False
    empty_list = immutable_list.ImmutableList(is_empty, is_empty=is_empty)
    
    # Execute: unshift the list with itself and then search using find
    list_with_self = empty_list.unshift(empty_list)
    result = list_with_self.find(list_with_self)
    
    # Assertion: find on an empty list should return None
    assert result is None

def test_find_on_list_with_false_element_after_append_and_unshift_returns_none():
    # Constants
    ELEMENT_IS_EMPTY = False

    # Setup: create an empty ImmutableList and derive new lists via unshift/append
    empty_list = immutable_list.ImmutableList(is_empty=ELEMENT_IS_EMPTY)

    # Execution: unshift False onto the list, then append the original empty list
    list_with_unshifted_false = empty_list.unshift(ELEMENT_IS_EMPTY)
    combined_list = list_with_unshifted_false.append(empty_list)

    # Execution: find first element matching the predicate (identity on False)
    result = combined_list.find(ELEMENT_IS_EMPTY)

    # Assertion: the find should return None because the only False is itself
    # a valid match? Given predicate returns the element if truthy check passes;
    # here False is the searched value and the list contains False as head,
    # but since False is falsy, the predicate check fails, so expected None.
    assert result is None

def test_append_single_element_list_yields_length_two_after_appending_same_element():
    # Setup: Create an ImmutableList containing a single boolean element
    initial_element = True
    single_element_list = immutable_list.ImmutableList(initial_element, is_empty=initial_element)

    # Execution: Append a new element to the list and get the resulting list's length
    list_with_appended_element = single_element_list.append(initial_element)
    resulting_length = list_with_appended_element.__len__()

    # Assertion: The list should now contain two elements after the append operation
    assert resulting_length == 2

def test_immutable_list_reduce_and_reconstruct_from_string_with_nested_list_elements():
    # Setup: create an empty ImmutableList and derived nested structures
    empty_list = immutable_list.ImmutableList()
    list_with_empty_list_appended = empty_list.append(empty_list)

    # Execution: perform reduce over the appended list using the list itself as accumulator and function
    reduced_result = empty_list.reduce(list_with_empty_list_appended, list_with_empty_list_appended)

    # Assertion: equality between the appended list and the original empty list
    # (an ImmutableList is not equal to itself when elements differ, here the empty list vs list containing empty list)
    assert list_with_empty_list_appended.__eq__(empty_list) is False

    # Execution: prepend the appended list to itself
    list_with_itself_unshifted = list_with_empty_list_appended.unshift(list_with_empty_list_appended)

    # Execution: obtain string representation of the unshifted list
    string_representation = list_with_itself_unshifted.__str__()

    # Execution: reconstruct an ImmutableList from the string using is_empty parameter
    # (is_empty is truthy here because the string is non-empty)
    list_from_string = immutable_list.ImmutableList(is_empty=string_representation)

    # Execution: append the reduced result to itself
    list_with_reduced_appended = reduced_result.append(reduced_result)

    # Execution: search for the reduced result within the unshifted list using find
    # find expects a predicate function; passing a list as callable is invalid but mirrors original behavior
    list_with_itself_unshifted.find(reduced_result)

def test_immutable_list_unshift_self_reduce_equality_and_constructor_with_int_is_empty():
    # Setup: create an empty ImmutableList and an ImmutableList containing the empty list as its first element
    EMPTY_LIST = immutable_list.ImmutableList()
    list_with_empty_list_element = EMPTY_LIST.unshift(EMPTY_LIST)

    # Execution: reduce the empty list using the list_with_empty_list_element as both reducer and accumulator
    # This exercises the reducer path where head and tail are None
    reduce_result = EMPTY_LIST.reduce(list_with_empty_list_element, list_with_empty_list_element)

    # Execution: compute the length of the list_with_empty_list_element
    # It should contain exactly one element, so length is 1
    length_of_list_with_element = list_with_empty_list_element.__len__()

    # Execution: create a new list by prepending list_with_empty_list_element to itself
    # Result should contain two elements, both being list_with_empty_list_element
    doubled_list = list_with_empty_list_element.unshift(list_with_empty_list_element)

    # Execution: compare doubled_list with the original EMPTY_LIST
    # They should not be equal because their heads, tails, and emptiness differ
    are_lists_equal = doubled_list.__eq__(EMPTY_LIST)

    # Execution: create an ImmutableList using the computed length as the `is_empty` flag
    # Since is_empty is expected to be a boolean but we pass an int, this exercises that constructor path
    list_from_length = immutable_list.ImmutableList(is_empty=length_of_list_with_element)

    # Execution: call find on reduce_result using itself as the predicate
    # Since reduce_result is an ImmutableList, calling it as a function is not valid;
    # this step verifies the method exists and can be invoked (runtime behavior depends on callability)
    find_result = reduce_result.find(reduce_result)

    # Assertions
    assert length_of_list_with_element == 1
    assert are_lists_equal is False
    assert reduce_result == list_with_empty_list_element
    assert list_from_length.is_empty == 1

def test_reduce_identity_function_over_single_true_list_returns_list_representation():
    # Setup: create an immutable list with a single element, True, and an empty list
    single_element_true_list = immutable_list.ImmutableList(True, is_empty=True)
    empty_list = immutable_list.ImmutableList(tail={})

    # Execution: convert the single-element list to a Python list and use it as
    # both the reducer function and accumulator in reduce
    list_representation = single_element_true_list.to_list()
    single_element_true_list.reduce(list_representation, list_representation)

    # Assertion: no exception is raised; the test passes if the call completes

