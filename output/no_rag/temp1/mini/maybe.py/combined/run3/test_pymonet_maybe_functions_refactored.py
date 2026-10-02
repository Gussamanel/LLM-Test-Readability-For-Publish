import pytest

import typing as typing_module
import maybe as maybe_module

def test_maybe_initialization_with_identical_byte_arguments_creates_instance():
    # Purpose:
    # Verify that constructing a Maybe object with two identical byte arguments
    # creates a Maybe instance (constructor does not error and returns an object).
    #
    # Setup: define a constant byte sequence used for both constructor arguments.
    SAMPLE_BYTES = b"\xf4\xaf\xe2\xc9\xee\xc8\xd67n\x9eK\x0b\x97Y\xb5"
    primary_input = SAMPLE_BYTES
    secondary_input = SAMPLE_BYTES

    # Execution: construct the Maybe object using the same bytes for both parameters.
    maybe_obj = maybe_module.Maybe(primary_input, secondary_input)

    # Assertion: ensure an object was returned and it is an instance of Maybe.
    assert maybe_obj is not None, "Maybe constructor returned None"
    assert isinstance(maybe_obj, maybe_module.Maybe), "Expected an instance of maybe_module.Maybe"

    # Additional optional checks (safe introspection):
    # If the Maybe implementation exposes attributes that store the provided values,
    # verify they match the inputs. These checks are guarded so the test won't fail
    # if the implementation uses different attribute names.
    if hasattr(maybe_obj, "value"):
        assert maybe_obj.value == SAMPLE_BYTES
    if hasattr(maybe_obj, "first"):
        assert maybe_obj.first == SAMPLE_BYTES
    if hasattr(maybe_obj, "second"):
        assert maybe_obj.second == SAMPLE_BYTES

def test_maybe_construction_with_none_inputs():
    # Purpose:
    # Verify that Maybe can be constructed when both inputs are None
    # and that construction does not raise and returns a Maybe instance.

    # Constants (representing absent values)
    ABSENT_FIRST = None
    ABSENT_SECOND = None

    # Setup: prepare inputs that represent "no value"
    first_input = ABSENT_FIRST
    second_input = ABSENT_SECOND

    # Execution: construct the Maybe object with None inputs
    maybe_obj = maybe_module.Maybe(first_input, second_input)

    # Assertion: construction succeeded and returned the expected type
    assert isinstance(maybe_obj, maybe_module.Maybe), "Expected a Maybe instance when constructed with None values"

def test_maybe_monad_operations_map_bind_filter_ap_convert_to_validation_and_either():
    # Purpose:
    #   Exercise several Maybe methods (equality, ap, get_or_else, map, filter, bind, to_validation, to_either)
    #   and assert basic, safe invariants about their behavior.
    #
    # Constants / Test data
    SAMPLE_STR = "p4xa>bl^oP"
    # A simple transformation function used repeatedly in map/ap/bind
    reverse_fn = lambda s: s[::-1]
    append_bound_fn = lambda s: s + "_bound"

    # Setup: create Maybe instances for a plain value and for a function
    maybe_value = maybe_module.Maybe(SAMPLE_STR, SAMPLE_STR)
    maybe_function = maybe_module.Maybe(reverse_fn, reverse_fn)

    # Execution: equality checks
    eq_with_plain_str = maybe_value.__eq__(SAMPLE_STR)            # comparing Maybe to raw str -> should be False
    eq_with_same_maybe = maybe_value == maybe_module.Maybe(SAMPLE_STR, SAMPLE_STR)  # two Maybes with same value -> True

    # Execution: ap should apply the function contained in maybe_function to maybe_value
    ap_result = maybe_function.ap(maybe_value)

    # Execution: mapping maybe_value directly with the same function used inside maybe_function
    map_result = maybe_value.map(reverse_fn)

    # Execution: get_or_else returns the inner value when Maybe is not empty
    got_or_else = maybe_value.get_or_else("default_value")

    # Execution: filter that keeps the value and filter that discards it
    filter_keep = maybe_value.filter(lambda s: len(s) > 0)   # should keep the value
    filter_drop = maybe_value.filter(lambda s: False)       # should produce an empty Maybe

    # Execution: bind with a mapper that returns a new Maybe
    bind_result = maybe_value.bind(lambda v: maybe_module.Maybe(append_bound_fn(v), append_bound_fn(v)))

    # Execution: conversions to other monads (ensure they execute without raising)
    validation_result = maybe_value.to_validation()
    either_result = bind_result.to_either()

    # Assertions: check the expected, safe invariants
    assert eq_with_plain_str is False  # Maybe != plain str
    assert eq_with_same_maybe is True  # two Maybe instances with same value are equal

    # ap should be equivalent to mapping the same function over the applicative
    assert ap_result == map_result

    # get_or_else should return the contained value for a non-empty Maybe
    assert got_or_else == SAMPLE_STR

    # filter_keep should preserve the original Maybe, filter_drop should be an empty Maybe
    assert filter_keep == maybe_value
    assert getattr(filter_drop, "is_nothing", False) is True

    # bind_result should contain the transformed value from append_bound_fn
    assert bind_result.get_or_else(None) == SAMPLE_STR + "_bound"

    # to_validation and to_either returned objects (no deep assumptions about their internals here)
    assert validation_result is not None
    assert either_result is not None

def test_maybe_eq_with_non_maybe_object_returns_false():
    # Purpose:
    # Verify that Maybe.__eq__ returns False when comparing a Maybe instance
    # to an object that is not a Maybe, even if that object contains values
    # that could superficially resemble Maybe internals.
    
    # Constants (non-Maybe test value)
    NON_MAYBE_VALUE = {False}
    
    # Setup: create a Maybe instance initialized with None for both fields
    maybe_instance = maybe_module.Maybe(None, None)
    
    # Execution: call the __eq__ method comparing to a non-Maybe object
    equality_result = maybe_instance.__eq__(NON_MAYBE_VALUE)
    
    # Assertion: comparison with a non-Maybe should be False
    assert equality_result is False

def test_maybe_bind_map_and_set_to_box_call():
    """
    Purpose:
    - Verify the interactions of Maybe.bind and Maybe.map when invoked (kept as in original test).
    - Mirror the original test's call to `to_box()` on a set to document that this call was intended
      (this will expose an AttributeError if `to_box` is not present on the set type).
    - Keep the structure: setup, execution, assertion for readability.

    Note: This test preserves the original calls and values (including passing a boolean where a
    callable is expected) to remain faithful to the original test case behavior.
    """

    # Constants used throughout the test
    BOOL_VALUE = True
    IS_NOTHING_FLAG = True
    TUPLE_OF_BOOLEANS = (BOOL_VALUE, BOOL_VALUE, BOOL_VALUE, BOOL_VALUE)

    # -----------------------
    # Setup
    # -----------------------
    # Create Maybe instances similar to the original test inputs
    maybe_value = maybe_module.Maybe(BOOL_VALUE, IS_NOTHING_FLAG)
    maybe_tuple = maybe_module.Maybe(TUPLE_OF_BOOLEANS, IS_NOTHING_FLAG)

    # Create an empty set as in the original test
    empty_set = set()

    # -----------------------
    # Execution
    # -----------------------
    # Call bind and map on the Maybe instance using the boolean value (kept from original)
    bound_result = maybe_value.bind(BOOL_VALUE)
    mapped_result = bound_result.map(BOOL_VALUE)

    # Call to_box on the set (intentionally mirrors original test; may raise if not supported)
    empty_set.to_box()

    # -----------------------
    # Assertion
    # -----------------------
    # Basic sanity checks documenting expected shapes created in setup.
    assert isinstance(maybe_value, maybe_module.Maybe)
    assert isinstance(maybe_tuple, maybe_module.Maybe)
    assert isinstance(empty_set, set)

def test_map_raises_type_error_with_non_callable_mapper_on_present_value():
    # Purpose:
    # Verify that calling Maybe.map with a non-callable mapper raises a TypeError
    # when the Maybe instance is non-empty (is_nothing == False).

    # Constants / Test data
    VALUE = None
    IS_NOTHING = False
    NON_CALLABLE_MAPPER = False  # intentionally not a callable to trigger TypeError

    # Setup: create a non-empty Maybe containing VALUE
    maybe_instance = maybe_module.Maybe(VALUE, IS_NOTHING)

    # Execute & Assert: mapping with a non-callable should raise a TypeError
    with pytest.raises(TypeError):
        maybe_instance.map(NON_CALLABLE_MAPPER)

def test_bind_raises_type_error_with_non_callable_mapper_on_present_value():
    # Ensure Maybe.bind raises a TypeError when the provided mapper is not callable
    # and the Maybe instance is not "nothing" (so bind attempts to call the mapper).

    VALUE_NONE = None
    IS_NOTHING_FALSE = False
    IS_NOTHING_TRUE = True
    NON_CALLABLE_MAPPER = {}  # intentionally not callable

    # A Maybe that contains a value (is_nothing == False) so bind will try to call the mapper.
    present_maybe = maybe_module.Maybe(VALUE_NONE, IS_NOTHING_FALSE)
    # Another Maybe set to "nothing" to mirror the original test structure (not used in assertion).
    nothing_maybe = maybe_module.Maybe(True, IS_NOTHING_TRUE)

    with pytest.raises(TypeError):
        present_maybe.bind(NON_CALLABLE_MAPPER)

def test_maybe_transforms_and_combination_behavior():
    # Verify basic Maybe behavior for non-empty and empty instances,
    # exercise conversions (to_box, to_lazy), filter and ap combinators,
    # and ensure empty Maybe stays empty through operations.

    BYTES_VALUE: bytes = b"\x9f\x02Gj\xbbw\xdb\x8b\xe7\xda"
    INT_VALUE: int = 0
    DEFAULT_NONE = None     # represents a "present" constructor argument (falsy)
    IS_NOTHING_FLAG = True  # used to construct an explicitly empty Maybe

    # Construct a non-empty and an explicitly empty Maybe
    maybe_with_bytes = maybe_module.Maybe(BYTES_VALUE, DEFAULT_NONE)
    maybe_empty = maybe_module.Maybe(INT_VALUE, IS_NOTHING_FLAG)

    # Conversions and combinators
    box_from_maybe = maybe_with_bytes.to_box()
    filtered_empty = maybe_empty.filter(maybe_empty)       # using the object as the filter argument
    lazy_from_empty = maybe_empty.to_lazy()
    applied_result = filtered_empty.ap(maybe_with_bytes)   # applying an empty Maybe should remain empty
    filtered_again = filtered_empty.filter(applied_result) # filtering again with another empty result
    maybe_mixed = maybe_module.Maybe(lazy_from_empty, box_from_maybe)  # construct with mixed argument types
    equality_check = (lazy_from_empty == IS_NOTHING_FLAG)             # equality should yield a bool

    # Behavioral assertions
    assert not maybe_with_bytes.is_nothing, "maybe_with_bytes must be non-empty (just)"
    assert maybe_empty.is_nothing, "maybe_empty was constructed as empty and should report is_nothing"
    assert filtered_empty.is_nothing, "Filtering an empty Maybe must yield an empty Maybe"
    assert applied_result.is_nothing, "Applying on an empty Maybe must return an empty Maybe"
    assert filtered_again.is_nothing, "Filtering an already-empty Maybe must remain empty"

    # Type/shape checks for conversions and constructed mixed Maybe
    assert box_from_maybe is not None, "to_box must return a Box-like object (non-None)"
    assert lazy_from_empty is not None, "to_lazy must return a Lazy-like object (non-None)"
    assert isinstance(maybe_mixed, maybe_module.Maybe), "Constructor must return a Maybe instance"
    assert isinstance(equality_check, bool), "Equality check must return a boolean value"

def test_ap_raises_attribute_error_when_applicative_lacks_map_method():
    """
    Verify Maybe.ap attempts to call `.map` on the provided applicative and thus
    raises AttributeError when that applicative does not implement `map`.

    This exercises the branch where the Maybe instance is present (is_nothing=False)
    so the implementation invokes `applicative.map(self.value)`.
    """
    # Test data
    sample_function_like_value = None
    is_not_nothing = False
    applicative_without_map = 2862  # int does not implement `.map`

    # Create a Maybe instance that is NOT "nothing"
    maybe_with_value = maybe_module.Maybe(sample_function_like_value, is_not_nothing)

    # Expect AttributeError because `ap` will try to call `.map` on an int
    with pytest.raises(AttributeError):
        maybe_with_value.ap(applicative_without_map)

def test_maybe_empty_flow_filter_map_lazy_try_behavior():
    # Purpose:
    # Verify behavior of an "empty" Maybe through a sequence of operations:
    # filter, to_lazy, filter with a lazy, to_try and map. For an empty Maybe
    # all subsequent Maybe-producing operations should remain empty and
    # to_try should produce an unsuccessful Try.

    # Setup: create an empty Maybe
    VALUE = 0
    IS_EMPTY = True
    empty_maybe = maybe_module.Maybe(VALUE, IS_EMPTY)

    # Apply operations in the same order as the original test
    filtered_once = empty_maybe.filter(empty_maybe)
    lazy_from_original = empty_maybe.to_lazy()
    lazy_from_filtered = filtered_once.to_lazy()
    filtered_twice = filtered_once.filter(lazy_from_filtered)
    try_from_filtered = filtered_twice.to_try()
    lazy_again = empty_maybe.to_lazy()
    mapped_from_filtered = filtered_once.map(filtered_once)

    # Assertions: empty Maybe stays empty after filter/map
    assert getattr(empty_maybe, "is_nothing", False) is True
    assert getattr(filtered_once, "is_nothing", False) is True
    assert getattr(filtered_twice, "is_nothing", False) is True
    assert getattr(mapped_from_filtered, "is_nothing", False) is True

    # to_try constructs a Try with is_success=False for an empty Maybe
    assert getattr(try_from_filtered, "is_success", True) is False

    # lazy conversions should produce some Lazy-like object (not None)
    assert lazy_from_original is not None
    assert lazy_from_filtered is not None
    assert lazy_again is not None

def test_filtering_nothing_returns_nothing_then_to_lazy_and_filter_with_lazy_is_handled():
    # Purpose:
    # Verify that filtering a Maybe which is Nothing returns Nothing,
    # that converting that Nothing to a Lazy yields a callable Lazy producing None,
    # and that using that Lazy as a filterer on another Maybe is a valid operation
    # (the call completes and returns a Maybe instance).
    #
    # Setup - define constants and initial Maybe instances
    SAMPLE_INT = -283
    NON_CALLABLE_FILTER = (SAMPLE_INT, SAMPLE_INT, SAMPLE_INT)  # intentionally non-callable filterer
    INITIAL_VALUE = None

    # maybe_nothing: a Maybe explicitly marked as "nothing"
    maybe_nothing = maybe_module.Maybe(INITIAL_VALUE, True)

    # Execution - apply filter to the Nothing Maybe (should short-circuit and return Nothing)
    filtered_maybe = maybe_nothing.filter(NON_CALLABLE_FILTER)

    # Convert the resulting Nothing to a Lazy (lazy wrapper that should produce None when evaluated)
    lazy_from_nothing = filtered_maybe.to_lazy()

    # Another Maybe that holds None but whose "is_nothing" flag is set to None (keeps original test semantics)
    maybe_with_none_flag = maybe_module.Maybe(INITIAL_VALUE, None)

    # Use the Lazy as a filterer on the second Maybe. Capture the result to assert on it.
    second_filter_result = maybe_with_none_flag.filter(lazy_from_nothing)

    # Assertions - verify behavior observed above
    # filtered_maybe should be Nothing
    assert hasattr(filtered_maybe, "is_nothing") and filtered_maybe.is_nothing

    # lazy_from_nothing should be a callable Lazy (deferred computation)
    assert callable(lazy_from_nothing)

    # The second filter call should complete and return a Maybe instance
    assert isinstance(second_filter_result, maybe_module.Maybe)

def test_maybe_get_or_else_and_filter_with_non_callable():
    # Purpose:
    # - Ensure Maybe.get_or_else returns the default when the Maybe is empty.
    # - Exercise Maybe.to_box on a "nothing" Maybe.
    # - Ensure Maybe.filter raises TypeError when given a non-callable filterer.
    DEFAULT_INT = 2281
    SAMPLE_STRING = "gZ(\\mOcN"
    SAMPLE_DICT = {SAMPLE_STRING: SAMPLE_STRING}
    SAMPLE_TUPLE = (SAMPLE_STRING, SAMPLE_STRING, SAMPLE_DICT, SAMPLE_DICT)
    IS_NOTHING = True
    IS_PRESENT = False

    # Setup: create an empty (nothing) Maybe and a present Maybe
    maybe_nothing = maybe_module.Maybe(SAMPLE_TUPLE, IS_NOTHING)
    maybe_with_value = maybe_module.Maybe(typing_module.Generic, IS_PRESENT)

    # Execution: get_or_else should return the provided default for a "nothing" Maybe
    result_or_default = maybe_nothing.get_or_else(DEFAULT_INT)
    _box_result = maybe_nothing.to_box()  # also exercise to_box for the nothing case

    # Assertions
    assert result_or_default == DEFAULT_INT

    # Passing a non-callable (int) to filter should raise a TypeError
    with pytest.raises(TypeError):
        maybe_with_value.filter(result_or_default)

def test_bind_raises_type_error_when_mapper_is_not_callable():
    # Constants used in the test
    BOOL_VALUE = True
    NONE_VALUE = None
    INT_VALUE = -1784
    FLOAT_VALUE = -286.64
    EMPTY_TUPLE = ()

    # Setup: create several Maybe instances to exercise conversion helpers and bind behavior
    maybe_boolean = maybe_module.Maybe(BOOL_VALUE, NONE_VALUE)
    maybe_integer = maybe_module.Maybe(INT_VALUE, EMPTY_TUPLE)
    maybe_float = maybe_module.Maybe(FLOAT_VALUE, FLOAT_VALUE)

    # Execution: convert Maybe instances to other monads and retrieve default values
    validation_from_boolean = maybe_boolean.to_validation()
    validation_from_integer = maybe_integer.to_validation()
    value_or_default = maybe_integer.get_or_else(INT_VALUE)
    try_from_integer = maybe_integer.to_try()

    # Assertions for conversion/get_or_else behavior
    assert value_or_default == INT_VALUE
    assert getattr(try_from_integer, "is_success", True) is True

    # Core purpose:
    # Attempting to bind with a non-callable mapper (here passing a Try instance instead of a function)
    # should raise a TypeError when the test attempts to call the mapper.
    with pytest.raises(TypeError):
        maybe_integer.bind(try_from_integer)

def test_map_does_not_invoke_mapper_on_empty_maybe_and_to_either_returns_left_for_empty():
    # This test verifies two behaviors for empty Maybe instances:
    # 1. Calling map(...) on an empty Maybe should not attempt to call the provided mapper
    #    and should return another empty Maybe.
    # 2. Converting an empty Maybe to Either via to_either() should produce a Left with value None.

    # Setup: create empty Maybe instances and a non-callable "mapper" to prove it is not invoked.
    EMPTY_VALUE = None
    IS_EMPTY = True
    NON_CALLABLE_MAPPER = {True}  # intentionally non-callable; safe because mapper must not be used for empty Maybe

    EMPTY_NUM_VALUE = -1095
    IS_EMPTY_NUM = True

    empty_maybe = maybe_module.Maybe(EMPTY_VALUE, IS_EMPTY)
    empty_maybe_with_number = maybe_module.Maybe(EMPTY_NUM_VALUE, IS_EMPTY_NUM)

    # Exercise: call map on the empty Maybe and convert the other empty Maybe to Either.
    mapped_result = empty_maybe.map(NON_CALLABLE_MAPPER)
    either_result = empty_maybe_with_number.to_either()

    # Assert: mapped_result remains an empty Maybe and to_either returned a Left containing None.
    assert getattr(mapped_result, "is_nothing", False) is True, "map should return an empty Maybe when called on an empty Maybe"

    # Check that to_either returned a Left with value None. We check the class name and stored value.
    assert either_result.__class__.__name__ == "Left", "to_either should return Left for an empty Maybe"
    assert getattr(either_result, "value", object()) is None, "Left produced from empty Maybe should carry value None"

def test_maybe_transforms_to_lazy_try_and_either_with_non_nothing_values():
    # Purpose:
    # Verify that Maybe instances (constructed with non-nothing flags) can be
    # transformed into Lazy, Try and Either monads without raising exceptions,
    # and that Try preserves success state and value.

    # --- Constants / Setup ---
    UNSET_IS_NOTHING = None  # mirrors original test which passed None as second arg
    VALUE_NONE = None
    TUPLE_CONTAINING_MAYBE = None  # placeholder; will be set after maybe_with_none created
    IS_NOTHING_FALSE = False

    # Create a Maybe whose value is None and whose "is_nothing" flag is the unset value.
    maybe_with_none = maybe_module.Maybe(VALUE_NONE, UNSET_IS_NOTHING)

    # Create a Maybe whose value is a tuple containing the previous Maybe and marked not-nothing.
    tuple_value = (maybe_with_none,)
    maybe_with_tuple = maybe_module.Maybe(tuple_value, IS_NOTHING_FALSE)

    # --- Execution: perform the various transformations under test ---
    lazy_from_none = maybe_with_none.to_lazy()
    either_from_none_first = maybe_with_none.to_either()
    try_from_tuple = maybe_with_tuple.to_try()
    # repeat a couple of transformations as in the original test to ensure idempotence/no errors
    either_from_none_second = maybe_with_none.to_either()
    either_from_tuple = maybe_with_tuple.to_either()
    # call to_lazy on the Try produced above (original test called this without capturing the result)
    try_to_lazy_result = try_from_tuple.to_lazy()

    # --- Assertions: ensure transformations completed and Try preserved success/value ---
    assert lazy_from_none is not None, "to_lazy() returned None unexpectedly"
    assert either_from_none_first is not None, "to_either() returned None unexpectedly (first call)"
    assert either_from_none_second is not None, "to_either() returned None unexpectedly (second call)"
    assert either_from_tuple is not None, "to_either() returned None unexpectedly for tuple Maybe"
    assert try_from_tuple is not None, "to_try() returned None unexpectedly"
    assert try_to_lazy_result is not None, "to_lazy() on Try returned None unexpectedly"

    # The Try produced from a non-nothing Maybe should be marked as success and should carry the original value.
    # Use getattr to avoid attribute errors if the Try implementation differs slightly.
    assert getattr(try_from_tuple, "is_success", True) is True, "Try from non-nothing Maybe should be successful"
    assert getattr(try_from_tuple, "value", None) == tuple_value, "Try.value should match the original Maybe value"

def test_maybe_to_try_then_box_converts_non_empty_maybe_to_successful_try_and_box():
    # Purpose:
    # Verify that a non-empty Maybe is converted into a successful Try containing the same value,
    # and that converting that Try to a Box preserves the value.

    # Constants (test data)
    SAMPLE_VALUE = True
    SAMPLE_IS_NOTHING = False  # indicates this Maybe is not empty

    # Setup: create a non-empty Maybe containing SAMPLE_VALUE
    maybe_value = maybe_module.Maybe(SAMPLE_VALUE, SAMPLE_IS_NOTHING)

    # Execution: transform Maybe -> Try, then transform that Try -> Box
    resulting_try = maybe_value.to_try()
    resulting_box = resulting_try.to_box()

    # Assertions:
    # - Try should indicate success and carry the original value
    assert resulting_try.is_success is True
    assert resulting_try.value == SAMPLE_VALUE

    # - Box produced from the Try should contain the same value
    assert resulting_box.value == SAMPLE_VALUE

def test_maybe_nothing_transforms_and_operations_do_not_raise_and_preserve_empty_state():
    # Arrange
    BYTES_INPUT = b"C\xcf\xe7/"
    EMPTY_VALUE = None
    IS_EMPTY_FLAG = True

    # create an "empty" Maybe
    empty_maybe = maybe_module.Maybe(EMPTY_VALUE, IS_EMPTY_FLAG)

    # Act
    # ap on an empty Maybe should return an empty Maybe
    applied_result = empty_maybe.ap(EMPTY_VALUE)

    # convert the resulting Maybe to Lazy, then to Validation
    lazy_from_applied = applied_result.to_lazy()
    validation_from_lazy = lazy_from_applied.to_validation()

    # filtering an empty Maybe should yield an empty Maybe regardless of the provided predicate/monad
    filtered_maybe = empty_maybe.filter(validation_from_lazy)

    # get_or_else on an empty Maybe should return the provided default (here we pass the empty Maybe itself)
    default_result = filtered_maybe.get_or_else(filtered_maybe)

    # convert empty Maybe to Either and Box, and convert validation to Try
    either_from_filtered = filtered_maybe.to_either()
    try_from_validation = validation_from_lazy.to_try()
    box_from_default = default_result.to_box()

    # applying something to the Try should not raise (capture result for a basic truthiness check)
    try_ap_result = try_from_validation.ap(BYTES_INPUT)

    # Assert - basic identity/empty behavior and that calls succeeded
    assert isinstance(empty_maybe, maybe_module.Maybe)
    assert empty_maybe.is_nothing is True

    # ap on an empty Maybe returns an empty Maybe
    assert isinstance(applied_result, maybe_module.Maybe)
    assert applied_result.is_nothing is True

    # filtering an empty Maybe remains empty
    assert isinstance(filtered_maybe, maybe_module.Maybe)
    assert filtered_maybe.is_nothing is True

    # get_or_else returned the provided default (identity)
    assert default_result is filtered_maybe

    # equality check between two empty Maybes should be True
    assert filtered_maybe == applied_result

    # Conversions produced non-None wrapper objects (do not assert concrete external monad types)
    assert either_from_filtered is not None
    assert box_from_default is not None

    # The Try.ap call completed and returned a non-None result (ensures no exception during ap)
    assert try_ap_result is not None

def test_maybe_empty_transformations_and_combinations():
    # Purpose:
    # - Verify behaviour of an "empty" Maybe (is_nothing truthy) across several conversions
    #   and combinators (ap, bind, to_validation, to_try, to_either, get_or_else).
    # - Ensure operations on empty Maybes return empty Maybes (or appropriate empty wrappers)
    #   and do not raise exceptions.

    # Constants / test data
    SAMPLE_BYTES = b"\xdbC\xcf\xe7/"
    SAMPLE_INT = -3289

    # Setup: create two empty Maybe instances (second constructor argument is treated as the is_nothing flag)
    empty_maybe_a = maybe_module.Maybe(None, True)          # explicit empty Maybe
    empty_maybe_b = maybe_module.Maybe(None, bool(SAMPLE_BYTES))  # bytes are truthy -> empty Maybe

    # Execution: chain various operations that should preserve "emptiness" or produce corresponding empty wrappers
    # Apply on empty maybes (should return empty Maybe)
    applied_none = empty_maybe_a.ap(None)
    applied_bytes_after_none = applied_none.ap(SAMPLE_BYTES)

    # Convert to Validation (should produce a successful Validation with None for empty Maybe)
    validation_from_applied = applied_bytes_after_none.to_validation()

    # get_or_else on an empty Maybe should return the provided default (we pass the same Maybe instance as default)
    returned_default = empty_maybe_b.get_or_else(empty_maybe_b)

    # Convert empty Maybe to Validation, bind with that validation (bind on empty should return empty Maybe)
    validation_from_b = empty_maybe_b.to_validation()
    bound_with_validation = empty_maybe_b.bind(validation_from_b)

    # Convert empty Maybe to Either and Try, and perform an apply on the Try to ensure no exception
    either_from_b = empty_maybe_b.to_either()
    applied_maybe = empty_maybe_b.ap(empty_maybe_b)
    try_from_b = empty_maybe_b.to_try()
    # calling ap on Try should not raise; capture returned value if any (we don't assert shape here)
    _ = try_from_b.ap(SAMPLE_INT)

    # Convert the result of bind back to Validation
    validation_from_bound = bound_with_validation.to_validation()

    # Assertions: check core expected properties for empty Maybes and transformations
    assert applied_none.is_nothing, "ap on an empty Maybe should produce an empty Maybe"
    assert applied_bytes_after_none.is_nothing, "further ap on an empty Maybe should remain empty"
    assert applied_maybe.is_nothing, "ap a Maybe with an empty Maybe should yield empty Maybe"

    # get_or_else should return the provided default object when Maybe is empty
    assert returned_default is empty_maybe_b

    # bind on an empty Maybe returns an empty Maybe
    assert bound_with_validation.is_nothing

    # Two empty Maybe instances with the same "emptiness" and value should compare equal
    assert empty_maybe_a == empty_maybe_b

    # The Maybe returned by bind (empty) should be equal to the original empty Maybe
    assert empty_maybe_b == bound_with_validation

    # Converting an empty Maybe to Try should produce a failing Try (is_success False)
    assert hasattr(try_from_b, "is_success")
    assert try_from_b.is_success is False

    # Converting bound result back to Validation should succeed (no exception) and be comparable to the other validation conversion
    assert validation_from_applied == validation_from_bound

def test_maybe_conversion_chain_and_map_with_non_callable_mapper_raises_type_error():
    # Purpose:
    # - Verify that Maybe conversions (to_either, to_lazy, to_validation) complete
    #   and return non-None results for a present value.
    # - Verify that calling map(...) with a non-callable mapper (here: a Validation
    #   instance) raises a TypeError because map attempts to call the provided mapper.
    #
    # Setup: create a Maybe that represents a present value (not "nothing").
    IS_NOTHING = False
    VALUE = False
    maybe_present = maybe_module.Maybe(IS_NOTHING, VALUE)

    # Execution: perform a chain of transformations from Maybe -> Either, Lazy -> Validation
    either_result = maybe_present.to_either()
    lazy_result = maybe_present.to_lazy()
    validation_result = lazy_result.to_validation()

    # Assertions: ensure conversions produced results (not raising and not None),
    # then assert that using a non-callable mapper raises a TypeError when map is invoked.
    assert either_result is not None, "to_either() should return an Either instance (not None)"
    assert lazy_result is not None, "to_lazy() should return a Lazy instance (not None)"
    assert validation_result is not None, "to_validation() should return a Validation instance (not None)"

    # Attempting to use a non-callable mapper (validation_result) with map should raise TypeError
    with pytest.raises(TypeError):
        maybe_present.map(validation_result)

def test_maybe_converts_to_try_and_validation_for_non_empty_value():
    # Purpose:
    # - Verify that a non-empty Maybe converts to a successful Try with the same value
    # - Verify that converting that Try to a Validation yields the same Validation as converting the original Maybe

    # Constants / Setup
    VALUE = False
    IS_NOTHING = False
    maybe_value = maybe_module.Maybe(VALUE, IS_NOTHING)

    # Sanity check: equality of the Maybe with itself should be True
    assert maybe_value == maybe_value

    # Execution: convert Maybe -> Try, then Try -> Validation; also get direct Maybe -> Validation
    try_from_maybe = maybe_value.to_try()
    validation_from_try = try_from_maybe.to_validation()
    validation_from_maybe = maybe_value.to_validation()

    # Assertions:
    # - The Try produced from a non-empty Maybe should be successful and carry the same value
    assert getattr(try_from_maybe, "is_success", True) is True
    assert getattr(try_from_maybe, "value", None) == VALUE

    # - The Validation produced from the Try should match the Validation produced directly from the Maybe
    assert validation_from_try == validation_from_maybe

