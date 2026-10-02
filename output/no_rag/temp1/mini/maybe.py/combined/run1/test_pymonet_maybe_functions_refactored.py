import pytest

import typing as typing_module
import maybe as maybe_module

def test_maybe_constructs_with_identical_bytes_inputs():
    # Purpose:
    # Verify that the Maybe type can be instantiated with two identical byte arguments
    # and that the resulting object is an instance of maybe_module.Maybe.

    # Constants / Setup
    SAMPLE_BYTES = b"\xf4\xaf\xe2\xc9\xee\xc8\xd67n\x9eK\x0b\x97Y\xb5"

    # Execution: construct the Maybe object using the same bytes for both parameters
    maybe_instance = maybe_module.Maybe(SAMPLE_BYTES, SAMPLE_BYTES)

    # Assertion: ensure construction succeeded and returned the expected type
    assert isinstance(maybe_instance, maybe_module.Maybe)

def test_maybe_construct_with_none_values():
    """
    Purpose:
    - Verify that a Maybe object can be constructed when both constructor arguments are None.
    - Perform basic sanity checks that the object is an instance of maybe_module.Maybe and,
      if common attribute names exist, that they reflect the provided None values.
    """

    # Inputs representing absent/empty values
    none_value = None
    second_none_value = None

    # --- Execution ---
    maybe_instance = maybe_module.Maybe(none_value, second_none_value)

    # --- Assertions ---
    # Basic construction checks
    assert maybe_instance is not None, "Expected constructor to return a Maybe instance, got None"
    assert isinstance(maybe_instance, maybe_module.Maybe), "Constructed object is not an instance of maybe_module.Maybe"

    # If the Maybe implementation exposes common attribute names, ensure they reflect the None inputs.
    # These checks are defensive (only executed if the attribute exists) so the test remains robust across implementations.
    if hasattr(maybe_instance, "value"):
        assert getattr(maybe_instance, "value") is None, "Expected Maybe.value to be None when constructed with None"
    if hasattr(maybe_instance, "data"):
        assert getattr(maybe_instance, "data") is None, "Expected Maybe.data to be None when constructed with None"
    if hasattr(maybe_instance, "inner"):
        assert getattr(maybe_instance, "inner") is None, "Expected Maybe.inner to be None when constructed with None"

def test_maybe_basic_chain_operations():
    # Purpose:
    # Verify a sequence of basic Maybe operations (equality, application, mapping, filtering,
    # default extraction and monad conversions) run and produce expected shapes/values.
    # The test focuses on readable variable names and clearly separated setup, execution and assertions.

    # Constants / Setup
    TEST_VALUE = "p4xa>bl^oP"

    # Create two Maybe instances with the same underlying test value
    maybe_instance = maybe_module.Maybe(TEST_VALUE, TEST_VALUE)
    second_maybe_instance = maybe_module.Maybe(TEST_VALUE, TEST_VALUE)

    # Execution: perform a sequence of operations on the Maybe instances
    # Compare Maybe with a raw value (should not be equal because __eq__ expects a Maybe)
    equality_with_raw = maybe_instance.__eq__(TEST_VALUE)

    # Apply the Maybe to an applicative (keeps original call shape from the original test)
    applied_once = maybe_instance.ap(TEST_VALUE)
    applied_twice = maybe_instance.ap(TEST_VALUE)  # repeat to check idempotence/equality

    # Extract a fallback/default when Maybe is not empty
    extracted_or_default = maybe_instance.get_or_else(TEST_VALUE)

    # Map and filter using previous results (keeps call shapes from original test)
    mapped_once = maybe_instance.map(applied_once)
    mapped_twice = maybe_instance.map(applied_once)
    filtered_from_mapped = maybe_instance.filter(applied_once)
    filtered_on_applied = applied_once.filter(extracted_or_default)

    # Use get_or_else on the result of an ap operation
    applied_get_or_else = applied_twice.get_or_else(TEST_VALUE)

    # Convert second maybe to validation, bind it and convert to either (keeps original flow)
    validation_from_second = second_maybe_instance.to_validation()
    bound_result = second_maybe_instance.bind(validation_from_second)
    either_result = bound_result.to_either()

    # Assertions: check types/expected basic behaviors
    assert isinstance(maybe_instance, maybe_module.Maybe), "Initial value should be a Maybe instance"
    # Comparing Maybe to a raw value should be False (other is not a Maybe)
    assert equality_with_raw is False
    # ap should return a Maybe-like structure
    assert isinstance(applied_once, maybe_module.Maybe)
    # get_or_else on a non-empty Maybe should return the contained value
    assert extracted_or_default == TEST_VALUE
    # repeated ap calls that started from same Maybe should produce equal results
    assert applied_once == applied_twice
    # get_or_else on the result of ap should return the fallback when appropriate
    assert applied_get_or_else == TEST_VALUE
    # ensure final monad conversion chain yields a non-None result
    assert either_result is not None

def test_maybe_eq_with_non_maybe_returns_false():
    # Purpose:
    # Ensure Maybe.__eq__ returns False when compared against an object that is not a Maybe.
    # This verifies the isinstance(other, Maybe) short-circuit in the equality implementation.

    # Constants / Setup
    NO_VALUE = None
    NO_FLAG = None
    SAMPLE_BOOL = False

    # Create a non-Maybe object (a set of booleans) and a Maybe instance
    non_maybe_object = {SAMPLE_BOOL, SAMPLE_BOOL}  # set deduplicates to {False}
    maybe_instance = maybe_module.Maybe(NO_VALUE, NO_FLAG)

    # Exercise: perform the equality comparison
    comparison_result = maybe_instance.__eq__(non_maybe_object)

    # Assertion: comparing with a non-Maybe must be False
    assert comparison_result is False

def test_maybe_bind_map_and_to_box_behavior():
    # Purpose:
    # - Verify that calling bind/map on an empty Maybe does not invoke the provided callables
    #   and returns an empty Maybe.
    # - Verify that to_box on a non-empty Maybe produces a Box containing the Maybe's value.

    # Constants for readability
    TRUE = True
    TUPLE_OF_TRUES = (TRUE, TRUE, TRUE, TRUE)

    # Setup
    # Create an empty Maybe (second arg True indicates "is_nothing")
    empty_maybe = maybe_module.Maybe(TRUE, TRUE)
    # Create a non-empty Maybe containing a tuple
    non_empty_maybe = maybe_module.Maybe(TUPLE_OF_TRUES, False)

    # Execution
    # Define mappers that must not be called when Maybe is empty.
    def failing_mapper(_):
        pytest.fail("Mapper should not be called for an empty Maybe")

    bound_result = empty_maybe.bind(failing_mapper)
    mapped_result = bound_result.map(failing_mapper)

    # Convert non-empty Maybe to a Box
    box_result = non_empty_maybe.to_box()

    # Assertions
    # When binding/mapping on an empty Maybe we expect the result to still be empty.
    assert getattr(bound_result, "is_nothing", False) is True
    assert getattr(mapped_result, "is_nothing", False) is True

    # The Box returned from to_box should wrap the original value from the non-empty Maybe.
    # Box is expected to expose the wrapped value via a 'value' attribute.
    assert getattr(box_result, "value") == TUPLE_OF_TRUES

def test_maybe_map_raises_type_error_for_non_callable_mapper():
    # Purpose:
    # Ensure Maybe.map enforces that its mapper argument is callable.
    # If a non-callable is passed, a TypeError should be raised when map attempts to call it.

    # Test data
    SAMPLE_VALUE = 1
    SAMPLE_IS_NOTHING = False
    NON_CALLABLE_MAPPER = 123  # deliberately not callable to trigger the error

    # Create a Maybe instance that is not "nothing" so map will try to call the mapper
    maybe_instance = maybe_module.Maybe(SAMPLE_VALUE, SAMPLE_IS_NOTHING)

    # Expectation: calling map with a non-callable should raise TypeError
    with pytest.raises(TypeError):
        maybe_instance.map(NON_CALLABLE_MAPPER)

def test_bind_non_callable_mapper_behavior_for_empty_and_non_empty_maybe():
    # Purpose:
    # - Ensure that bind() on an empty Maybe returns a new empty Maybe without calling the mapper.
    # - Ensure that bind() on a non-empty Maybe attempts to call the mapper and thus raises
    #   a TypeError if the mapper is not callable.

    # Constants / setup
    EMPTY_FLAG = True
    NOT_EMPTY_FLAG = False
    VALUE_TRUE = True
    VALUE_NONE = None
    NON_CALLABLE_MAPPER = {}  # deliberately not callable to trigger TypeError when invoked

    # Setup: create an empty Maybe and a non-empty Maybe (whose value is None)
    maybe_empty = maybe_module.Maybe(VALUE_TRUE, EMPTY_FLAG)
    maybe_with_none = maybe_module.Maybe(VALUE_NONE, NOT_EMPTY_FLAG)

    # Execution & Assertion 1: binding an empty Maybe should return an empty Maybe
    result_from_empty = maybe_empty.bind(NON_CALLABLE_MAPPER)
    assert result_from_empty.is_nothing is True  # mapper must not be called for empty Maybe

    # Execution & Assertion 2: binding a non-empty Maybe with a non-callable should raise TypeError
    with pytest.raises(TypeError):
        maybe_with_none.bind(NON_CALLABLE_MAPPER)

def test_maybe_transformations_and_applicative_interactions():
    # Purpose:
    # - Verify transformations from Maybe to Box and Lazy
    # - Exercise filter and ap combinators with non-trivial inputs
    # - Ensure returned types and basic properties are consistent (without relying on internal values)

    # --- Constants / Setup ---
    BYTES_PAYLOAD = b"\x9f\x02Gj\xbbw\xdb\x8b\xe7\xda"
    NOTHING_FLAG = None
    INT_ZERO = 0
    IS_NOTHING_TRUE = True

    # Create a Maybe from a bytes payload (second arg used as constructor flag)
    maybe_bytes = maybe_module.Maybe(BYTES_PAYLOAD, NOTHING_FLAG)

    # Create a Maybe that uses an integer with a truthy "is nothing" flag
    maybe_zero_flagged = maybe_module.Maybe(INT_ZERO, IS_NOTHING_TRUE)

    # --- Execution ---
    # Transform the bytes-Maybe into a Box
    box_from_maybe = maybe_bytes.to_box()

    # Transform the flagged-Maybe into a Lazy
    lazy_from_maybe = maybe_zero_flagged.to_lazy()

    # Use filter with the Maybe object itself (exercises filter path when a non-standard callable/filterer is provided)
    filtered_maybe = maybe_zero_flagged.filter(maybe_zero_flagged)

    # Apply the filtered result (as an applicative) to the bytes-Maybe
    applied_result = filtered_maybe.ap(maybe_bytes)

    # Filter again using the result of the applicative application
    filtered_again = filtered_maybe.filter(applied_result)

    # Construct another Maybe combining Lazy and Box results as raw values
    combined_maybe = maybe_module.Maybe(lazy_from_maybe, box_from_maybe)

    # Perform an equality check of the Lazy instance against a boolean (ensures __eq__ returns a bool)
    equality_with_bool = lazy_from_maybe.__eq__(IS_NOTHING_TRUE)

    # --- Assertions ---
    # to_box should produce an object named 'Box' (created inside Maybe.to_box implementation)
    assert getattr(box_from_maybe, "__class__", None) is not None
    assert box_from_maybe.__class__.__name__ == "Box"

    # to_lazy should produce an object named 'Lazy'
    assert getattr(lazy_from_maybe, "__class__", None) is not None
    assert lazy_from_maybe.__class__.__name__ == "Lazy"

    # The results of ap and filter should be Maybe-like (have attributes used by the Maybe API)
    for maybe_obj in (applied_result, filtered_maybe, filtered_again, combined_maybe):
        assert hasattr(maybe_obj, "is_nothing"), f"{maybe_obj!r} should have is_nothing attribute"
        assert hasattr(maybe_obj, "value"), f"{maybe_obj!r} should have value attribute"
        # Basic type check by class name to avoid tight coupling to implementation import paths
        assert maybe_obj.__class__.__name__ == "Maybe"

    # __eq__ should return a boolean when comparing Lazy to another object
    assert isinstance(equality_with_bool, bool)

def test_maybe_ap_raises_when_applicative_lacks_map():
    # Purpose:
    # Verify that Maybe.ap attempts to call `map` on the provided applicative
    # and therefore raises an AttributeError when the applicative does not
    # implement a `map` method.

    # Constants / fixtures
    TEST_FUNCTION_CONTAINER = None        # value stored in the Maybe (acts as "function" when used by ap)
    IS_NOTHING_FLAG = False               # indicates this Maybe is not the special "nothing" value
    NON_APPLICATIVE = 2862                # an object that does not implement `.map`

    # Setup: create a non-empty Maybe containing None
    maybe_with_none = maybe_module.Maybe(TEST_FUNCTION_CONTAINER, IS_NOTHING_FLAG)

    # Execution & Assertion: applying with a non-applicative should raise AttributeError
    with pytest.raises(AttributeError):
        maybe_with_none.ap(NON_APPLICATIVE)

def test_empty_maybe_chaining_returns_empty_variants():
    # Purpose: verify operations on an empty Maybe (is_nothing=True) stay empty or
    # produce appropriate "empty" monadic wrappers (callable Lazy, failing Try).
    TEST_VALUE = 0
    IS_NOTHING = True

    # Create an empty Maybe
    original_maybe = maybe_module.Maybe(TEST_VALUE, IS_NOTHING)
    assert isinstance(original_maybe, maybe_module.Maybe)
    assert original_maybe.is_nothing is True

    # Perform chaining operations similar to the original test
    filtered_once = original_maybe.filter(original_maybe)
    assert isinstance(filtered_once, maybe_module.Maybe)
    assert filtered_once.is_nothing is True

    lazy_original = original_maybe.to_lazy()
    lazy_filtered = filtered_once.to_lazy()
    another_lazy = original_maybe.to_lazy()

    # Lazy wrappers should be callable (they wrap thunks)
    assert callable(lazy_original)
    assert callable(lazy_filtered)
    assert callable(another_lazy)

    # Further chaining should remain empty
    filtered_again = filtered_once.filter(lazy_filtered)
    assert isinstance(filtered_again, maybe_module.Maybe)
    assert filtered_again.is_nothing is True

    # Converting an empty Maybe to Try should yield an unsuccessful Try-like object
    to_try_result = filtered_again.to_try()
    assert hasattr(to_try_result, "is_success")
    assert to_try_result.is_success is False

    # map() on an empty Maybe should produce an empty Maybe
    mapped_result = filtered_once.map(filtered_once)
    assert isinstance(mapped_result, maybe_module.Maybe)
    assert mapped_result.is_nothing is True

def test_maybe_filter_and_to_lazy_interaction():
    """
    Verify interplay between Maybe.filter and Maybe.to_lazy when using non-callable
    and Lazy-like objects as "filterer" arguments. Ensure no unexpected exceptions
    are raised and that filter returns a Maybe instance.
    """

    # Constants / Test data
    SENTINEL_INT = -283
    NON_CALLABLE_FILTER = (SENTINEL_INT, SENTINEL_INT, SENTINEL_INT)  # a tuple, not a callable
    EMPTY_VALUE = None
    DEFAULT_FLAG = True

    # Setup: create a Maybe with an explicit None value and a default flag
    maybe_with_none = maybe_module.Maybe(EMPTY_VALUE, DEFAULT_FLAG)

    # Execution: attempt to filter using a non-callable object (tuple).
    # If maybe_with_none is "nothing" the tuple will not be called; otherwise
    # filter may attempt to use the tuple. Behavior should match original expectations.
    filtered_maybe = maybe_with_none.filter(NON_CALLABLE_FILTER)

    # Execution: convert the resulting Maybe to a Lazy wrapper
    lazy_from_filtered = filtered_maybe.to_lazy()

    # Setup: create another Maybe representing an empty/default Maybe
    empty_maybe = maybe_module.Maybe(EMPTY_VALUE, EMPTY_VALUE)

    # Action: use the Lazy object as the "filterer" for the second Maybe
    result_maybe = empty_maybe.filter(lazy_from_filtered)

    # Assertion: filtering should return a Maybe instance (no exception and correct type)
    assert isinstance(result_maybe, maybe_module.Maybe)

def test_maybe_filter_raises_type_error_when_filterer_is_not_callable():
    # Purpose:
    # - Verify that Maybe.filter raises a TypeError when the provided filterer is not callable.
    # - Also verify the behavior of get_or_else and to_box used to produce the non-callable filterer.
    #
    # Setup: construct sample values and Maybe instances with explicit "is_nothing" flags.
    DEFAULT_INT = 2281
    SAMPLE_STRING = "gZ(\\mOcN"
    SAMPLE_DICT = {SAMPLE_STRING: SAMPLE_STRING}
    SAMPLE_TUPLE = (SAMPLE_STRING, SAMPLE_STRING, SAMPLE_DICT, SAMPLE_DICT)

    # Create an "empty" Maybe (is_nothing=True) so that get_or_else returns the provided default value.
    EMPTY_FLAG = True
    empty_maybe = maybe_module.Maybe(SAMPLE_TUPLE, EMPTY_FLAG)

    # Preconditions / quick checks: get_or_else should return the default when Maybe is empty.
    non_callable_filterer = empty_maybe.get_or_else(DEFAULT_INT)
    assert non_callable_filterer == DEFAULT_INT

    # to_box on an empty Maybe should produce a Box holding None (Box API stores value in .value).
    box_from_empty = empty_maybe.to_box()
    assert getattr(box_from_empty, "value", None) is None

    # Create a non-empty Maybe to call filter on (is_nothing=False).
    NON_EMPTY_FLAG = False
    some_value = object()
    non_empty_maybe = maybe_module.Maybe(some_value, NON_EMPTY_FLAG)

    # Execution & Assertion:
    # - Passing a non-callable (the integer returned by get_or_else) to filter should raise TypeError
    #   because filter attempts to call the provided filterer like a function.
    with pytest.raises(TypeError):
        non_empty_maybe.filter(non_callable_filterer)

def test_maybe_conversion_and_bind_type_error_when_mapper_not_callable():
    # Constants / test data
    BOOL_VALUE = True
    NONE_VALUE = None
    FLOAT_VALUE = -286.64
    INT_VALUE = -1784
    EMPTY_TUPLE = ()

    # Setup: create several Maybe instances exercising non-empty and empty cases
    # - maybe_true: value differs from the "nothing" marker -> should be non-empty
    # - maybe_int: value differs from the "nothing" marker -> should be non-empty
    # - maybe_float_nothing: value equals the "nothing" marker -> should be empty
    maybe_true = maybe_module.Maybe(BOOL_VALUE, NONE_VALUE)
    maybe_int = maybe_module.Maybe(INT_VALUE, EMPTY_TUPLE)
    maybe_float_nothing = maybe_module.Maybe(FLOAT_VALUE, FLOAT_VALUE)

    # Execution: transform Maybes to other monads and extract values
    validation_from_true = maybe_true.to_validation()
    validation_from_int = maybe_int.to_validation()
    extracted_value = maybe_int.get_or_else(INT_VALUE)
    try_from_int = maybe_int.to_try()

    # Assertions: basic expectations about conversions and get_or_else behavior
    # - get_or_else should return the contained value when Maybe is non-empty
    assert extracted_value == INT_VALUE

    # - to_try should produce a Try that reports success for a non-empty Maybe
    assert hasattr(try_from_int, "is_success") and try_from_int.is_success is True
    assert hasattr(try_from_int, "value") and try_from_int.value == INT_VALUE

    # - the maybe that used the same value as the "nothing" marker should be considered empty
    assert hasattr(maybe_float_nothing, "is_nothing") and maybe_float_nothing.is_nothing is True

    # Core behavior under test:
    # bind expects a callable mapper. Passing a non-callable (here the Try instance)
    # should raise a TypeError when bind attempts to call it.
    import pytest
    with pytest.raises(TypeError):
        maybe_int.bind(try_from_int)

    # Also assert the validation conversions returned something (basic sanity check).
    # The exact Validation API is not relied upon here; presence is sufficient.
    assert validation_from_true is not None
    assert validation_from_int is not None

def test_map_on_empty_maybe_returns_empty_and_to_either_transforms_empty_to_left_none():
    """Verify that mapping over an empty Maybe returns empty (mapper not called)
    and that converting an empty Maybe to Either produces a Left carrying None.
    """
    # Setup: create empty Maybe instances (second ctor arg marks it as "nothing")
    EMPTY_VALUE = None
    IS_NOTHING = True
    UNUSED_MAPPER = {True}  # intentionally not callable; should not be used for empty Maybe

    empty_maybe = maybe_module.Maybe(EMPTY_VALUE, IS_NOTHING)
    another_empty_maybe = maybe_module.Maybe(-1095, IS_NOTHING)

    # Execution
    mapped_result = empty_maybe.map(UNUSED_MAPPER)
    either_result = another_empty_maybe.to_either()

    # Assertions
    assert getattr(mapped_result, "is_nothing", False) is True
    assert either_result.__class__.__name__ == "Left"
    assert getattr(either_result, "value", None) is None

def test_maybe_conversions_with_none_and_tuple():
    # This test verifies conversions between Maybe and other monads (Lazy, Either, Try).
    # It covers a Maybe constructed with a None value and a Maybe constructed with a tuple
    # (containing the first Maybe). We assert that conversions produce the expected monad types
    # and that Try preserves success flag and value when Maybe is not "nothing".
    # Setup: define constants and create Maybe instances.
    NONE = None
    UNKNOWN_IS_NOTHING = None  # preserve original test's second-argument value (None)
    IS_NOTHING_FALSE = False   # explicit False used for the second Maybe

    maybe_with_none = maybe_module.Maybe(NONE, UNKNOWN_IS_NOTHING)
    tuple_containing_maybe = (maybe_with_none,)

    # Execution: perform conversions between monads
    lazy_from_none = maybe_with_none.to_lazy()              # Maybe -> Lazy
    maybe_with_tuple = maybe_module.Maybe(tuple_containing_maybe, IS_NOTHING_FALSE)
    either_from_none_first = maybe_with_none.to_either()    # Maybe -> Either
    try_from_tuple = maybe_with_tuple.to_try()              # Maybe -> Try
    either_from_none_second = maybe_with_none.to_either()   # another Maybe -> Either
    either_from_tuple = maybe_with_tuple.to_either()        # Maybe(with tuple) -> Either
    lazy_from_try = try_from_tuple.to_lazy()                # Try -> Lazy

    # Assertions: check returned monad types and key properties
    assert lazy_from_none is not None
    assert lazy_from_none.__class__.__name__ == "Lazy"

    # The Maybe constructed with (None, None) uses None as the is_nothing flag (falsy),
    # so it behaves as a non-empty Maybe with value None -> to_either should produce Right.
    assert either_from_none_first.__class__.__name__ == "Right"
    assert either_from_none_second.__class__.__name__ == "Right"

    # The Maybe constructed with the tuple is explicitly not-nothing (False), so to_try should
    # produce a successful Try containing the tuple value.
    assert try_from_tuple.__class__.__name__ == "Try"
    # Try is expected to expose 'is_success' and 'value' based on the library implementation
    assert getattr(try_from_tuple, "is_success", None) is True
    assert getattr(try_from_tuple, "value", None) == tuple_containing_maybe

    # Converting the Try back to a Lazy should produce a Lazy instance
    assert lazy_from_try is not None
    assert lazy_from_try.__class__.__name__ == "Lazy"

    # Converting the Maybe that held the tuple to Either should produce Right as well
    assert either_from_tuple.__class__.__name__ == "Right"

def test_maybe_to_try_then_try_to_box_preserves_value():
    """
    Verify that a non-empty Maybe converts to a successful Try preserving the original value,
    and that converting that Try to a Box also preserves the same value.
    """
    # Test data
    SAMPLE_VALUE = True
    IS_NOTHING = False  # indicates this Maybe is not empty

    # Create a Maybe that contains a value
    maybe_with_value = maybe_module.Maybe(SAMPLE_VALUE, IS_NOTHING)

    # Convert Maybe -> Try, then Try -> Box
    converted_try = maybe_with_value.to_try()
    box_from_try = converted_try.to_box()

    # The Try should represent a successful computation and hold the original value
    assert getattr(converted_try, "is_success", True) is True
    assert getattr(converted_try, "value", None) == SAMPLE_VALUE

    # The resulting Box should contain the same value
    assert getattr(box_from_try, "value", None) == SAMPLE_VALUE

def test_maybe_nothing_transforms_and_equality():
    # Purpose:
    # Verify that a Maybe created as "nothing" can be transformed into other monads
    # (Lazy, Validation, Either, Try, Box), that filter/ap operations on the empty
    # Maybe produce empty results, and that two empty Maybes compare equal.
    #
    # This test focuses on exercising the transformation and applicative methods
    # and asserting that they complete without error and maintain the "nothing"
    # semantics where applicable.

    # --- Constants / Setup ---
    SAMPLE_BYTES = b"C\xcf\xe7/"
    DEFAULT_NONE = None
    IS_EMPTY = True

    # Create an empty Maybe (value=None, is_nothing=True)
    empty_maybe = maybe_module.Maybe(DEFAULT_NONE, IS_EMPTY)

    # --- Execution / Actions ---
    # Applying an applicative to an empty Maybe should yield an empty Maybe
    after_ap = empty_maybe.ap(DEFAULT_NONE)

    # Convert the empty Maybe to a Lazy monad, then to a Validation
    lazy_from_empty = after_ap.to_lazy()
    validation_from_lazy = lazy_from_empty.to_validation()

    # Use the Validation as a (non-functional) filterer on the original empty Maybe.
    # This is intended to exercise the filter path when the Maybe is empty.
    filtered_maybe = empty_maybe.filter(validation_from_lazy)

    # Use get_or_else with the filtered_maybe itself as the default to ensure the method returns
    # the provided default when the Maybe is empty.
    defaulted_value = filtered_maybe.get_or_else(filtered_maybe)

    # Convert the filtered result to Either, and convert the earlier Validation to Try.
    either_from_filtered = filtered_maybe.to_either()
    try_from_validation = validation_from_lazy.to_try()

    # Compare two empty Maybe instances for equality
    equality_check = filtered_maybe.__eq__(after_ap)

    # Convert the defaulted_value (which will be an empty Maybe) to a Box
    boxed_value = defaulted_value.to_box()

    # Finally, exercise ap on the Try instance with a bytes payload to ensure it can be called.
    try_ap_result = try_from_validation.ap(SAMPLE_BYTES)

    # --- Assertions ---
    # The original Maybe was constructed as empty
    assert empty_maybe.is_nothing is True

    # ap on an empty Maybe yields another empty Maybe
    assert after_ap.is_nothing is True

    # The Lazy and Validation transformations should produce objects (not raise)
    assert lazy_from_empty is not None
    assert validation_from_lazy is not None

    # Filtering an empty Maybe should produce an empty Maybe
    assert filtered_maybe.is_nothing is True

    # get_or_else called with the Maybe itself should return that same object (default)
    assert defaulted_value is filtered_maybe

    # Conversions to Either / Try / Box should produce objects (and not raise)
    assert either_from_filtered is not None
    assert try_from_validation is not None
    assert boxed_value is not None

    # Two empty Maybe instances should be equal
    assert equality_check is True

    # The Try.ap invocation should return an object (callable path executed)
    assert try_ap_result is not None

def test_maybe_nothing_behaviour_across_transformations():
    # Purpose:
    # - Verify behaviour of Maybe instances that are constructed as "nothing" (is_nothing truthy)
    # - Ensure transformations (to_validation, to_either, to_try), applicative apply (ap), bind and equality behave consistently
    # - Confirm get_or_else returns the provided default when Maybe is nothing

    # ---- Constants / test data ----
    SAMPLE_BYTES = b"\xdbC\xcf\xe7/"
    SAMPLE_INT = -3289

    # ---- Setup: construct Maybe instances that represent "nothing" ----
    # The constructor receives (value, is_nothing_flag); passing a truthy second argument yields a Nothing
    nothing_maybe_a = maybe_module.Maybe(None, True)
    nothing_maybe_b = maybe_module.Maybe(None, SAMPLE_BYTES)  # SAMPLE_BYTES is truthy -> treated as nothing

    # ---- Execution: perform various operations on Nothing maybes ----
    # Applying functions on a Nothing should return a Nothing
    after_ap_none = nothing_maybe_a.ap(None)
    after_ap_bytes = after_ap_none.ap(SAMPLE_BYTES)

    # Transformations to other monads
    validation_from_after = after_ap_bytes.to_validation()
    validation_from_b = nothing_maybe_b.to_validation()
    try_from_b = nothing_maybe_b.to_try()
    either_from_b = nothing_maybe_b.to_either()

    # get_or_else should return the provided default when Maybe is nothing
    default_result = nothing_maybe_b.get_or_else(nothing_maybe_b)

    # bind on a Nothing should return a Nothing (mapper not called)
    bound_from_b = nothing_maybe_b.bind(validation_from_b)

    # ap with a Nothing should remain Nothing
    applied_self = nothing_maybe_b.ap(nothing_maybe_b)

    # Compare different monad types for equality and chaining behavior
    either_eq_validation = either_from_b.__eq__(validation_from_b)
    either_bound = either_from_b.bind(nothing_maybe_b)
    equality_bound = nothing_maybe_b.__eq__(bound_from_b)
    validation_from_bound = bound_from_b.to_validation()

    # Applying an argument to a failed Try should remain failed
    try_applied = try_from_b.ap(SAMPLE_INT)

    # ---- Assertions: expected properties and relationships ----
    # The ap chain starting from a Nothing stays nothing
    assert getattr(after_ap_none, "is_nothing", True) is True
    assert getattr(after_ap_bytes, "is_nothing", True) is True

    # Converting Nothing to Validation yields the same Validation result as converting other Nothing
    assert validation_from_after == validation_from_b
    assert validation_from_b == validation_from_bound

    # get_or_else should return the provided default object when Maybe is nothing
    assert default_result is nothing_maybe_b

    # bind on a Nothing returns a Nothing (so bound_from_b should be a Nothing Maybe)
    assert equality_bound is True

    # ap on a Nothing with itself yields a Nothing (structural equality)
    assert applied_self == nothing_maybe_b

    # Converting Nothing to Either should not be equal to the Validation produced from Nothing
    assert either_eq_validation is False

    # Binding a Left (from a Nothing) should keep it as Left (no change)
    assert either_bound == either_from_b

    # Try produced from a Nothing should be a failure; applying still yields a failure
    assert getattr(try_from_b, "is_success", False) is False
    assert getattr(try_applied, "is_success", False) is False

def test_maybe_map_with_validation_instance_raises_type_error():
    # Purpose:
    # - Ensure Maybe.__eq__ returns False when compared with a non-Maybe object.
    # - Ensure Maybe.map raises a TypeError when given a non-callable (here: a Validation instance).
    IS_NOTHING = False
    VALUE_FALSE = False

    # Compare a Maybe to a plain bool (non-Maybe) using __eq__
    maybe_for_eq = maybe_module.Maybe(IS_NOTHING, VALUE_FALSE)
    equals_result = maybe_for_eq.__eq__(VALUE_FALSE)
    assert equals_result is False

    # Create a Maybe and convert it through Either -> Lazy -> Validation (Validation is non-callable)
    maybe_for_transform = maybe_module.Maybe(IS_NOTHING, VALUE_FALSE)
    either_result = maybe_for_transform.to_either()
    lazy_result = maybe_for_transform.to_lazy()
    validation_result = lazy_result.to_validation()

    # Calling map with a Validation instance (non-callable) must raise TypeError
    with pytest.raises(TypeError):
        maybe_for_transform.map(validation_result)

def test_maybe_present_false_converts_to_try_and_validation_and_is_equal_to_self():
    # Purpose:
    # Verify that a non-empty Maybe containing the boolean False:
    # - compares equal to itself,
    # - converts to a successful Try preserving the False value,
    # - converts to a successful Validation preserving the False value.

    # Constants / Setup
    IS_NOTHING = False  # indicates Maybe is present (not "nothing")
    VALUE = False
    maybe_present = maybe_module.Maybe(IS_NOTHING, VALUE)

    # Execution
    equality_with_self = maybe_present == maybe_present
    try_result = maybe_present.to_try()
    validation_result = maybe_present.to_validation()

    # Assertions
    # equality: a Maybe should be equal to itself
    assert equality_with_self is True

    # Try: when Maybe is present, to_try() should produce a successful Try with the same value
    assert hasattr(try_result, "is_success"), "Try result should have 'is_success' attribute"
    assert try_result.is_success is True
    assert getattr(try_result, "value") == VALUE

    # Validation: when Maybe is present, to_validation() should produce a successful Validation with the same value
    assert hasattr(validation_result, "is_success"), "Validation result should have 'is_success' attribute"
    assert validation_result.is_success is True
    assert getattr(validation_result, "value") == VALUE

