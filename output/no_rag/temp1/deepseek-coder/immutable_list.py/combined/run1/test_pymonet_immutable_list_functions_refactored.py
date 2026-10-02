import immutable_list as lists

def test_ImmutableList_equality_method():
    EMPTY_IMMUTABLE_LIST = module_0.ImmutableList()
    COMPARE_IMMUTABLE_LIST = module_0.ImmutableList()

    immutable_list_0 = EMPTY_IMMUTABLE_LIST
    bool_0 = immutable_list_0.__eq__(immutable_list_0)
    assert bool_0 is True

    immutable_list_0 = module_0.ImmutableList(COMPARE_IMMUTABLE_LIST.head, COMPARE_IMMUTABLE_LIST.tail)
    bool_1 = immutable_list_0.__eq__(COMPARE_IMMUTABLE_LIST)
    assert bool_1 is True

def test_immutable_list_equality_method():
    # Constants
    BOOL_0 = True
    IMMUTABLE_LIST_0 = module_0.ImmutableList()

    # Setup
    IMMUTABLE_LIST_1 = IMMUTABLE_LIST_0.__add__(IMMUTABLE_LIST_0)

    # Execution
    bool_1 = IMMUTABLE_LIST_0.__eq__(BOOL_0)
    
    # Assertion
    assert bool_1 is False, "Test should fail because IMMUTABLE_LIST_0 should not be equal to BOOL_0"

def test_ImmutableList_append_and_find():
    # Setup
    bool_value_true = True
    empty_immutable_list = module_0.ImmutableList(bool_value_true, is_empty=bool_value_true)

    # Execution
    # Append a new element to the list
    updated_immutable_list = empty_immutable_list.append(bool_value_true)

    # Try to find the element in the updated list
    element_found = updated_immutable_list.find(lambda x: x == bool_value_true)

    # Assertion
    # Check if the found element is the same as the value we appended
    assert element_found == bool_value_true, "The found element is not the expected value"

def test_add_none_to_empty_immutable_list():
    # Define constants for variable names
    EMPTY_IMMUTABLE_LIST = module_0.ImmutableList()
    NONE_VALUE = None

    # Setup:
    # Create an empty immutable list and a None value
    immutable_list = EMPTY_IMMUTABLE_LIST
    none_value = NONE_VALUE

    # Execution:
    # Attempt to add None to the empty immutable list
    result = immutable_list.__add__(none_value)

    # Assertion:
    # The result should be equal to the None value
    assert result == none_value, "Adding None to an empty ImmutableList did not return None"

def test_immutable_list_find_empty_list_modified():
    empty_list = module_0.ImmutableList()
    assert empty_list.__len__() == 0, "Empty list cannot contain elements"
    
    new_list = module_0.ImmutableList(empty_list, is_empty=empty_list)
    result = new_list.find(lambda x: x is not None)

    assert result is None, "Find function should not return any element when list is empty"

def test_immutable_list_finds_an_element():
    """
    This test case is to verify if the find function in ImmutableList can find an element based on the given function.
    We first initialize an ImmutableList with boolean values. The ImmutableList is created using the __init__() method,
    which takes in a 'head' value (which is False) and an 'is_empty' flag (also False).

    Then we feed this ImmutableList into the find method of the same ImmutableList
    with the condition that the element must exist in the list for it to pass. In this case, we are using the find method
    to search for the first occurrence of 'False' value in the list. This value should exist in the list so the find method
    should return the element found.

    We also check the length of the list before and after the find operation to ensure no elements are added or removed.
    """

    # Set up
    bool_value = False
    immutable_list = module_0.ImmutableList(bool_value, is_empty=bool_value)
    list_length_before_find_operation = immutable_list.__len__()

    # Execution
    result = immutable_list.find(immutable_list)

    # Assertion
    assert result == bool_value
    assert list_length_before_find_operation == immutable_list.__len__()

def test_case_6():
    is_empty = False
    immutable_list = module_0.ImmutableList(is_empty, is_empty=is_empty)
    immutable_list_as_list = immutable_list.to_list()
    check_head = lambda element: element is False
    assert immutable_list.find(check_head) is False

def test_empty_list_append_new_element():
    # Define initial list element
    initial_list = module_0.ImmutableList()

    # Define element to append to list
    new_element = None

    # Check that the list does not contain the new element
    assert initial_list.find(new_element) is None

    # Append new element to list
    appended_list = initial_list.append(new_element)

    # Check that new element is now in the list
    assert appended_list.find(new_element) is not None

    # Convert list to python list
    list_as_python_list = appended_list.to_list()

    # Check that the python list now contains the new element
    assert new_element in list_as_python_list

def test_case_9():
    # Constants
    BOOL_IS_EMPTY = False

    # Setup
    mutable_list = lists.ImmutableList(is_empty=BOOL_IS_EMPTY)
    EXPECTED_MUTABLE_LIST = [None]

    MUTABLE_LIST = lists.ImmutableList()
    EXPECTED_IMMUTABLE_LIST = [None]

    # Execution
    result_mutable_list = mutable_list.to_list()
    result_immutable_list = MUTABLE_LIST.to_list()

    # Assertion
    assert result_mutable_list == EXPECTED_MUTABLE_LIST, "Expected mutable list does not match result"
    assert result_immutable_list ==  EXPECTED_IMMUTABLE_LIST, "Expected immutable list does not match result"

    # If assertion passed we map the result with a function
    MUTABLE_LIST.map(lambda x: x+1)

# Test unshift and append methods with None value
def test_case_10():
    NONE_VALUE = None 
    # Setup
    immutable_list_0 = ImmutableList(NONE_VALUE, NONE_VALUE)

    # Execution - append None value to list
    immutable_list_1 = immutable_list_0.unshift(NONE_VALUE)
    immutable_list_2 = immutable_list_0.unshift(immutable_list_1)
    immutable_list_3 = immutable_list_1.append(NONE_VALUE)
    immutable_list_4 = immutable_list_3.map(NONE_VALUE)

    # Assertion - verify if all unshift and append operations were performed correctly
    assert immutable_list_0 == ImmutableList(NONE_VALUE, NONE_VALUE)
    assert immutable_list_1 == ImmutableList(NONE_VALUE, NONE_VALUE)
    assert immutable_list_2 == ImmutableList(NONE_VALUE, immutable_list_0)
    assert immutable_list_3 == ImmutableList(NONE_VALUE, NONE_VALUE)
    assert immutable_list_4 == ImmutableList(NONE_VALUE, NONE_VALUE.NONE_VALUE)

def test_filtering_with_true_fn():
    '''
    This test case is designed to verify that the filter function works correctly 
    when a function that always returns True is passed to it. The test includes a 
    setup step where an ImmutableList object is created using the module_0.ImmutableList 
    function. Then, a filter function is applied to the list, where the passed 
    function always returns True. The purpose of this test is to confirm that the 
    output ImmutableList remains the same as the input ImmutableList when True is 
    always returned by the function.
    '''

    # Preparation
    is_empty = False
    initial_data = [True, False, True]
    filtered_data = initial_data
    immutable_list = module_0.ImmutableList(initial_data, is_empty=is_empty)

    # Execution
    def always_return_true(item):
        return True

    result = immutable_list.filter(always_return_true)

    # Assertion
    assert result.as_list() == filtered_data, "Filter with 'True' function did not return the same list"

def test_filter_by_length():
    # Arrange
    INITIAL_LENGTH = 5
    MAX_SIZE = 10

    # Create an ImmutableList with a specific length.
    initial_list = ImmutableList(range(INITIAL_LENGTH))

    # Duplicate the list twice to have larger list.
    replicated_list = initial_list + initial_list

    # Act
    # Filter the list based on the length of the list. It should remove all but two elements.
    filtered_list = replicated_list.filter(lambda x: len(x) < MAX_SIZE)

    # Assert
    # Check that the filtered list has the correct length.
    assert len(filtered_list) == 2

def test_immutable_list_length_after_find_element_is_correct():
    # Arrange
    element_to_find = 1947
    list_with_element = ImmutableList(ImmutableList(None, None), 2022, element_to_find)

    # Act
    result_element = list_with_element.find(lambda x: x == element_to_find)
    result_length = len(list_with_element)

    # Assert
    assert result_element == element_to_find, "Expected the found element to be the one we are looking for"
    assert result_length == 3, "Expected the length of the list with the found element to be 3"

def test_find_valid_element_unique():
    data_list = [True, False, True]
    immutable_list = ImmutableList(data_list)

    def is_true(x):
        return x is True

    result = immutable_list.find(is_true)

    assert result is True

import pytest

def test_reducing_immutable_list_returns_correct_result():
    # Arrange
    initial_accumulator = 0
    immutable_list = ImmutableList(1, 2, 3)

    # Act
    result = immutable_list.reduce(lambda acc, x: acc + x, initial_accumulator)

    # Assert
    expected_result = sum(immutable_list)
    assert result == expected_result, "Expected sum {expected_result} should be returned when reducing"

def test_create_immutable_list_default():
    # Test Case: Create Immutable List with Default Arguments
    # Purpose: The purpose of this test case is to verify that the creation
    # of an immutable list object doesn't throw an error when no arguments are passed.

    # Setup
    IMMUTABLE_LIST = ImmutableList()

    # Execution
    result = IMMUTABLE_LIST

    # Assertion
    assert isinstance(result, ImmutableList), "The created object is not of type ImmutableList"

def test_immutable_list_find_functionality():
    # Define Constants
    IS_EMPTY = False
    HEAD_ELEMENT = False

    # Setup
    immutable_list = ImMutableList(HEAD_ELEMENT, is_empty=IS_EMPTY)

    # Execution
    list_string_representation = immutable_list.__str__()
    found_element = immutable_list.find(lambda x: x == HEAD_ELEMENT)

    # Assertion
    assert type(list_string_representation) == str, "List representation should be a string"
    assert found_element == HEAD_ELEMENT, "Find function should return the HEAD_ELEMENT when a function that checks equality HEAD_ELEMENT is passed"

def test_immutableList_unshift_find():
    # Setup
    EMPTY_BOOL = False
    empty_immutable_list = module_0.ImmutableList(EMPTY_BOOL, is_empty=EMPTY_BOOL)

    # Execution: unshift the new object before the list
    new_element = empty_immutable_list.unshift(empty_immutable_list)
    # Execution: Find the first object that matches the condition
    found_element = new_element.find(lambda x: x == empty_immutable_list)

    # Assertion: Check if the found element is the same as the element unshifted
    assert found_element == empty_immutable_list

def test_immutable_list_append_unshift_find():
    # Constants
    EMPTY_LIST = module_0.ImmutableList(is_empty=True)
    NON_EMPTY_LIST = module_0.ImmutableList(is_empty=False)
    VALUE_TO_APPEND = True
    VALUE_TO_PREPEND = False

    # Setup
    immutable_list = NON_EMPTY_LIST

    # Execution: append a value to the end of the list
    immutable_list_after_append = immutable_list.append(VALUE_TO_APPEND)

    # Execution: prepend a value to the start of the list
    immutable_list_after_prepend = immutable_list_after_append.unshift(VALUE_TO_PREPEND)

    # Execution: find a value in the list
    found_value = immutable_list_after_prepend.find(lambda x: x == VALUE_TO_PREPEND)

    # Assertion: check that the expected value is found
    assert found_value == VALUE_TO_PREPEND, f"Expected {VALUE_TO_PREPEND}, but got {found_value}"

def test_append_element_to_immutable_list():
    """
    Test Case Name: test_ImmutableList_append_and_find
    Given an empty ImmutableList, when an element is appended,
    then the length of the ImmutableList should increase by 1 and the element should be found in the list.
    """

    # Setup
    IS_EMPTY = True
    ELEMENT = True
    immutable_list_empty = module_0.ImmutableList(IS_EMPTY, is_empty=IS_EMPTY)

    # Test Append
    immutable_list_new = immutable_list_empty.append(ELEMENT)

    # Assertions
    assert len(immutable_list_new) == len(immutable_list_empty) + 1, "Test failed: the length of the ImmutableList did not increase after appending an element"
    assert immutable_list_new.find(ELEMENT) == ELEMENT, "Test failed: the newly appended element was not found in the ImmutableList"

def test_immutable_list_append_unshift_find():
    original_list = ImmutableList(1, 2, 3)
    new_element = 4
    expected_result = ImmutableList(1, 2, 3, 4)

    # Execution
    result = original_list.append(new_element)

    # Assertion 
    assert result == expected_result, "Append method failed"

    find_element = lambda x: x == 4
    result = original_list.find(find_element)

    # Assertion 
    assert result == new_element, "Find method failed"

def test_case_21_reduce_unshift_find():
    # set up: create an immutable list and reduce it
    immutable_list_0 = module_0.ImmutableList()
    immutable_list_1 = immutable_list_0.unshift(immutable_list_0)
    var_0 = immutable_list_0.reduce(immutable_list_1, immutable_list_1)

    # execute: find the length of the list_1
    var_1 = immutable_list_1.__len__()

    # execute: add an element at the beginning of list_1
    immutable_list_2 = immutable_list_1.unshift(immutable_list_1)

    # execute: check if list_2 is equivalent to list_0
    bool_0 = immutable_list_2.__eq__(immutable_list_0)

    # execute: create a new empty list with length of var_1
    immutable_list_3 = module_0.ImmutableList(is_empty=var_1)

    # execute: find an element in the list_0 matching the condition in fn
    var_0.find(lambda element: element == var_0)

def test_checking_conversion_and_reduction():
    # Constants for setup
    EMPTY_IMMUTABLE_LIST = immutable_list.ImmutableList()
    NON_EMPTY_IMMUTABLE_LIST = immutable_list.ImmutableList(1, 2, 3)
    NON_EMPTY_IMMUTABLE_LIST_HAVING_BOOL_AS_HEAD = immutable_list.ImmutableList(True)
    
    # Setup stage - Create some immutable lists for testing
    empty_immutable_list = EMPTY_IMMUTABLE_LIST
    non_empty_immutable_list = NON_EMPTY_IMMUTABLE_LIST
    non_empty_immutable_list_having_bool_as_head = NON_EMPTY_IMMUTABLE_LIST_HAVING_BOOL_AS_HEAD
    
    # Execution and Assertion - Check conversion and reduction
    assert non_empty_immutable_list.to_list() == [1, 2, 3]
    assert non_empty_immutable_list_having_bool_as_head.to_list() == [True]
    assert empty_immutable_list.to_list() == []

    # For the boolean list, we are going to calculate a logical conjunction.
    assert non_empty_immutable_list.reduce(lambda x, y: x and y, True) == True
    assert non_empty_immutable_list_having_bool_as_head.reduce(lambda x, y: x and y, True) == True
    assert empty_immutable_list.reduce(lambda x, y: x and y, True) == True

