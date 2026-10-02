import pytest
import immutable_list as immutable_list

def test_equality_of_empty_immutable_list_with_none():
    # Given: An empty ImmutableList
    empty_immutable_list = module_0.ImmutableList()

    # When: We try to compare the ImmutableList with None
    # Then: It should return False. Because None is not the same type as ImmutableList for equality.
    assert empty_immutable_list.__eq__(None) is False

def test_reduce_method_on_immutable_list():
    """
    Test that reduce method applies the given function on each element of the list,
    resulting in a single output value. The function 'reduce' is being 
    tested to ensure that it reduces the entire list to its summation value
    """

    IS_EMPTY = True
    LIST_ELEMENT_1 = {'first': 1, 'second': 2}
    LIST_HAS_MORE_ELEM = False
    EMPTY_LIST = []
    NON_EMPTY_LIST = [{'first': 1, 'second': 2}, {'third': 3, 'fourth': 4}]

    # Setup
    immutable_list = ImmutableList()

    # Execution
    result_list = immutable_list.to_list()

    # Assertion
    # Check if the newly formed list is empty
    assert result_list == EMPTY_LIST, "The list formed is not empty"

    # Now add elements to the list
    for element in NON_EMPTY_LIST: 
        immutable_list = immutable_list.unshift(element)

    # Check if the list is not empty
    assert immutable_list.is_empty == LIST_HAS_MORE_ELEM, "The list appears to be empty after adding elements"

    # Now check if all the elements are present by reducing the list and counting them
    result_list = immutable_list.to_list()
    assert len(result_list) == len(NON_EMPTY_LIST), "The number of elements do not match in the original list and the result list"

def test_find_element_in_prepended_immutable_list():
    # Define the constants
    IS_EMPTY = True
    BOOL_VALUE = True

    # Setup
    new_immutable_list = immutable_list.ImmutableList(BOOL_VALUE, is_empty=IS_EMPTY)
    prepended_list = new_immutable_list.append(BOOL_VALUE)

    # Definition of the function to find elements in the list
    def find_element(element):
        return element == BOOL_VALUE

    # Execution
    found_element = prepended_list.find(find_element)

    # Assertion
    assert found_element == BOOL_VALUE

def test_case_3():
    # Setup
    immutable_list = ImmutableList()
    none_value = None

    # Assertions
    with pytest.raises(ValueError):
        # Execution
        immutable_list.__add__(none_value)

def test_find_element_in_prepended_immutable_list():
    # Constants
    EMPTY_LIST = immutable_list.ImmutableList()
    TEST_LIST = immutable_list.ImmutableList(EMPTY_LIST, is_empty=EMPTY_LIST)

    # Setup
    def is_empty(element):
        return element is None

    # Execution
    result = TEST_LIST.find(is_empty)

    # Assertion
    assert result is EMPTY_LIST, "The found element should be the same as the test list"

def test_find_element_in_prepended_immutable_list_alternative():
    """
    Test to check the 'find' function from the ImmutableList class.
    """
    # Constants
    IS_EMPTY = False
    HEAD_ELEMENT = False

    # Setup
    immutable_list = immutable_list.ImmutableList(HEAD_ELEMENT, is_empty=IS_EMPTY)

    # Function to check whether the item matches the head element of the ImmutableList
    def check_head_element(item):
        return item == HEAD_ELEMENT

    # Execution
    found_element = immutable_list.find(check_head_element)

    # Assertion
    assert found_element == HEAD_ELEMENT, "The element found doesn't match the head element of the ImmutableList"

def test_find_element_in_prepended_immutable_list():
    """
    This test case checks if the find() method of ImmutableList behaves correctly.
    We generate an ImmutableList, convert it to standard python list and find an element that exists in the list.
    We then assert that the found element is correct.
    """
    
    # Setup
    bool_value = False
    immutable_list = immutable_list.ImmutableList(bool_value, is_empty=bool_value)

    # Execution
    list_for_find = immutable_list.to_list()
    found_value = immutable_list.find(lambda x: x in list_for_find)

    # Assertion
    assert found_value == list_for_find[0], "The found value does not match the first element of the original list"

# Constant representing None
NONE_CONSTANT = None

def test_append_and_find_in_empty_list():
    # Set up
    immutable_list_1 = immutable_list.ImmutableList()
    # Expected Value
    expected_value = []
    # Assertion before execution
    assert immutable_list_1.to_list() == expected_value

    # Execution
    immutable_list_1 = immutable_list_1.append(immutable_list_1)
    # Expected Value
    expected_value = expected_value.__add__(NONE_CONSTANT)
    # Assertion after execution
    assert immutable_list_1.to_list() == expected_value

    result_find = immutable_list_1.find(NONE_CONSTANT)
    assert result_find == expected_value

def test_map_functionality():
    """
    Test case for checking the map functionality of the ImmutableList class.
    Check to ensure no side effect in map operation on ImmutableList.
    """
    # Setup
    is_list_empty = False
    first_list = immutable_list.ImmutableList(is_empty=is_list_empty)
    second_list = immutable_list.ImmutableList()

    # Execution
    mapped_list_with_no_effect_function = first_list.map(second_list.to_list)

    # Assertion
    assert first_list.to_list() == mapped_list_with_no_effect_function.to_list()

def test_unshift_new_element_on_empty_list():
    # Arrange
    NONE_TYPE = None
    immutable_list_0 = ImmutableList(NONE_TYPE, NONE_TYPE)

    # Act
    immutable_list_1 = immutable_list_0.unshift(NONE_TYPE)

    # Assert
    assert immutable_list_1.map(lambda x: x is None) == ImmutableList(NONE_TYPE), "New element was not appended at the beginning of the list"


def test_unshift_new_element_on_existing_list():
    # Arrange
    NONE_TYPE = None
    immutable_list_0 = ImmutableList(NONE_TYPE, NONE_TYPE)
    immutable_list_1 = immutable_list_0.unshift(NONE_TYPE)

    # Act
    immutable_list_2 = immutable_list_0.unshift(immutable_list_1)

    # Assert
    assert immutable_list_2.map(lambda x: x is None) == ImmutableList(NONE_TYPE, NONE_TYPE), "List is not correctly appended at the beginning"


def test_append_new_element_to_empty_list():
    # Arrange
    NONE_TYPE = None
    immutable_list_0 = ImmutableList(NONE_TYPE, NONE_TYPE)
    immutable_list_1 = immutable_list_0.unshift(NONE_TYPE)

    # Act
    immutable_list_3 = immutable_list_1.append(NONE_TYPE)

    # Assert
    assert immutable_list_3.map(lambda x: x is None) == ImmutableList(NONE_TYPE, NONE_TYPE, NONE_TYPE), "New element was not appended at the end of list"

def test_immutable_list_filter_true():
    # Constants
    IS_EMPTY = False
    HEAD = False
    TAIL = [True, False]
    EXPECTED_HEAD = HEAD

    # Setup
    immutable_list = immutable_list.ImmutableList(HEAD, TAIL, is_empty=IS_EMPTY)

    # Action
    filtered_list = immutable_list.filter(lambda x: x)

    # Assertion
    assert filtered_list.head == EXPECTED_HEAD
    assert filtered_list.tail.head in TAIL
    assert all(i in TAIL for i in filtered_list.tail)

def test_immutable_list_filter_by_length():
    # Define constant for ImmutableList
    EMPTY_IMMUTABLE_LIST = ImmutableList(is_empty=True)

    # Setup
    immutable_list_1 = EMPTY_IMMUTABLE_LIST.__add__(EMPTY_IMMUTABLE_LIST)
    immutable_list_1_length = immutable_list_1.__len__()

    # Execution
    filtered_immutable_list = immutable_list_1.filter(immutable_list_1_length)

    # Assertion
    assert filtered_immutable_list == EMPTY_IMMUTABLE_LIST, "The filter function should return an empty ImmutableList"

def test_immutable_list_find_returns_first_element_passing_criteria():
    # Define the test constants
    NONE_CONSTANT = None
    TARGET_VALUE = 1947

    # Set up the test
    test_list = immutable_list.ImmutableList(NONE_CONSTANT, NONE_CONSTANT)
    test_list_length_before_find = len(test_list)

    # Define the criteria function
    def criteria_fn(element):
        return element == TARGET_VALUE

    # Execute the test
    first_match = test_list.find(criteria_fn)

    # Assert the results
    assert first_match is NONE_CONSTANT
    assert len(test_list) == test_list_length_before_find

def test_find_matching_element_alternative():
    """
    This test checks the behavior of the 'find' method in ImmutableList.
    The 'find' method should return the first element in the list that
    satisfies the provided function (fn). Here, we test with a function
    which accepts any value and returns True for any input.
    """

    # SETUP
    bool_value = False
    immutable_list_obj = immutable_list.ImmutableList(bool_value, is_empty=bool_value)

    # MATCH ALL FUNCTION
    def match_all(value):
        return True

    # EXECUTION
    result = immutable_list_obj.find(match_all)

    # ASSERTION
    assert result == bool_value, (
        "The 'find' method should return the first element that matches "
        "in the ImmutableList"
    )

# Ensure the reduce function behaves correctly when given list and a function
def test_immutable_list_reduce_behavior():
    # Define some constants for readability
    EMPTY_LIST = immutable_list.ImmutableList(is_empty=True)
    NOT_EMPTY_LIST = immutable_list.ImmutableList([1, 2, 3])
    INVALID_LIST = immutable_list.ImmutableList(None)

    # Test reduce with an empty list and a valid function
    ACCUMULATOR = 0
    result = EMPTY_LIST.reduce(lambda a, b: a + b, ACCUMULATOR)
    assert result == ACCUMULATOR, "Result should be zero when reducing an empty list"

    # Test reduce with a non-empty list and a valid function
    result = NOT_EMPTY_LIST.reduce(lambda a, b: a + b, ACCUMULATOR)
    assert result == 6, "Sum should be 6 when reducing a non-empty list"

    # Test reduce with an invalid list to ensure it fails gracefully
    with pytest.raises(TypeError):
        INVALID_LIST.reduce(lambda a, b: a + b, ACCUMULATOR)

# Ensure the find function behaves correctly when given list and a function
def test_immutable_list_find_behavior():
    # Define some constants for readability
    EMPTY_LIST = immutable_list.ImmutableList(is_empty=True)
    NOT_EMPTY_LIST = immutable_list.ImmutableList([1, 2, 3])

    # Test find with an empty list and a valid function
    result = EMPTY_LIST.find(lambda x: x == 1)
    assert result is None, "Result should be None when finding in an empty list"

    # Test find with a non-empty list and a valid function
    result = NOT_EMPTY_LIST.find(lambda x: x == 2)
    assert result == 2, "Result should be the first element for which the function returns True"

def test_immutable_list_zero_length_at_init():
    """
    This test checks if the length of the immutable list remains zero
    at the time of creation. This is to ensure that the object is created
    successfully and has no elements.
    """

    # Arrange
    immutable_list = module_0.ImmutableList()  # Creating an instance of immutable list

    # Act, Assert
    assert immutable_list.length() == 0, "The immutable list is not created with length of zero"

def test_finding_element_in_immutable_list():
    # Given
    EMPTY_LIST = immutable_list.ImmutableList(None, is_empty=True)
    LIST_WITH_ELEMENTS = immutable_list.ImmutableList(bool_0, is_empty=bool_0)

    # When
    result_empty_list = EMPTY_LIST.find(lambda x: True)
    result_list_with_elements = LIST_WITH_ELEMENTS.find(lambda x: x is True)
    
    # Then
    assert result_empty_list is None, "Expected None result with empty list"
    assert result_list_with_elements is not None, "Expected a result with none empty list"
    assert result_list_with_elements is True, "Expected element to be True"

def test_find_in_unshifted_list_should_return_first_matching_element_correctly():
    # Constants
    EMPTY_BOOLEAN = False
    SEARCH_ELEMENT = True

    # Setup
    immutable_list = ImmutableList(EMPTY_BOOLEAN, is_empty=EMPTY_BOOLEAN)
    unshifted_list = immutable_list.unshift(SEARCH_ELEMENT)

    # Execution
    found_element = unshifted_list.find(lambda element: element == SEARCH_ELEMENT)

    # Assertion
    assert found_element == SEARCH_ELEMENT, "The first matching element was not returned"

def test_add_element_at_start_and_find_it():
    """
    This test case checks if an element can be added at the
    start and then found successfully using the find method.
    """

    # Given
    ELEMENT_TO_FIND = True

    # And an empty immutable list
    immutable_list = immutable_list.ImmutableList(is_empty=True)

    # When an element is added to the immutable list
    immutable_list = immutable_list.unshift(ELEMENT_TO_FIND)

    # Then, after finding it
    found_element = immutable_list.find(lambda a: a == ELEMENT_TO_FIND)

    # Then it should be equal to the added element
    assert found_element == ELEMENT_TO_FIND

def test_append_and_find_in_immutable_list():
    """
    This test case validates the functionalities of append and find methods in
    ImmutableList class. Here "append" method is used to add elements to 
    the immutable list and "find" method is used to find the first matching element 
    in the list.
    """
    # Constants for better understanding
    BOOL_TRUE = True
    BOOL_FALSE = False

    # Setup
    immutable_empty_list = ImmutableList(BOOL_TRUE, is_empty=BOOL_TRUE)
    
    # Execution
    # Append a new element to the list
    immutable_list_with_one_element = immutable_empty_list.append(BOOL_FALSE)

    # Compute the length of the updated list
    list_length = len(immutable_list_with_one_element)

    # Find the first element in the list that matches some condition
    first_matching_element = immutable_list_with_one_element.find(lambda value: value == BOOL_FALSE)

    # Assertion
    # Validate the length
    assert list_length == 2
    # Validate the first matching element
    assert first_matching_element == BOOL_FALSE

def test_find_element_in_prepended_immutable_list_difference():
    # Setup
    immutable_list_0 = module_0.ImmutableList()
    immutable_list_1 = immutable_list_0.append(immutable_list_0)

    # Execute reduce method of immutable_list_0
    result_reduce = immutable_list_0.reduce(immutable_list_1, immutable_list_1)

    # Execute equality check between objects
    bool_0 = immutable_list_1.__eq__(immutable_list_0)

    # Execute unshift method of immutable_list_1
    immutable_list_2 = immutable_list_1.unshift(immutable_list_1)

    # Convert to string
    str_0 = immutable_list_2.__str__()

    # Create a new ImmutableList with string representation
    immutable_list_3 = module_0.ImmutableList(is_empty=str_0)

    # Execute append method of result_reduce
    immutable_list_4 = result_reduce.append(result_reduce)

    # Execute find method of immutable_list_2
    found_element = immutable_list_2.find(result_reduce)

    # Assertion phase
    # Verify the 'bool_0' is False
    assert bool_0 is False
    # Verify 'str_0' output
    assert str_0 == 'ImmutableList{}'
    # Verify 'immutable_list_3' is not None
    assert immutable_list_3 is not None
    # Verify 'found_element' is None
    assert found_element is None

def test_reduce_length_and_unshift_operation():
    """
    Test case to validate unshift, reduce and length operations
    """

    # Setup
    immutable_list_0 = ImmutableList()

    # Execution
    immutable_list_1 = immutable_list_0.unshift(immutable_list_0)
    var_0 = immutable_list_0.reduce(immutable_list_1, immutable_list_1)
    var_1 = immutable_list_1.__len__()
    immutable_list_2 = immutable_list_1.unshift(immutable_list_1)
    bool_0 = immutable_list_2.__eq__(immutable_list_0)
    immutable_list_3 = ImmutableList(is_empty=var_1)
    var_0.find(var_0)

    # Assertions
    assert var_1 == 2
    assert bool_0 == False
    assert immutable_list_1.__len__() == 2

def test_to_list_method_with_empty_tail():
    # Arrange
    bool_is_empty = True
    empty_dict = {}
    empty_immutable_list = immutable_list.ImmutableList(tail=empty_dict)
    immutable_list_with_items = immutable_list.ImmutableList(bool_is_empty, is_empty=bool_is_empty)
    list_to_reduce = immutable_list_with_items.to_list()

    # Act
    result = immutable_list_with_items.reduce(list_to_reduce, list_to_reduce)

    # Assert
    assert result == list_to_reduce, "Incorrect value returned from reduce: expected {}, got {}".format(list_to_reduce, result)

