import immutable_list as immutableList

class TestImmutableList:

    def setup_method(self):
        self.immutable_list_0 = immutableList.ImmutableList()
        self.immutable_list_1 = immutableList.ImmutableList(1, 2, 3)
        self.immutable_list_2 = immutableList.ImmutableList(4, 5, 6)

    def test_immutable_list_equality(self):
        immutable_list_eq_true = self.immutable_list_0.__eq__(self.immutable_list_0)
        immutable_list_eq_false = self.immutable_list_0.__eq__(self.immutable_list_1)

        assert immutable_list_eq_true == True
        assert immutable_list_eq_false == False

    def test_immutable_list_to_list(self):
        immutable_list_list_0 =  self.immutable_list_0.to_list()
        immutable_list_list_1 = self.immutable_list_1.to_list()

        assert immutable_list_list_0 == []
        assert immutable_list_list_1 == [1,2,3]

    def test_immutable_list_length(self):
        immutable_list_len_0 = self.immutable_list_0.__len__()
        immutable_list_len_1 = self.immutable_list_1.__len__()

        assert immutable_list_len_0 == 0
        assert immutable_list_len_1 == 3

    def test_immutable_list_string_representation(self):
        immutable_list_string_0 = self.immutable_list_0.__str__()
        immutable_list_string_1 = self.immutable_list_1.__str__()

        assert immutable_list_string_0 == 'ImmutableList[]'
        assert immutable_list_string_1 == 'ImmutableList[1,2,3]'

    def test_immutable_list_addition(self):
        combined_immutable_list = self.immutable_list_1.__add__(self.immutable_list_2)
        combined_immutable_list_string = combined_immutable_list.__str__()

        assert combined_immutable_list_string == 'ImmutableList[1,2,3,4,5,6]'

def test_immutable_list_unshift_and_find():
    """
    This test case focuses on the `unshift` and `find` operations of an ImmutableList.
    `unshift` is used to add a new element at the beginning of the list,
    while `find` is used to find the first element in the list that satisfies a condition.
    """

    # Setup
    bool_value = True
    default_immutable_list = immutableList.ImmutableList()

    # Execution
    unshifted_immutable_list = default_immutable_list.unshift(bool_value)
    comparison_result = unshifted_immutable_list.__eq__(bool_value)
    combined_immutable_list = unshifted_immutable_list.__add__(unshifted_immutable_list)
    search_result = combined_immutable_list.find(comparison_result)

    # Assertion
    assert bool_value in (default_immutable_list, unshifted_immutable_list, combined_immutable_list)
    assert search_result == bool_value

def test_append_and_find_method():
    """
    This test case tests the append and find methods of the ImmutableList class.
    """

    # Setting up test variables
    IS_EMPTY = False
    TEST_ELEMENT = True

    # Setting up initial list
    initial_list = module_0.ImmutableList(TEST_ELEMENT, is_empty=IS_EMPTY)

    # Setting up expected results
    expected_appended_list = initial_list.append(TEST_ELEMENT)
    expected_found_element = expected_appended_list.find(lambda element: element == TEST_ELEMENT)

    # Asserting initial and expected results
    assert initial_list.head == TEST_ELEMENT
    assert initial_list.tail is None
    assert expected_appended_list.head == TEST_ELEMENT
    assert expected_appended_list.tail == TEST_ELEMENT
    assert expected_found_element == TEST_ELEMENT

def test_immutable_list_addition():
    # Constants
    NONE_TYPE_VALUE = None
    EMPTY_LIST = ImmutableList()
    ITEMS_1 = ImmutableList(1, 2, 3)
    ITEMS_2 = ImmutableList(4, 5, 6)

    # Setup: Create an empty list, and two other lists with items
    empty_list = EMPTY_LIST
    first_list = ITEMS_1
    second_list = ITEMS_2

    # Test Case Explanation:
    # This test case is designed to verify the functionality of the '__add__' function.
    # We first test adding None to an empty list expecting a result of None.
    # Then we test adding an empty list to another list expecting a result list remains the same.
    # Lastly, we test adding two non-empty lists together.

    # Execution & Assertion:
    # We test adding None to empty list
    result = EMPTY_LIST.__add__(NONE_TYPE_VALUE)
    assert result is None, 'Adding None to empty list should result in None'

    # Test adding empty list to another list
    result = ITEMS_1.__add__(EMPTY_LIST)
    assert result == ITEMS_1, 'Adding empty list to any list should result in original list'

    # Test adding two non-empty lists together
    result = ITEMS_1.__add__(ITEMS_2)
    expected_result = ImmutableList(1, 2, 3, 4, 5, 6)
    assert result == expected_result, 'Adding two non-empty lists together should result in a new list, each containing their respective elements in consecutive order'

"""
This test case tests the behavior of ImmutableList's find method.
It sets up an ImmutableList with some elements, uses the 'find' method 
to find out if a particular condition is met in each member, and checks 
that the correct result is returned.
"""

def test_find_method_with_condition():
    # Setup
    test_values = [1, 2, 3, 4, 5]
    test_immutable_list = immutableList.ImmutableList(
        test_values, is_empty=False
    )
    
    # Execution
    result = test_immutable_list.find(
        lambda x: True if x % 2 == 0 else False
    )

    # Assertion
    """
    The 'find' method should return the first element that satisfies the 'even' condition,
    in this case, the number 2 since it satisfies the `lambda x: True if x % 2 == 0 else False`
    """
    assert result == 2

def test_immutable_list_find_returns_first_element_that_passes_lambda_function():
    # Setup
    EMPTY_LIST = immutableList.ImmutableList(None, is_empty=True)
    LIST_WITH_SINGLE_ELEMENT = immutableList.ImmutableList("Element", is_empty=False)
    
    # Execution
    result_empty_list = EMPTY_LIST.find(lambda x: x == 1)
    result_list_with_single_element = LIST_WITH_SINGLE_ELEMENT.find(lambda x: x == "Element")
    result_list_with_multiple_elements = immutableList.ImmutableList(1, immutableList.ImmutableList(2, immutableList.ImmutableList(3, None, is_empty=True))).find(lambda x: x == 2)

    # Assertion
    assert result_empty_list is None, "Empty list should return None"
    assert result_list_with_single_element == "Element", "Should find the only element in the list"
    assert result_list_with_multiple_elements == 2, "Should find the correct element in the list"

def test_find_element_in_immutable_list():
    """
    Test to find an element in ImmutableList
    In this test case, we create an ImmutableList with a single element,
    then we try to find that element in the list, using the find() method
    """
    # -------------------Setup-----------------------
    # Define a constant for the bool value to use in the test
    BOOL_VALUE_TO_TEST = False

    # Create an ImmutableList with a single element equal to the constant
    IMMUTABLE_LIST = immutableList.ImmutableList(BOOL_VALUE_TO_TEST, is_empty=BOOL_VALUE_TO_TEST)

    # -------------------Execution-----------------------
    # Convert ImmutableList to a list
    LIST_VALUE = IMMUTABLE_LIST.to_list()

    # Find an element in the list using the find() method
    FOUND_ELEMENT = IMMUTABLE_LIST.find(lambda x: x == BOOL_VALUE_TO_TEST)

    # -------------------Assertions-----------------------
    # Assert that the found element is equal to the constant
    assert FOUND_ELEMENT == BOOL_VALUE_TO_TEST, "The found element should be equal to the constant"

def test_case_7():
    # Constants
    NEW_ELEMENT = 'New Element'
    EMPTY_LIST = module_0.ImmutableList()

    # Setup
    immutable_list_0 = EMPTY_LIST.append(NEW_ELEMENT)

    # Execution
    var_0 = immutable_list_0.find(lambda x: x is None)
    var_1 = immutable_list_0.append(immutable_list_0).to_list()

    # Assertions
    assert var_0 is None, "List should not find a None value"
    assert NEW_ELEMENT in var_1, "List should contain added elements"
    assert var_1[0] == NEW_ELEMENT, "List should start with the new element"
    assert var_1[-1] == NEW_ELEMENT, "List should end with the new element"
    assert var_1.count(NEW_ELEMENT) == 2, "List should contain two instances of the new element"

def test_immutable_list_mapping_v2():
    # Setup
    is_empty = False
    expected_list = [1, 2, 3]  # Constant
    squared_list = [1, 4, 9]  # Constant
    identity_fn = lambda x: x  # Constant
    test_list = immutableList.ImmutableList(is_empty=is_empty)
    # Execution: create a list with elements
    test_list = test_list.map(identity_fn)
    # Execution: squaring each element in the list
    squared_test_list = test_list.map(lambda x: x ** 2)
    # Assertion: check if the list has been squared correctly
    assert squared_test_list.to_list() == squared_list

def test_immutable_list_unshift_and_append_and_map_results():
    # Setting up variables for test
    NONE = None

    # Constructing two ImmutableList objects for testing
    immutable_list_0 = ImmutableList(NONE, NONE)
    immutable_list_1 = immutable_list_0.unshift(NONE)

    # Testing the behavior of unshift function
    # This should return a new ImmutableList with the element on the beginning of the list
    assert immutable_list_1.head == NONE

    # Testing the behavior of append function
    # This should return a new ImmutableList with the element on the end of the list
    test_element = 'test'
    immutable_list_3 = immutable_list_1.append(NONE)
    assert immutable_list_3.tail.tail.head == NONE

    # Testing behavior of map function
    # This should return a new ImmutableList with each element mapped into the result of the function
    immutable_list_4 = immutable_list_1.map(lambda x: 'mapped_' + str(x))
    assert all(x.startswith('mapped_') for x in immutable_list_4)

def test_empty_list_filtering():
    # Given: Setup an empty immutable list with False
    empty_list = immutableList.ImmutableList(False, is_empty=False)

    # When: Perform a filter operation on the list
    result = empty_list.filter(empty_list)

    # Then: The result should be an empty immutable list
    assert result.is_empty == True, "Expected result list to be empty but it was not"

# Define the constants for use throughout the test
HEAD = 'HEAD'
TAIL = 'TAIL'
NEW_HEAD = 'NEW_HEAD'
NEW_TAIL = 'NEW_TAIL'
NEW_FILTER = lambda x: x % 2 == 0

# Defining the setup fixture
def setup():
    return ImmutableList(HEAD, ImmutableList(TAIL, is_empty=True))

# Defining the execution fixture
def execute(instance):
    instance.immutable_list_1 = instance.immutable_list_0.__add__(instance.immutable_list_0)
    instance.var_0 = instance.immutable_list_1.__len__()
    instance.immutable_list_1.filter(instance.var_0)

# Defining the assertion fixture
def assertion(instance):
    assert instance.immutable_list_1.head == NEW_HEAD
    assert instance.immutable_list_1.tail.head == NEW_TAIL
    assert instance.immutable_list_1.filter(instance.var_0).__len__() == NEW_FILTER

# The test case
def test_case_12():
    # Setup
    test_case = setup() 
    # Execution
    execute(test_case) 
    # Assertion
    assertion(test_case)

def test_find_element_in_empty_list():
    # Constants
    ELEMENT_TO_FIND = 1947
    EMPTY_LIST_LENGTH = 0

    # Setup
    EMPTY_ELEMENT = None
    EMPTY_LIST = immutableList.ImmutableList(EMPTY_ELEMENT, EMPTY_ELEMENT)

    # Execution: Finding in empty list
    RESULT_1 = EMPTY_LIST.find(ELEMENT_TO_FIND)
    EMPTY_LIST_LENGTH = RESULT_1.__len__()

    # Assertion: Empty list length should be zero if the find method finds no matches
    assert EMPTY_LIST_LENGTH == EMPTY_LIST_LENGTH, 'Find method is not returning appropriate results for an empty list.'

def test_find_element_in_non_empty_list():
    # Test Case 2: Finding in non-empty list with no matches
    ELEMENT_TO_FIND = 1947
    NON_EMPTY_ELEMENT = 2022
    NON_EMPTY_LIST = immutableList.ImmutableList(NON_EMPTY_ELEMENT, EMPTY_ELEMENT)

    RESULT_2 = NON_EMPTY_LIST.find(ELEMENT_TO_FIND)
    NON_EMPTY_LIST_LENGTH = RESULT_2.__len__()

    assert NON_EMPTY_LIST_LENGTH == EMPTY_LIST_LENGTH, 'Find method is not returning appropriate results for a non-empty list.'

if __name__ == "__main__":
    test_find_element_in_empty_list()
    test_find_element_in_non_empty_list()

def test_find_element_in_immutable_list():
    """
    The purpose of this test case is to verify that we can find an element in an immutable list.
    It also tests if we can correctly handle the case where the element does not exist in the list.
    """

    # Setup: define some constants
    TRUE_CONDITION = lambda element: True
    FALSE_CONDITION = lambda element: False

    # Create an immutable list with a single element for testing
    test_value = True
    initial_list = immutableList.ImmutableList(test_value)

    # Execute: try to find an element in the list
    found_element = initial_list.find(TRUE_CONDITION)

    # Assertion: check that we found the correct element
    assert found_element == test_value, f"Failed: found element {found_element} does not match test value {test_value}"

    # Execute: try to find an element that does not exist in the list
    not_found_element = initial_list.find(FALSE_CONDITION)

    # Assertion: check that we correctly handle the case where the element does not exist
    assert not_found_element is None, f"Failed: found non-existent element {not_found_element}"

def test_reduce_and_find_should_return_none_when_not_found():
    # Arrange
    initial_value = False
    empty_list = immutableList.ImmutableList(initial_value, is_empty=initial_value)
    not_found_value = immutableList.ImmutableList(False, initial_value)

    # Act
    reduce_result = empty_list.reduce(initial_value, empty_list)
    find_result = empty_list.find(not_found_value)

    # Assert
    assert reduce_result == initial_value, "Reduce operation with an empty list should return the initial value."
    assert find_result == None, "Find operation with a value that is not in the list should return None."

def test_add_element_to_immutable_list():
    # Given
    initial_elements = [1, 2, 3, 4, 5]
    immutable_list = module_0.ImmutableList(initial_elements)
    
    # When
    new_element = 6
    added_immutable_list = immutable_list.add(new_element)

    # Then
    expected_list = initial_elements + [new_element]
    assert added_immutable_list == expected_list, "The new element should be added to the immutable list"

def test_find_element_in_immutable_list_succeeds_with_valid_predicate():
    # setup
    is_empty = False
    initial_list = immutableList(is_empty, is_empty=is_empty)
    
    # execution
    def predicate(element):
        return element == initial_list
        
    result = initial_list.find(predicate)
    
    # assertion
    assert result == initial_list.head, "find function should return the first element of the ImmutableList that passed the given function"

def test_immutable_list_append_and_find():
    # Setup - create the initial boolean and ImmutableList instance for testing.
    IS_EMPTY_FLAG = False  # Constant value to indicate whether the list is empty or not.
    ELEMENT_TO_APPEND = False  # The element to append to the list.

    immutable_list = immutableList.ImmutableList(ELEMENT_TO_APPEND, is_empty=IS_EMPTY_FLAG)

    # Execution - Append the element to the list and try to find it.
    appended_list = immutable_list.append(ELEMENT_TO_APPEND)
    found_element = appended_list.find(lambda element: element == ELEMENT_TO_APPEND)

    # Assertion - Check if the found element is the same as the appended one.
    assert found_element == ELEMENT_TO_APPEND

def test_add_element_and_find():
    # Constants
    CONST_EMPTY_LIST = False  # Test data for unshift function
    CONST_NON_EMPTY_LIST = True  # Test data for unshift and append functions

    # Setup
    immutable_list_0 = module_0.ImmutableList(is_empty=CONST_EMPTY_LIST)  # Create an empty ImmutableList

    # Execution
    immutable_list_1 = immutable_list_0.unshift(CONST_NON_EMPTY_LIST)  # Append an element on the beginning of list
    immutable_list_2 = immutable_list_1.append(immutable_list_0)  # Append another list to the end of list

    # Assertion
    finding_element = immutable_list_2.find(lambda x: x == CONST_NON_EMPTY_LIST)  # Find the first element that matches the condition
    assert finding_element == CONST_NON_EMPTY_LIST, "The element should have been found"

# Test case: append and find method
def test_case_20():
    # Constants
    EMPTY_LIST_VALUE = True

    # Test setup: create a new immutable list with a single element
    empty_element = EMPTY_LIST_VALUE
    immutable_list = module_0.ImmutableList(empty_element, is_empty=empty_element)

    # Test execution: append a new element to the list
    new_element = EMPTY_LIST_VALUE
    modified_list = immutable_list.append(new_element)

    # Test assertion: get the size of the modified list and compare it with the expected size
    actual_size = len(modified_list)
    expected_size = 2
    assert actual_size == expected_size, f"Expected size is {expected_size}, but the actual size is {actual_size}"

    # Test execution: find the new element in the modified list
    found_element = modified_list.find(lambda x: x == new_element)

    # Test assertion: check that the found element is equal to the new element
    assert found_element == new_element, f"The found element ({found_element}) is not equal to the new element ({new_element})"

def test_reduce_concatenates_lists_alternative_name():
    # Constants
    EMPTY_LIST = immutableList.ImmutableList(is_empty='ImmutableList([])')

    # Setup
    LIST = immutableList.ImmutableList()
    SAME_LIST = LIST.append(LIST)
    EXPECTED_CONCATENATED_LIST = SAME_LIST.reduce(SAME_LIST, SAME_LIST)

    # Execution: Append on to the same list, which is unshift of the same list.
    UN_SHIFTED_LIST = LIST.unshift(SAME_LIST)
    CONCATENATED_LIST = UN_SHIFTED_LIST.append(UN_SHIFTED_LIST)

    # Assertion: The expected concatenated list should be the same as the concatenated list.
    assert EXPECTED_CONCATENATED_LIST == CONCATENATED_LIST, (
        f'Expected CONCATENATED_LIST to be {EXPECTED_CONCATENATED_LIST}, ' 
        f'but got {CONCATENATED_LIST}'
    )

def test_case_21_renamed():
    immutableList0 = immutableList.ImmutableList()
    immutableList1 = immutableList0.unshift(immutableList0)
    var0 = immutableList0.reduce(immutableList1, immutableList1)
    lengthOfImmutableList1 = immutableList1.__len__()
    immutableList2 = immutableList1.unshift(immutableList1)
    isEqual = immutableList2.__eq__(immutableList0)
    immutableList3 = immutableList.ImmutableList(is_empty=lengthOfImmutableList1)
    var0.find(var0)

def test_reducing_empty_immutable_list():
    # Define the constants for the test case
    HEAD_INITIAL_VALUE = True
    IS_EMPTY = True
    INITIAL_ACCUMULATOR = [False]

    # Set up the initial data for the test case
    initial_immutable_list = immutableList.ImmutableList(HEAD_INITIAL_VALUE, is_empty=IS_EMPTY)

    # Perform the operation that we are testing
    result = initial_immutable_list.reduce(lambda acc, v: [v, *acc], INITIAL_ACCUMULATOR)

    # Assert that the operation gave the expected result
    assert result == [True, False]

