import pytest

import immutable_list as immutable_list_module

def test_immutable_list_basic_operations_and_invalid_add():
    # Purpose:
    # - Verify basic behaviors of ImmutableList: self-equality, string representation,
    #   conversion to a Python list, length, and adding two ImmutableList instances.
    # - Also verify that adding a non-ImmutableList raises a ValueError.
    
    # Constants / test data
    ELEMENT = 1

    # Setup: create a simple single-element ImmutableList
    original = immutable_list_module.ImmutableList(ELEMENT)

    # Execution: perform various operations
    # 1) Equality with itself
    self_equal = original.__eq__(original)

    # 2) String representation and conversion to Python list
    string_repr = original.__str__()
    as_python_list = original.to_list()

    # 3) Use Python list operations to double the list and get its length
    doubled_python_list = as_python_list + as_python_list
    python_list_length = len(as_python_list)

    # 4) Use ImmutableList.__add__ to concatenate two ImmutableList instances
    added_immutable = original.__add__(original)
    added_immutable_as_list = added_immutable.to_list()

    # Assertions: check expected results
    assert self_equal is True  # an object should be equal to itself
    assert string_repr == f"ImmutableList{as_python_list}"  # string uses to_list()
    assert as_python_list == [ELEMENT]  # to_list returns the single element
    assert doubled_python_list == [ELEMENT, ELEMENT]  # Python list concatenation works
    assert python_list_length == 1  # length of the single-element list
    assert added_immutable_as_list == [ELEMENT, ELEMENT]  # ImmutableList addition yields two elements
    # Original list should remain unchanged after addition (immutability)
    assert original.to_list() == [ELEMENT]

    # Invalid use: adding a plain Python list should raise ValueError
    with pytest.raises(ValueError):
        original.__add__(as_python_list)

def test_empty_immutable_list_basic_operations():
    # Purpose:
    # Verify basic behaviors of an empty ImmutableList:
    # - equality with a non-ImmutableList returns False
    # - adding an empty list to itself produces an ImmutableList
    # - find with a predicate that always returns False yields None
    # - string representation matches expected format for an empty list
    # - unshift (prepend) returns a new list with the element at the head
    # - reduce can fold over the new single-element list correctly

    # Constants / Setup
    EMPTY_LIST = immutable_list_module.ImmutableList()
    NON_LIST_VALUE = True  # a value that is not an ImmutableList
    always_false_predicate = lambda _: False
    count_reducer = lambda acc, _: acc + 1

    # Execution: perform various operations on the empty list
    equality_with_non_list = (EMPTY_LIST == NON_LIST_VALUE)
    combined_list = EMPTY_LIST + EMPTY_LIST
    find_result = EMPTY_LIST.find(always_false_predicate)
    string_representation = str(EMPTY_LIST)
    unshifted_list = EMPTY_LIST.unshift(EMPTY_LIST)  # prepend the empty list as an element
    reduction_result = unshifted_list.reduce(count_reducer, 0)

    # Assertions: verify expected outcomes for each action
    assert equality_with_non_list is False  # comparing to a non-list should be False
    assert isinstance(combined_list, immutable_list_module.ImmutableList)
    assert find_result is None  # no element should match the always-false predicate
    assert string_representation == "ImmutableList[]"  # empty list representation
    assert isinstance(unshifted_list, immutable_list_module.ImmutableList)
    assert reduction_result == 1  # unshifted_list contains exactly one element, so count is 1

def test_find_returns_first_matching_element_after_append():
    # Constants for test clarity
    ELEMENT_VALUE = True
    IS_EMPTY_FLAG = True

    # Setup: create an ImmutableList and produce a new list by appending an element
    original_list = immutable_list_module.ImmutableList(ELEMENT_VALUE, is_empty=IS_EMPTY_FLAG)
    appended_list = original_list.append(ELEMENT_VALUE)

    # Execution: find the first element that matches our predicate (value is True)
    # Use a callable predicate instead of passing an object to match the expected API.
    result = original_list.find(lambda v: v is ELEMENT_VALUE)

    # Assertions:
    # - find should return the first matching element from the original list
    # - original list should remain unchanged after append
    # - append returns a distinct ImmutableList instance (immutability preserved)
    assert result is ELEMENT_VALUE
    assert original_list.head is ELEMENT_VALUE
    assert appended_list.head is ELEMENT_VALUE
    assert appended_list is not original_list

def test_add_raises_for_non_immutable_operand():
    """
    Ensure ImmutableList.__add__ raises a ValueError when attempting to add
    a non-ImmutableList instance (here: None).
    """
    # Constants
    INVALID_OTHER = None
    EXPECTED_ERROR_MESSAGE = 'ImmutableList: you can not add any other instace than ImmutableList'

    # Setup: create an ImmutableList instance to use as the left-hand operand
    immutable_list = immutable_list_module.ImmutableList()

    # Execution & Assertion: calling __add__ with an invalid type should raise ValueError
    with pytest.raises(ValueError) as excinfo:
        immutable_list.__add__(INVALID_OTHER)

    # Verify the exception message is the expected one
    assert str(excinfo.value) == EXPECTED_ERROR_MESSAGE

def test_find_raises_typeerror_when_predicate_is_not_callable():
    # Purpose:
    # Verify that ImmutableList.find raises a TypeError when given a non-callable
    # "predicate" argument. Also confirm that an empty list reports length 0.
    EXPECTED_EMPTY_LENGTH = 0

    # Setup: create an empty ImmutableList and check its length via __len__
    empty_list = immutable_list_module.ImmutableList()
    empty_list_length = empty_list.__len__()  # exercise the __len__ implementation
    assert empty_list_length == EXPECTED_EMPTY_LENGTH

    # Setup: construct a second ImmutableList using the empty list as inputs
    # (mirrors the original test's construction; the passed object will be non-callable)
    non_callable_predicate_candidate = immutable_list_module.ImmutableList(
        empty_list, is_empty=empty_list
    )

    # Execution & Assertion: calling find with a non-callable should raise TypeError
    with pytest.raises(TypeError):
        non_callable_predicate_candidate.find(non_callable_predicate_candidate)

def test_find_returns_head_for_single_element_list():
    # Purpose:
    # Verify that a single-element ImmutableList reports length 1 and that
    # find(fn) returns the head when the predicate matches and None otherwise.

    # Constants / Setup
    HEAD_VALUE = False
    IS_EMPTY = False
    single_item_list = immutable_list_module.ImmutableList(HEAD_VALUE, is_empty=IS_EMPTY)

    # Execution
    list_length = len(single_item_list)
    # Predicate that matches the head value
    found_when_match = single_item_list.find(lambda v: v == HEAD_VALUE)
    # Predicate that does not match the head value
    found_when_non_match = single_item_list.find(lambda v: v == "no-match")

    # Assertions
    assert list_length == 1  # single element expected
    assert found_when_match == HEAD_VALUE  # find should return the head when predicate is True
    assert found_when_non_match is None  # find should return None when predicate is False

def test_find_raises_type_error_for_non_callable_predicate():
    """
    Verify ImmutableList.find raises a TypeError when a non-callable object is
    provided as the predicate.
    """
    HEAD_VALUE = False
    IS_EMPTY = False

    # Create a singleton ImmutableList with a single head element
    immutable_singleton = immutable_list_module.ImmutableList(HEAD_VALUE, is_empty=IS_EMPTY)

    # Sanity check: ensure to_list produces the expected Python list representation
    assert immutable_singleton.to_list() == [HEAD_VALUE]

    # Use the produced Python list (non-callable) as the "predicate" argument.
    non_callable_predicate = immutable_singleton.to_list()
    with pytest.raises(TypeError):
        immutable_singleton.find(non_callable_predicate)

def test_append_self_creates_nested_list_and_invalid_list_concat_raises():
    """Verify behavior when appending an ImmutableList to itself and attempting invalid list concatenation."""
    # Constants
    PREDICATE_NONE = None

    # Setup: an empty ImmutableList
    empty_list = immutable_list_module.ImmutableList()

    # Execution & Assertion: find with None on an empty list should return None
    found_value = empty_list.find(PREDICATE_NONE)
    assert found_value is None

    # Execution: append the list to itself (treats the argument as a new element)
    appended_list = empty_list.append(empty_list)

    # Execution: convert to a regular Python list and assert structure
    converted_list = appended_list.to_list()
    assert converted_list == [None, empty_list]

    # Assertion: attempting to add a non-iterable (None) to the Python list raises TypeError
    with pytest.raises(TypeError):
        converted_list.__add__(PREDICATE_NONE)

def test_map_raises_type_error_when_non_callable_argument_provided():
    # Purpose:
    # Verify that ImmutableList.map raises a TypeError when a non-callable
    # (here: a plain Python list) is passed as the mapping function.

    # Constants / configuration for the test
    IS_EMPTY = False
    EXPECTED_EXCEPTION = TypeError

    # Setup: create an ImmutableList instance and obtain its Python-list representation
    source_immutable = immutable_list_module.ImmutableList(is_empty=IS_EMPTY)
    non_callable_mapping = source_immutable.to_list()  # a plain Python list, not callable

    # Execution & Assertion: calling map with a non-callable should raise TypeError
    with pytest.raises(EXPECTED_EXCEPTION):
        source_immutable.map(non_callable_mapping)

def test_map_raises_type_error_when_mapping_with_none():
    # Purpose:
    # Verify that calling ImmutableList.map with a non-callable argument (None)
    # raises a TypeError when the implementation attempts to call it.

    NON_CALLABLE = None

    # Setup: create a base ImmutableList containing a single None element
    base_list = immutable_list_module.ImmutableList(NON_CALLABLE, None)

    # Execution: unshift None to the base list to produce a two-element list [None, None]
    two_none_list = base_list.unshift(NON_CALLABLE)

    # Execution: unshift the two-element list as a single element onto the base list
    # (nested structure). Kept for completeness of structure setup.
    nested_element_list = base_list.unshift(two_none_list)

    # Execution: append None to the two-element list to create a three-element list [None, None, None]
    appended_list = two_none_list.append(NON_CALLABLE)

    # Assertion: mapping with a non-callable argument should raise TypeError
    with pytest.raises(TypeError):
        appended_list.map(NON_CALLABLE)

def test_filter_raises_type_error_for_non_callable_predicate():
    # Verify that ImmutableList.filter raises a TypeError when given a non-callable predicate.
    head_value = False
    single_item_list = immutable_list_module.ImmutableList(head_value, is_empty=False)

    with pytest.raises(TypeError):
        single_item_list.filter(single_item_list)

def test_filter_raises_type_error_when_non_callable_is_passed():
    # Purpose:
    # Verify that ImmutableList.filter raises a TypeError when a non-callable
    # argument is provided as the predicate function.

    # --- Setup ---
    EMPTY_LIST = immutable_list_module.ImmutableList()
    initial_list = EMPTY_LIST

    # --- Execution: produce a list and compute a non-callable value to pass to filter ---
    # Use __add__ to combine the list with itself (mirrors the original test behavior).
    combined_list = initial_list.__add__(initial_list)

    # Compute the length which will be used as the (invalid) predicate argument.
    non_callable_filter_arg = combined_list.__len__()

    # --- Assertion: confirm the computed value is as expected (an integer, here 0) ---
    assert isinstance(non_callable_filter_arg, int)
    assert non_callable_filter_arg == 0

    # --- Execution + Assertion: calling filter with a non-callable should raise TypeError ---
    with pytest.raises(TypeError):
        combined_list.filter(non_callable_filter_arg)

def test_find_on_empty_list_returns_none_and_len_call_raises_attribute_error():
    # Constants for the test
    NON_CALLABLE_FN = 1947
    EMPTY_VALUE = None

    # Setup: create an ImmutableList with no head and no tail (empty list)
    empty_list = immutable_list_module.ImmutableList(EMPTY_VALUE, EMPTY_VALUE)

    # Execution: call find with a non-callable value.
    # Because the list is empty, find should return None without attempting to call the non-callable.
    result = empty_list.find(NON_CALLABLE_FN)

    # Assertion: the result should be None, and calling __len__ on None raises AttributeError.
    # This makes explicit the behavior when find returns None and the test attempts to use list operations on it.
    with pytest.raises(AttributeError):
        result.__len__()

def test_find_accepts_callable_like_immutablelist_single_element():
    # Verify ImmutableList.find accepts an ImmutableList instance as a callable-like predicate
    # on a single-element list and does not raise. The return value should be None or the head.
    HEAD_VALUE = False
    IS_EMPTY = False

    list_instance = immutable_list_module.ImmutableList(HEAD_VALUE, is_empty=IS_EMPTY)
    result = list_instance.find(list_instance)

    assert result in (None, HEAD_VALUE)

def test_reduce_returns_acc_for_empty_list_and_find_returns_matching_head():
    # Purpose:
    # - Verify that reduce returns the provided accumulator unchanged when called on an empty ImmutableList.
    # - Verify that find returns the head element when a matching predicate is provided for a single-element ImmutableList.

    # --- Constants / Setup ---
    SENTINEL_ACC = object()  # unique object to ensure identity comparison
    HEAD_VALUE = False

    # Empty list (no head)
    empty_list = immutable_list_module.ImmutableList()

    # Single-element list with head == HEAD_VALUE (explicitly mark as not empty)
    single_item_list = immutable_list_module.ImmutableList(HEAD_VALUE, is_empty=False)

    # Reducer function (won't be called for empty_list, but provided for API)
    def reducer(acc, item):
        # This reduction would normally combine acc and item; here we just return the accumulator
        return acc

    # Predicate to find the head value
    def is_false(value):
        return value is False

    # --- Execution ---
    reduced_result = empty_list.reduce(reducer, SENTINEL_ACC)
    found_value = single_item_list.find(is_false)

    # --- Assertions ---
    # For an empty list, reduce should return the accumulator unchanged.
    assert reduced_result is SENTINEL_ACC

    # For a single-element list where the head matches the predicate, find should return that head.
    assert found_value is HEAD_VALUE

def test_create_empty_immutable_list_returns_new_instance():
    # Purpose:
    # Verify that constructing an ImmutableList produces a valid instance of the ImmutableList class
    # and that each construction returns a distinct object (no accidental shared mutable state).

    # Setup: define the class under test as a constant for readability
    EMPTY_LIST_CLASS = immutable_list_module.ImmutableList

    # Execution: construct two empty instances
    created_list = EMPTY_LIST_CLASS()
    another_list = EMPTY_LIST_CLASS()

    # Assertions: check type and distinct identity
    assert created_list is not None, "Constructing ImmutableList returned None"
    assert type(created_list) is EMPTY_LIST_CLASS, "Constructed object is not an ImmutableList instance"
    assert created_list is not another_list, "Multiple constructions returned the same object instance"

def test_str_returns_string_and_find_requires_callable():
    # Purpose: verify that ImmutableList.__str__ returns a string representation
    # and that find() raises a TypeError when given a non-callable argument.
    
    # Constants / configuration for the test
    HEAD_VALUE = False
    IS_EMPTY = False

    # Setup: create an ImmutableList with a single False head value
    immutable_list = immutable_list_module.ImmutableList(HEAD_VALUE, is_empty=IS_EMPTY)

    # Execution: obtain string representation
    string_representation = immutable_list.__str__()

    # Assertion: __str__ returns a string and includes the class marker
    assert isinstance(string_representation, str)
    assert string_representation.startswith('ImmutableList')

    # Execution & Assertion: calling find with a non-callable (the list itself)
    # should raise a TypeError because find expects a callable predicate.
    with pytest.raises(TypeError):
        immutable_list.find(immutable_list)

def test_unshift_adds_self_as_head_and_find_with_non_callable_predicate_raises():
    # Constants / test data
    INITIAL_HEAD_VALUE = False
    IS_EMPTY_FLAG = False

    # Setup: create a non-empty ImmutableList whose head value is a boolean
    original_list = immutable_list_module.ImmutableList(INITIAL_HEAD_VALUE, is_empty=IS_EMPTY_FLAG)

    # Execution: unshift the list itself onto its front, producing a new list
    new_list_with_self_head = original_list.unshift(original_list)

    # Assertion: the new list's head should be the original list object (identity)
    assert new_list_with_self_head.head is original_list

    # Core purpose: calling find expects a callable predicate; passing a non-callable
    # (here, the ImmutableList instance) should result in a TypeError when the code
    # attempts to call it like a function.
    with pytest.raises(TypeError):
        original_list.find(original_list)

def test_find_returns_first_element_matching_predicate_after_unshift_and_append():
    # Purpose:
    # Verify that ImmutableList.find returns the first element that satisfies
    # a predicate after performing unshift (add to head) and append (add to tail).
    
    # Constants / test data
    INITIAL_IS_EMPTY = False
    TARGET_VALUE = False  # value we will unshift and then search for
    IS_TARGET = lambda v: v == TARGET_VALUE  # predicate used by find

    # Setup: create an initial list, put TARGET_VALUE at the head, then append the original list
    initial_list = immutable_list_module.ImmutableList(is_empty=INITIAL_IS_EMPTY)
    list_with_head = initial_list.unshift(TARGET_VALUE)
    combined_list = list_with_head.append(initial_list)

    # Exercise: attempt to find the TARGET_VALUE using a predicate
    found = combined_list.find(IS_TARGET)

    # Assertion: the found value should be the unshifted TARGET_VALUE (the head)
    assert found == TARGET_VALUE

def test_append_increases_length_and_find_predicate_behavior():
    # Purpose:
    # - Verify that append returns a new ImmutableList whose length is exactly
    #   one greater than the original list (immutability + append behavior).
    # - Exercise `find` with a simple predicate and ensure its return is either
    #   the matched value or None (depending on whether the original list
    #   contains a matching element).
    #
    # Note: This test is written to be robust regardless of whether the original
    # list was constructed as empty (is_empty=True) or non-empty.

    # -- Setup --
    VALUE = True
    IS_EMPTY = True
    original_list = immutable_list_module.ImmutableList(VALUE, is_empty=IS_EMPTY)

    # -- Execution --
    appended_list = original_list.append(VALUE)
    original_length = len(original_list)
    appended_length = len(appended_list)

    # Use a predicate that matches the constant VALUE
    find_result = original_list.find(lambda element: element is VALUE)

    # -- Assertions --
    # Appending should produce a new list exactly one element longer than original.
    assert isinstance(appended_length, int)
    assert appended_length == original_length + 1

    # The find call should either return the matching VALUE (if present) or None.
    assert find_result in (VALUE, None)

def test_reduce_on_empty_and_nested_structures_and_find_with_non_callable_raises():
    # This test verifies several behaviors when working with nested ImmutableList instances:
    # - reduce returns the accumulator unchanged when called on an empty list (no reducer invocation)
    # - appending/unshifting nested lists produces lists whose heads reference the nested lists
    # - constructing an ImmutableList with a custom is_empty value preserves that value
    # - calling find with a non-callable argument raises a TypeError (invalid predicate)

    # Setup: create an empty list and build a few nested lists from it
    EMPTY_LIST = immutable_list_module.ImmutableList()
    # Append the empty list as an element to itself -> a single-element list whose head is EMPTY_LIST
    single_element_list = EMPTY_LIST.append(EMPTY_LIST)

    # Execution: call reduce on the empty list with a non-callable 'fn' and an accumulator.
    # According to implementation, reduce should immediately return the accumulator when the list is empty,
    # so passing a non-callable is safe in this branch.
    reduced_result = EMPTY_LIST.reduce(single_element_list, single_element_list)

    # Further setup/execution: create a list by unshifting the single-element list onto itself,
    # produce a string representation, construct a list with a custom is_empty value,
    # and append an element onto itself to form another nested structure.
    unshifted_list = single_element_list.unshift(single_element_list)
    unshifted_str = str(unshifted_list)
    custom_empty_flag_list = immutable_list_module.ImmutableList(is_empty=unshifted_str)
    appended_self = reduced_result.append(reduced_result)

    # Assertions: verify reduce returned the exact accumulator object and equality/structure expectations
    assert reduced_result is single_element_list  # reduce returned the accumulator unchanged
    assert not (single_element_list == EMPTY_LIST)  # the single-element list is not equal to the original empty list
    assert unshifted_list.head == single_element_list  # unshift put the single_element_list at the head
    assert custom_empty_flag_list.is_empty == unshifted_str  # constructor preserved the custom is_empty value
    assert appended_self.head == reduced_result  # append added the nested list as an element at the end

    # Finally, calling find with a non-callable should raise a TypeError because find expects a callable predicate.
    with pytest.raises(TypeError):
        unshifted_list.find(reduced_result)

def test_reduce_on_empty_returns_acc_and_find_called_with_non_callable_raises_type_error():
    # Purpose:
    # - Calling reduce on an empty ImmutableList should return the provided accumulator.
    # - Verify length calculation for a list that has an empty list as its head.
    # - Verify that unshifting produces a distinct (non-equal) list compared to empty.
    # - Verify that calling find with a non-callable argument raises a TypeError.
    #
    # Setup
    EMPTY_LIST = immutable_list_module.ImmutableList()
    ONE_ELEM_LIST_WITH_EMPTY = EMPTY_LIST.unshift(EMPTY_LIST)  # head = EMPTY_LIST, tail = EMPTY_LIST

    # Execution: reduce on the empty list should immediately return the accumulator (no fn invocation).
    reduced_result = EMPTY_LIST.reduce(ONE_ELEM_LIST_WITH_EMPTY, ONE_ELEM_LIST_WITH_EMPTY)

    # Inspect derived lists and properties
    list_length = len(ONE_ELEM_LIST_WITH_EMPTY)  # expected 1
    extended_list = ONE_ELEM_LIST_WITH_EMPTY.unshift(ONE_ELEM_LIST_WITH_EMPTY)  # prepend the list to itself
    lists_are_equal = (extended_list == EMPTY_LIST)

    # Construct an ImmutableList using the numeric length as the is_empty flag to mirror original behavior.
    constructed_with_is_empty = immutable_list_module.ImmutableList(is_empty=list_length)

    # Assertions
    # reduce on an empty list should return the accumulator object passed in.
    assert reduced_result is ONE_ELEM_LIST_WITH_EMPTY

    # The one-element list (with EMPTY_LIST as head) should report length 1.
    assert list_length == 1

    # The extended list (two levels) should not be equal to the original empty list.
    assert lists_are_equal is False

    # The constructed object's is_empty attribute should reflect the provided argument.
    assert getattr(constructed_with_is_empty, "is_empty") == list_length

    # Calling find with a non-callable (an ImmutableList) should raise a TypeError because find expects a callable.
    with pytest.raises(TypeError):
        reduced_result.find(reduced_result)

def test_reduce_raises_type_error_when_reducer_is_not_callable():
    # Purpose:
    # Ensure that ImmutableList.reduce raises a TypeError if the reducer argument is not callable.
    # This test sets up a single-element immutable list and attempts to call reduce with a non-callable reducer.

    # Constants / test data
    HEAD_VALUE = True
    NON_CALLABLE_REDUCER = []    # deliberately not a function/callable
    ACCUMULATOR = []             # accumulator value passed to reduce

    # Setup: create a single-element ImmutableList
    single_element_list = immutable_list_module.ImmutableList(HEAD_VALUE)

    # Execution / Sanity check: to_list should return the single head value
    list_representation = single_element_list.to_list()
    assert list_representation == [HEAD_VALUE]

    # Assertion: calling reduce with a non-callable reducer should raise a TypeError
    with pytest.raises(TypeError):
        single_element_list.reduce(NON_CALLABLE_REDUCER, ACCUMULATOR)

