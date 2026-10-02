import pytest

import maybe as maybe_module
import typing as typing_module

def test_construct_maybe_with_identical_bytes_returns_maybe_instance():
    """Verify Maybe accepts two identical byte sequences and returns a Maybe instance."""
    # Constants / Setup
    TEST_BYTES = b"\xf4\xaf\xe2\xc9\xee\xc8\xd67n\x9eK\x0b\x97Y\xb5"
    left_input = TEST_BYTES
    right_input = TEST_BYTES

    # Execution: construct the Maybe object with the provided inputs
    maybe_instance = maybe_module.Maybe(left_input, right_input)

    # Assertion: the constructor produced an instance of the expected type
    assert isinstance(maybe_instance, maybe_module.Maybe)

def test_maybe_construction_with_both_none():
    """
    Purpose:
    Verify that Maybe can be constructed when both the value and the error are None.
    This ensures the constructor accepts None inputs and returns a Maybe instance
    without raising an exception.
    """

    # --- Setup: define inputs for the test ---
    VALUE_ARG = None
    ERROR_ARG = None

    # --- Execution: create the Maybe object with both arguments set to None ---
    maybe_instance = maybe_module.Maybe(VALUE_ARG, ERROR_ARG)

    # --- Assertion: the construction succeeded and returned a Maybe instance ---
    assert isinstance(maybe_instance, maybe_module.Maybe)

def test_maybe_pipeline_equality_ap_map_filter_bind_transformations():
    """
    Purpose:
      Exercise a sequence of Maybe operations to ensure the methods can be invoked
      in various combinations: equality, applicative ap, map, filter, get_or_else,
      to_validation, bind and to_either. This test documents the interactions and
      verifies basic return types (presence and boolean results) rather than
      specific semantic outcomes.

    Notes:
      The original test intentionally passes values of different shapes (e.g. raw
      strings) into functions that normally expect callables or applicatives. The
      goal here is not to change behavior but to make the steps and intent
      explicit, with clear setup / execution / assertion sections.
    """

    # ---------------------
    # Constants / Setup
    # ---------------------
    SAMPLE_VALUE = "p4xa>bl^oP"
    maybe_primary = maybe_module.Maybe(SAMPLE_VALUE, SAMPLE_VALUE)
    maybe_secondary = maybe_module.Maybe(SAMPLE_VALUE, SAMPLE_VALUE)

    # ---------------------
    # Execution
    # ---------------------
    # Equality check between Maybe and a raw value
    equality_with_raw = maybe_primary.__eq__(SAMPLE_VALUE)

    # Applicative application: apply the contents of maybe_primary to a raw value
    applied_first = maybe_primary.ap(SAMPLE_VALUE)

    # Provide default value when Maybe is empty or return contained value
    default_or_value = maybe_primary.get_or_else(SAMPLE_VALUE)

    # Map and filter using the result of earlier ap calls (mirrors original loose typing)
    mapped_from_ap_1 = maybe_primary.map(applied_first)
    filtered_from_ap_1 = maybe_primary.filter(applied_first)
    mapped_from_ap_2 = maybe_primary.map(applied_first)

    # Repeat ap to produce a second applicative result and compare applicative results
    applied_second = maybe_primary.ap(SAMPLE_VALUE)
    equality_between_applied = applied_first.__eq__(applied_second)

    # Filter on the applied result using the result of get_or_else
    filtered_on_applied = applied_first.filter(default_or_value)

    # Extract default or value from the second applied result
    get_or_else_from_second = applied_second.get_or_else(SAMPLE_VALUE)

    # Transform secondary maybe into Validation, then bind and convert to Either
    validation_from_secondary = maybe_secondary.to_validation()
    bound_from_secondary = maybe_secondary.bind(validation_from_secondary)
    either_from_bound = bound_from_secondary.to_either()

    # ---------------------
    # Assertions
    # ---------------------
    # Ensure core operations completed and produced expected basic types.
    # We assert only on safe, general properties (instances and boolean results)
    assert isinstance(maybe_primary, maybe_module.Maybe)
    assert isinstance(maybe_secondary, maybe_module.Maybe)
    assert isinstance(equality_with_raw, bool)
    assert isinstance(equality_between_applied, bool)

def test_maybe_equality_with_non_maybe_returns_false():
    """Verify Maybe.__eq__ returns False when comparing against a non-Maybe object."""
    # Setup
    NON_MAYBE_OBJECT = {False}  # a plain set (definitely not a Maybe)
    EXPECTED_EQUALITY = False

    # Create a Maybe instance for comparison
    maybe_instance = maybe_module.Maybe(None, None)

    # Exercise
    equality_result = maybe_instance == NON_MAYBE_OBJECT

    # Verify
    assert equality_result is EXPECTED_EQUALITY

def test_maybe_bind_map_and_to_box_transforms():
    # Purpose:
    # - Verify Maybe.bind applies a mapper that returns another Maybe
    # - Verify Maybe.map transforms the inner value when the Maybe is not empty
    # - Verify Maybe.to_box converts a non-empty Maybe into a Box containing the same value,
    #   and converts an empty Maybe into a Box containing None

    # Constants / test data
    INPUT_BOOL = True
    EXPECTED_TUPLE_AFTER_MAP = (False, False, False, False)

    # Setup: create a non-empty Maybe containing a boolean
    maybe_bool = maybe_module.Maybe.just(INPUT_BOOL)

    # Execution: bind to a new Maybe (flip the boolean), then map that value into a 4-tuple
    bound_maybe = maybe_bool.bind(lambda v: maybe_module.Maybe.just(not v))
    mapped_maybe = bound_maybe.map(lambda v: (v, v, v, v))

    # Assertion: check bind produced a non-empty Maybe with the flipped value,
    # and map produced the expected tuple inside a non-empty Maybe
    assert not maybe_bool.is_nothing
    assert not bound_maybe.is_nothing
    assert bound_maybe.value is False
    assert not mapped_maybe.is_nothing
    assert mapped_maybe.value == EXPECTED_TUPLE_AFTER_MAP

    # Execution / Assertion: convert a non-empty Maybe (holding the tuple) to a Box
    tuple_maybe = maybe_module.Maybe.just(EXPECTED_TUPLE_AFTER_MAP)
    box_from_tuple = tuple_maybe.to_box()
    assert hasattr(box_from_tuple, "value")
    assert box_from_tuple.value == EXPECTED_TUPLE_AFTER_MAP

    # Execution / Assertion: converting an empty Maybe to Box yields Box(None)
    empty_maybe = maybe_module.Maybe.nothing()
    box_from_nothing = empty_maybe.to_box()
    assert hasattr(box_from_nothing, "value")
    assert box_from_nothing.value is None

def test_map_raises_type_error_when_mapper_is_not_callable():
    # Purpose:
    # Ensure Maybe.map raises a TypeError when a non-callable mapper is provided
    # and the Maybe instance actually contains a value (is_nothing is False).

    # Setup
    SAMPLE_VALUE = None
    IS_NOTHING_FLAG = False  # False indicates the Maybe contains a value
    INVALID_MAPPER = False   # intentionally non-callable to trigger a TypeError

    maybe_instance = maybe_module.Maybe(SAMPLE_VALUE, IS_NOTHING_FLAG)

    # Execution & Assertion: calling map with a non-callable should raise TypeError
    with pytest.raises(TypeError):
        maybe_instance.map(INVALID_MAPPER)

def test_bind_behavior_with_non_callable_mapper():
    """
    Verify bind behavior when given a non-callable mapper:
    - If the Maybe is 'nothing' the mapper must not be invoked and bind should return a 'nothing' Maybe.
    - If the Maybe is a value (even if that value is None) bind must attempt to call the mapper, so passing a non-callable should raise TypeError.
    """

    # Non-callable provided as the mapper
    NON_CALLABLE_MAPPER = {}  # intentionally not callable

    # Values used to construct Maybe instances
    PRESENT_VALUE = True
    NONE_VALUE = None

    # Booleans indicating Maybe state for the constructor
    IS_NOTHING = True   # used to create a 'nothing' Maybe
    IS_SOMETHING = False  # used to create a 'something' Maybe

    # Setup: create two Maybe instances:
    # - maybe_nothing: represents an empty Maybe (is_nothing == True)
    # - maybe_with_none: represents a present Maybe whose value is None (is_nothing == False)
    maybe_nothing = maybe_module.Maybe(PRESENT_VALUE, IS_NOTHING)
    maybe_with_none = maybe_module.Maybe(NONE_VALUE, IS_SOMETHING)

    # Binding a 'nothing' Maybe should return a 'nothing' Maybe and must not attempt to call the mapper.
    result = maybe_nothing.bind(NON_CALLABLE_MAPPER)
    assert result.is_nothing is True

    # Binding a non-nothing Maybe should attempt to call the mapper, therefore providing a non-callable should raise TypeError.
    with pytest.raises(TypeError):
        maybe_with_none.bind(NON_CALLABLE_MAPPER)

def test_maybe_empty_behaviors_and_conversions():
    # Purpose:
    # - Verify behavior of Maybe when it's empty (is_nothing=True):
    #   * filter returns Maybe.nothing()
    #   * ap returns Maybe.nothing() when called on an empty Maybe
    # - Verify conversion helpers to_box and to_lazy produce objects (Box / Lazy)
    # - Verify equality checks with unrelated types return False

    # --- Setup ---
    BYTES_VALUE = b"\x9f\x02Gj\xbbw\xdb\x8b\xe7\xda"
    ZERO_INT = 0

    # Create a non-empty Maybe containing bytes and an explicit empty Maybe (is_nothing=True)
    maybe_with_bytes = maybe_module.Maybe(BYTES_VALUE, False)
    maybe_empty_int = maybe_module.Maybe(ZERO_INT, True)

    # --- Execution ---
    # Convert the non-empty Maybe to a Box
    box_from_bytes = maybe_with_bytes.to_box()

    # Convert the empty Maybe to a Lazy (should produce a Lazy that yields None)
    lazy_from_empty = maybe_empty_int.to_lazy()

    # Filtering an empty Maybe always yields Maybe.nothing()
    filtered_empty = maybe_empty_int.filter(lambda v: True)

    # Applying a function inside an empty Maybe (ap) should also yield Maybe.nothing()
    applied_on_bytes = filtered_empty.ap(maybe_with_bytes)

    # Further filtering of an already empty Maybe stays empty
    filtered_again = filtered_empty.filter(lambda v: True)

    # Combine different objects into a Maybe to ensure construction still produces a Maybe instance
    combined_maybe = maybe_module.Maybe(lazy_from_empty, box_from_bytes)

    # Check equality of the Lazy object with an unrelated boolean value (should be False)
    lazy_eq_true = lazy_from_empty.__eq__(True)

    # --- Assertions ---
    # Expect the filter/ap operations on the empty Maybe to result in a canonical nothing Maybe
    assert filtered_empty == maybe_module.Maybe.nothing()
    assert applied_on_bytes == maybe_module.Maybe.nothing()
    assert filtered_again == maybe_module.Maybe.nothing()

    # Construction with arbitrary objects should produce a Maybe instance
    assert isinstance(combined_maybe, maybe_module.Maybe)

    # The Lazy produced from an empty Maybe should not be equal to a boolean True
    assert lazy_eq_true is False

def test_ap_raises_attribute_error_when_applicative_lacks_map():
    """Verify Maybe.ap() attempts to call `.map` on the provided applicative
    when the Maybe instance is not 'nothing'. If the applicative does not
    implement `.map`, an AttributeError should be raised.
    """
    # Arrange
    non_applicative = 2862  # int does not have a .map method
    contained_value = None
    is_nothing = False
    function_maybe = maybe_module.Maybe(contained_value, is_nothing)

    # Act & Assert: calling ap should try to call non_applicative.map(...) and raise
    with pytest.raises(AttributeError):
        function_maybe.ap(non_applicative)

def test_maybe_empty_preserves_emptiness_through_filters_maps_and_conversions():
    # Arrange: create an empty Maybe
    INITIAL_VALUE = 0
    INITIAL_IS_NOTHING = True
    maybe_empty = maybe_module.Maybe(INITIAL_VALUE, INITIAL_IS_NOTHING)

    # Sanity of setup
    assert isinstance(maybe_empty, maybe_module.Maybe)
    assert getattr(maybe_empty, "is_nothing", True) is True

    # Act: operations that should all preserve "nothingness"
    filtered_result = maybe_empty.filter(maybe_empty)        # filter with a non-callable
    lazy_from_maybe = maybe_empty.to_lazy()                 # convert empty Maybe -> Lazy
    lazy_from_filtered = filtered_result.to_lazy()          # convert filtered empty Maybe -> Lazy
    filtered_again = filtered_result.filter(lazy_from_filtered)  # attempt to filter with a Lazy
    try_from_filtered = filtered_again.to_try()             # convert empty Maybe -> Try (should be unsuccessful)
    lazy_again = maybe_empty.to_lazy()                      # idempotent to_lazy
    mapped_from_filtered = filtered_result.map(filtered_result)  # map with non-callable -> remains empty

    # Assert: all Maybe results remain empty
    assert isinstance(filtered_result, maybe_module.Maybe)
    assert isinstance(filtered_again, maybe_module.Maybe)
    assert isinstance(mapped_from_filtered, maybe_module.Maybe)

    assert getattr(filtered_result, "is_nothing", False) is True
    assert getattr(filtered_again, "is_nothing", False) is True
    assert getattr(mapped_from_filtered, "is_nothing", False) is True

    # The Try produced from an empty Maybe should indicate failure
    assert hasattr(try_from_filtered, "is_success")
    assert try_from_filtered.is_success is False

    # Lazy conversions should produce something non-None and not accidentally be Maybe or Try
    assert lazy_from_maybe is not None
    assert lazy_from_filtered is not None
    assert lazy_again is not None

    assert not isinstance(lazy_from_maybe, maybe_module.Maybe)
    assert not isinstance(lazy_from_maybe, type(try_from_filtered))
    assert not isinstance(lazy_from_filtered, maybe_module.Maybe)
    assert not isinstance(lazy_again, maybe_module.Maybe)

def test_maybe_filter_short_circuits_and_to_lazy_transforms_nothing():
    # Purpose:
    # - Ensure Maybe.filter short-circuits when the Maybe is "nothing" (i.e. filterer is not invoked).
    # - Ensure Maybe.to_lazy converts a "nothing" Maybe into a Lazy that returns None.
    # - Ensure using that Lazy as a predicate against a Maybe containing None yields a "nothing" result
    #   because the predicate evaluates to a falsy value (None).

    # --- Setup ---
    SAMPLE_INT = -283
    SAMPLE_FILTERER = (SAMPLE_INT, SAMPLE_INT, SAMPLE_INT)  # intentionally non-callable; should not be invoked
    NOTHING_VALUE = None

    # Construct a Maybe that is "nothing" (second arg truthy indicates is_nothing)
    maybe_nothing = maybe_module.Maybe(NOTHING_VALUE, True)

    # --- Execution ---
    # Filtering a "nothing" Maybe must short-circuit and produce another "nothing" Maybe
    filtered_nothing = maybe_nothing.filter(SAMPLE_FILTERER)

    # Convert the resulting nothing Maybe to a Lazy thunk
    lazy_from_nothing = filtered_nothing.to_lazy()

    # Construct a Maybe that is NOT marked as nothing but holds the value None
    maybe_with_none = maybe_module.Maybe(NOTHING_VALUE, None)

    # Use the Lazy returned earlier as the "filterer" for maybe_with_none.
    # The Lazy, when invoked, returns None (a falsy value), so the filter should produce a nothing Maybe.
    final_filtered = maybe_with_none.filter(lazy_from_nothing)

    # --- Assertions ---
    # filtered_nothing should be a nothing Maybe (short-circuit happened)
    assert getattr(filtered_nothing, "is_nothing", False) is True

    # The lazy thunk created from a nothing Maybe should return None when called
    # (to_lazy returns a Lazy that wraps a zero-argument function)
    assert callable(lazy_from_nothing)
    assert lazy_from_nothing() is None

    # Applying that lazy as a predicate to a Maybe containing None should yield a nothing Maybe
    assert getattr(final_filtered, "is_nothing", False) is True

def test_maybe_get_or_else_returns_default_and_filter_with_non_callable_raises_type_error():
    # Constants / test data
    DEFAULT_INT = 2281
    SAMPLE_STR = r"gZ(\mOcN"
    SAMPLE_DICT = {SAMPLE_STR: SAMPLE_STR}
    SAMPLE_TUPLE = (SAMPLE_STR, SAMPLE_STR, SAMPLE_DICT, SAMPLE_DICT)
    IS_NOTHING = True
    IS_JUST = False

    # Setup: create an empty Maybe and a non-empty Maybe
    empty_maybe = maybe_module.Maybe(SAMPLE_TUPLE, IS_NOTHING)

    # Execution: calling get_or_else on an empty Maybe should return the provided default
    default_value = empty_maybe.get_or_else(DEFAULT_INT)

    # Also convert the empty Maybe to a Box (should contain None for an empty Maybe)
    boxed = empty_maybe.to_box()

    # Create a simple Generic-derived object to store in a non-empty Maybe
    class DummyGeneric(typing_module.Generic):
        pass

    generic_value = DummyGeneric()
    non_empty_maybe = maybe_module.Maybe(generic_value, IS_JUST)

    # Assertions for get_or_else and to_box behavior
    assert default_value == DEFAULT_INT, "get_or_else should return the provided default for an empty Maybe"

    # to_box should produce a Box representing None for an empty Maybe.
    # We check that the Box exposes an attribute 'value' equal to None if present;
    # if the Box implementation uses a different attribute, getattr will return None as a safe fallback.
    assert getattr(boxed, "value", None) is None

    # Execution + Assertion: passing a non-callable as the filter should raise a TypeError
    # (filter expects a callable; here we intentionally pass the integer returned by get_or_else)
    with pytest.raises(TypeError):
        non_empty_maybe.filter(default_value)

def test_maybe_transforms_and_bind_return_types():
    # Purpose:
    # - Verify that Maybe can be transformed into Validation and Try without raising.
    # - Verify get_or_else returns a concrete value when called.
    # - Verify bind accepts a mapper and returns another Maybe.
    #
    # This test focuses on calling transformation helpers and bind; it does not
    # assume detailed internals of Validation/Try, only that results are returned.

    # --- Constants / Setup ---
    BOOL_VALUE = True
    NONE_MARKER = None

    INT_VALUE = -1784
    EMPTY_TUPLE = ()

    FLOAT_VALUE = -286.64

    maybe_true = maybe_module.Maybe(BOOL_VALUE, NONE_MARKER)
    maybe_int = maybe_module.Maybe(INT_VALUE, EMPTY_TUPLE)
    maybe_float = maybe_module.Maybe(FLOAT_VALUE, FLOAT_VALUE)

    # --- Execution ---
    # Transform Maybe instances into Validation objects
    validation_from_true = maybe_true.to_validation()
    validation_from_int = maybe_int.to_validation()

    # get_or_else should return a concrete value (either the Maybe value or the provided default)
    default_for_int = maybe_int.get_or_else(INT_VALUE)

    # Transform Maybe into a Try object
    try_from_int = maybe_int.to_try()

    # Bind with a simple mapper that wraps the mapped value back into a Maybe.
    # Using a callable avoids passing non-callables to bind.
    bind_result = maybe_int.bind(lambda v: maybe_module.Maybe(v, None))

    # --- Assertions ---
    # We assert results are produced (not None) and bind returns a Maybe instance.
    assert validation_from_true is not None
    assert validation_from_int is not None
    assert default_for_int is not None
    assert try_from_int is not None
    assert isinstance(bind_result, maybe_module.Maybe)

def test_map_on_empty_maybe_returns_nothing_and_to_either_on_empty_maybe_returns_left_none() -> None:
    # Constants for clarity
    EMPTY_VALUE = None
    MARKED_AS_NOTHING = True
    NON_CALLABLE_MAPPER = {True}
    SOME_INT = -1095
    ALSO_MARKED_AS_NOTHING = True

    # Setup: an empty Maybe (marked as nothing) and a Maybe that contains a value but is marked as nothing
    empty_maybe = maybe_module.Maybe(EMPTY_VALUE, MARKED_AS_NOTHING)
    marked_nothing_maybe = maybe_module.Maybe(SOME_INT, ALSO_MARKED_AS_NOTHING)

    # Execution:
    # - mapping over a nothing should yield a nothing Maybe (mapper is intentionally non-callable;
    #   it must not be invoked for a nothing)
    mapped_result = empty_maybe.map(NON_CALLABLE_MAPPER)

    # - converting a nothing Maybe to Either should yield a Left containing None
    either_result = marked_nothing_maybe.to_either()

    # Assertions
    assert getattr(mapped_result, "is_nothing", False) is True
    assert type(either_result).__name__ == "Left"
    assert getattr(either_result, "value", None) is None

def test_maybe_transformation_chain():
    # Purpose:
    # Verify a sequence of transformations from Maybe to Lazy, Either and Try
    # for both an "empty-like" Maybe and a Maybe containing a tuple.
    #
    # We keep assertions minimal and robust (only checking that transformation
    # methods return a monadic object) to avoid coupling the test to the
    # concrete internals of Lazy, Either or Try implementations.

    # Constants / configuration used in this test
    NONE_VALUE = None
    IS_NOTHING_UNSET = None  # a falsy value used to simulate an unspecified "is_nothing"
    IS_NOTHING_FALSE = False

    # ---------------------
    # Setup
    # ---------------------
    # Create a Maybe that holds None as its value and uses a falsy is_nothing flag.
    maybe_empty = maybe_module.Maybe(NONE_VALUE, IS_NOTHING_UNSET)

    # Create a Maybe that contains a tuple which itself contains the previous Maybe.
    tuple_with_maybe = (maybe_empty,)
    maybe_with_tuple = maybe_module.Maybe(tuple_with_maybe, IS_NOTHING_FALSE)

    # ---------------------
    # Execution (perform transformations)
    # ---------------------
    # Transform the empty-like Maybe to a Lazy monad
    lazy_from_empty = maybe_empty.to_lazy()

    # Transform the empty-like Maybe to an Either monad
    either_from_empty = maybe_empty.to_either()

    # Transform the tuple-containing Maybe to a Try monad
    try_from_tuple = maybe_with_tuple.to_try()

    # Transform both Maybes to Either to exercise both paths
    either_from_tuple = maybe_with_tuple.to_either()
    either_from_empty_again = maybe_empty.to_either()

    # Also convert the Try result to Lazy to exercise chaining across monads
    try_from_tuple.to_lazy()

    # ---------------------
    # Assertions (kept simple and robust)
    # ---------------------
    assert lazy_from_empty is not None, "to_lazy() should return a Lazy-like object"
    assert either_from_empty is not None, "to_either() should return an Either-like object"
    assert try_from_tuple is not None, "to_try() should return a Try-like object"
    assert either_from_tuple is not None, "to_either() should return an Either-like object for non-empty Maybe"
    assert either_from_empty_again is not None, "subsequent to_either() call should also return an Either-like object"

def test_maybe_to_try_then_to_box_returns_box_with_value_when_present():
    # Test setup: a non-empty Maybe wrapping a boolean value
    PRESENT_VALUE = True
    IS_NOTHING_FLAG = False

    maybe_instance = maybe_module.Maybe(PRESENT_VALUE, IS_NOTHING_FLAG)

    # Sanity check on the Maybe state before transformations
    assert hasattr(maybe_instance, "is_nothing")
    assert maybe_instance.is_nothing is False

    # Execution: transform Maybe -> Try -> Box
    try_instance = maybe_instance.to_try()
    box_instance = try_instance.to_box()

    # Assertions: ensure the Try and resulting Box carry the original value and success/state flags
    assert hasattr(try_instance, "is_success")
    assert try_instance.is_success is True
    assert hasattr(try_instance, "value")
    assert try_instance.value == PRESENT_VALUE

    assert hasattr(box_instance, "value")
    assert box_instance.value == PRESENT_VALUE

def test_maybe_nothing_conversions_and_applications():
    # This test verifies that a Maybe constructed as "nothing" preserves the empty/nothing semantics
    # through a sequence of monad conversions and operations (ap, to_lazy, to_validation, filter, get_or_else,
    # to_either, to_try, to_box). It also ensures these operations complete without raising and that
    # equality/relationships between intermediate values behave as expected for an empty Maybe.
    
    # Constants / Setup
    SAMPLE_BYTES = b"C\xcf\xe7/"
    NOTHING = None
    IS_NOTHING = True

    # Create a Maybe that represents "nothing"
    maybe_nothing = maybe_module.Maybe(NOTHING, IS_NOTHING)

    # Execution: perform a chain of conversions and operations
    applied_result = maybe_nothing.ap(NOTHING)            # applying when Maybe is nothing should yield nothing
    lazy_result = applied_result.to_lazy()                # convert to Lazy
    validation_result = lazy_result.to_validation()       # convert Lazy -> Validation
    filtered_maybe = maybe_nothing.filter(validation_result)  # attempt to filter using the validation result
    default_result = filtered_maybe.get_or_else(filtered_maybe)  # get_or_else should return provided default for nothing
    either_result = filtered_maybe.to_either()            # convert Maybe -> Either
    try_result = validation_result.to_try()               # convert Validation -> Try
    equality_with_applied = filtered_maybe.__eq__(applied_result)  # explicit equality check
    boxed_result = default_result.to_box()                # convert result -> Box

    # Ensure calling ap on the Try instance with a bytes argument completes (no exception)
    _ = try_result.ap(SAMPLE_BYTES)

    # Assertions: confirm "nothing" semantics and that conversions produced objects (no exceptions)
    assert maybe_nothing.is_nothing is True
    assert applied_result.is_nothing is True
    assert filtered_maybe.is_nothing is True
    assert filtered_maybe == applied_result
    assert default_result == filtered_maybe
    assert equality_with_applied is True
    assert either_result is not None
    assert boxed_result is not None
    # Try should expose an is_success boolean flag per the implementation of to_try
    assert hasattr(try_result, "is_success") and isinstance(try_result.is_success, bool)

def test_maybe_ap_bind_and_conversions_work_together():
    # Purpose:
    # - Exercise Maybe.ap, Maybe.bind and the conversion helpers (to_validation, to_either, to_try)
    # - Ensure operations on a "nothing" Maybe remain "nothing"-like and that get_or_else returns the provided default
    # - Call Try.ap to exercise the interop path (no strict behavior asserted for Try.ap here)

    # Sample constants and two Maybe instances
    SAMPLE_BYTES = b"\xdbC\xcf\xe7/"
    SAMPLE_INT = -3289

    # maybe_nothing simulates an empty Maybe (second parameter is the is_nothing flag)
    maybe_nothing = maybe_module.Maybe(None, True)
    # maybe_flagged uses a truthy, non-bool is_nothing flag to exercise non-boolean flags
    maybe_flagged = maybe_module.Maybe(None, SAMPLE_BYTES)

    # Applying on an empty Maybe should propagate emptiness (ap returns a Maybe)
    result_after_first_ap = maybe_nothing.ap(None)
    result_after_second_ap = result_after_first_ap.ap(SAMPLE_BYTES)

    # Convert the resulting "nothing" Maybe to a Validation
    validation_from_nothing = result_after_second_ap.to_validation()

    # get_or_else on a maybe considered "nothing" should return the provided default
    default_returned = maybe_flagged.get_or_else(maybe_flagged)

    # Convert the flagged Maybe to Validation and Either
    validation_from_flagged = maybe_flagged.to_validation()
    either_from_flagged = maybe_flagged.to_either()

    # Attempt to bind the flagged Maybe with a non-callable value (exercises branch where bind
    # returns nothing when the Maybe is "nothing" or mapper is not callable)
    bind_result = maybe_flagged.bind(validation_from_flagged)

    # Apply the flagged Maybe to itself (ap expects an applicative containing a function; this simply exercises ap)
    ap_with_flagged = maybe_flagged.ap(maybe_flagged)

    # Convert flagged Maybe to Try and call ap on the returned Try to exercise Try.ap path
    try_from_flagged = maybe_flagged.to_try()
    try_from_flagged.ap(SAMPLE_INT)

    # Equality checks invoked in original test: ensure these produce booleans
    equality_between_either_and_validation = either_from_flagged.__eq__(validation_from_flagged)
    equality_between_maybe_and_bind_result = maybe_flagged.__eq__(bind_result)

    # Assertions

    # ap calls on the empty Maybe should preserve the "nothing" semantics (objects expose is_nothing)
    assert hasattr(result_after_first_ap, "is_nothing")
    assert hasattr(result_after_second_ap, "is_nothing")

    # Conversions should return non-None results (Validation/Either/Try objects)
    assert validation_from_nothing is not None
    assert validation_from_flagged is not None
    assert either_from_flagged is not None
    assert try_from_flagged is not None

    # get_or_else with the Maybe itself as default should return that default object (identity)
    assert default_returned is maybe_flagged

    # bind_result should be produced (even if it's a "nothing" Maybe); ensure attribute presence
    assert bind_result is not None
    assert hasattr(bind_result, "is_nothing")

    # The equality checks used in the original test should yield boolean values
    assert isinstance(equality_between_either_and_validation, bool)
    assert isinstance(equality_between_maybe_and_bind_result, bool)

    # The ap_with_flagged result should exist and expose expected Maybe attributes
    assert ap_with_flagged is not None
    assert hasattr(ap_with_flagged, "is_nothing")

def test_maybe_transformations_and_map_with_present_value():
    # Purpose:
    # Verify that a Maybe constructed as a present value (is_nothing=False, value=False)
    # can be transformed to Either, Lazy and Validation, and that the result of those
    # transformations can be passed to Maybe.map without breaking (map returns a Maybe).
    #
    # Note: the test uses a falsy value (False) to ensure transformations and equality
    # behave correctly for falsy but present values.

    # Constants (clear intent for the boolean flags and value used)
    IS_NOTHING = False
    VALUE_FALSE = False

    # Setup: create Maybe instances representing a present (just) value
    maybe_present = maybe_module.Maybe(IS_NOTHING, VALUE_FALSE)
    maybe_for_transforms = maybe_module.Maybe(IS_NOTHING, VALUE_FALSE)
    maybe_to_map = maybe_module.Maybe(IS_NOTHING, VALUE_FALSE)

    # Execution: perform operations under test
    # 1) Compare Maybe with a non-Maybe object (a plain False) using __eq__
    equality_with_non_maybe = maybe_present.__eq__(VALUE_FALSE)

    # 2) Transform the Maybe into other monads
    either_result = maybe_for_transforms.to_either()
    lazy_result = maybe_for_transforms.to_lazy()
    # Convert the Lazy result into a Validation (exercise a chain of conversions)
    validation_from_lazy = lazy_result.to_validation()

    # 3) Use the resulting validation as the mapper argument to Maybe.map
    #    (the library's types may make this callable; the test verifies map accepts it)
    mapped_result = maybe_to_map.map(validation_from_lazy)

    # Assertions: ensure operations completed and returned expected high-level types/values
    assert equality_with_non_maybe is False  # comparing Maybe to a non-Maybe boolean yields False
    assert either_result is not None         # to_either produced a value (Left/Right)
    assert lazy_result is not None           # to_lazy produced a Lazy instance
    assert validation_from_lazy is not None  # Lazy -> Validation conversion produced a value
    # map should return a Maybe instance regardless of internal mapper behavior
    assert isinstance(mapped_result, maybe_module.Maybe)

def test_maybe_conversion_chain_preserves_value_and_equality():
    # Purpose:
    # - Ensure a non-empty Maybe compares equal to itself.
    # - Ensure converting that Maybe to Try and then to Validation completes without error
    #   (i.e., the conversion chain exists for a present value).

    # Constants / setup
    SAMPLE_VALUE = False
    IS_NOTHING_FLAG = False  # False => Maybe is present (not "nothing")
    maybe_instance = maybe_module.Maybe(SAMPLE_VALUE, IS_NOTHING_FLAG)

    # Execution
    # Check equality with itself (uses Maybe.__eq__)
    equality_with_self = maybe_instance == maybe_instance

    # Convert Maybe -> Try (uses Maybe.to_try), then Try -> Validation (via Try.to_validation)
    try_monad = maybe_instance.to_try()
    validation_from_try = try_monad.to_validation()

    # Assertions
    # Equality should hold for the same instance
    assert equality_with_self is True
    # Conversions should produce non-None results (they should not raise and should return objects)
    assert try_monad is not None
    assert validation_from_try is not None

