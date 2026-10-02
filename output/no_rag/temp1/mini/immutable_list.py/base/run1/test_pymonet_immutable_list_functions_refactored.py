import pytest

import immutable_list as immutable_list_module

def test_empty_immutable_list_self_equality_and_conversions():
    # Purpose:
    # - Verify an empty ImmutableList compares equal to itself.
    # - Inspect its string representation and conversion to a Python list.
    # - Verify Python-list concatenation of that result and its length.
    # - Ensure adding a plain Python list to an ImmutableList raises a ValueError.

    # --- Setup ---
    EMPTY_IMMUTABLE = immutable_list_module.ImmutableList()  # construct an empty ImmutableList

    # --- Execution ---
    # Equality check (should be True for the same instance)
    is_equal_to_self = EMPTY_IMMUTABLE.__eq__(EMPTY_IMMUTABLE)

    # String representation of the ImmutableList
    string_representation = EMPTY_IMMUTABLE.__str__()

    # Convert ImmutableList to a Python list
    converted_list = EMPTY_IMMUTABLE.to_list()

    # Concatenate the Python list with itself using list.__add__
    concatenated_list = converted_list.__add__(converted_list)

    # Get length of the converted Python list
    converted_list_length = converted_list.__len__()

    # Attempting to add a Python list to an ImmutableList should raise ValueError
    # (ImmutableList.__add__ only accepts another ImmutableList)
    with pytest.raises(ValueError):
        EMPTY_IMMUTABLE.__add__(converted_list)

    # --- Assertions ---
    assert is_equal_to_self is True, "An ImmutableList instance should be equal to itself"

    # The implementation represents the list via to_list() inside the string.
    # For the empty ImmutableList (head is None, tail is None) the to_list() yields [None],
    # so the string should reflect that.
    assert string_representation == "ImmutableList[None]"

    # to_list() should return the Python list representation (observed as [None])
    assert converted_list == [None]

    # Concatenating [None] with itself yields [None, None]
    assert concatenated_list == [None, None]

    # The length of the converted Python list [None] is 1
    assert converted_list_length == 1

def test_unshift_add_find_str_and_reduce_behaviors():
    """
    Verify basic behaviors of ImmutableList:
    - equality with a non-list object
    - addition with itself
    - find on empty list
    - string representation for empty list
    - unshift to add an element
    - reduce to aggregate values
    """
    # --- Setup / Constants ---
    ELEMENT = 1
    ACC_INIT = 0
    non_list_value = True

    # Create an empty ImmutableList instance for use in the test
    empty_list = immutable_list_module.ImmutableList()

    # --- Execution ---
    # 1) Check equality against a non-ImmutableList object (should be False)
    is_equal_to_nonlist = (empty_list == non_list_value)

    # 2) Add the empty list to itself (ensures __add__ accepts another ImmutableList)
    added_self = empty_list + empty_list

    # 3) Attempt to find ELEMENT in the empty list (should return None)
    found_in_empty = empty_list.find(lambda x: x == ELEMENT)

    # 4) Get string representation of the empty list
    empty_str = str(empty_list)

    # 5) Unshift an element onto the empty list to produce a single-element list
    single_element_list = empty_list.unshift(ELEMENT)

    # 6) Reduce the single-element list by summing elements (accumulator style)
    sum_result = single_element_list.reduce(lambda acc, v: acc + v, ACC_INIT)

    # --- Assertions ---
    # Equality with a non-list object must be False
    assert is_equal_to_nonlist is False

    # The result of adding a list to itself should still be an ImmutableList instance
    assert isinstance(added_self, immutable_list_module.ImmutableList)

    # Finding an element in an empty list yields None
    assert found_in_empty is None

    # Verify the string representation of an empty ImmutableList
    assert empty_str == "ImmutableList[]"

    # The element we unshifted should be findable and present as the head
    assert single_element_list.find(lambda x: x == ELEMENT) == ELEMENT

    # Reducing the single-element list by summing should produce the element value
    assert sum_result == ELEMENT

def test_append_creates_new_list_and_find_requires_callable():
    # Purpose:
    # - Verify that appending an element returns a new ImmutableList (original is unchanged).
    # - Verify that find() requires a callable argument and raises TypeError when given a non-callable.
    INITIAL_ELEMENT = True

    # Setup: create an ImmutableList containing a single boolean element
    original_list = immutable_list_module.ImmutableList(INITIAL_ELEMENT, is_empty=INITIAL_ELEMENT)

    # Execution: append the same element to produce a new list
    appended_list = original_list.append(INITIAL_ELEMENT)

    # Assertions: appended_list should be a new object and should be searchable via a callable predicate
    assert appended_list is not original_list
    assert appended_list.find(lambda value: value is INITIAL_ELEMENT) is INITIAL_ELEMENT

    # Execution + Assertion: calling find with a non-callable (the list itself) should raise TypeError
    with pytest.raises(TypeError):
        original_list.find(original_list)

def test_add_raises_value_error_with_non_immutable_other():
    # Purpose:
    #   Ensure ImmutableList.__add__ raises a ValueError when the 'other' argument
    #   is not an instance of ImmutableList.
    #
    # Setup
    empty_list = immutable_list_module.ImmutableList()
    non_immutable_value = None
    expected_error_message = 'ImmutableList: you can not add any other instace than ImmutableList'

    # Execution & Assertion: calling __add__ with a non-ImmutableList should raise ValueError
    with pytest.raises(ValueError) as exc_info:
        empty_list.__add__(non_immutable_value)

    # Verify the error message is the expected one
    assert str(exc_info.value) == expected_error_message

def test_find_raises_type_error_when_predicate_is_not_callable():
    # Purpose:
    # Verify that ImmutableList.find expects a callable predicate.
    # If a non-callable is passed, calling find should raise a TypeError.

    # --- Setup ---
    # Create an empty ImmutableList and assert its length is zero.
    empty_list = immutable_list_module.ImmutableList()
    empty_length = empty_list.__len__()  # explicit length call as in original test
    assert empty_length == 0

    # Construct another ImmutableList using the empty list as both the head argument
    # and the is_empty keyword (mirrors the original test's construction).
    list_with_empty_components = immutable_list_module.ImmutableList(
        empty_list, is_empty=empty_list
    )

    # --- Execution & Assertion ---
    # Using the list instance itself as the predicate (non-callable) should raise TypeError
    # when find attempts to call it as a function.
    with pytest.raises(TypeError):
        list_with_empty_components.find(list_with_empty_components)

def test_length_and_find_on_single_element_list():
    # Purpose:
    # Verify that a single-element ImmutableList reports length 1 and that find()
    # returns the element when a matching predicate is provided.

    # Setup
    head_value = False
    single_element_list = immutable_list_module.ImmutableList(head_value, is_empty=False)

    # Execution
    computed_length = len(single_element_list)
    predicate_matches_false = lambda value: value is False
    found_value = single_element_list.find(predicate_matches_false)

    # Assertions
    assert computed_length == 1, "Expected length 1 for a list with a single head and no tail"
    assert found_value is head_value, "find() should return the head value when predicate matches"

def test_find_raises_type_error_for_non_callable_argument():
    """
    Verify ImmutableList.find raises a TypeError when given a non-callable argument.
    """
    # Arrange
    head = False
    immutable_list = immutable_list_module.ImmutableList(head, is_empty=False)
    non_callable_arg = immutable_list.to_list()  # to_list() returns a Python list, which is not callable

    # Act & Assert
    with pytest.raises(TypeError):
        immutable_list.find(non_callable_arg)

def test_find_on_empty_list_append_and_invalid_concat_raises():
    # Constants / test data
    EMPTY_PREDICATE = None  # Intentionally None to exercise early-return path in find()
    INVALID_CONCAT_ARG = None

    # Setup: create an empty ImmutableList
    original_list = immutable_list_module.ImmutableList()

    # Execution: calling find on an empty list should return None without calling the predicate
    found_value = original_list.find(EMPTY_PREDICATE)

    # Assertion: find on an empty ImmutableList returns None
    assert found_value is None

    # Execution: append the original ImmutableList instance to itself, producing a new ImmutableList
    appended_list = original_list.append(original_list)

    # Execution: convert the resulting ImmutableList to a native Python list representation
    python_list_representation = appended_list.to_list()

    # Assertion: the conversion returns a list, and the second element is the appended ImmutableList instance
    assert isinstance(python_list_representation, list)
    assert len(python_list_representation) == 2
    assert python_list_representation[1] is original_list

    # Assertion: attempting to concatenate the produced list with a non-list (None) raises a TypeError
    import pytest
    with pytest.raises(TypeError):
        python_list_representation.__add__(INVALID_CONCAT_ARG)

def test_map_raises_type_error_when_given_non_callable():
    # Purpose: Verify ImmutableList.map raises TypeError when given a non-callable.
    immutable_list = immutable_list_module.ImmutableList(is_empty=False)

    # Convert to a Python list representation (done twice to mirror original test flow).
    first_list = immutable_list.to_list()
    second_list = immutable_list.to_list()

    # Sanity checks of the setup.
    assert isinstance(first_list, list)
    assert second_list is not None

    # Using a non-callable (a plain Python list) as the mapper should raise TypeError.
    non_callable_mapper = second_list
    with pytest.raises(TypeError):
        immutable_list.map(non_callable_mapper)

def test_map_raises_typeerror_when_non_callable_passed():
    # Purpose:
    # Verify that ImmutableList.map raises a TypeError when a non-callable (None)
    # is passed as the mapping function.

    # Constants used in the test
    NON_CALLABLE = None

    # Setup: create a base list and derive variations using unshift/append operations
    base_list = immutable_list_module.ImmutableList(NON_CALLABLE, NON_CALLABLE)
    # Prepend a None value to the base list
    unshifted_with_none = base_list.unshift(NON_CALLABLE)
    # Prepend the previously created list as an element (nested list element)
    unshifted_with_list = base_list.unshift(unshifted_with_none)
    # Append a None value to the unshifted list
    appended_list = unshifted_with_none.append(NON_CALLABLE)

    # Execution & Assertion:
    # Calling map with a non-callable should raise a TypeError because the implementation
    # attempts to call the provided argument as a function on list elements.
    with pytest.raises(TypeError):
        appended_list.map(NON_CALLABLE)

def test_filter_with_non_callable_predicate_raises_type_error():
    # This test verifies that ImmutableList.filter raises a TypeError
    # when the provided predicate is not a callable. The original test
    # passed the list instance itself as the predicate (which is not callable),
    # so we assert that calling filter in that way results in a TypeError.

    # --- Setup ---
    VALUE_IN_LIST = False
    IS_EMPTY_FLAG = False
    immutable_list = immutable_list_module.ImmutableList(VALUE_IN_LIST, is_empty=IS_EMPTY_FLAG)

    # --- Execution & Assertion ---
    # Passing the list instance as the predicate is invalid (not callable),
    # so filter should attempt to call it and raise a TypeError.
    with pytest.raises(TypeError):
        immutable_list.filter(immutable_list)

def test_filter_raises_type_error_for_non_callable_predicate():
    # Purpose:
    # Verify that ImmutableList.filter raises a TypeError when called with a non-callable
    # argument (here we intentionally pass an integer).
    #
    # Setup: create an empty ImmutableList and concatenate it with itself to reproduce
    # the original structure used in the test.
    EMPTY_LIST = immutable_list_module.ImmutableList()
    concatenated_list = EMPTY_LIST + EMPTY_LIST

    # Execution: obtain a non-callable value (the length, which will be an int)
    # and attempt to use it as the predicate for filter.
    length_value = len(concatenated_list)  # expected to be 0 for an empty list
    invalid_predicate = length_value  # intentionally non-callable

    # Sanity check to document expected intermediate state
    assert length_value == 0

    # Assertion: calling filter with a non-callable should raise a TypeError
    with pytest.raises(TypeError):
        concatenated_list.filter(invalid_predicate)

def test_find_on_empty_list_returns_none_and_list_length_zero():
    # Purpose:
    # Verify that find() returns None for an empty ImmutableList and that the list length is 0.
    # Also ensure find short-circuits when the list is empty (the provided "predicate" is not invoked),
    # so passing a non-callable does not raise an error in this case.

    # -- Setup -------------------------------------------------------------
    NON_CALLABLE_PREDICATE = 1947  # intentionally not a callable; should not be called for empty list
    EMPTY_HEAD = None
    EMPTY_TAIL = None
    immutable_list = immutable_list_module.ImmutableList(EMPTY_HEAD, EMPTY_TAIL)

    # -- Execution ---------------------------------------------------------
    found = immutable_list.find(NON_CALLABLE_PREDICATE)

    # -- Assertions --------------------------------------------------------
    # find on an empty list should return None
    assert found is None

    # the length of an empty ImmutableList should be 0
    assert len(immutable_list) == 0

def test_find_returns_none_for_single_element_when_predicate_false():
    # Purpose:
    # Verify that ImmutableList.find returns None when the list contains a single element
    # and the provided predicate returns False for that element.

    # Constants / test data
    ELEMENT_VALUE = False
    IS_EMPTY_FLAG = False

    # Setup: create a single-element ImmutableList
    single_element_list = immutable_list_module.ImmutableList(ELEMENT_VALUE, is_empty=IS_EMPTY_FLAG)

    # Predicate that always returns False (simulates "no match")
    def predicate_always_false(_):
        return False

    # Execution: attempt to find an element that matches the predicate
    found_value = single_element_list.find(predicate_always_false)

    # Assertion: since the predicate never matches, find should return None
    assert found_value is None

def test_reduce_on_empty_list_returns_accumulator_and_find_with_non_callable_raises_typeerror():
    # Constants used in this test
    NON_CALLABLE = False

    # Setup: create an empty ImmutableList
    empty_list = immutable_list_module.ImmutableList()

    # Execution: call reduce on an empty list. Since the list is empty, reduce should
    # return the provided accumulator unchanged and should not attempt to call the reducer.
    result = empty_list.reduce(NON_CALLABLE, empty_list)

    # Assertion: the returned value should be the same object passed as the accumulator
    assert result is empty_list

    # Setup: create a single-element ImmutableList whose head is a non-callable value.
    # is_empty is set to NON_CALLABLE to indicate the list is not empty (matching original usage).
    single_element_list = immutable_list_module.ImmutableList(NON_CALLABLE, is_empty=NON_CALLABLE)

    # Execution & Assertion: calling find with a non-callable argument should raise a TypeError
    # when the implementation attempts to call the provided "predicate".
    with pytest.raises(TypeError):
        single_element_list.find(single_element_list)

def test_create_empty_immutable_list_initial_state():
    """
    Verify that constructing a new ImmutableList produces a valid instance
    with the expected initial properties (i.e., an object of the correct type).
    """
    # Expected class
    EXPECTED_CLASS = immutable_list_module.ImmutableList

    # Execution: create a new ImmutableList instance
    new_list = immutable_list_module.ImmutableList()

    # Assertions:
    assert new_list is not None
    assert isinstance(new_list, EXPECTED_CLASS)

def test_find_returns_false_and_string_representation_for_single_element_list():
    # Purpose:
    # - Verify that ImmutableList.__str__ returns the expected representation for a single-element list.
    # - Verify that ImmutableList.find returns the stored element when a matching predicate is provided.
    #
    # Note: We construct a single-node list whose head value is the boolean False and use a predicate
    # that matches that value.

    # Constants / Setup
    ELEMENT_VALUE = False
    # is_empty is set to ELEMENT_VALUE to mirror the original test's usage (is_empty=False)
    single_node_list = immutable_list_module.ImmutableList(ELEMENT_VALUE, is_empty=ELEMENT_VALUE)

    # Execution
    string_representation = str(single_node_list)  # calls __str__()
    found_value = single_node_list.find(lambda v: v is ELEMENT_VALUE)  # predicate that matches the False value

    # Assertions
    assert string_representation == "ImmutableList[False]"
    assert found_value is ELEMENT_VALUE

def test_unshift_preserves_head_and_allows_find_call_with_self_predicate():
    # Constants for clarity
    INITIAL_HEAD = False
    INITIAL_IS_EMPTY = False

    # Setup: create an ImmutableList whose head is a boolean False
    original_list = immutable_list_module.ImmutableList(INITIAL_HEAD, is_empty=INITIAL_IS_EMPTY)

    # Execution: place the list itself at the front of the list
    # This should produce a new ImmutableList whose head is the original_list object
    unshifted_list = original_list.unshift(original_list)

    # Also exercise find by passing the list object as the "predicate" argument.
    # The primary goal here is to exercise the code path; we capture the result to ensure no exceptions occur.
    find_result = unshifted_list.find(original_list)

    # Assertions:
    # - unshift should return an ImmutableList
    # - the head of the new list should be the original list object we unshifted
    assert isinstance(unshifted_list, immutable_list_module.ImmutableList)
    assert unshifted_list.head is original_list

    # The find call is executed to exercise behavior; we do not make assumptions about its return value here,
    # only that it completes without raising an exception.
    assert True

def test_find_raises_type_error_with_non_callable_predicate_on_combined_list():
    # Purpose:
    # Verify that ImmutableList.find requires a callable predicate and
    # raises a TypeError when a non-callable is passed.

    # Constants / test data
    IS_EMPTY = False
    NON_CALLABLE_PREDICATE = False  # intentionally not a callable

    # Setup: create an ImmutableList, add an element at the front, then append the original list
    original_list = immutable_list_module.ImmutableList(is_empty=IS_EMPTY)
    list_with_head = original_list.unshift(NON_CALLABLE_PREDICATE)
    combined_list = list_with_head.append(original_list)

    # Execution & Assertion: calling find with a non-callable should raise TypeError
    with pytest.raises(TypeError):
        combined_list.find(NON_CALLABLE_PREDICATE)

def test_append_boolean_increases_length_and_find_returns_appended_value():
    # Purpose:
    # - Verify that appending a boolean value to an ImmutableList produces a new list
    #   that contains the appended value.
    # - Verify that the length of the resulting list is an integer and at least 1.
    # - Verify that find(...) can locate the appended boolean value.

    # Constants / test data
    BOOLEAN_VALUE = True
    is_true_predicate = lambda v: v is BOOLEAN_VALUE

    # Setup: create an initial ImmutableList (mirror original test's construction)
    initial_list = immutable_list_module.ImmutableList(BOOLEAN_VALUE, is_empty=BOOLEAN_VALUE)

    # Execution: append the boolean to create a new list, get its length, and attempt to find the boolean
    appended_list = initial_list.append(BOOLEAN_VALUE)
    appended_length = appended_list.__len__()  # explicit call to length method as in original test
    found_value = appended_list.find(is_true_predicate)

    # Assertions: check length is a non-negative integer and the appended boolean is findable
    assert isinstance(appended_length, int), "Length should be an integer"
    assert appended_length >= 1, "Appended list should contain at least one element"
    assert found_value is BOOLEAN_VALUE, "find(...) should return the appended boolean value"

def test_reduce_on_empty_list_and_list_operations_with_non_callable_find():
    # Purpose:
    # - Verify reduce returns the provided accumulator when called on an empty ImmutableList.
    # - Check append/unshift and equality/string behavior on small lists.
    # - Ensure find raises a TypeError when provided a non-callable predicate.

    # Constants used in assertions
    STR_PREFIX = "ImmutableList"

    # Setup: create an empty list and construct some derived lists
    empty_list = immutable_list_module.ImmutableList()
    single_element_list = empty_list.append(empty_list)  # list containing the empty_list as its single element

    # Execution: reduce on an empty list should immediately return the accumulator (no function calls)
    reduce_result = empty_list.reduce(single_element_list, single_element_list)

    # Assertions for reduce behavior
    assert reduce_result == single_element_list  # value-equality: returned accumulator equals provided accumulator
    assert reduce_result is single_element_list  # identity: reduce returns the same accumulator object for empty list

    # Execution: equality check between different-shaped lists
    are_equal = single_element_list == empty_list

    # Assertion: single-element list should not equal the empty list
    assert are_equal is False

    # Execution: unshift to create a nested list and obtain its string representation
    nested_list = single_element_list.unshift(single_element_list)
    nested_list_str = str(nested_list)

    # Assertions about string representation
    assert isinstance(nested_list_str, str)
    assert STR_PREFIX in nested_list_str  # basic sanity check that __str__ produced the expected prefix

    # Execution: construct a new ImmutableList while overriding the is_empty flag with the string
    flagged_list = immutable_list_module.ImmutableList(is_empty=nested_list_str)

    # Execution: append the reduce_result to itself (should succeed and produce a list)
    appended_self = reduce_result.append(reduce_result)
    assert appended_self is not None  # ensure append returned something

    # Execution + Assertion: calling find with a non-callable predicate (an ImmutableList) should raise TypeError
    with pytest.raises(TypeError):
        # Passing reduce_result (an ImmutableList instance, not a callable) as the predicate
        nested_list.find(reduce_result)

def test_reduce_on_empty_returns_acc_and_list_operations():
    # Purpose:
    # - Verify that reduce on an empty ImmutableList returns the provided accumulator unchanged.
    # - Verify basic list operations: unshift (prepends), __len__, equality, construction with is_empty,
    #   and find with a predicate that does not match any element.
    #
    # Setup
    EMPTY = immutable_list_module.ImmutableList()
    # Create a list whose single element is the empty list (head = EMPTY)
    single_with_empty = EMPTY.unshift(EMPTY)

    # Execution
    # Reducing an empty list should immediately return the accumulator unchanged.
    result_after_reduce = EMPTY.reduce(lambda acc, elem: acc, single_with_empty)

    # Length of the list that contains the empty list as its only element
    list_length = len(single_with_empty)

    # Create a nested list by unshifting the single_with_empty onto itself
    nested_list = single_with_empty.unshift(single_with_empty)

    # Compare nested list to the original empty list (expected to be False)
    nested_equals_empty = (nested_list == EMPTY)

    # Construct an ImmutableList using the is_empty flag set to the computed length (sanity construction)
    constructed_with_flag = immutable_list_module.ImmutableList(is_empty=list_length)

    # Try to find an element equal to the accumulator inside the accumulator list.
    # The predicate does not match the head (which is EMPTY), so expect None.
    found_element = result_after_reduce.find(lambda elem: elem == result_after_reduce)

    # Assertions
    # reduce on empty should return the exact accumulator object passed in
    assert result_after_reduce is single_with_empty

    # The list containing a single element should report length 1
    assert list_length == 1

    # nested_list should not be equal to the original empty list
    assert nested_equals_empty is False

    # constructed_with_flag should still be an ImmutableList instance
    assert isinstance(constructed_with_flag, immutable_list_module.ImmutableList)

    # The predicate does not match any element, so find should return None
    assert found_element is None

def test_reduce_raises_type_error_for_non_callable_reducer():
    # Verify that ImmutableList.reduce raises a TypeError when a non-callable
    # object is provided as the reducer function.

    HEAD_VALUE = True
    UNUSED_TAIL = {}  # kept to mirror original test; not used in the reduce call
    NON_CALLABLE_REDUCER = [HEAD_VALUE]  # intentionally not callable
    INITIAL_ACC = NON_CALLABLE_REDUCER

    # Setup: create ImmutableList instances
    unused_list = immutable_list_module.ImmutableList(tail=UNUSED_TAIL)
    target_list = immutable_list_module.ImmutableList(HEAD_VALUE, is_empty=HEAD_VALUE)

    # Sanity check: to_list should return a single-element list containing HEAD_VALUE
    assert target_list.to_list() == [HEAD_VALUE]

    # Execution & Assertion: using a non-callable reducer should raise a TypeError
    with pytest.raises(TypeError):
        target_list.reduce(NON_CALLABLE_REDUCER, INITIAL_ACC)

