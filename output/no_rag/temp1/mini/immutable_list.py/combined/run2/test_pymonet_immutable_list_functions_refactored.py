import pytest

import immutable_list as immutable_list_module

def test_empty_immutable_list_basic_behaviors():
    """Verify basic behaviors of an empty ImmutableList."""
    # Setup
    EMPTY_IMMUTABLE = immutable_list_module.ImmutableList()

    # Identity and representation
    assert EMPTY_IMMUTABLE == EMPTY_IMMUTABLE
    assert "ImmutableList" in str(EMPTY_IMMUTABLE)

    # to_list() returns a Python list and standard list operations behave as expected
    py_list = EMPTY_IMMUTABLE.to_list()
    assert isinstance(py_list, list)
    assert len(py_list + py_list) == len(py_list) * 2

    # Adding a plain Python list to an ImmutableList should raise ValueError
    with pytest.raises(ValueError):
        EMPTY_IMMUTABLE.__add__(py_list)

def test_immutable_list_empty_behaviour_and_reduce_raises_type_error():
    # Purpose:
    # - Verify basic behaviours of an empty ImmutableList: equality with non-list,
    #   concatenation (adding empty list to itself), find with a non-callable predicate,
    #   string representation, and unshift.
    # - Confirm that calling reduce with a non-callable "fn" raises a TypeError.
    
    # Constants / Setup
    BOOL_TRUE = True
    empty_list = immutable_list_module.ImmutableList()  # empty ImmutableList instance

    # Execution
    # 1. Equality check with a non-ImmutableList object (should be False).
    eq_with_non_list = empty_list == BOOL_TRUE

    # 2. Concatenate the empty list with itself.
    concatenated = empty_list + empty_list

    # 3. Call find with a non-callable (the equality result). For an empty list,
    #    find should return None without attempting to call the predicate.
    find_result = empty_list.find(eq_with_non_list)

    # 4. Obtain string representation of the empty list.
    str_repr = str(empty_list)

    # 5. Prepend the empty list onto itself (unshift).
    unshifted = empty_list.unshift(empty_list)

    # Assertions
    # Equality with a non-list value must be False.
    assert eq_with_non_list is False

    # Concatenation produces an ImmutableList with expected structure.
    assert isinstance(concatenated, immutable_list_module.ImmutableList)
    # For an empty list, the head is None and tail should be equal to the original empty list.
    assert concatenated.head is None
    assert concatenated.tail == empty_list

    # find on an empty list returns None (predicate is not called).
    assert find_result is None

    # String representation starts with the class name "ImmutableList".
    assert str_repr.startswith("ImmutableList")

    # reduce called with a non-callable fn should raise a TypeError.
    with pytest.raises(TypeError):
        unshifted.reduce(unshifted, BOOL_TRUE)

def test_append_returns_new_list_and_find_locates_element():
    # Purpose:
    # - Appending returns a new ImmutableList (immutability).
    # - find(...) with a predicate locates the expected element.

    # Setup
    ELEMENT = True
    initial_list = immutable_list_module.ImmutableList(ELEMENT, is_empty=False)

    # Exercise
    appended_list = initial_list.append(ELEMENT)
    predicate = lambda value: value is True

    # Verify immutability: append returns a new object
    assert appended_list is not initial_list

    # Verify find locates the element in both lists
    found_in_initial = initial_list.find(predicate)
    assert found_in_initial is ELEMENT

    found_in_appended = appended_list.find(predicate)
    assert found_in_appended is ELEMENT

def test_add_raises_for_non_immutable_list_operand():
    """Verify ImmutableList.__add__ raises ValueError when operand is not an ImmutableList."""
    # Arrange
    EMPTY_LIST = immutable_list_module.ImmutableList()
    INVALID_OPERAND = None
    EXPECTED_ERROR_MESSAGE = 'ImmutableList: you can not add any other instace than ImmutableList'

    # Act & Assert
    with pytest.raises(ValueError) as excinfo:
        EMPTY_LIST.__add__(INVALID_OPERAND)

    # Verify the error message contains the expected text
    assert EXPECTED_ERROR_MESSAGE in str(excinfo.value)

def test_find_returns_head_when_predicate_matches():
    # Purpose:
    # Verify that find returns the head element when the provided predicate
    # matches the head of a single-element ImmutableList.

    # Setup: create an empty list and confirm its length is zero
    empty_list = immutable_list_module.ImmutableList()
    initial_length = len(empty_list)
    assert initial_length == 0  # sanity check for __len__ on empty list

    # Setup: create a single-element list containing a unique sentinel value
    SENTINEL = object()
    single_element_list = immutable_list_module.ImmutableList(SENTINEL)

    # Execution: search for the sentinel using a predicate that checks identity
    result = single_element_list.find(lambda value: value is SENTINEL)

    # Assertion: find should return the sentinel (the head) when the predicate matches
    assert result is SENTINEL

def test_find_returns_none_when_predicate_returns_false_for_single_element_list():
    """
    Verify that for an ImmutableList containing a single falsy element,
    len(...) reports 1 and find(...) returns None when the provided predicate
    does not match the element (predicate here is the list object itself).
    """
    # Constants / test data
    HEAD_VALUE = False
    IS_EMPTY = False  # matches original construction in the test suite

    # Setup: create a single-element ImmutableList
    single_element_list = immutable_list_module.ImmutableList(HEAD_VALUE, is_empty=IS_EMPTY)

    # Execution: get the length and attempt to find using the list object as predicate
    list_length = len(single_element_list)
    find_result = single_element_list.find(single_element_list)

    # Assertions: length should be 1 for a single-element list; find should return None
    assert list_length == 1
    assert find_result is None

def test_find_raises_typeerror_when_predicate_is_not_callable():
    # Purpose:
    # Verify that ImmutableList.find raises a TypeError when the provided
    # predicate argument is not a callable (e.g., a list).

    # Constants / Test data
    SINGLE_VALUE = False
    IS_EMPTY = False

    # Setup: create a single-element ImmutableList and obtain its list representation
    immutable_list = immutable_list_module.ImmutableList(SINGLE_VALUE, is_empty=IS_EMPTY)
    list_representation = immutable_list.to_list()

    # Execution & Assertion: calling find with a non-callable (the list) should raise TypeError
    with pytest.raises(TypeError):
        immutable_list.find(list_representation)

def test_append_self_and_invalid_add_operations_raise():
    # Core purpose:
    # - Verify find(None) on an empty ImmutableList returns None (does not call predicate).
    # - Verify append(self) creates an ImmutableList that, when converted to a Python list,
    #   contains the original head followed by the appended element.
    # - Verify invalid addition operations raise the correct exceptions:
    #     * ImmutableList.__add__ with a non-ImmutableList raises ValueError
    #     * Python list.__add__ with a non-list raises TypeError

    # Constants
    NONE_VALUE = None

    # Setup: create an empty ImmutableList instance
    empty_immutable = immutable_list_module.ImmutableList()

    # Execution: calling find with None on an empty list should return None
    found = empty_immutable.find(NONE_VALUE)

    # Execution: append the list to itself and convert to a Python list
    appended_immutable = empty_immutable.append(empty_immutable)
    as_python_list = appended_immutable.to_list()

    # Assertions: find returned None for empty list
    assert found is None

    # Assertions: to_list returns a list containing the original head (None) followed by the appended element
    assert isinstance(as_python_list, list)
    assert as_python_list == [None, empty_immutable]

    # Assertions: invalid add operations raise the expected exceptions
    with pytest.raises(ValueError):
        # ImmutableList.__add__ expects an ImmutableList instance, so passing None should raise ValueError
        appended_immutable.__add__(NONE_VALUE)

    with pytest.raises(TypeError):
        # Python list.__add__ expects another list; passing None should raise TypeError
        as_python_list.__add__(NONE_VALUE)

def test_map_raises_type_error_when_given_non_callable_argument():
    # Purpose:
    # Verify that ImmutableList.map raises a TypeError when the provided argument is not callable.
    # This ensures callers must pass a function to map, not arbitrary objects.

    # Setup: create an ImmutableList instance that is not flagged as empty so it has a head value,
    # and capture its list representation to use as a non-callable argument.
    IS_EMPTY_FALSE = False
    immutable_list = immutable_list_module.ImmutableList(is_empty=IS_EMPTY_FALSE)
    list_representation_of_immutable = immutable_list.to_list()

    # (Preserve original test's creation of a second ImmutableList instance;
    # it is not used in the assertion but kept to reflect the original setup.)
    unused_immutable_list = immutable_list_module.ImmutableList()

    # Execution & Assertion: passing a non-callable (the list representation) to map should raise TypeError.
    non_callable_argument = list_representation_of_immutable
    with pytest.raises(TypeError):
        immutable_list.map(non_callable_argument)

def test_map_with_non_callable_raises_type_error():
    # Purpose:
    # Verify that calling ImmutableList.map with a non-callable (None) raises a TypeError
    # because the map implementation attempts to call the provided argument as a function.

    # Constants used in the test
    NON_CALLABLE_FN = None
    EMPTY_VALUE = None
    EMPTY_TAIL = None

    # Setup: create a base immutable list and perform a sequence of unshift/append operations
    base_list = immutable_list_module.ImmutableList(EMPTY_VALUE, EMPTY_TAIL)
    # Prepend None to the base list
    list_with_prepended_none = base_list.unshift(EMPTY_VALUE)
    # Prepend the previously created list as an element to the base list
    list_with_prepended_list = base_list.unshift(list_with_prepended_none)
    # Append None to the list that had None prepended
    appended_list = list_with_prepended_none.append(EMPTY_VALUE)

    # Execution & Assertion:
    # Attempting to map using a non-callable should raise TypeError when the implementation tries to call it.
    with pytest.raises(TypeError):
        appended_list.map(NON_CALLABLE_FN)

def test_filter_with_non_callable_argument_raises_type_error():
    # Purpose:
    # Ensure ImmutableList.filter raises a TypeError when given a non-callable
    # argument (here, another ImmutableList) because filter expects a callable.
    
    # Constants / Setup
    INITIAL_VALUE = False
    source_list = immutable_list_module.ImmutableList(INITIAL_VALUE, is_empty=False)
    
    # Execution & Assertion: calling filter with a non-callable should raise TypeError
    with pytest.raises(TypeError):
        source_list.filter(source_list)

def test_filter_raises_type_error_when_given_non_callable_after_concatenating_empty_lists():
    # Purpose:
    # Verify that calling ImmutableList.filter with a non-callable argument
    # raises a TypeError. This covers the case after concatenating two empty lists.

    # Setup: create an empty immutable list and concatenate it with itself
    EMPTY_LIST = immutable_list_module.ImmutableList()
    concatenated_list = EMPTY_LIST + EMPTY_LIST

    # Execution: compute a non-callable value (length of the concatenated list)
    non_callable_value = len(concatenated_list)

    # Assertion: filter expects a callable; passing a non-callable should raise TypeError
    with pytest.raises(TypeError):
        concatenated_list.filter(non_callable_value)

def test_find_on_empty_immutable_list_returns_none_and_none_has_no_len():
    # Constants for the test
    EMPTY_VALUE = None
    NON_CALLABLE_FN = 1947  # intentionally not a callable; irrelevant for empty list case

    # Setup: create an ImmutableList whose head and tail are both None (empty list)
    empty_list = immutable_list_module.ImmutableList(EMPTY_VALUE, EMPTY_VALUE)

    # Execution: call find with a non-callable argument (function not used because list is empty)
    found = empty_list.find(NON_CALLABLE_FN)

    # Assertion: find should return None for an empty list, and attempting to call __len__ on that result
    # should raise AttributeError because NoneType has no __len__ attribute.
    assert found is None
    with pytest.raises(AttributeError):
        found.__len__()

def test_find_raises_type_error_for_non_callable_predicate():
    # Purpose:
    # Verify that ImmutableList.find raises a TypeError when the provided predicate
    # argument is not a callable (i.e., cannot be called with the list element).

    # Constants for setup
    ELEMENT = False
    IS_EMPTY = False

    # Setup: create an ImmutableList with a single element
    immutable_list = immutable_list_module.ImmutableList(ELEMENT, is_empty=IS_EMPTY)

    # Use the list object itself as a non-callable predicate to trigger the error
    non_callable_predicate = immutable_list

    # Execution & Assertion: calling find with a non-callable should raise TypeError
    with pytest.raises(TypeError):
        immutable_list.find(non_callable_predicate)

def test_reduce_on_empty_returns_acc_and_find_with_non_callable_raises_typeerror():
    # Purpose:
    # - reduce should return the provided accumulator immediately for an empty ImmutableList,
    #   so a non-callable reducer must never be invoked.
    # - find should raise a TypeError when the provided predicate is not callable
    #   (find attempts to call the predicate with the head element).

    # Use an intentionally non-callable value to simulate a bad function argument
    NON_CALLABLE = False

    # Empty list: reduce should return the accumulator unchanged even if the reducer is non-callable
    empty_list = immutable_list_module.ImmutableList()
    returned_acc = empty_list.reduce(NON_CALLABLE, empty_list)
    assert returned_acc is empty_list

    # Single-element list: calling find with a non-callable predicate should raise TypeError
    single_element_list = immutable_list_module.ImmutableList(NON_CALLABLE, is_empty=False)
    with pytest.raises(TypeError):
        single_element_list.find(NON_CALLABLE)

def test_create_empty_immutable_list_is_instance_and_initially_empty():
    """Verify constructing an ImmutableList returns the expected type and is initially empty where supported."""
    ImmutableListType = immutable_list_module.ImmutableList

    # Construct a new empty ImmutableList
    instance = ImmutableListType()

    # The created object is an instance of the expected type.
    assert isinstance(instance, ImmutableListType)

    # If the implementation supports __len__, a new list should have length 0.
    if hasattr(instance, "__len__"):
        assert len(instance) == 0

    # repr() should not raise and should return a string.
    repr_value = repr(instance)
    assert isinstance(repr_value, str)

def test_str_and_find_on_empty_immutable_list_returns_expected():
    # Purpose:
    # Verify that an ImmutableList explicitly constructed as empty:
    #  - has the expected string representation
    #  - returns None when searching for any element
    #
    # Constants for clarity
    HEAD_VALUE = False
    IS_EMPTY = True
    EXPECTED_STR = "ImmutableList[]"

    # Setup: create an ImmutableList marked as empty
    immutable_list = immutable_list_module.ImmutableList(HEAD_VALUE, is_empty=IS_EMPTY)

    # Execution: obtain string representation and attempt to find a value matching HEAD_VALUE
    list_representation = immutable_list.__str__()
    found_element = immutable_list.find(lambda v: v is HEAD_VALUE)

    # Assertions: string should indicate an empty list, and find should return None
    assert list_representation == EXPECTED_STR
    assert found_element is None

def test_unshift_puts_element_at_head_and_find_with_non_callable_predicate_raises_type_error():
    # Purpose:
    # - Verify that unshift places the new element at the head of the returned ImmutableList.
    # - Verify that calling find with a non-callable argument raises a TypeError
    #   (find expects a callable predicate).
    
    # Constants / test data
    HEAD_VALUE = False
    IS_EMPTY_FLAG = False

    # Setup: create an ImmutableList with a boolean head
    original_list = immutable_list_module.ImmutableList(HEAD_VALUE, is_empty=IS_EMPTY_FLAG)

    # Execution: unshift the list itself onto the front of the original list
    unshifted_list = original_list.unshift(original_list)

    # Assertion: the new list's head should be the element we unshifted (the original list)
    assert unshifted_list.head is original_list

    # Execution + Assertion: calling find with a non-callable (the list itself) should raise TypeError
    # because find expects a callable predicate that can be invoked with a value.
    with pytest.raises(TypeError):
        original_list.find(original_list)

def test_find_returns_none_when_predicate_matches_no_elements():
    # Constants for the test
    INITIAL_IS_EMPTY_FLAG = False
    ELEMENT_VALUE = False

    # Predicate that always returns False (no element should match)
    always_false_predicate = lambda _: False

    # Setup: create an initial immutable list, then unshift and append to form the test list
    initial_list = immutable_list_module.ImmutableList(is_empty=INITIAL_IS_EMPTY_FLAG)
    list_with_element = initial_list.unshift(ELEMENT_VALUE)
    combined_list = list_with_element.append(initial_list)

    # Execution: attempt to find an element that matches the always-false predicate
    found = combined_list.find(always_false_predicate)

    # Assertion: since the predicate never matches, find should return None
    assert found is None

def test_append_increases_length_and_find_returns_matching_head():
    """Verify append returns a list one element longer and find returns head when predicate matches."""
    # Setup
    ELEMENT = True
    IS_EMPTY_FLAG = True
    original_list = immutable_list_module.ImmutableList(ELEMENT, is_empty=IS_EMPTY_FLAG)

    # Exercise
    appended_list = original_list.append(ELEMENT)
    original_length = len(original_list)
    appended_length = len(appended_list)
    predicate = lambda v: v == ELEMENT
    found_value = original_list.find(predicate)

    # Verify
    assert appended_length == original_length + 1
    assert found_value == ELEMENT

def test_reduce_unshift_append_and_find_non_callable_predicate_behavior():
    # This test verifies several behaviors of ImmutableList:
    # 1. reduce on an empty list returns the accumulator without calling the reducer.
    # 2. append and unshift create new lists with expected structure.
    # 3. __str__ produces a string beginning with "ImmutableList".
    # 4. Constructing an ImmutableList with a custom is_empty value preserves that value.
    # 5. Passing a non-callable object to find raises a TypeError (predicate must be callable).

    # Setup: create an empty list and a single-element list (the element is the empty list itself).
    EMPTY_LIST = immutable_list_module.ImmutableList()
    single_item_list = EMPTY_LIST.append(EMPTY_LIST)  # list containing EMPTY_LIST as its only element

    # Execution: reduce on the empty list should immediately return the accumulator (single_item_list).
    reduced_result = EMPTY_LIST.reduce(single_item_list, single_item_list)

    # Assertion: reduce returned the accumulator object.
    assert reduced_result is single_item_list

    # Execution: equality check between single_item_list and EMPTY_LIST
    equality_result = single_item_list == EMPTY_LIST

    # Assertion: the lists are not equal (different structure/content).
    assert equality_result is False

    # Execution: add the single_item_list to the front of itself and get its string representation.
    unshifted_list = single_item_list.unshift(single_item_list)
    string_repr = str(unshifted_list)

    # Assertion: string representation begins with the class name (implementation detail).
    assert isinstance(string_repr, str)
    assert string_repr.startswith("ImmutableList")

    # Execution: construct a new ImmutableList using the string as the is_empty sentinel.
    custom_is_empty_list = immutable_list_module.ImmutableList(is_empty=string_repr)

    # Assertion: the constructed object's is_empty attribute preserves the provided value.
    assert getattr(custom_is_empty_list, "is_empty") == string_repr

    # Execution: append the reduced_result to itself (creates a list with two elements).
    appended_twice = reduced_result.append(reduced_result)

    # Assertion: the appended list contains two entries (both should be equal to single_item_list).
    # Use to_list() (used by __str__) to observe internal elements.
    assert appended_twice.to_list() == [single_item_list, single_item_list]

    # Execution & Assertion: calling find with a non-callable (an ImmutableList) should raise TypeError.
    # The predicate argument to find is expected to be callable.
    with pytest.raises(TypeError):
        unshifted_list.find(reduced_result)

def test_reduce_on_empty_returns_acc_and_list_operations():
    # Setup - create an empty list and a simple non-empty list by unshifting the empty list
    EMPTY_LIST = immutable_list_module.ImmutableList()
    SINGLETON_LIST = EMPTY_LIST.unshift(EMPTY_LIST)  # list whose head is the EMPTY_LIST

    # Execution - perform operations under test
    # 1) Reduce on an empty list should immediately return the accumulator (no calls to reducer)
    def identity_reducer(acc, _):
        return acc

    reduced_result = EMPTY_LIST.reduce(identity_reducer, SINGLETON_LIST)

    # 2) Inspect length and create a new list by unshifting the singleton list onto itself
    singleton_length = len(SINGLETON_LIST)
    nested_list = SINGLETON_LIST.unshift(SINGLETON_LIST)

    # 3) Compare equality between the nested list and the original empty list
    nested_eq_empty = (nested_list == EMPTY_LIST)

    # 4) Construct an ImmutableList using the observed length for the is_empty flag (exercise constructor)
    constructed_with_flag = immutable_list_module.ImmutableList(is_empty=singleton_length)

    # 5) Use find with a predicate that always returns True to retrieve the first element
    found_element = reduced_result.find(lambda _: True)

    # Assertions - verify expected behaviors
    # reduce on an empty list should return the exact accumulator object passed
    assert reduced_result is SINGLETON_LIST

    # length should be an integer and reflect a non-negative size
    assert isinstance(singleton_length, int)
    assert singleton_length >= 0

    # The nested list created by unshifting the singleton should not be equal to the original empty list
    assert nested_eq_empty is False

    # Constructor should have set the is_empty attribute to the provided value
    assert hasattr(constructed_with_flag, "is_empty")
    assert constructed_with_flag.is_empty == singleton_length

    # find with a predicate that always returns True should return the first element (the head of SINGLETON_LIST)
    # For SINGLETON_LIST, the head is EMPTY_LIST, so we expect found_element to be EMPTY_LIST
    assert found_element is EMPTY_LIST

def test_reduce_with_non_callable_fn_raises_type_error():
    # Purpose:
    # Verify that ImmutableList.reduce raises a TypeError when the provided
    # reducer argument is not a callable (here we pass a list).
    #
    # This test also constructs an ImmutableList with an explicit tail value
    # to exercise the constructor path that accepts a 'tail' keyword.

    # Constants / test data
    HEAD_VALUE = True
    EMPTY_FLAG = True
    EMPTY_TAIL = {}

    # Setup: create ImmutableList instances used in the test
    list_with_empty_tail = immutable_list_module.ImmutableList(tail=EMPTY_TAIL)
    list_with_head_marked_empty = immutable_list_module.ImmutableList(HEAD_VALUE, is_empty=EMPTY_FLAG)

    # Execution: use to_list() to produce a non-callable reducer and use it as the accumulator too
    non_callable_reducer = list_with_head_marked_empty.to_list()
    accumulator = non_callable_reducer

    # Assertion: reduce should attempt to call the reducer and therefore raise a TypeError
    with pytest.raises(TypeError):
        list_with_head_marked_empty.reduce(non_callable_reducer, accumulator)

