import pytest
import immutable_list as immutable_list_module

def test_immutable_list_basic_behaviors_str_and_invalid_add_raises():
    # Verify several behaviors of ImmutableList:
    # 1. Equality to itself.
    # 2. String representation uses "ImmutableList{...}" based on to_list().
    # 3. to_list() returns a Python list that concatenates like a normal list.
    # 4. len() and __len__ agree.
    # 5. Adding a plain Python list raises ValueError.
    EMPTY_IMMUTABLE = immutable_list_module.ImmutableList()
    STRING_PREFIX = "ImmutableList"

    # Convert to a regular Python list for list-specific checks
    python_list = EMPTY_IMMUTABLE.to_list()

    # Self-equality and string representation
    assert EMPTY_IMMUTABLE == EMPTY_IMMUTABLE
    assert str(EMPTY_IMMUTABLE) == f"{STRING_PREFIX}{python_list}"

    # Python list behaviors
    concatenated_python_list = python_list + python_list
    assert concatenated_python_list == python_list.__add__(python_list)
    assert len(python_list) == python_list.__len__()

    # Adding a plain Python list to an ImmutableList should raise ValueError
    raised = False
    try:
        EMPTY_IMMUTABLE.__add__(python_list)
    except ValueError:
        raised = True
    assert raised

def test_immutable_list_operations_on_empty_list():
    # Purpose:
    # Verify core ImmutableList methods on an initially empty list:
    # equality with a non-list, concatenation with itself, find with a predicate,
    # string representation, unshift (prepend) and reduce (aggregation).

    # Constants / Setup
    NON_LIST_VALUE = True
    INITIAL_REDUCE_ACC = 0

    empty_list = immutable_list_module.ImmutableList()

    # Execution: equality check with a non-list value
    is_equal_to_non_list = (empty_list == NON_LIST_VALUE)

    # Execution: concatenate empty list with itself
    concatenated_list = empty_list + empty_list

    # Execution: find with a predicate that always returns False (should not find anything)
    found_element = empty_list.find(lambda v: False)

    # Execution: string representation
    string_repr = str(empty_list)

    # Execution: unshift (prepend the empty list as an element) -> produces a list whose head is the empty_list
    unshifted_list = empty_list.unshift(empty_list)

    # Execution: reduce over the unshifted list with a simple counter reducer
    # reducer increments the accumulator for every non-None element encountered
    def count_non_none(acc, element):
        return acc + (1 if element is not None else 0)

    reduced_count = unshifted_list.reduce(count_non_none, INITIAL_REDUCE_ACC)

    # Assertions
    # equality with a non-list should be False
    assert is_equal_to_non_list is False

    # concatenation returns an ImmutableList instance and its tail should be the original empty list
    assert isinstance(concatenated_list, immutable_list_module.ImmutableList)
    assert getattr(concatenated_list, "tail", None) == empty_list

    # find with a predicate that always returns False yields None
    assert found_element is None

    # string representation should be a string and include the class marker
    assert isinstance(string_repr, str)
    assert "ImmutableList" in string_repr

    # unshifted list should have the original empty list as its head and tail
    assert isinstance(unshifted_list, immutable_list_module.ImmutableList)
    assert getattr(unshifted_list, "head", None) == empty_list
    assert getattr(unshifted_list, "tail", None) == empty_list

    # reduce should count one non-None element (the head we just prepended)
    assert reduced_count == 1

def test_append_returns_new_list_and_find_locates_first_matching_element():
    # Constants used in the test
    VALUE = True
    IS_EMPTY = True

    # Setup: create an ImmutableList with a head value
    initial_list = immutable_list_module.ImmutableList(VALUE, is_empty=IS_EMPTY)

    # Execution: append a value to the list (should return a new ImmutableList)
    appended_list = initial_list.append(VALUE)

    # Execution: define a predicate that matches the head value and use find to locate it
    predicate = lambda element: element == VALUE
    found_value = initial_list.find(predicate)

    # Assertions:
    # - append should return an ImmutableList instance
    # - the appended list should be a different object (immutability)
    # - find should return the first element that matches the predicate (the head)
    assert isinstance(appended_list, immutable_list_module.ImmutableList)
    assert appended_list is not initial_list
    assert found_value == VALUE

def test_add_with_non_immutable_list_raises_value_error():
    # Arrange: a value that is not an ImmutableList and an empty ImmutableList instance
    NON_LIST_VALUE = None
    immutable_list = immutable_list_module.ImmutableList()

    # Act & Assert: adding a non-ImmutableList should raise ValueError
    with pytest.raises(ValueError) as excinfo:
        immutable_list.__add__(NON_LIST_VALUE)

    # Ensure the error message references ImmutableList to confirm the reason
    assert "ImmutableList" in str(excinfo.value)

def test_find_returns_head_when_predicate_matches_empty_head():
    # Purpose:
    # Verify that find() returns the head element when the provided predicate
    # matches that head. Also exercise the __len__ path for an empty list.

    # -- Constants / Setup --
    # Create an empty ImmutableList and verify its length is zero.
    EMPTY_LIST = immutable_list_module.ImmutableList()
    initial_length = len(EMPTY_LIST)

    # Build an ImmutableList whose head is the EMPTY_LIST (mirrors original construction).
    list_with_empty_head = immutable_list_module.ImmutableList(EMPTY_LIST, is_empty=EMPTY_LIST)

    # -- Execution --
    # Predicate that matches exactly the empty list used as the head.
    predicate_matches_empty = lambda value: value is EMPTY_LIST
    found_item = list_with_empty_head.find(predicate_matches_empty)

    # -- Assertions --
    # The empty list should report length 0 and find() should return the head that matched.
    assert initial_length == 0
    assert found_item is EMPTY_LIST

def test_find_returns_head_and_length_for_single_element_list():
    # Purpose:
    # Verify that an ImmutableList with a single element reports length 1
    # and that find(...) returns the head when the predicate matches the head value.

    # --- Setup ---
    TEST_VALUE = False
    IS_EMPTY_FLAG = False
    single_item_list = immutable_list_module.ImmutableList(TEST_VALUE, is_empty=IS_EMPTY_FLAG)

    # --- Execution ---
    # Use len(...) to exercise the __len__ implementation and capture the result.
    list_length = len(single_item_list)
    # Provide a predicate that matches the head value to exercise find(...)
    found_value = single_item_list.find(lambda v: v == TEST_VALUE)

    # --- Assertion ---
    assert list_length == 1, "A list with a single head and no tail should have length 1"
    assert found_value == TEST_VALUE, "find should return the head when the predicate matches it"

def test_find_raises_type_error_when_predicate_is_not_callable():
    # Purpose:
    # Ensure ImmutableList.find raises a TypeError when given a non-callable argument.
    # The test constructs a single-element ImmutableList, converts it to a Python list,
    # and uses that list (which is not callable) as the "predicate" argument to find().
    
    # Constants / Setup
    HEAD_VALUE = False
    IS_EMPTY_FLAG = False
    immutable_list = immutable_list_module.ImmutableList(HEAD_VALUE, is_empty=IS_EMPTY_FLAG)
    
    # Execution: obtain a non-callable object by converting the immutable list to a regular list
    non_callable_predicate = immutable_list.to_list()
    
    # Assertion: calling find with a non-callable should raise a TypeError when the implementation tries to call it
    with pytest.raises(TypeError):
        immutable_list.find(non_callable_predicate)

def test_find_returns_none_for_empty_list_and_list_add_with_none_raises():
    # Purpose:
    # - Verify that calling find with None on an empty ImmutableList returns None
    # - Verify that appending an ImmutableList instance results in a Python list
    #   representation that contains an ImmutableList element
    # - Verify that calling list.__add__ with None raises a TypeError

    # Setup
    EMPTY_LIST = immutable_list_module.ImmutableList()
    NONE_AS_CALLABLE = None  # intentionally not a callable

    # Exercise: call find on an empty list with None (should return None without calling it)
    find_result = EMPTY_LIST.find(NONE_AS_CALLABLE)

    # Exercise: append the empty ImmutableList as an element and convert to Python list
    appended_immutable_list = EMPTY_LIST.append(EMPTY_LIST)
    python_list_representation = appended_immutable_list.to_list()

    # Assertions
    # find should return None for an empty list when a non-callable (None) is passed
    assert find_result is None

    # to_list should return a Python list containing the appended ImmutableList element
    assert isinstance(python_list_representation, list)
    assert len(python_list_representation) == 1
    assert isinstance(python_list_representation[0], immutable_list_module.ImmutableList)

    # Using list.__add__ (i.e., list + other) with None should raise a TypeError
    with pytest.raises(TypeError):
        python_list_representation.__add__(None)

def test_map_raises_type_error_when_called_with_non_callable():
    """Verify that ImmutableList.map raises a TypeError when the mapper argument is not callable."""
    # Constants / configuration
    IS_EMPTY = False

    # Setup: create an ImmutableList instance and obtain its list representation
    immutable = immutable_list_module.ImmutableList(is_empty=IS_EMPTY)
    initial_list_representation = immutable.to_list()

    # Sanity assertion: ensure to_list returned a Python list representation of the ImmutableList
    assert isinstance(initial_list_representation, list), "to_list should return a Python list"

    # Prepare a non-callable mapper (reusing the list representation)
    non_callable_mapper = initial_list_representation

    # Execution & Assertion: calling map with a non-callable should raise TypeError
    with pytest.raises(TypeError):
        immutable.map(non_callable_mapper)

def test_map_raises_type_error_when_mapping_with_none():
    """Verify that calling ImmutableList.map with a non-callable (None) raises TypeError."""
    # Test data
    NONE_VALUE = None
    NONE_FUNC = None

    # Build lists:
    # start_list: a single-node list whose head is None and tail is None -> [None]
    start_list = immutable_list_module.ImmutableList(NONE_VALUE, NONE_VALUE)
    # prepended_none: unshift None onto start_list -> [None, None]
    prepended_none = start_list.unshift(NONE_VALUE)
    # appended_none: append None to the prepended_none list -> [None, None, None]
    appended_none = prepended_none.append(NONE_VALUE)

    # Mapping with a non-callable should raise TypeError
    with pytest.raises(TypeError):
        appended_none.map(NONE_FUNC)

def test_filter_raises_type_error_when_predicate_is_not_callable():
    # Constants for the test
    ELEMENT = False
    IS_EMPTY_FLAG = False
    EXPECTED_EXCEPTION = TypeError

    # Setup: create an ImmutableList instance containing a single element
    immutable_list = immutable_list_module.ImmutableList(ELEMENT, is_empty=IS_EMPTY_FLAG)

    # Use a non-callable object (the list itself) as the predicate argument
    non_callable_predicate = immutable_list

    # Execution & Assertion: calling filter with a non-callable should raise a TypeError
    with pytest.raises(EXPECTED_EXCEPTION):
        immutable_list.filter(non_callable_predicate)

def test_filter_raises_type_error_with_non_callable_argument():
    # Purpose:
    # - Verify that ImmutableList.filter raises a TypeError when a non-callable
    #   value is passed as the predicate function.
    #
    # Setup: create an empty ImmutableList and concatenate it with itself.
    EMPTY_LIST = immutable_list_module.ImmutableList()
    concatenated_list = EMPTY_LIST + EMPTY_LIST

    # Execution / intermediate assertion: the concatenated list should be empty (length 0).
    computed_length = len(concatenated_list)
    assert computed_length == 0, "Expected concatenated empty lists to have length 0"

    # Attempt to call filter with a non-callable value and assert that a TypeError is raised.
    NON_CALLABLE_FILTER_ARG = computed_length  # int is not callable
    with pytest.raises(TypeError):
        concatenated_list.filter(NON_CALLABLE_FILTER_ARG)

def test_find_on_empty_immutable_list_returns_none_and_has_length_zero():
    # Purpose:
    # - Verify that ImmutableList.find returns None for an empty list regardless of the predicate.
    # - Verify that the length of an empty ImmutableList is reported as 0.

    # Constants / test data
    SEARCH_VALUE = 1947
    predicate = lambda x: x == SEARCH_VALUE  # predicate to search for the SEARCH_VALUE

    # Setup: create an empty ImmutableList (head=None, tail=None)
    empty_list = immutable_list_module.ImmutableList(None, None)

    # Execution: attempt to find an element matching the predicate and get the list length
    found = empty_list.find(predicate)
    list_length = len(empty_list)

    # Assertions: no element should be found and length should be zero
    assert found is None
    assert list_length == 0

def test_find_raises_type_error_for_non_callable_predicate():
    # Purpose:
    # Verify that calling ImmutableList.find with a non-callable argument
    # raises a TypeError (i.e., the predicate must be callable).

    # Constants / Test data
    ELEMENT_VALUE = False
    IS_EMPTY_FLAG = False

    # Setup: create a single-element ImmutableList (tail defaults to None)
    single_element_list = immutable_list_module.ImmutableList(ELEMENT_VALUE, is_empty=IS_EMPTY_FLAG)

    # Execution & Assertion:
    # Passing a non-callable (the list object itself) as the predicate should raise TypeError
    with pytest.raises(TypeError):
        single_element_list.find(single_element_list)

def test_reduce_on_empty_returns_accumulator_and_find_returns_matching_head():
    # Purpose:
    # - Verify that reduce() returns the provided accumulator unchanged when called on an empty ImmutableList
    #   (the reducer must not be invoked).
    # - Verify that find() returns the list head when a predicate matches the head value.

    # Constants / test data
    HEAD_VALUE = False
    ACCUMULATOR = object()  # sentinel to ensure reduce returns exactly this object

    # Setup
    empty_list = immutable_list_module.ImmutableList()  # empty list (head is None)
    # Construct a non-empty list with head == HEAD_VALUE. Passing is_empty=HEAD_VALUE (False) mirrors original usage.
    non_empty_list = immutable_list_module.ImmutableList(HEAD_VALUE, is_empty=HEAD_VALUE)

    # Execution
    # Reducer that must not be called for an empty list; if called, the test should fail immediately.
    def failing_reducer(acc, item):
        raise AssertionError("Reducer should not be called for an empty list")

    reduced_result = empty_list.reduce(failing_reducer, ACCUMULATOR)

    # Find using a predicate that matches the head value
    find_result = non_empty_list.find(lambda value: value == HEAD_VALUE)

    # Assertions
    assert reduced_result is ACCUMULATOR, "reduce() did not return the provided accumulator for an empty list"
    assert find_result == HEAD_VALUE, "find() did not return the head when the predicate matched"

def test_create_empty_immutable_list_is_instance_of_expected_type():
    """Verify constructing an empty ImmutableList returns the expected type."""
    EXPECTED_CLASS = immutable_list_module.ImmutableList

    # Exercise: create a new empty immutable list instance
    empty_list = immutable_list_module.ImmutableList()

    # Assertion: the created object is an instance of the expected ImmutableList class
    assert isinstance(empty_list, EXPECTED_CLASS)

def test_immutable_list_str_and_find_returns_head_when_predicate_matches():
    # Purpose:
    # - Verify the string representation includes the list contents.
    # - Verify find returns the head element when the predicate matches the head.

    # Constants / Setup
    HEAD_VALUE = False
    IS_EMPTY_FLAG = False
    immutable_list = immutable_list_module.ImmutableList(HEAD_VALUE, is_empty=IS_EMPTY_FLAG)

    # Execution: obtain string representation
    list_str = immutable_list.__str__()

    # Execution: attempt to find the first element that matches the predicate.
    # Use a predicate that matches the head value (False) explicitly.
    found_value = immutable_list.find(lambda v: v is False)

    # Assertions
    # The string representation should identify this as an ImmutableList and include the head value.
    assert list_str.startswith("ImmutableList")
    assert "False" in list_str

    # find should return the head value when the predicate matches it.
    assert found_value is HEAD_VALUE

def test_find_accepts_predicate_like_object_and_returns_head_or_none():
    # Purpose:
    # Verify that calling find on a single-element ImmutableList with the list itself
    # as the predicate-like argument completes without error and returns either the head
    # element or None depending on the predicate behavior.
    #
    # Note: This test does not assume a specific boolean outcome, only that the call
    # completes and returns a valid result (the head or None).

    # Setup
    ELEMENT_VALUE = False
    IS_EMPTY_FLAG = False
    original_list = immutable_list_module.ImmutableList(ELEMENT_VALUE, is_empty=IS_EMPTY_FLAG)

    # Execution: call find on the original single-element list using the list itself as the predicate
    result = original_list.find(original_list)

    # Assertion: the call should complete and return either the list head or None.
    assert result in (original_list.head, None)

def test_find_returns_none_when_predicate_never_matches():
    # Constants for readability
    INITIAL_IS_EMPTY = False
    ELEMENT_VALUE = False

    # Setup: create an immutable list, add an element at the front, then append the original list
    original_list = immutable_list_module.ImmutableList(is_empty=INITIAL_IS_EMPTY)
    list_after_unshift = original_list.unshift(ELEMENT_VALUE)
    combined_list = list_after_unshift.append(original_list)

    # Execution: call find with a predicate that always returns False
    # This simulates searching for a value that does not exist / never matches.
    result = combined_list.find(lambda _: False)

    # Assertion: since the predicate never matches any element, find should return None
    assert result is None

def test_append_creates_new_list_and_find_returns_matching_head():
    # Purpose:
    # - Verify that append() returns a new ImmutableList with the new element added,
    #   increasing the reported length.
    # - Verify that find() returns the head element when a predicate matches it.

    # Setup
    INITIAL_VALUE = True
    MARK_AS_EMPTY = True  # preserved from original test input (constructor flag)
    original_list = immutable_list_module.ImmutableList(INITIAL_VALUE, is_empty=MARK_AS_EMPTY)

    # Execution: append a value to create a new list and measure its length
    appended_list = original_list.append(INITIAL_VALUE)
    appended_length = len(appended_list)

    # Assertion: the appended list should contain the original element plus the appended one
    assert appended_length == 2

    # Execution: find using a predicate that matches the head value of the original list
    predicate_matching_head = lambda value: value is INITIAL_VALUE
    found_value = original_list.find(predicate_matching_head)

    # Assertion: find should return the head value when the predicate matches
    assert found_value is INITIAL_VALUE

def test_reduce_on_empty_list_returns_accumulator_and_find_raises_type_error_for_non_callable():
    # Setup: create an empty immutable list and build related lists/constants
    EMPTY_LIST = immutable_list_module.ImmutableList()
    # Append the empty list as an element to itself -> single-element list whose element is EMPTY_LIST
    SINGLE_WRAPPED_LIST = EMPTY_LIST.append(EMPTY_LIST)

    # Execution: reduce on an empty list should immediately return the accumulator (no calls to reducer)
    reduced_result = EMPTY_LIST.reduce(SINGLE_WRAPPED_LIST, SINGLE_WRAPPED_LIST)

    # Execution: check equality between the single-element list and the original empty list
    equality_with_empty = SINGLE_WRAPPED_LIST.__eq__(EMPTY_LIST)

    # Execution: unshift the single-element list onto itself to create a two-element list
    prepended_list = SINGLE_WRAPPED_LIST.unshift(SINGLE_WRAPPED_LIST)

    # Execution: obtain string representation of the new list (used to set a custom is_empty marker)
    repr_str = prepended_list.__str__()

    # Execution: create a list while intentionally setting its is_empty attribute to the string repr_str
    custom_empty_marker_list = immutable_list_module.ImmutableList(is_empty=repr_str)

    # Execution: append the reduced_result to itself (creates a new list different from the original)
    appended_to_self = reduced_result.append(reduced_result)

    # Assertion: reduce on empty list returned the provided accumulator object
    assert reduced_result == SINGLE_WRAPPED_LIST

    # Assertion: the single-element wrapped list is not equal to the original empty list
    assert equality_with_empty is False

    # Assertion: string representation contains the ImmutableList marker
    assert repr_str.startswith("ImmutableList")

    # Assertion: the custom list's is_empty attribute was set to the repr string
    assert getattr(custom_empty_marker_list, "is_empty") == repr_str

    # Assertion: appending the list to itself produced a different list instance/value
    assert appended_to_self != reduced_result

    # Assertion: calling find with a non-callable argument should raise a TypeError
    # (find expects a callable predicate; passing an ImmutableList is incorrect)
    with pytest.raises(TypeError):
        prepended_list.find(reduced_result)

def test_reduce_empty_returns_acc_and_self_reference_behaviors_and_find_type_error():
    # Purpose:
    # - reduce on an empty ImmutableList should return the provided accumulator unchanged.
    # - verify len(), unshift() and equality for a simple self-referential list.
    # - verify find() raises TypeError when given a non-callable predicate.
    EMPTY_LIST = immutable_list_module.ImmutableList()

    # Create a list whose head is the empty list itself and whose tail is the empty list
    list_with_self = EMPTY_LIST.unshift(EMPTY_LIST)

    # Calling reduce on the empty list with a non-callable "fn" (the list) and the same list as acc
    reduced_result = EMPTY_LIST.reduce(list_with_self, list_with_self)
    # reduce should short-circuit and return the accumulator object unchanged
    assert reduced_result is list_with_self

    # The list that contains itself as head should have length 1
    assert len(list_with_self) == 1

    # Unshift the self-containing list onto itself to create a nested list; it should not equal the empty list
    nested_list = list_with_self.unshift(list_with_self)
    assert nested_list != EMPTY_LIST

    # Construct an ImmutableList using the is_empty keyword with the computed length and ensure it was preserved
    constructed_with_flag = immutable_list_module.ImmutableList(is_empty=len(list_with_self))
    assert getattr(constructed_with_flag, "is_empty") == len(list_with_self)

    # Calling find with a non-callable argument should raise TypeError
    with pytest.raises(TypeError):
        reduced_result.find(reduced_result)

def test_reduce_raises_type_error_when_reducer_not_callable():
    # Purpose:
    # Verify that ImmutableList.reduce raises a TypeError when the reducer argument is not callable.
    # This test also uses to_list() to obtain a non-callable object to use as the reducer/accumulator.

    # Constants / Setup
    HEAD_VALUE = True
    TAIL_VALUE = {}  # used to demonstrate creation of an ImmutableList with a non-None tail (unused further)
    list_with_dict_tail = immutable_list_module.ImmutableList(tail=TAIL_VALUE)

    # Create a singleton ImmutableList (head=True, tail defaults to None)
    singleton_list = immutable_list_module.ImmutableList(HEAD_VALUE, is_empty=HEAD_VALUE)

    # Execution: obtain a list representation to use as a non-callable reducer and accumulator
    list_representation = singleton_list.to_list()  # expected to be [True]

    # Assertion: reduce should raise TypeError because the reducer argument is not callable
    with pytest.raises(TypeError):
        singleton_list.reduce(list_representation, list_representation)

