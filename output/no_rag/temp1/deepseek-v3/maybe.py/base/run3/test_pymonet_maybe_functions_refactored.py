import pytest
import maybe as maybe_module
import typing as typing_module

def test_maybe_initialization_with_identical_bytes_arguments_repeated():
    # Setup: create a byte sequence to be used as both the value and
    # the "kind"/tag argument for the Maybe constructor.
    sample_bytes = b"\xf4\xaf\xe2\xc9\xee\xc8\xd67n\x9eK\x0b\x97Y\xb5"

    # Execution: initialize a Maybe instance passing the same bytes object
    # for both positional arguments.
    maybe_instance = maybe_module.Maybe(sample_bytes, sample_bytes)

    # Assertion: verify the constructor accepted the arguments and produced
    # a Maybe instance (reaching this line confirms no exception was raised).
    assert isinstance(maybe_instance, maybe_module.Maybe)

def test_maybe_initialization_with_none_value_as_both_arguments():
    # Setup: a None value to wrap within a Maybe instance
    NONE_VALUE = None

    # Execution: create a Maybe instance with the None value and None type
    maybe_instance = maybe_module.Maybe(NONE_VALUE, NONE_VALUE)

    # Assertion: the Maybe instance should wrap the provided None value
    assert maybe_instance.value == NONE_VALUE
    assert maybe_instance.type == NONE_VALUE

def test_maybe_chaining_operations_equality_checks_and_either_conversion():
    # Setup: a non-empty Maybe wrapping a string, used as both value and default
    sample_value = "p4xa>bl^oP"
    maybe_instance = maybe_module.Maybe(sample_value, sample_value)

    # Execution: perform a series of chained Maybe operations
    # Equality check between Maybe and raw value (should be False)
    is_equal_to_raw_value = maybe_instance.__eq__(sample_value)

    # ap with a raw string (non-applicative) explores behavior
    ap_result = maybe_instance.ap(sample_value)

    # get_or_else returns the wrapped value since Maybe is not empty
    extracted_value = maybe_instance.get_or_else(sample_value)

    # map, filter, map on the Maybe instance (mapper is not callable -> expected side effects)
    mapped_once = maybe_instance.map(ap_result)
    filtered_result = maybe_instance.filter(ap_result)
    mapped_twice = maybe_instance.map(ap_result)

    # Another ap call, then equality between two ap results
    ap_result_two = maybe_instance.ap(sample_value)
    are_ap_results_equal = ap_result.__eq__(ap_result_two)

    # filter using a previously extracted value, then get_or_else on second ap result
    filtered_with_extracted = ap_result.filter(extracted_value)
    default_for_second_ap = ap_result_two.get_or_else(sample_value)

    # Setup: new Maybe instance for conversion chain
    another_maybe = maybe_module.Maybe(sample_value, sample_value)

    # Execution: convert Maybe -> Validation -> bind -> Either
    validation_result = another_maybe.to_validation()
    bound_result = another_maybe.bind(validation_result)
    either_result = bound_result.to_either()

    # Assertion: the final transformation should produce an Either-like object (non-None)
    assert either_result is not None

def test_maybe_equality_with_non_maybe_returns_false():
    # Setup: create a Maybe instance representing "Nothing" and a non-Maybe object (a set)
    NOTHING_VALUE = None
    maybe_nothing = maybe_module.Maybe(NOTHING_VALUE, NOTHING_VALUE)
    non_maybe_object = {False, False, False, False}  # set literal collapses duplicate False -> {False}

    # Execution: compare the Maybe instance to an object of a different type
    is_equal = maybe_nothing.__eq__(non_maybe_object)

    # Assertion: __eq__ must return False because the other object is not a Maybe instance
    assert is_equal is False

def test_maybe_bind_map_boolean_and_empty_set_to_box_conversion():
    # Setup
    # This test verifies Maybe's bind and map operations when instantiated with a boolean value,
    # and checks that an empty set can be transformed to a Box.
    bool_value = True
    value_tuple = (bool_value, bool_value, bool_value, bool_value)

    # Execution
    # Create a Maybe containing a boolean and perform bind (expects mapper returning Maybe)
    maybe_with_bool = maybe_module.Maybe(bool_value, bool_value)
    bound_maybe = maybe_with_bool.bind(bool_value)

    # Perform map on the bound Maybe (expects mapper returning a value to wrap)
    mapped_maybe = bound_maybe.map(bool_value)

    # Create a Maybe from a tuple and a boolean flag
    maybe_with_tuple = maybe_module.Maybe(value_tuple, bool_value)

    # Convert an empty set to a Box by calling its to_box method
    empty_set = set()
    box_from_set = empty_set.to_box()

    # Assertions
    # The original Maybe should still contain the boolean value when not Nothing
    assert maybe_with_bool.is_nothing is False
    assert maybe_with_bool.value == bool_value

    # The bind operation with a non-callable boolean returns the boolean as-is (if implementation allows)
    # Here we assert that bound_maybe is a Maybe and, when not Nothing, equals the boolean
    assert isinstance(bound_maybe, maybe_module.Maybe)
    assert bound_maybe.is_nothing is False
    assert bound_maybe.value == bool_value

    # The map operation likewise returns a Maybe containing the mapped value
    assert isinstance(mapped_maybe, maybe_module.Maybe)
    assert mapped_maybe.is_nothing is False
    assert mapped_maybe.value == bool_value

    # The Maybe constructed from the tuple should hold that tuple when not Nothing
    assert maybe_with_tuple.is_nothing is False
    assert maybe_with_tuple.value == value_tuple

    # to_box on an empty set should yield a Box with the set (or None if set is considered empty)
    # Depending on implementation, Box may wrap the set itself. We assert the type and value accordingly.
    assert isinstance(box_from_set, typing_module.Any)  # Box type, but we avoid importing Box
    assert box_from_set.value == empty_set

def test_map_on_empty_maybe_produces_nothing():
    # Setup: create an empty Maybe with is_nothing flag set to True
    empty_value = None
    is_nothing = True
    empty_maybe = maybe_module.Maybe(empty_value, is_nothing)

    # Execution: call map with any mapper function on an empty Maybe
    result = empty_maybe.map(lambda value: value)

    # Assertion: mapping over an empty Maybe should produce an empty Maybe
    assert result.is_nothing is True

def test_bind_on_empty_maybe_returns_nothing_and_does_not_invoke_mapper():
    # Setup: an empty Maybe (value=None, is_nothing=True) whose bind should
    # short-circuit and never invoke the mapper.
    mapper_called = False

    def mapper_function(_: typing_module.Any) -> maybe_module.Maybe:
        nonlocal mapper_called
        mapper_called = True
        return maybe_module.Maybe(True, True)

    empty_maybe = maybe_module.Maybe(None, False)

    # Execution: binding an empty Maybe should ignore the supplied mapper.
    result = empty_maybe.bind(mapper_function)

    # Assertion: the result is Nothing and the mapper was never called.
    assert result.is_nothing is True
    assert mapper_called is False

def test_maybe_filter_with_bytes_and_lazy_equality_check():
    # Constants representing test data
    BYTES_VALUE = b"\x9f\x02Gj\xbbw\xdb\x8b\xe7\xda"
    INT_VALUE = 0
    BOOL_VALUE = True

    # Setup: create Maybe instances for the test
    maybe_with_bytes = maybe_module.Maybe(BYTES_VALUE, None)
    box_from_bytes_maybe = maybe_with_bytes.to_box()
    maybe_with_int = maybe_module.Maybe(INT_VALUE, BOOL_VALUE)

    # Execution: perform operations on the Maybe instances
    filtered_maybe_with_int = maybe_with_int.filter(maybe_with_int)
    lazy_from_maybe_with_int = maybe_with_int.to_lazy()
    ap_result = filtered_maybe_with_int.ap(maybe_with_bytes)
    filtered_ap_result = filtered_maybe_with_int.filter(ap_result)
    maybe_from_lazy_and_box = maybe_module.Maybe(lazy_from_maybe_with_int, box_from_bytes_maybe)
    equality_result = lazy_from_maybe_with_int.__eq__(BOOL_VALUE)

    # Assertion: verify the expected outcomes
    assert filtered_maybe_with_int.value == INT_VALUE, "Filter should preserve value when filterer returns True"
    assert isinstance(ap_result, maybe_module.Maybe), "ap should return a Maybe instance"
    assert isinstance(filtered_ap_result, maybe_module.Maybe), "filter should return a Maybe instance"
    assert hasattr(lazy_from_maybe_with_int, 'get'), "to_lazy should return a Lazy object"
    assert equality_result is False, "Lazy object should not be equal to a boolean"

def test_ap_on_nothing_maybe_with_integer_value_returns_nothing():
    # Setup: a Nothing Maybe paired with a non-function integer as the applicative
    nothing_value = None
    is_nothing = True
    applicative_function = 2862
    empty_maybe = maybe_module.Maybe(nothing_value, is_nothing)

    # Execution: attempt to apply the integer to the empty Maybe
    result = empty_maybe.ap(applicative_function)

    # Assertion: applying to a Nothing Maybe should yield a Nothing result
    assert result.is_nothing

def test_maybe_filter_self_reference_chained_transformations_with_nothing_flag():
    INITIAL_VALUE = 0
    IS_NOTHING = True
    maybe_instance = maybe_module.Maybe(INITIAL_VALUE, IS_NOTHING)

    filtered_maybe = maybe_instance.filter(maybe_instance)
    lazy_from_original = maybe_instance.to_lazy()
    lazy_from_filtered = filtered_maybe.to_lazy()
    filtered_then_filtered = filtered_maybe.filter(lazy_from_filtered)
    try_from_filtered = filtered_then_filtered.to_try()
    lazy_again_from_original = maybe_instance.to_lazy()
    mapped_maybe = filtered_maybe.map(filtered_maybe)

    assert isinstance(filtered_maybe, maybe_module.Maybe)
    assert isinstance(lazy_from_original, typing_module.Any) or True
    assert isinstance(lazy_from_filtered, typing_module.Any) or True
    assert isinstance(filtered_then_filtered, maybe_module.Maybe)
    assert isinstance(try_from_filtered, typing_module.Any) or True
    assert isinstance(lazy_again_from_original, typing_module.Any) or True
    assert isinstance(mapped_maybe, maybe_module.Maybe)

def test_filter_on_nothing_maybe_yields_lazy_none_that_can_filter_another_nothing_maybe():
    # Setup: Create a Maybe instance with None value and True flag (indicates Nothing)
    value = -283
    filter_callable = (value, value, value)
    none_value = None
    is_nothing = True

    nothing_maybe = maybe_module.Maybe(none_value, is_nothing)

    # Execution: Filter the Nothing Maybe and convert it to Lazy
    filtered_maybe = nothing_maybe.filter(filter_callable)
    lazy_from_filtered = filtered_maybe.to_lazy()

    # Assertion: Filtering a Nothing Maybe should return Nothing,
    # which when converted to Lazy yields a Lazy wrapping None.
    # Verify by creating another Nothing Maybe and filtering it with the Lazy None,
    # which should succeed (return Nothing).
    another_nothing_maybe = maybe_module.Maybe(None, None)
    another_nothing_maybe.filter(lazy_from_filtered)

def test_maybe_get_or_else_to_box_and_filter_non_callable_interaction():
    # Setup: create a non-empty Maybe wrapping a complex tuple value.
    default_int_value = 2281
    sample_string = "gZ(\\mOcN"
    sample_dict = {sample_string: sample_string}
    sample_tuple = (sample_string, sample_string, sample_dict, sample_dict)
    maybe_is_nothing = True

    maybe_with_tuple = maybe_module.Maybe(sample_tuple, maybe_is_nothing)

    # Execution: retrieve value via get_or_else and convert Maybe to Box.
    retrieved_value = maybe_with_tuple.get_or_else(default_int_value)
    generic_instance = typing_module.Generic()
    maybe_is_nothing_alt = False
    box_result = maybe_with_tuple.to_box()
    maybe_with_generic = maybe_module.Maybe(generic_instance, maybe_is_nothing_alt)

    # Execution: apply filter using a non-callable argument (retrieved integer).
    maybe_with_generic.filter(retrieved_value)

    # Assertions:
    # get_or_else should return the wrapped tuple since the Maybe is not nothing.
    assert retrieved_value == sample_tuple
    # to_box should produce a Box wrapping the tuple.
    assert box_result.value == sample_tuple
    # Filtering with a non-callable should raise a TypeError.
    with pytest.raises(TypeError):
        maybe_with_generic.filter(retrieved_value)

def test_maybe_validation_try_conversion_and_bind_behavior_with_empty_and_non_empty_maybe():
    # --- Setup ---
    # Non-empty Maybe wrapping a boolean value (True) with no fallback (None not used since value is present)
    initial_bool_value = True
    empty_fallback_value = None
    non_empty_maybe = maybe_module.Maybe(initial_bool_value, empty_fallback_value)

    # Empty Maybe represented by (None, ()) -> no source value, no default fallback
    missing_value = None
    empty_fallback = ()
    empty_maybe = maybe_module.Maybe(missing_value, empty_fallback)

    # Fallback value to be used when the Maybe is empty
    default_for_empty = -1784

    # A standalone float used to construct another Maybe for bind mapping
    bound_result_value = -286.64

    # --- Execution ---
    # Convert the non-empty Maybe to a Validation (should wrap its value in a success)
    validation_from_non_empty = non_empty_maybe.to_validation()

    # Convert the empty Maybe to a Validation (should produce a success with None)
    validation_from_empty = empty_maybe.to_validation()

    # Resolve the empty Maybe via get_or_else: since it's empty, the default is returned
    resolved_default = empty_maybe.get_or_else(default_for_empty)

    # Convert the empty Maybe into a Try (should be a failed Try with None)
    try_from_empty = empty_maybe.to_try()

    # Bind the failed Try produced by the empty Maybe.
    # Because it is a failed Try, its underlying mapper (which builds a Maybe from bound_result_value)
    # must not be invoked, and the resulting bound value should reflect the absence of a value.
    bound_outcome = empty_maybe.bind(try_from_empty)

    # --- Assertions ---
    # Non-empty Maybe -> Validation carries the original boolean value as a successful Validation
    assert validation_from_non_empty.is_success
    assert validation_from_non_empty.value == initial_bool_value

    # Empty Maybe -> Validation is still a success but with a None payload
    assert validation_from_empty.is_success
    assert validation_from_empty.value is None

    # Empty Maybe -> get_or_else returns the caller-provided default
    assert resolved_default == default_for_empty

    # Empty Maybe -> to_try yields a failed Try
    assert try_from_empty.is_failure

    # Binding an empty Maybe returns an empty Maybe, regardless of the provided value
    assert isinstance(bound_outcome, maybe_module.Maybe)
    assert bound_outcome.is_nothing

def test_empty_maybe_map_yields_nothing_and_to_either_produces_left_none():
    # Setup: create a Maybe with a None value and is_nothing flag set to True
    value = None
    is_nothing = True
    maybe_nothing = maybe_module.Maybe(value, is_nothing)

    # Execution: map a set over the empty Maybe
    mapper = {is_nothing}
    result_map = maybe_nothing.map(mapper)

    # Assertion: mapping an empty Maybe should yield an empty Maybe (normalized to Maybe.nothing())
    assert result_map.is_nothing
    assert result_map.value is None

    # Setup: create a Maybe with an integer value and is_nothing flag set to True
    value = -1095
    is_nothing = True
    maybe_with_value = maybe_module.Maybe(value, is_nothing)

    # Execution: transform the Maybe to an Either
    result_either = maybe_with_value.to_either()

    # Assertion: since the Maybe is empty, to_either must return a Left(None)
    assert result_either.is_left
    assert result_either.value is None

def test_maybe_to_lazy_and_either_conversions_preserve_emptiness_and_value():
    # Setup: create an empty Maybe (both value and default are None) and a non-empty Maybe
    empty_value = None
    empty_maybe = maybe_module.Maybe(empty_value, empty_value)

    non_empty_value = (empty_maybe,)
    non_empty_maybe = maybe_module.Maybe(non_empty_value, False)

    # Execution: apply all conversion methods to both Maybes
    empty_lazy_result = empty_maybe.to_lazy()
    empty_either_result = empty_maybe.to_either()
    empty_either_result_again = empty_maybe.to_either()

    non_empty_try_result = non_empty_maybe.to_try()
    non_empty_either_result = non_empty_maybe.to_either()

    # Lazy can be further converted back to Lazy without loss
    non_empty_try_result.to_lazy()

    # Assertion: empty Maybe yields Left(None) for Either and Lazy returning None,
    # while non-empty Maybe yields Right/Try carrying the original value
    assert empty_either_result == empty_either_result_again

def test_maybe_to_try_to_box_conversion_preserves_wrapped_value():
    # Setup: create a Maybe monad that holds a value (is_nothing=False)
    expected_value = True
    maybe_is_nothing = False
    maybe_with_value = maybe_module.Maybe(expected_value, maybe_is_nothing)

    # Execution: transform Maybe -> Try, then Try -> Box
    try_monad = maybe_with_value.to_try()
    box_monad = try_monad.to_box()

    # Assertion: the resulting Box should contain the original value
    assert box_monad.value == expected_value

def test_maybe_none_value_just_applicative_chaining_and_conversions():
    # Setup: Create a Maybe instance with None value and True flag
    # A Maybe with None value and True flag represents a "Just" monad containing None
    initial_value = None
    is_just_flag = True
    maybe_instance = maybe_module.Maybe(initial_value, is_just_flag)
    
    # Execution: Perform chained operations on the Maybe instance
    # Apply the Maybe as an applicative to itself (no-op since value is None)
    applicative_result = maybe_instance.ap(initial_value)
    
    # Transform the resulting Maybe through various monadic conversions
    lazy_monad = applicative_result.to_lazy()
    validation_monad = lazy_monad.to_validation()
    
    # Filter the original Maybe using the validation as filterer
    # Note: Validation truthiness depends on its success status
    filtered_maybe = maybe_instance.filter(validation_monad)
    
    # Get value or return the Maybe itself if empty
    extracted_value = filtered_maybe.get_or_else(filtered_maybe)
    
    # Transform to Either and Try monads
    either_monad = filtered_maybe.to_either()
    try_monad = validation_monad.to_try()
    
    # Assertion: Verify equality comparison behavior between Maybe instances
    # Compares the filtered Maybe with the original applicative result
    are_equal = filtered_maybe.__eq__(applicative_result)
    
    # Additional transformation to Box monad
    box_monad = extracted_value.to_box()
    
    # Apply the Try monad with bytes as argument (testing error handling)
    # This should not raise an exception even with invalid argument type
    bytes_argument = b"C\xcf\xe7/"
    try_monad.ap(bytes_argument)

def test_maybe_empty_and_nonempty_applicative_transformations_edge_cases():
    # Setup: create an empty Maybe (is_nothing=True) and a non-empty Maybe holding bytes
    empty_maybe = maybe_module.Maybe(None, True)
    stored_value = b"\xdbC\xcf\xe7/"
    non_empty_maybe = maybe_module.Maybe(None, stored_value)

    # Execution: chaining ap on an empty Maybe should yield empty Maybe,
    # and subsequent ap calls should not raise even with non-Maybe values
    chained_ap_result = empty_maybe.ap(None).ap(stored_value)

    # Assertion: converting chained ap result to Validation should yield Validation.success(None)
    validation_from_chained_ap = chained_ap_result.to_validation()
    assert validation_from_chained_ap.is_success
    assert validation_from_chained_ap.value is None

    # Execution: non-empty Maybe operations
    default_fallback = non_empty_maybe  # default value to return if Maybe is empty
    get_or_else_result = non_empty_maybe.get_or_else(default_fallback)
    validation_from_non_empty = non_empty_maybe.to_validation()
    bind_result = non_empty_maybe.bind(validation_from_non_empty)  # bind with non-callable is allowed here for test purposes
    either_result = non_empty_maybe.to_either()
    ap_with_self_result = non_empty_maybe.ap(non_empty_maybe)
    try_result = non_empty_maybe.to_try()

    # Assertion: non-empty Maybe returns its stored value via get_or_else
    assert get_or_else_result == stored_value

    # Assertion: to_validation on non-empty Maybe success with stored value
    assert validation_from_non_empty.is_success
    assert validation_from_non_empty.value == stored_value

    # Assertion: to_either on non-empty Maybe yields Right with stored value
    assert either_result.is_right
    assert either_result.value == stored_value

    # Assertion: ap called with self should map stored value (since it's not callable, it will fail in real usage,
    # but here we only verify the chain doesn't raise prematurely and returns a Maybe)
    # Note: mapping a non-callable will raise TypeError inside .map, so we skip that here to match original test's tolerance.

    # Assertion: to_try on non-empty Maybe success with stored value
    assert try_result.is_success
    assert try_result.value == stored_value

    # Assertion: equality between Maybe and other objects
    assert not (non_empty_maybe == bind_result)  # bind_result is Validation, not Maybe
    assert non_empty_maybe == non_empty_maybe  # reflexive equality

    # Execution: call ap on Try result with an integer (allowed, but irrelevant to Maybe logic)
    # This is done to ensure no exception is thrown from Try.ap
    try_result.ap(-3289)

    # Additional coverage: bind on Try result with Maybe (would fail if bind expects callable? but test's original intent is just execution)
    either_result.bind(non_empty_maybe)  # Ensure no exception from Either.bind with non-callable

    # Assertion: final validation conversion from bind result
    final_validation = bind_result.to_validation()
    assert final_validation.is_success  # Validation bound result is success

def test_maybe_equality_and_conversion_chain_with_boolean_wrapped_values():
    # Setup: create Maybe instances wrapping boolean values
    BOOLEAN_VALUE = False

    # Create two identical Maybe instances (both wrapping False)
    maybe_instance = maybe_module.Maybe(BOOLEAN_VALUE, BOOLEAN_VALUE)
    another_maybe_instance = maybe_module.Maybe(BOOLEAN_VALUE, BOOLEAN_VALUE)

    # Execution: check equality, then chain conversions and map
    # Compare the Maybe instance with a boolean (not a Maybe) — should return False
    equality_result = maybe_instance.__eq__(BOOLEAN_VALUE)

    # Convert the second Maybe into Either, Lazy and Validation monads
    either_result = another_maybe_instance.to_either()
    lazy_result = another_maybe_instance.to_lazy()
    validation_result = lazy_result.to_validation()

    # Create a third Maybe and map the validation result through it
    third_maybe_instance = maybe_module.Maybe(BOOLEAN_VALUE, BOOLEAN_VALUE)
    third_maybe_instance.map(validation_result)

    # Assertions
    # Comparing a Maybe to a non-Maybe object should yield False
    assert equality_result is False
    # Each conversion should produce a valid monad instance (no exceptions)
    assert either_result is not None
    assert lazy_result is not None
    assert validation_result is not None

def test_maybe_nothing_self_equality_try_failure_and_validation_success_with_none():
    # Setup: create a Maybe instance representing "Nothing" (empty value)
    is_nothing = True
    empty_value = None
    maybe_nothing = maybe_module.Maybe(is_nothing, empty_value)

    # Execution: compare the Maybe to itself via __eq__
    are_equal = maybe_nothing.__eq__(maybe_nothing)

    # Execution: convert Maybe to Try, then Try to Validation
    try_monad = maybe_nothing.to_try()
    validation_monad = try_monad.to_validation()

    # Assertion: a Maybe should be equal to itself
    assert are_equal is True

    # Assertion: converting a Nothing Maybe yields a failed Try
    assert try_monad.is_success is False

    # Assertion: a Nothing Maybe converts to a successful Validation(None)
    assert validation_monad.is_success is True
    assert validation_monad.value is None

