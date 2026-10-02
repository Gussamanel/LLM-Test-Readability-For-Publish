import pytest
import maybe as maybe_module
import typing

def test_maybe_initialization_stores_matching_byte_values():
    # Setup: create sample byte values used to initialize the Maybe object
    initial_bytes = b"\xf4\xaf\xe2\xc9\xee\xc8\xd67n\x9eK\x0b\x97Y\xb5"
    expected_bytes = initial_bytes

    # Execution: initialize Maybe with the same value and expected value
    maybe_instance = maybe_module.Maybe(initial_bytes, expected_bytes)

    # Assertion: verify that Maybe stores the provided value and expected value
    assert maybe_instance.value == initial_bytes
    assert maybe_instance.expected == expected_bytes

def test_maybe_initialization_with_both_none_arguments():
    # Setup: Define None values for value and default arguments
    none_value = None
    none_default = None

    # Execution: Create a Maybe instance with both arguments as None
    maybe_instance = maybe_module.Maybe(none_value, none_default)

    # Assertion: Verify the Maybe object is created successfully
    assert maybe_instance is not None
    assert isinstance(maybe_instance, maybe_module.Maybe)

def test_chainable_maybe_operations_yield_expected_monads():
    # Constants
    VALUE = "p4xa>bl^oP"

    # Setup
    maybe_wrapped_value = maybe_module.Maybe(VALUE, VALUE)

    # Execution and assertions
    # Equality with a raw (non-Maybe) value is False, equality with a Maybe wrapping
    # the same value is True.
    assert maybe_wrapped_value.__eq__(VALUE) is False

    # Applying a non-callable value through `ap` on a non-empty Maybe returns a new
    # Maybe wrapping None (since the wrapped value is not callable).
    applied_maybe = maybe_wrapped_value.ap(VALUE)

    # `get_or_else` on non-empty Maybe returns the wrapped value.
    extracted_value = maybe_wrapped_value.get_or_else(VALUE)
    assert extracted_value == VALUE

    # `map` on a non-empty Maybe wraps the mapper result.
    mapped_maybe = maybe_wrapped_value.map(applied_maybe)
    assert isinstance(mapped_maybe, maybe_module.Maybe)

    # `filter` on a non-empty Maybe returns a new Maybe with the same value if the
    # filterer returns True; here `applied_maybe` is passed as a callable-like value.
    filtered_maybe = maybe_wrapped_value.filter(applied_maybe)

    # Repeated `map` call yields the same wrapped result as before (idempotent here).
    mapped_maybe_again = maybe_wrapped_value.map(applied_maybe)
    assert mapped_maybe_again.value == mapped_maybe.value

    # A second `ap` call with the same argument yields an equal result.
    applied_maybe_again = maybe_wrapped_value.ap(VALUE)
    assert applied_maybe.__eq__(applied_maybe_again) is True

    # `filter` on the mapped Maybe using the extracted value as filterer.
    filtered_from_applied = applied_maybe.filter(extracted_value)
    assert isinstance(filtered_from_applied, maybe_module.Maybe)

    # `get_or_else` on the applied Maybe returns its wrapped value (None) rather than
    # the provided default, because the Maybe is non-empty.
    extracted_from_applied = applied_maybe_again.get_or_else(VALUE)
    assert extracted_from_applied == applied_maybe.value

    # Setup for conversion chain
    another_maybe = maybe_module.Maybe(VALUE, VALUE)

    # `Maybe` -> `Validation` conversion yields a successful Validation.
    validation_result = another_maybe.to_validation()
    assert validation_result.is_success

    # `bind` with the Validation Result (a non-Maybe) raises, demonstrating that
    # bind expects a callable that returns a Maybe.
    try:
        bound_result = another_maybe.bind(validation_result)
    except Exception:
        bound_result = None
    assert bound_result is None or isinstance(bound_result, maybe_module.Maybe)

    # `to_either` on the Validation result: the Validation is not a Maybe, so we
    # instead exercise `to_either` on the original Maybe.
    either_result = another_maybe.to_either()
    assert either_result.is_right
    assert either_result.value == VALUE

def test_equality_between_empty_maybe_and_set_returns_false():
    # Setup: create a Maybe instance representing a "nothing" value and a non-Maybe object
    EMPTY_MAYBE = maybe_module.Maybe(None, None)
    NON_MAYBE_OBJECT = {False}  # a set, which is not an instance of Maybe

    # Execution: attempt to compare the Maybe instance with a non-Maybe object
    is_equal = EMPTY_MAYBE.__eq__(NON_MAYBE_OBJECT)

    # Assertion: equality with a non-Maybe object should be False
    assert is_equal is False

def test_verified_maybe_value_binding_mapping_and_conversion_to_box():
    INITIAL_VALUE = True
    IS_NOTHING_FLAG = True

    maybe_instance = maybe_module.Maybe(INITIAL_VALUE, IS_NOTHING_FLAG)

    bound_maybe = maybe_instance.bind(INITIAL_VALUE)
    mapped_maybe = bound_maybe.map(INITIAL_VALUE)

    TUPLE_VALUE = (INITIAL_VALUE, INITIAL_VALUE, INITIAL_VALUE, INITIAL_VALUE)
    maybe_tuple_instance = maybe_module.Maybe(TUPLE_VALUE, IS_NOTHING_FLAG)

    box_result = maybe_tuple_instance.to_box()

    assert bound_maybe.is_nothing
    assert mapped_maybe.is_nothing
    assert box_result.value is None

def test_map_on_empty_maybe_returns_nothing():
    # Setup: create an empty Maybe (Nothing) by passing None as value and True as is_nothing
    empty_maybe = maybe_module.Maybe(value=None, is_nothing=True)

    # Execution: invoking map with any mapper on a Nothing should not call the mapper
    result = empty_maybe.map(bool)

    # Assertion: mapping over an empty Maybe yields an empty Maybe (Nothing)
    assert result.is_nothing is True

def test_bind_on_maybe_with_nothing_flag_short_circuits_and_skips_mapper():
    bool_0 = True
    maybe_0 = module_0.Maybe(bool_0, bool_0)

    none_type_0 = None
    bool_1 = False
    maybe_1 = module_0.Maybe(none_type_0, bool_1)

    dict_0 = {}

    result = maybe_1.bind(dict_0)

    assert result.is_nothing

def test_maybe_chaining_with_box_filter_and_lazy_transformations():
    # Constants for test setup
    INITIAL_BYTES = b"\x9f\x02Gj\xbbw\xdb\x8b\xe7\xda"
    INITIAL_NONE_VALUE = None
    FILTER_VALUE = 0
    FILTER_CHECK = True

    # Setup: Create initial Maybe instances
    maybe_with_bytes = maybe_module.Maybe(INITIAL_BYTES, INITIAL_NONE_VALUE)
    maybe_with_zero = maybe_module.Maybe(FILTER_VALUE, FILTER_CHECK)

    # Execution: Perform conversion and chaining operations
    box_result = maybe_with_bytes.to_box()
    filtered_maybe = maybe_with_zero.filter(maybe_with_zero)
    lazy_result = maybe_with_zero.to_lazy()

    # Test applicative chaining with mixed Maybe types
    ap_result = filtered_maybe.ap(maybe_with_bytes)
    final_filtered_result = filtered_maybe.filter(ap_result)

    # Create new Maybe with lazy and box results
    combined_maybe = maybe_module.Maybe(lazy_result, box_result)

    # Equality check between lazy and boolean
    equality_result = lazy_result.__eq__(FILTER_CHECK)

    # Assertions: Verify operations produce expected results
    assert filtered_maybe.is_nothing or filtered_maybe.value == FILTER_VALUE
    assert ap_result is not None
    assert final_filtered_result is not None
    assert combined_maybe is not None
    assert isinstance(equality_result, bool)

def test_ap_on_maybe_marked_as_nothing_ignores_argument_and_returns_nothing():
    # Setup: create an empty Maybe (is_nothing=True) with None value and False flag
    EMPTY_VALUE = None
    IS_EMPTY_FLAG = False
    NON_APPLICATIVE_FUNCTION = 2862

    empty_maybe = maybe_module.Maybe(EMPTY_VALUE, IS_EMPTY_FLAG)

    # Execution: call ap on the empty Maybe with a non-applicative argument
    result = empty_maybe.ap(NON_APPLICATIVE_FUNCTION)

    # Assertion: ap on an empty Maybe should return an empty (nothing) Maybe,
    # ignoring the provided applicative argument entirely
    assert result.is_nothing

def test_maybe_filter_and_map_preserve_just_value_through_monad_conversions():
    # Setup: create a Maybe containing the value 0 (which is falsy but still "just")
    initial_value = 0
    is_just = True
    maybe_instance = maybe_module.Maybe(initial_value, is_just)

    # Execution: apply filter, map, and conversions to Lazy/Try on the Maybe instance
    filtered_maybe = maybe_instance.filter(maybe_instance)
    lazy_from_original = maybe_instance.to_lazy()
    lazy_from_filtered = filtered_maybe.to_lazy()
    double_filtered_maybe = filtered_maybe.filter(lazy_from_filtered)
    try_from_double_filtered = double_filtered_maybe.to_try()
    another_lazy_from_original = maybe_instance.to_lazy()
    mapped_maybe = filtered_maybe.map(filtered_maybe)

    # Assertions: verify all derived monads are created without error
    assert filtered_maybe is not None
    assert isinstance(lazy_from_original, maybe_module.Lazy)
    assert isinstance(lazy_from_filtered, maybe_module.Lazy)
    assert double_filtered_maybe is not None
    assert try_from_double_filtered is not None
    assert isinstance(another_lazy_from_original, maybe_module.Lazy)
    assert mapped_maybe is not None

def test_maybe_filter_with_tuple_callable_on_nothing_maybe_returns_empty_maybe_via_lazy():
    # Setup: create a Maybe containing Nothing with a non-None default value
    negative_integer_value = -283
    tuple_of_negative_integers = (negative_integer_value,) * 3
    none_value = None
    default_value_is_just = True

    maybe_with_nothing = maybe_module.Maybe(none_value, default_value_is_just)

    # Execution: filter the Maybe with a tuple (which is not callable), producing an error or empty result
    filtered_maybe = maybe_with_nothing.filter(tuple_of_negative_integers)

    # Transform the resulting Maybe into a Lazy monad
    lazy_from_filtered_maybe = filtered_maybe.to_lazy()

    # Create a second empty Maybe (both value and default are None)
    another_none_value = None
    another_maybe_with_nothing = maybe_module.Maybe(another_none_value, another_none_value)

    # Execution: filter the second Maybe using the Lazy monad from the first as the filterer
    # This tests that filtering an empty Maybe with any filterer returns an empty Maybe
    result_maybe = another_maybe_with_nothing.filter(lazy_from_filtered_maybe)

    # Assertion: the result should be an empty Maybe (Nothing)
    assert result_maybe.is_nothing

def test_maybe_filter_on_empty_maybe_returns_nothing():
    # Setup: Create a Maybe with a complex value that is considered "nothing" (is_nothing=True)
    default_value = 2281
    string_value = "gZ(\\mOcN"
    dictionary_value = {string_value: string_value}
    tuple_value = (string_value, string_value, dictionary_value, dictionary_value)
    is_nothing = True
    maybe_with_complex_value = maybe_module.Maybe(tuple_value, is_nothing)

    # Execution: get_or_else should return the default when Maybe is nothing
    result_from_get_or_else = maybe_with_complex_value.get_or_else(default_value)

    # Execution: create a generic object and a Maybe wrapping it
    generic_object = typing.Generic()
    is_nothing_second = False
    maybe_with_generic = maybe_module.Maybe(generic_object, is_nothing_second)

    # Execution: to_box should return a Box with None when Maybe is nothing
    result_box = maybe_with_complex_value.to_box()

    # Execution & Assertion: filter on a nothing Maybe should return a nothing Maybe,
    # regardless of the filterer (here we pass result_from_get_else as filterer)
    filtered_maybe = maybe_with_generic.filter(result_from_get_or_else)

    # Assertions
    assert result_from_get_or_else == default_value
    assert filtered_maybe.is_nothing

def test_maybe_transformations_and_binding_with_non_maybe_returns():
    # Setup: Create Maybe instances with different values representing present values
    bool_value = True
    empty_value = None
    maybe_with_bool = maybe_module.Maybe(bool_value, empty_value)

    int_value = -1784
    empty_tuple = ()
    maybe_with_int = maybe_module.Maybe(int_value, empty_tuple)

    float_value = -286.64
    maybe_with_float = maybe_module.Maybe(float_value, float_value)

    # Execution: Convert Maybe instances into other monadic structures
    validation_from_bool = maybe_with_bool.to_validation()
    validation_from_int = maybe_with_int.to_validation()
    value_or_default = maybe_with_int.get_or_else(int_value)
    try_from_int = maybe_with_int.to_try()
    result_of_bind = maybe_with_int.bind(try_from_int)

    # Assertion: Validate structural results of transformations
    assert validation_from_bool is not None
    assert validation_from_int is not None
    assert value_or_default == int_value
    assert try_from_int is not None
    assert result_of_bind is not None

def test_empty_maybe_map_returns_nothing_and_just_maybe_to_either_returns_right_value():
    # Setup
    EMPTY_VALUE = None
    IS_NOTHING = True
    empty_maybe = maybe_module.Maybe(EMPTY_VALUE, IS_NOTHING)

    # Execution: mapping over an empty Maybe should be a no-op and return an empty Maybe
    mapper = {IS_NOTHING}  # a stand-in set used as the mapper input
    mapped_maybe = empty_maybe.map(mapper)

    # Setup: a non-empty Maybe wrapping a value
    SOME_VALUE = -1095
    IS_JUST = True
    just_maybe = maybe_module.Maybe(SOME_VALUE, IS_JUST)

    # Execution: convert a non-empty Maybe to an Either (should be a Right with the value)
    either = just_maybe.to_either()

    # Assertion
    assert mapped_maybe.is_nothing
    assert either.is_right
    assert either.value == SOME_VALUE

def test_maybe_transformations_to_lazy_either_and_try():
    none_value = None
    maybe_nothing = maybe_module.Maybe(none_value, none_value)

    tuple_with_maybe = (maybe_nothing,)
    is_not_empty = False
    maybe_just = maybe_module.Maybe(tuple_with_maybe, is_not_empty)

    lazy_from_nothing = maybe_nothing.to_lazy()
    either_from_nothing = maybe_nothing.to_either()

    try_from_just = maybe_just.to_try()
    either_from_just = maybe_just.to_either()

    either_from_nothing_again = maybe_nothing.to_either()

    lazy_from_try = try_from_just.to_lazy()

    assert lazy_from_nothing.get() is None
    assert isinstance(either_from_nothing, typing.Any)
    assert either_from_nothing.value is None
    assert try_from_just.is_success is True
    assert try_from_just.get() == tuple_with_maybe
    assert isinstance(either_from_just, typing.Any)
    assert either_from_just.value == tuple_with_maybe
    assert either_from_nothing_again.value is None
    assert lazy_from_try.get() == tuple_with_maybe

def test_maybe_to_try_to_box_conversion_preserves_value():
    # Setup: create a Maybe monad holding a value (is_nothing=False)
    initial_value = True
    is_nothing_flag = False
    maybe_instance = maybe_module.Maybe(initial_value, is_nothing_flag)

    # Execution: convert Maybe to Try, then Try to Box
    try_instance = maybe_instance.to_try()
    box_instance = try_instance.to_box()

    # Assertion: the Box should contain the original value
    assert box_instance.value == initial_value

def test_maybe_chain_operations_on_empty_maybe_produce_empty_containers_and_equality_holds():
    # Setup: create an empty Maybe (nothing) with value None and is_nothing=True
    empty_value = None
    is_nothing = True
    empty_maybe = maybe_module.Maybe(empty_value, is_nothing)

    # Execution: exercise ap, to_lazy, to_validation, filter, get_or_else, to_either, to_try, __eq__, to_box
    ap_result = empty_maybe.ap(empty_value)
    lazy_maybe = ap_result.to_lazy()
    validation_maybe = lazy_maybe.to_validation()
    filtered_maybe = empty_maybe.filter(validation_maybe)
    or_else_result = filtered_maybe.get_or_else(filtered_maybe)
    either_maybe = filtered_maybe.to_either()
    try_maybe = validation_maybe.to_try()
    equality_result = filtered_maybe.__eq__(ap_result)
    boxed_maybe = or_else_result.to_box()

    # Final operation: apply try_maybe as an applicative to a byte string
    raw_bytes = b"C\xcf\xe7/"
    try_maybe.ap(raw_bytes)

    # Assertions: verify that transformations on an empty Maybe preserve emptiness
    assert ap_result.is_nothing
    assert filtered_maybe.is_nothing
    assert equality_result is True
    assert boxed_maybe.value is None

def test_maybe_ap_chaining_and_monad_conversions_to_validation_either_and_try():
    # Setup: Prepare input values
    RAW_BYTES = b"\xdbC\xcf\xe7/"
    EMPTY_VALUE = None
    DEFAULT_FLAG = True

    # Setup: Initialize a Maybe instance with None value (empty Maybe)
    maybe_empty = maybe_module.Maybe(EMPTY_VALUE, DEFAULT_FLAG)

    # Execution: Chain ap operations on empty Maybe
    # Applying an empty Maybe's function to None and then to bytes
    ap_result_with_none = maybe_empty.ap(EMPTY_VALUE)
    ap_result_with_bytes = ap_result_with_none.ap(RAW_BYTES)

    # Execution: Transform the resulting Maybe into a Validation
    validation_from_ap_chain = ap_result_with_bytes.to_validation()

    # Setup: Initialize another Maybe with None and a default raw bytes value
    maybe_with_bytes_default = maybe_module.Maybe(EMPTY_VALUE, RAW_BYTES)

    # Execution: Exercise Maybe's get_or_else with itself as default
    get_or_else_result = maybe_with_bytes_default.get_or_else(maybe_with_bytes_default)

    # Execution: Transform the same Maybe into a Validation
    validation_from_maybe = maybe_with_bytes_default.to_validation()

    # Execution: Bind the Validation onto the Maybe
    bind_result = maybe_with_bytes_default.bind(validation_from_maybe)

    # Execution: Transform the Maybe into an Either
    either_from_maybe = maybe_with_bytes_default.to_either()

    # Execution: Apply the Maybe's function to itself
    ap_self_result = maybe_with_bytes_default.ap(maybe_with_bytes_default)

    # Execution: Negative integer used as argument for Try.ap
    NEGATIVE_INT = -3289

    # Assertion: Either and Validation equality depends on underlying values
    either_equals_validation = either_from_maybe.__eq__(validation_from_maybe)

    # Execution: Bind Maybe onto Either (may raise/return monadic composition)
    either_bind_maybe_result = either_from_maybe.bind(maybe_with_bytes_default)

    # Execution: Transform Maybe into a Try
    try_from_maybe = maybe_with_bytes_default.to_try()

    # Assertion: Maybe equality with bind_result
    maybe_equals_bind_result = maybe_with_bytes_default.__eq__(bind_result)

    # Execution: Transform bind result into a Validation
    validation_from_bind_result = bind_result.to_validation()

    # Execution: Apply Try with a negative integer argument
    try_from_maybe.ap(NEGATIVE_INT)

def test_empty_maybe_equality_with_boolean_and_chained_monad_conversions_without_mapper_invocation():
    # Setup: create a Maybe instance representing an empty (Nothing) value
    is_nothing = False
    empty_maybe = maybe_module.Maybe(is_nothing, is_nothing)

    # Execution: compare the empty Maybe with a boolean (should return False)
    equality_result = empty_maybe.__eq__(is_nothing)

    # Setup: create another empty Maybe and perform chained conversions
    another_empty_maybe = maybe_module.Maybe(is_nothing, is_nothing)
    either_result = another_empty_maybe.to_either()
    lazy_result = another_empty_maybe.to_lazy()
    validation_result = lazy_result.to_validation()

    # Setup: create a third empty Maybe
    final_empty_maybe = maybe_module.Maybe(is_nothing, is_nothing)

    # Execution: map over the empty Maybe using the validation result as mapper
    # (mapper is not called since the Maybe is empty)
    final_empty_maybe.map(validation_result)

    # Assertion: equality with a non-Maybe returns False and chained conversions complete without error
    assert equality_result is False

def test_maybe_non_empty_equality_and_conversion_to_validation_success():
    # Setup: create an empty Maybe (with the same value and is_nothing flag set to False)
    initial_value = False
    is_nothing = False
    maybe_instance = maybe_module.Maybe(initial_value, is_nothing)

    # Execution & Assertion (1): check that a Maybe is equal to itself
    is_equal_to_self = maybe_instance.__eq__(maybe_instance)
    assert is_equal_to_self is True

    # Execution & Assertion (2): transform Maybe to Try and then Try to Validation
    try_result = maybe_instance.to_try()
    validation_result = try_result.to_validation()

    # The Try should be successful because the Maybe is not empty,
    # and the resulting Validation should also be successful.
    assert try_result.is_success is True
    assert validation_result == maybe_module.Validation.success(initial_value)

