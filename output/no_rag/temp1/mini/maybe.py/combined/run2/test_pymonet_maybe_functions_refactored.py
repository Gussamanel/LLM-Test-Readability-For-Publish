import pytest

import maybe as maybe_module
import typing as typing_module

def test_maybe_constructs_when_both_args_are_same_byte_sequence():
    # Verify Maybe can be instantiated when both constructor arguments are identical bytes.
    SAMPLE_BYTES = b"\xf4\xaf\xe2\xc9\xee\xc8\xd67n\x9eK\x0b\x97Y\xb5"

    first_bytes = SAMPLE_BYTES
    second_bytes = SAMPLE_BYTES

    maybe_instance = maybe_module.Maybe(first_bytes, second_bytes)

    assert isinstance(maybe_instance, maybe_module.Maybe)

def test_maybe_constructs_with_none_inputs():
    # Purpose:
    #   Ensure the Maybe type can be instantiated when both constructor arguments are None.
    #
    # Setup (Arrange):
    #   Define a clear constant for the None input so intent is explicit.
    NONE_VALUE: typing_module.Optional[typing_module.Any] = None

    # Execution (Act):
    #   Construct a Maybe using None for both parameters.
    maybe_instance = maybe_module.Maybe(NONE_VALUE, NONE_VALUE)

    # Verification (Assert):
    #   - Construction should succeed (object is not None).
    #   - The returned object should be an instance of maybe_module.Maybe.
    #   - Basic operations like repr() should work and return a string.
    assert maybe_instance is not None
    assert isinstance(maybe_instance, maybe_module.Maybe)
    assert isinstance(repr(maybe_instance), str)

def test_maybe_ap_map_filter_bind_and_transforms():
    # Purpose:
    # Verify core Maybe behaviors: equality comparison with raw values,
    # applying a contained function to another Maybe (ap),
    # mapping, filtering, binding to another Maybe, and conversions to other monads.

    # Constants / test data
    ORIGINAL_STR = "p4xa>bl^oP"
    SUFFIX_AP = "_applied"
    SUFFIX_MAP = "_mapped"
    SUFFIX_BOUND = "_bound"
    DEFAULT = "default_value"

    # Setup: create Maybe instances for a value and for a function
    maybe_value = maybe_module.Maybe.just(ORIGINAL_STR)
    maybe_function = maybe_module.Maybe.just(lambda s: s + SUFFIX_AP)

    # Execution: perform a variety of operations
    # 1) Comparing a Maybe instance to a raw value (should be False)
    equality_with_raw = (maybe_value == ORIGINAL_STR)

    # 2) Apply the function inside maybe_function to maybe_value (ap semantics)
    ap_result = maybe_function.ap(maybe_value)

    # 3) get_or_else should return the contained value for non-empty Maybe
    got_or_else = maybe_value.get_or_else(DEFAULT)

    # 4) map the contained value to produce a new Maybe
    mapped_result = maybe_value.map(lambda s: s + SUFFIX_MAP)

    # 5) filter the Maybe with a predicate that keeps the value
    filtered_result = maybe_value.filter(lambda s: "p4x" in s)

    # 6) further map the mapped_result to ensure chaining works
    mapped_then_uppercased = mapped_result.map(lambda s: s.upper())

    # 7) perform the same ap again to produce a comparable result
    ap_result_again = maybe_function.ap(maybe_value)

    # 8) compare two ap results for equality
    ap_results_equal = (ap_result == ap_result_again)

    # 9) filter the ap_result using a predicate derived from got_or_else
    filtered_by_value = ap_result.filter(lambda v: v == (got_or_else + SUFFIX_AP))

    # 10) extract underlying value from the ap result with default fallback
    ap_value_or_default = ap_result.get_or_else(DEFAULT)

    # 11) create another Maybe and demonstrate bind and transformation to Either
    maybe_second = maybe_module.Maybe.just(ORIGINAL_STR)
    # to_validation should return a Validation representing success for non-empty Maybe
    validation_from_maybe = maybe_second.to_validation()
    # bind with a mapper that returns a new Maybe
    bound_result = maybe_second.bind(lambda s: maybe_module.Maybe.just(s + SUFFIX_BOUND))
    # convert the bound result to Either
    either_from_bound = bound_result.to_either()

    # Assertions: verify expected outcomes of the above operations
    assert equality_with_raw is False, "Maybe should not compare equal to a raw value"
    assert isinstance(ap_result, maybe_module.Maybe), "ap should return a Maybe"
    assert got_or_else == ORIGINAL_STR, "get_or_else should return the contained value for non-empty Maybe"
    assert mapped_result.get_or_else(DEFAULT) == ORIGINAL_STR + SUFFIX_MAP, "map should transform the contained value"
    assert isinstance(filtered_result, maybe_module.Maybe) and filtered_result.get_or_else(DEFAULT) == ORIGINAL_STR, "filter with a passing predicate should keep the value"
    assert mapped_then_uppercased.get_or_else(DEFAULT) == (ORIGINAL_STR + SUFFIX_MAP).upper(), "chained map should apply both transformations"
    assert ap_results_equal is True, "repeating the same ap should produce equal Maybe results"
    assert isinstance(filtered_by_value, maybe_module.Maybe), "filtering the ap result with a matching predicate should return a Maybe"
    assert ap_value_or_default == ORIGINAL_STR + SUFFIX_AP, "ap should have applied the function to the original value"
    assert bound_result.get_or_else(DEFAULT) == ORIGINAL_STR + SUFFIX_BOUND, "bind should apply mapper that returns a Maybe"
    assert either_from_bound is not None, "to_either should return an Either representation (non-None for non-empty Maybe)"
    # Also ensure that to_validation returned something (basic sanity check)
    assert validation_from_maybe is not None, "to_validation should produce a Validation for a non-empty Maybe"

def test_maybe_equality_returns_false_when_compared_with_non_maybe():
    # Purpose:
    #   Verify that Maybe.__eq__ returns False when the other object is not an instance of Maybe.
    # Setup:
    #   - Create a Maybe instance representing a "nothing" value.
    #   - Prepare a non-Maybe object (a set) to compare against.
    NOTHING = None
    non_maybe_object = {False}
    maybe_instance = maybe_module.Maybe(NOTHING, NOTHING)

    # Execution:
    #   Call __eq__ directly to exercise the isinstance(other, Maybe) check path.
    equality_result = maybe_instance.__eq__(non_maybe_object)

    # Assertion:
    #   The result must be False because the other object is not a Maybe instance.
    assert equality_result is False

def test_maybe_short_circuits_bind_and_map_and_converts_to_box_with_none():
    # Purpose:
    # - Verify that Maybe.bind and Maybe.map short-circuit when the Maybe instance is "nothing"
    #   (they should not attempt to call the provided mapper, even if it's not callable).
    # - Verify that Maybe.to_box() produces a Box containing None when the Maybe is "nothing".

    # Constants / Setup
    INITIAL_VALUE = True
    IS_NOTHING = True
    NON_CALLABLE_MAPPER = True  # Intentionally not a callable to ensure short-circuiting prevents a TypeError
    TEST_TUPLE = (INITIAL_VALUE, INITIAL_VALUE, INITIAL_VALUE, INITIAL_VALUE)

    # Create a Maybe instance that is "nothing" (second arg indicates is_nothing in this test setup)
    maybe_nothing = maybe_module.Maybe(INITIAL_VALUE, IS_NOTHING)

    # Execution
    # Because maybe_nothing.is_nothing is True, these operations should short-circuit and not attempt to call
    # NON_CALLABLE_MAPPER (which is not callable).
    result_after_bind = maybe_nothing.bind(NON_CALLABLE_MAPPER)
    result_after_map = result_after_bind.map(NON_CALLABLE_MAPPER)

    # Also create another Maybe (with a tuple value) that is marked as "nothing" and convert it to a Box
    maybe_tuple_nothing = maybe_module.Maybe(TEST_TUPLE, IS_NOTHING)
    box_from_nothing = maybe_tuple_nothing.to_box()

    # Assertions
    # bind and map should have returned Maybe instances that are still "nothing"
    assert getattr(result_after_bind, "is_nothing", False) is True
    assert getattr(result_after_map, "is_nothing", False) is True

    # to_box should return a Box object that wraps None when the Maybe was "nothing"
    # We check for a Box by name and that it exposes a 'value' attribute set to None.
    assert box_from_nothing is not None
    assert box_from_nothing.__class__.__name__ == "Box"
    assert hasattr(box_from_nothing, "value")
    assert box_from_nothing.value is None

def test_map_raises_type_error_when_mapper_is_not_callable_on_present_maybe():
    # Purpose:
    # Verify that Maybe.map raises a TypeError when given a non-callable mapper
    # and the Maybe instance represents a present value (is_nothing == False).
    # This ensures map only attempts to call the mapper for present values and
    # surfaces a clear error when the mapper is invalid.
    
    # Test data: a Maybe that is present but wraps a None value.
    value = None
    is_nothing = False
    invalid_mapper = False  # intentionally not callable to trigger TypeError

    # Setup
    maybe_instance = maybe_module.Maybe(value, is_nothing)
    # Sanity check: the instance should be present (not nothing)
    assert maybe_instance.is_nothing is False

    # Execution & Assertion: mapping with a non-callable should raise TypeError
    with pytest.raises(TypeError):
        maybe_instance.map(invalid_mapper)

def test_bind_raises_typeerror_with_non_callable_mapper_on_present_maybe():
    # Purpose:
    # Ensure Maybe.bind attempts to call the provided mapper when the Maybe is present,
    # and that passing a non-callable mapper raises a TypeError.
    value = 42
    is_nothing = False  # indicates this Maybe is present (bind should attempt to call the mapper)
    non_callable_mapper = {}  # dict is not callable and will cause a TypeError when invoked

    maybe_instance = maybe_module.Maybe(value, is_nothing)

    # bind should try to call non_callable_mapper(self.value) and therefore raise TypeError.
    with pytest.raises(TypeError):
        maybe_instance.bind(non_callable_mapper)

def test_maybe_to_box_lazy_filter_and_ap_interactions():
    # Purpose:
    # Verify interplay of Maybe's to_box, to_lazy, filter, ap and equality behavior
    # - to_box should wrap the inner value in a Box
    # - to_lazy should produce a callable Lazy that returns the inner value
    # - filter should keep the value when predicate is True and return Nothing otherwise
    # - ap should apply a Maybe-wrapped function to a Maybe-wrapped value
    # - equality comparisons between Maybe instances should behave as expected

    # --- Setup (constants and monads) ---
    SAMPLE_BYTES = b"\x9f\x02Gj\xbbw\xdb\x8b\xe7\xda"
    SAMPLE_INT = 0

    bytes_maybe = maybe_module.Maybe.just(SAMPLE_BYTES)
    int_maybe = maybe_module.Maybe.just(SAMPLE_INT)
    increment_maybe = maybe_module.Maybe.just(lambda x: x + 1)
    nothing_maybe = maybe_module.Maybe.nothing()

    # --- Execution (perform operations under test) ---
    # Convert a non-empty Maybe to a Box
    box_from_bytes = bytes_maybe.to_box()

    # Convert a non-empty Maybe to a Lazy and evaluate it
    lazy_from_int = int_maybe.to_lazy()

    # Filter the int Maybe with a predicate that should pass
    filtered_int = int_maybe.filter(lambda v: isinstance(v, int))

    # Apply a Maybe-wrapped function to a Maybe-wrapped value
    applied_result = increment_maybe.ap(int_maybe)

    # Filter the result of the application with a predicate that checks expected value
    filtered_applied = applied_result.filter(lambda v: v == SAMPLE_INT + 1)

    # Equality check between Maybe instances
    equality_check = filtered_int == maybe_module.Maybe.just(SAMPLE_INT)

    # --- Assertions (expected outcomes) ---
    # Box should contain the original bytes value
    assert hasattr(box_from_bytes, "value")
    assert box_from_bytes.value == SAMPLE_BYTES

    # Lazy should be callable and return the original integer when evaluated
    assert callable(lazy_from_int)
    assert lazy_from_int() == SAMPLE_INT

    # Filtered int should still be equal to the original Maybe.just(SAMPLE_INT)
    assert filtered_int == maybe_module.Maybe.just(SAMPLE_INT)
    assert equality_check is True

    # The application should produce Maybe.just(SAMPLE_INT + 1)
    assert applied_result == maybe_module.Maybe.just(SAMPLE_INT + 1)

    # Filtering the applied result with the matching predicate should keep the value
    assert filtered_applied == maybe_module.Maybe.just(SAMPLE_INT + 1)

    # Nothing remains Nothing under filter and ap where appropriate
    assert nothing_maybe.filter(lambda _: True) == maybe_module.Maybe.nothing()
    assert maybe_module.Maybe.nothing().ap(int_maybe) == maybe_module.Maybe.nothing()

def test_ap_raises_attribute_error_when_applicative_has_no_map():
    # Purpose:
    # Verify Maybe.ap attempts to call `map` on the provided applicative.
    # If the applicative does not provide a `map` method, an AttributeError should be raised.

    # Constants / setup
    NON_APPLICATIVE = 2862  # an int does not implement .map(...)
    MAYBE_VALUE = None
    MAYBE_IS_NOTHING = False  # create a non-empty Maybe that contains None as its value
    maybe_instance = maybe_module.Maybe(MAYBE_VALUE, MAYBE_IS_NOTHING)

    # Execution & assertion: calling ap with a non-applicative should raise AttributeError
    with pytest.raises(AttributeError):
        maybe_instance.ap(NON_APPLICATIVE)

def test_maybe_filter_map_and_conversions_with_callable_like_arguments():
    """
    Verify a sequence of operations on a Maybe instance:
    - filtering using objects that behave like callables,
    - converting Maybe to Lazy and Try,
    - mapping a Maybe using another Maybe-like callable.

    The test keeps the original inputs (value and flag) but organizes setup,
    execution and assertions with clear names and comments.
    """

    # Setup
    INITIAL_VALUE = 0
    INITIAL_FLAG = True
    maybe_original = maybe_module.Maybe(INITIAL_VALUE, INITIAL_FLAG)

    # Execution: perform chained operations similar to the original test.
    # Use the Maybe instance itself (and derived Maybe values) as the callable
    # arguments to filter/map to mirror the original test's intent.
    filtered_once = maybe_original.filter(maybe_original)
    lazy_from_original = maybe_original.to_lazy()
    lazy_from_filtered = filtered_once.to_lazy()
    filtered_twice = filtered_once.filter(lazy_from_filtered)
    try_from_filtered = filtered_twice.to_try()
    another_lazy_from_original = maybe_original.to_lazy()
    mapped_from_filtered = filtered_once.map(filtered_once)

    # Assertions: structural checks to ensure conversions/operations returned objects
    # of the expected shapes. Avoid depending on concrete Lazy/Try classes beyond
    # checking for commonly expected attributes so the test remains robust.
    assert isinstance(maybe_original, maybe_module.Maybe), "original should be a Maybe"
    assert isinstance(filtered_once, maybe_module.Maybe), "filter should return a Maybe"
    assert (
        hasattr(lazy_from_original, "__call__") or hasattr(lazy_from_original, "run")
    ), "to_lazy should return a lazy-like object (callable or have a run method)"
    assert (
        hasattr(lazy_from_filtered, "__call__") or hasattr(lazy_from_filtered, "run")
    ), "to_lazy on filtered value should return a lazy-like object"
    assert (
        hasattr(try_from_filtered, "is_success") or hasattr(try_from_filtered, "value")
    ), "to_try should return a Try-like object with is_success or value attribute"
    assert isinstance(mapped_from_filtered, maybe_module.Maybe), "map should return a Maybe"

    # Sanity: repeated conversions should produce objects
    assert another_lazy_from_original is not None

def test_maybe_filter_and_to_lazy_behavior_with_nothing_and_lazy():
    # Purpose:
    # - Verify that calling filter on a Maybe that is Nothing short-circuits (does not attempt to call the provided filterer)
    #   and returns a Nothing Maybe.
    # - Convert that Nothing Maybe to a Lazy and then pass that Lazy into another Maybe.filter call to ensure the call
    #   completes and returns a Maybe instance (no exceptions).
    #
    # This test separates setup, execution and assertions and uses descriptive names for clarity.

    # --- Constants / test data ---
    SAMPLE_INT = -283
    NON_CALLABLE_FILTER = (SAMPLE_INT, SAMPLE_INT, SAMPLE_INT)  # intentionally non-callable
    NONE_VALUE = None
    IS_NOTHING_TRUE = True
    IS_NOTHING_NONE = None  # ambiguous/falsey is_nothing value for the second Maybe

    # --- Setup: create a Maybe that represents Nothing ---
    maybe_nothing = maybe_module.Maybe(NONE_VALUE, IS_NOTHING_TRUE)

    # --- Execution: filter the Nothing Maybe with a non-callable filterer
    # Because maybe_nothing.is_nothing is True, filter should short-circuit and return a Nothing Maybe
    filtered_maybe = maybe_nothing.filter(NON_CALLABLE_FILTER)

    # --- Execution: convert the resulting Maybe to a Lazy monad ---
    lazy_from_filtered = filtered_maybe.to_lazy()

    # --- Setup: create another Maybe with an ambiguous is_nothing value ---
    maybe_ambiguous = maybe_module.Maybe(NONE_VALUE, IS_NOTHING_NONE)

    # --- Execution: pass the Lazy into filter of the second Maybe ---
    # This exercises the case where the filterer is a Lazy object returned by to_lazy()
    result_maybe = maybe_ambiguous.filter(lazy_from_filtered)

    # --- Assertions ---
    # filtered_maybe should be a Nothing Maybe (short-circuited by the original Nothing)
    assert getattr(filtered_maybe, "is_nothing", False) is True

    # The final call should return a Maybe instance (no exception raised during filter)
    assert isinstance(result_maybe, maybe_module.Maybe)

def test_maybe_get_or_else_to_box_and_filter_with_non_callable_raises_type_error():
    # Constants for clarity
    DEFAULT_INT = 2281
    SAMPLE_STRING = "gZ(\\mOcN"
    SAMPLE_DICT = {SAMPLE_STRING: SAMPLE_STRING}
    SAMPLE_TUPLE = (SAMPLE_STRING, SAMPLE_STRING, SAMPLE_DICT, SAMPLE_DICT)

    # Setup: create a Maybe that is "nothing" (so get_or_else should return the default)
    MAYBE_IS_NOTHING = True
    maybe_nothing = maybe_module.Maybe(SAMPLE_TUPLE, MAYBE_IS_NOTHING)

    # Execution: get_or_else should return the provided default when Maybe is nothing
    result_from_get_or_else = maybe_nothing.get_or_else(DEFAULT_INT)

    # Sanity assertion for get_or_else behavior
    assert result_from_get_or_else == DEFAULT_INT

    # Transform the maybe to a Box (should produce a Box containing None for a "nothing" Maybe)
    box_from_maybe = maybe_nothing.to_box()

    # Setup: create another Maybe that is not nothing, holding some generic object
    # Use a tiny Generic subclass to mirror the original intent of a "generic" payload
    class GenericStub(typing_module.Generic):
        pass

    generic_instance = GenericStub()
    MAYBE_IS_NOTHING_FALSE = False
    maybe_with_generic = maybe_module.Maybe(generic_instance, MAYBE_IS_NOTHING_FALSE)

    # Assertion: calling filter with a non-callable (the integer returned earlier) should raise TypeError
    # This mirrors the original test's use of a non-callable filterer argument.
    with pytest.raises(TypeError):
        maybe_with_generic.filter(result_from_get_or_else)

def test_maybe_transformations_and_bind_behavior():
    # Purpose:
    # Verify core Maybe transformations (to_validation, to_try), get_or_else behavior,
    # and that bind applies a mapper to a non-empty Maybe producing a new Maybe.

    # Constants / test data
    BOOL_VALUE = True
    NONE_FLAG = None
    INT_VALUE = -1784
    EMPTY_TUPLE = ()
    FLOAT_VALUE = -286.64

    # Setup: create a few Maybe instances representing different states
    maybe_bool = maybe_module.Maybe(BOOL_VALUE, NONE_FLAG)        # non-empty Maybe holding a bool
    maybe_int = maybe_module.Maybe(INT_VALUE, EMPTY_TUPLE)        # non-empty Maybe holding an int
    maybe_empty_float = maybe_module.Maybe(FLOAT_VALUE, FLOAT_VALUE)  # empty Maybe (truthy second arg)

    # Execution: call transformations and accessors
    validation_from_bool = maybe_bool.to_validation()
    validation_from_int = maybe_int.to_validation()
    got_or_else = maybe_int.get_or_else(INT_VALUE)
    try_from_int = maybe_int.to_try()

    # Prepare a simple mapper for bind and apply it to maybe_int
    double_mapper = lambda x: maybe_module.Maybe(x * 2, False)
    bind_result = maybe_int.bind(double_mapper)

    # Assertions:
    # to_validation should return some Validation object (at minimum not None).
    assert validation_from_bool is not None, "to_validation should return a Validation object for non-empty Maybe"
    # If Validation exposes a 'value' attribute assert it contains the original value.
    if hasattr(validation_from_bool, "value"):
        assert getattr(validation_from_bool, "value") == BOOL_VALUE

    if hasattr(validation_from_int, "value"):
        assert getattr(validation_from_int, "value") == INT_VALUE

    # get_or_else on a non-empty Maybe returns the contained value (not the default)
    assert got_or_else == INT_VALUE

    # to_try for a non-empty Maybe should produce a successful Try (is_success True) with the same value
    assert getattr(try_from_int, "is_success", True) is True
    if hasattr(try_from_int, "value"):
        assert getattr(try_from_int, "value") == INT_VALUE

    # bind should return a Maybe instance wrapping the mapped value
    assert isinstance(bind_result, maybe_module.Maybe)
    assert getattr(bind_result, "is_nothing", False) is False
    assert getattr(bind_result, "value", None) == INT_VALUE * 2

def test_map_on_nothing_returns_nothing_and_to_either_on_nothing_returns_left_with_none():
    # Purpose:
    # Verify that calling map on a Maybe that represents "nothing" returns another "nothing" Maybe,
    # and calling to_either on a Maybe marked as "nothing" returns a Left containing None.

    # Constants / setup
    VALUE_NONE = None
    IS_NOTHING_FLAG = True
    # Use a non-callable mapper (a set instance). This is safe because map should not call the mapper
    # when the Maybe is "nothing".
    NON_CALLABLE_MAPPER = {IS_NOTHING_FLAG}

    VALUE_INT = -1095

    # Create Maybe instances: both are marked as "nothing" via the flag.
    maybe_nothing = maybe_module.Maybe(VALUE_NONE, IS_NOTHING_FLAG)
    maybe_with_value_but_marked_nothing = maybe_module.Maybe(VALUE_INT, IS_NOTHING_FLAG)

    # Execution
    mapped_result = maybe_nothing.map(NON_CALLABLE_MAPPER)
    either_result = maybe_with_value_but_marked_nothing.to_either()

    # Assertions
    # Mapped result should still be a Maybe and represent "nothing".
    assert isinstance(mapped_result, maybe_module.Maybe)
    assert mapped_result.is_nothing is True

    # Converting a "nothing" Maybe to Either should produce a Left holding None.
    # We check the returned object's class name and that its contained value is None.
    assert type(either_result).__name__ == "Left"
    assert getattr(either_result, "value", None) is None

def test_maybe_conversion_chain_no_errors():
    """
    Purpose:
    - Verify that converting Maybe instances through various monad adapters
      (to_lazy, to_either, to_try) executes without raising and returns non-None objects.
    - This is a smoke test to ensure the conversion methods are callable and produce outputs.

    Structure:
    - Constants: values and flags used to build Maybe instances.
    - Setup: create an "empty-like" Maybe and a "container" Maybe that contains the first Maybe.
    - Execution: call the conversion methods in a small chain (to_lazy, to_either, to_try, to_lazy).
    - Assertions: ensure each conversion returned a non-None result (no exceptions and produced an object).
    """

    # Constants used for constructing Maybe instances
    EMPTY_VALUE = None
    EMPTY_FLAG = None        # keep same as original (could represent falsy is_nothing)
    NON_EMPTY_FLAG = False   # explicitly mark as not-nothing for the container maybe

    # Setup
    # Create a Maybe that is constructed with None (mirrors original test's usage)
    maybe_empty = maybe_module.Maybe(EMPTY_VALUE, EMPTY_FLAG)

    # Create a container Maybe that holds a tuple containing the previous Maybe
    maybe_container = maybe_module.Maybe((maybe_empty,), NON_EMPTY_FLAG)

    # Execution: perform conversions; original test called these methods to ensure they run
    lazy_from_empty = maybe_empty.to_lazy()
    either_from_empty_first = maybe_empty.to_either()
    try_from_container = maybe_container.to_try()
    either_from_empty_second = maybe_empty.to_either()
    either_from_container = maybe_container.to_either()
    # Also convert the Try result to a Lazy as in the original flow
    lazy_from_try = try_from_container.to_lazy()

    # Assertions: ensure conversion methods returned objects (smoke-check for successful conversions)
    assert lazy_from_empty is not None
    assert either_from_empty_first is not None
    assert try_from_container is not None
    assert either_from_empty_second is not None
    assert either_from_container is not None
    assert lazy_from_try is not None

def test_maybe_to_try_and_box_preserves_value_for_present_maybe():
    """
    Verify that a non-empty Maybe is transformed into a successful Try containing the same
    value, and into a Box containing the same value.
    """

    # Setup
    VALUE = True
    IS_NOTHING = False
    maybe_instance = maybe_module.Maybe(VALUE, IS_NOTHING)

    # Execution
    converted_try = maybe_instance.to_try()
    converted_box = maybe_instance.to_box()

    # Assertions for Try
    assert hasattr(converted_try, "value"), "Expected Try to expose a 'value' attribute"
    assert hasattr(converted_try, "is_success"), "Expected Try to expose an 'is_success' attribute"
    assert converted_try.value is VALUE
    assert converted_try.is_success is True

    # Assertions for Box
    assert hasattr(converted_box, "value"), "Expected Box to expose a 'value' attribute"
    assert converted_box.value is VALUE

def test_maybe_empty_transforms_and_applications():
    # Purpose:
    # Verify behavior when a Maybe is constructed as empty (is_nothing=True):
    # - transformations to other monads (Lazy, Validation, Try, Either, Box)
    # - filter on an empty Maybe returns an empty Maybe
    # - get_or_else returns the provided default when Maybe is empty
    # - equality between two empty Maybes
    # - applying an applicative to resulting Try does not raise

    # Constants / test data
    SAMPLE_BYTES = b"C\xcf\xe7/"
    EMPTY_VALUE = None
    IS_EMPTY = True

    # Setup: create an empty Maybe
    maybe_empty = maybe_module.Maybe(EMPTY_VALUE, IS_EMPTY)

    # Execution: perform a series of transformations and operations
    # ap on an empty Maybe should short-circuit to an empty Maybe
    applied_result = maybe_empty.ap(EMPTY_VALUE)

    # Convert the resulting Maybe to Lazy, then to Validation
    lazy_result = applied_result.to_lazy()
    validation_result = lazy_result.to_validation()

    # Filtering the original empty Maybe with the validation result (used as filterer)
    # should yield an empty Maybe (filter short-circuits on empty)
    filtered_result = maybe_empty.filter(validation_result)

    # get_or_else on an empty Maybe should return the provided default (here we pass the same object)
    get_or_else_result = filtered_result.get_or_else(filtered_result)

    # Convert to other monads for coverage
    either_result = filtered_result.to_either()
    try_result = validation_result.to_try()

    # Equality check between two empty Maybes
    equality_check = filtered_result.__eq__(applied_result)

    # Convert the get_or_else result (which should be an empty Maybe) to a Box
    box_result = get_or_else_result.to_box()

    # Attempt to apply something to the Try result to ensure it accepts applciative calls without raising
    try:
        try_result.ap(SAMPLE_BYTES)
    except Exception as exc:
        pytest.fail(f"Try.ap raised an unexpected exception: {exc}")

    # Assertions: verify expected properties of the intermediate results
    assert getattr(maybe_empty, "is_nothing", False) is True, "Initial Maybe should be empty"
    assert getattr(applied_result, "is_nothing", False) is True, "ap on empty Maybe should produce empty Maybe"
    assert getattr(filtered_result, "is_nothing", False) is True, "Filtering an empty Maybe should remain empty"
    # get_or_else should return the provided default when Maybe is empty
    assert get_or_else_result is filtered_result, "get_or_else should return the provided default for empty Maybe"
    # empty Maybes produced by operations should compare equal
    assert equality_check is True, "Two empty Maybe instances should be equal"
    # to_try on a validation coming from an empty Maybe should yield a Try marked as not successful (if attribute exists)
    if hasattr(try_result, "is_success"):
        assert try_result.is_success is False, "Try produced from empty value should be not successful"
    # Box produced from an empty Maybe should contain None (if Box exposes .value)
    if hasattr(box_result, "value"):
        assert box_result.value is None, "Box produced from empty Maybe should contain None"

def test_maybe_nothing_behaviour_and_conversions():
    """
    Purpose:
    - Verify behaviour of Maybe when constructed as "nothing" (is_nothing == True).
    - Ensure applicative (ap), bind and get_or_else behave as identity/no-op for nothing.
    - Ensure conversions to Try / Validation produce the expected "empty" semantics
      (Try should be unsuccessful for nothing).
    """

    # Constants / test fixtures
    SAMPLE_BYTES = b"\xdbC\xcf\xe7/"
    SAMPLE_INT = -3289
    NONE_VALUE = None

    # Setup: create two Maybe instances that represent "nothing"
    # The Maybe constructor used in this suite accepts (value, is_nothing_flag).
    maybe_nothing_by_trueflag = maybe_module.Maybe(NONE_VALUE, True)
    # Using a truthy bytes value as the second parameter should also mark as "nothing"
    maybe_nothing_by_bytesflag = maybe_module.Maybe(NONE_VALUE, SAMPLE_BYTES)

    # Sanity checks on setup (both should be Nothing)
    assert getattr(maybe_nothing_by_trueflag, "is_nothing") is True
    assert getattr(maybe_nothing_by_bytesflag, "is_nothing") is True
    # The two "nothing" instances should be equal according to Maybe.__eq__
    assert maybe_nothing_by_trueflag == maybe_nothing_by_bytesflag

    # Execution: apply/applicative operations on Nothing should remain Nothing
    after_ap_with_none = maybe_nothing_by_trueflag.ap(NONE_VALUE)
    after_second_ap_with_bytes = after_ap_with_none.ap(SAMPLE_BYTES)

    # Convert resulting Maybe (still Nothing) to Validation
    validation_from_ap_result = after_second_ap_with_bytes.to_validation()

    # get_or_else should return the provided default (in this case the same maybe_nothing_by_bytesflag object)
    default_returned = maybe_nothing_by_bytesflag.get_or_else(maybe_nothing_by_bytesflag)

    # Conversions of the second maybe to other monads
    validation_from_maybe = maybe_nothing_by_bytesflag.to_validation()
    bind_result_on_nothing = maybe_nothing_by_bytesflag.bind(validation_from_maybe)  # bind on Nothing -> Nothing
    either_from_nothing = maybe_nothing_by_bytesflag.to_either()
    ap_with_same_nothing = maybe_nothing_by_bytesflag.ap(maybe_nothing_by_bytesflag)

    # Convert Nothing to Try: per implementation this should produce an unsuccessful Try
    try_from_nothing = maybe_nothing_by_bytesflag.to_try()

    # Additional operations (kept from original flow)
    validation_from_bind_result = bind_result_on_nothing.to_validation()
    # attempt to call ap on the Try instance (should be callable in API; behaviour not asserted beyond not raising)
    try_from_nothing.ap(SAMPLE_INT)

    # Assertions: verify Maybe-level invariants and conversions
    assert getattr(after_ap_with_none, "is_nothing") is True
    assert getattr(after_second_ap_with_bytes, "is_nothing") is True
    assert getattr(bind_result_on_nothing, "is_nothing") is True
    assert getattr(ap_with_same_nothing, "is_nothing") is True

    # get_or_else returned the exact default object we passed in
    assert default_returned is maybe_nothing_by_bytesflag

    # binding a Nothing yields a Nothing equal to the original nothing
    assert maybe_nothing_by_bytesflag == bind_result_on_nothing

    # Converting Nothing to Try should produce an unsuccessful Try (per to_try implementation)
    # Use getattr to avoid relying on a specific Try class import here.
    assert getattr(try_from_nothing, "is_success") is False

    # Conversions to Validation should produce some Validation object — ensure calls do not return None
    assert validation_from_ap_result is not None
    assert validation_from_maybe is not None
    assert validation_from_bind_result is not None

def test_maybe_transform_and_map_flow():
    """
    Verify a Maybe instance can be compared to a non-Maybe value, transformed into other monads
    (Either, Lazy, Validation) and then used as an argument to Maybe.map without raising.
    The test asserts structural expectations (presence of results and types) rather than
    internal implementation details.
    """

    # Constants to make intent explicit
    SAMPLE_VALUE = False
    SAMPLE_IS_NOTHING = False

    # Setup: create separate Maybe instances for each part of the scenario
    maybe_for_equality = maybe_module.Maybe(SAMPLE_VALUE, SAMPLE_IS_NOTHING)
    maybe_for_transforms = maybe_module.Maybe(SAMPLE_VALUE, SAMPLE_IS_NOTHING)
    maybe_for_map = maybe_module.Maybe(SAMPLE_VALUE, SAMPLE_IS_NOTHING)

    # 1) Compare the Maybe instance to a non-Maybe value. Expect False because types differ.
    equality_result = (maybe_for_equality == SAMPLE_VALUE)

    # 2) Transform the Maybe into other monads.
    either_result = maybe_for_transforms.to_either()
    lazy_result = maybe_for_transforms.to_lazy()
    # Convert the Lazy result into a Validation (preserves the contained value or None)
    validation_result = lazy_result.to_validation()

    # 3) Call map on a Maybe using the validation result as the "mapper" argument.
    # The operation should complete and return a Maybe instance even if the mapper isn't callable.
    mapped_result = maybe_for_map.map(validation_result)

    # Assertions: structural checks to ensure operations produced expected shapes.

    # Source objects are Maybe instances and reported nothing-status should match the constant.
    assert isinstance(maybe_for_equality, maybe_module.Maybe)
    assert maybe_for_equality.is_nothing == SAMPLE_IS_NOTHING

    # Equality against a non-Maybe should be False.
    assert equality_result is False

    # Transformations should produce non-None monad-like results.
    assert either_result is not None
    assert lazy_result is not None
    assert validation_result is not None

    # The result of map should be a Maybe instance (map returns a Maybe regardless of mapper behavior).
    assert isinstance(mapped_result, maybe_module.Maybe)

def test_maybe_converts_non_empty_to_try_and_validation_and_is_reflexively_equal():
    # Purpose:
    # - A present Maybe should be equal to itself.
    # - to_try() should produce a successful Try carrying the Maybe's value.
    # - to_validation() should produce a Validation carrying the Maybe's value.

    # Setup
    VALUE_FALSE = False
    IS_NOTHING = False  # indicates this Maybe is present (not empty)
    maybe_instance = maybe_module.Maybe(VALUE_FALSE, IS_NOTHING)

    # Execution
    equality_result = (maybe_instance == maybe_instance)
    try_result = maybe_instance.to_try()
    validation_result = maybe_instance.to_validation()

    # Assertions
    assert equality_result is True, "Maybe should be equal to itself"

    # Try should be successful and preserve the Maybe's value
    assert hasattr(try_result, "is_success"), "to_try() should return a Try with 'is_success' attribute"
    assert try_result.is_success is True
    assert getattr(try_result, "value") == VALUE_FALSE

    # Validation should preserve the Maybe's value
    assert validation_result is not None
    assert hasattr(validation_result, "value"), "to_validation() should return a Validation with a 'value' attribute"
    assert getattr(validation_result, "value") == VALUE_FALSE

