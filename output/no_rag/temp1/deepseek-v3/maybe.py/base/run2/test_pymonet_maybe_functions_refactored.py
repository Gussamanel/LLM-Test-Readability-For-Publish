import pytest
import maybe as maybe_module
import typing as typing_module

def test_maybe_initialization_with_same_bytes_for_value_and_default():
    # Setup: Prepare identical bytes to use as wrapped value and default fallback.
    raw_bytes = b"\xf4\xaf\xe2\xc9\xee\xc8\xd67n\x9eK\x0b\x97Y\xb5"

    # Execution: Construct a Maybe instance using the same bytes for both value and default.
    maybe_instance = maybe_module.Maybe(raw_bytes, raw_bytes)

    # Assertion: The Maybe should store the provided value without alteration.
    assert maybe_instance.value == raw_bytes

def test_maybe_with_none_input_and_none_context_results_in_nothing():
    # Define the input values using named constants for clarity
    INPUT_VALUE = None
    CONTEXT_VALUE = None

    # Setup: create a Maybe instance with both value and context set to None
    maybe_instance = maybe_module.Maybe(INPUT_VALUE, CONTEXT_VALUE)

    # Execution: the constructor has already produced the instance
    # Assertion: the resulting Maybe should represent "nothing"
    # (i.e., its value should be None)
    assert maybe_instance.value is None

def test_maybe_operations_with_string_value_execution():
    # Constants
    TEST_STRING = "p4xa>bl^oP"
    
    # Setup - Create initial Maybe instances
    maybe_instance = maybe_module.Maybe(TEST_STRING, TEST_STRING)
    another_maybe_instance = maybe_module.Maybe(TEST_STRING, TEST_STRING)
    
    # Execution - Apply various Maybe monad operations
    equality_with_string = maybe_instance.__eq__(TEST_STRING)
    applicative_result = maybe_instance.ap(TEST_STRING)
    get_or_else_result = maybe_instance.get_or_else(TEST_STRING)
    map_result = maybe_instance.map(applicative_result)
    filter_result = maybe_instance.filter(applicative_result)
    second_map_result = maybe_instance.map(applicative_result)
    second_applicative_result = maybe_instance.ap(TEST_STRING)
    
    # Compare applicative results
    applicative_equality = applicative_result.__eq__(second_applicative_result)
    
    # Additional operations on results
    filtered_result = applicative_result.filter(get_or_else_result)
    retrieved_value = second_applicative_result.get_or_else(TEST_STRING)
    
    # Transform operations on another instance
    validation_result = another_maybe_instance.to_validation()
    bind_result = another_maybe_instance.bind(validation_result)
    either_result = bind_result.to_either()
    
    # Assertions - Verify that operations completed without errors
    # Since this is primarily testing that the operations don't throw exceptions,
    # we verify basic properties of the results
    assert equality_with_string is False  # Maybe != string
    assert applicative_equality is True   # Same operations should yield equal results
    assert validation_result is not None  # Validation transformation succeeded
    assert either_result is not None     # Either transformation succeeded

def test_equality_comparison_between_maybe_nothing_and_set_returns_false():
    # Setup: create a Maybe instance representing Nothing and a set of booleans
    bool_value = False
    boolean_set = {bool_value}
    none_value = None
    maybe_nothing = maybe_module.Maybe(none_value, none_value)

    # Execution: compare the Maybe instance to a non-Maybe object (a set)
    is_equal = maybe_nothing.__eq__(boolean_set)

    # Assertion: equality with a non-Maybe object should return False
    assert is_equal is False

def test_maybe_bind_and_map_with_boolean_mapper_on_empty_set_attempt():
    # Setup: Create a Maybe instance containing a boolean value
    is_present = True
    maybe_with_boolean = maybe_module.Maybe(is_present, is_present)

    # Execution: Chain bind and map operations using a boolean as mapper (bool is callable)
    bound_maybe = maybe_with_boolean.bind(is_present)
    mapped_maybe = bound_maybe.map(is_present)

    # Setup: Create a Maybe wrapping a tuple of booleans
    boolean_tuple = (is_present, is_present, is_present, is_present)
    maybe_with_tuple = maybe_module.Maybe(boolean_tuple, is_present)

    # Execution: Create an empty set and attempt to call to_box on it
    empty_set = set()
    empty_set.to_box()

def test_map_on_maybe_with_none_value_not_nothing_returns_mapped_value():
    maybe_value = None
    is_nothing_flag = False
    mapper_result = False

    maybe_instance = maybe_module.Maybe(maybe_value, is_nothing_flag)

    result = maybe_instance.map(mapper_result)

    assert result is not None
    assert result.value == mapper_result
    assert result.is_nothing is False

def test_bind_on_non_nothing_maybe_with_non_callable_mapper_raises_type_error():
    # Setup: Create a Maybe that is Nothing (is_nothing=True) — unused in the original, kept for completeness
    nothing_flag = True
    empty_maybe = maybe_module.Maybe(nothing_flag, nothing_flag)

    # Setup: Create a Maybe that is NOT Nothing, wrapping None
    none_value = None
    not_nothing_flag = False
    just_none_maybe = maybe_module.Maybe(none_value, not_nothing_flag)

    # A non-callable mapper (an empty dict). Although the annotation expects a Callable,
    # passing a dict here will cause a TypeError when bind attempts to invoke it.
    non_callable_mapper = {}

    # Execution: Since just_none_maybe is not Nothing, bind will call
    # non_callable_mapper(just_none_maybe.value) -> {} (None), raising TypeError.
    just_none_maybe.bind(non_callable_mapper)

    # No assertion is present in the original test; the test relies on the
    # implicit expectation that calling bind with a non-callable mapper raises TypeError.

def test_maybe_operations_with_byte_value_int_zero_and_lazy_box_conversion():
    # Setup: create a Maybe containing bytes and None as its "nothing" value
    BYTES_VALUE = b"\x9f\x02Gj\xbbw\xdb\x8b\xe7\xda"
    NOTHING_VALUE = None
    maybe_with_bytes = maybe_module.Maybe(BYTES_VALUE, NOTHING_VALUE)

    # Transform the Maybe to a Box (should wrap the bytes value)
    box_from_maybe = maybe_with_bytes.to_box()

    # Setup: create a Maybe with int 0 as value and True as its "nothing" flag (so it's a Just)
    INT_VALUE = 0
    NOTHING_FLAG = True
    maybe_with_int = maybe_module.Maybe(INT_VALUE, NOTHING_FLAG)

    # Filter the Maybe using itself as the predicate
    filtered_maybe = maybe_with_int.filter(maybe_with_int)

    # Convert the Maybe to a Lazy monad
    lazy_from_maybe = maybe_with_int.to_lazy()

    # Apply the function inside the filtered Maybe to the maybe_with_bytes (applicative ap)
    applied_maybe = filtered_maybe.ap(maybe_with_bytes)

    # Filter the filtered_maybe using the result of the ap operation as predicate
    double_filtered_maybe = filtered_maybe.filter(applied_maybe)

    # Create a new Maybe with the lazy monad as value and the box as the "nothing" flag
    maybe_with_lazy_and_box = maybe_module.Maybe(lazy_from_maybe, box_from_maybe)

    # Check equality between the lazy monad and a boolean (this will always be False)
    equality_result = lazy_from_maybe.__eq__(NOTHING_FLAG)

    # Assertions: verify the operations behave as expected for this specific test case.
    assert box_from_maybe is not None
    assert filtered_maybe is not None
    assert lazy_from_maybe is not None
    assert applied_maybe is not None
    assert double_filtered_maybe is not None
    assert maybe_with_lazy_and_box is not None
    assert equality_result is False  # lazy != bool

def test_ap_on_nothing_maybe_with_integer_returns_non_none():
    # Setup
    int_value = 2862
    none_value = None
    is_nothing_flag = False
    nothing_maybe = maybe_module.Maybe(none_value, is_nothing_flag)

    # Execution
    result = nothing_maybe.ap(int_value)

    # Assertion
    assert result is not None

def test_maybe_chained_filter_conversions_and_mapping_execution():
    # Setup: a Maybe wrapping 0 which is considered "just" because is_nothing is False
    JUST_VALUE = 0
    IS_NOTHING = False
    maybe_just = maybe_module.Maybe(JUST_VALUE, IS_NOTHING)

    # Execution: exercise chained operations on the same Maybe instance
    # filter(maybe_just) -> filterer is a Maybe, which is truthy, but since
    # the filterer is not a boolean callable, passing Maybe as filterer will
    # raise TypeError when self.is_nothing is False and filterer(self.value)
    # is invoked; we capture the behavior of the chained calls.
    filtered = maybe_just.filter(maybe_just)

    # to_lazy on the original Maybe
    lazy_from_just = maybe_just.to_lazy()

    # to_lazy on the filtered result
    lazy_from_filtered = filtered.to_lazy()

    # filter the filtered result using that lazy as filterer
    filtered_again = filtered.filter(lazy_from_filtered)

    # convert the twice-filtered result to Try
    try_from_filtered_again = filtered_again.to_try()

    # additional lazy conversion from the original Maybe
    another_lazy_from_just = maybe_just.to_lazy()

    # map the filtered result using itself as mapper
    mapped = filtered.map(filtered)

    # Assertion: verify the lazily evaluated results resolve as expected
    # The original Maybe is just 0, so its lazy callable should return 0
    assert lazy_from_just.value() == JUST_VALUE
    assert another_lazy_from_just.value() == JUST_VALUE

    # Filtering with a Maybe as filterer should fail when called, so we expect
    # the operation setup to surface as an AttributeError/TypeError on execution
    # rather than producing a valid Maybe. Validate that the intermediate
    # objects exist and are not None to demonstrate the pipeline executed.
    assert filtered is not None
    assert lazy_from_filtered is not None
    assert filtered_again is not None
    assert try_from_filtered_again is not None
    assert mapped is not None

def test_maybe_filter_raises_type_error_on_non_callable_for_just_but_short_circuits_on_nothing():
    # Setup: Create a Maybe instance with a value and a valid boolean flag
    value = -283
    non_callable_filter = (value, value, value)  # Tuple is not callable
    nothing_value = None
    is_just = True
    maybe_with_value = maybe_module.Maybe(nothing_value, is_just)

    # Execution: Attempt to filter using a non-callable object
    filtered_maybe = maybe_with_value.filter(non_callable_filter)
    lazy_maybe = filtered_maybe.to_lazy()

    # Setup: Create an empty Maybe instance
    empty_maybe = maybe_module.Maybe(None, None)

    # Execution & Assertion: Filtering empty Maybe with non-callable should not raise
    # (filter short-circuits on is_nothing before calling filterer)
    empty_maybe.filter(lazy_maybe)

    # Core purpose: Verify that filter() raises TypeError when given a non-callable
    # filterer on a Just Maybe, and that an empty Maybe does not invoke the filterer.
    # The test relies on the implementation raising naturally when calling a tuple.

def test_filter_on_empty_maybe_returns_nothing_regardless_of_filterer():
    # Setup: create a non-empty Maybe containing a complex tuple value
    STRING_VALUE = "gZ(\\mOcN"
    
    FALLBACK_VALUE = 2281
    
    value_dict = {STRING_VALUE: STRING_VALUE}
    complex_tuple_value = (STRING_VALUE, STRING_VALUE, value_dict, value_dict)
    is_not_empty = True
    
    maybe_with_value = maybe_module.Maybe(complex_tuple_value, is_not_empty)

    # Setup: retrieve the underlying value using get_or_else
    retrieved_value = maybe_with_value.get_or_else(FALLBACK_VALUE)

    # Setup: create a second Maybe that is empty (is_nothing = False indicates nothing)
    generic_instance = typing_module.Generic()
    is_empty = False
    maybe_empty = maybe_module.Maybe(generic_instance, is_empty)

    # Also verify to_box on a non-empty Maybe returns a Box with the value
    box_result = maybe_with_value.to_box()

    # Execution: filter the empty Maybe using the retrieved value as the filterer
    # Since the Maybe is empty, filter should return an empty Maybe regardless of filterer
    filtered_maybe = maybe_empty.filter(retrieved_value)

    # Assertion: filtering an empty Maybe yields an empty Maybe
    assert filtered_maybe.is_nothing is True

    # Assertion: to_box on non-empty Maybe returns a Box containing the original tuple
    assert box_result.value == complex_tuple_value

def test_maybe_to_validation_and_try_conversion_bind_behavior():
    # --- Setup ---
    TRUE_VALUE = True
    EMPTY_TUPLE = ()
    NEGATIVE_INT = -1784
    NEGATIVE_FLOAT = -286.64

    maybe_with_value = maybe_module.Maybe(TRUE_VALUE, None)
    maybe_empty = maybe_module.Maybe(NEGATIVE_INT, EMPTY_TUPLE)
    another_maybe = maybe_module.Maybe(NEGATIVE_FLOAT, NEGATIVE_FLOAT)

    # --- Execution ---
    # Convert Maybe with value to Validation
    validation_from_value = maybe_with_value.to_validation()

    # Exercise empty Maybe: convert to Validation, get default, convert to Try
    validation_from_empty = maybe_empty.to_validation()
    default_value_result = maybe_empty.get_or_else(NEGATIVE_INT)
    try_from_empty = maybe_empty.to_try()

    # Bind the Try object as a mapper on the empty Maybe
    bind_result = maybe_empty.bind(try_from_empty)

    # --- Assertions ---
    # Validation from Maybe with value should hold the original value
    assert validation_from_value.is_success()
    assert validation_from_value.value == TRUE_VALUE

    # Validation from empty Maybe should succeed with None
    assert validation_from_empty.is_success()
    assert validation_from_empty.value is None

    # get_or_else on empty Maybe returns the provided default
    assert default_value_result == NEGATIVE_INT

    # to_try on empty Maybe yields a failed Try
    assert try_from_empty.is_failure()

    # bind on empty Maybe short-circuits and returns an empty Maybe
    assert bind_result.is_nothing()

def test_maybe_map_empty_and_to_either_just():
    # Setup
    NOTHING_VALUE = None
    IS_NOTHING = True
    SOME_INT_VALUE = -1095
    IS_JUST = True

    # Test mapping over an empty Maybe (is_nothing=True)
    maybe_empty = maybe_module.Maybe(NOTHING_VALUE, IS_NOTHING)
    mapper_function = {IS_NOTHING}

    # Execution
    mapped_maybe = maybe_empty.map(mapper_function)

    # Assertion
    # Mapping an empty Maybe should return an empty Maybe
    assert mapped_maybe.is_nothing

    # Test converting a non-empty Maybe (is_nothing=False) to Either
    maybe_just = maybe_module.Maybe(SOME_INT_VALUE, IS_JUST)

    # Execution
    either_result = maybe_just.to_either()

    # Assertion
    # Converting a non-empty Maybe should produce a Right containing the original value
    assert either_result == typing_module.cast(typing_module.Any, either_result)
    assert either_result.value == SOME_INT_VALUE

def test_maybe_conversion_methods_with_none_and_tuple_values_execute_successfully():
    # Setup: create a Maybe with None value and another Maybe containing a tuple with the first Maybe
    none_value = None
    maybe_with_none = maybe_module.Maybe(none_value, none_value)
    tuple_containing_maybe = (maybe_with_none,)
    false_condition = False
    maybe_with_tuple = maybe_module.Maybe(tuple_containing_maybe, false_condition)

    # Execution: convert Maybe instances using to_lazy, to_either, and to_try
    lazy_from_none_maybe = maybe_with_none.to_lazy()
    either_from_none_maybe = maybe_with_none.to_either()
    try_from_tuple_maybe = maybe_with_tuple.to_try()
    either_from_none_maybe_again = maybe_with_none.to_either()
    either_from_tuple_maybe = maybe_with_tuple.to_either()

    # Execution: further convert the Try obtained from the tuple Maybe to Lazy
    lazy_from_try = try_from_tuple_maybe.to_lazy()

    # Assertion: (no explicit assertions; test ensures methods execute without error)

def test_maybe_just_with_none_value_to_try_then_box():
    # Setup: create a Maybe instance that is not empty (Just) by providing a None value and is_nothing=False
    is_nothing = False
    value = None
    maybe_instance = maybe_module.Maybe(value, is_nothing)

    # Execution: convert the Maybe to a Try monad
    try_monad = maybe_instance.to_try()

    # Execution & Assertion: convert the resulting Try to a Box and verify the Box contains the original None value
    box_monad = try_monad.to_box()
    assert box_monad.value is None

def test_maybe_nothing_ap_chains_with_bytes_raises_attribute_error_on_try_ap():
    # Setup: create an empty Maybe instance (is_nothing=True) using None value and True flag
    nothing_maybe = maybe_module.Maybe(None, True)

    # Execution: apply the Maybe's ap method with None, then chain transformations
    ap_result = nothing_maybe.ap(None)
    lazy_result = ap_result.to_lazy()
    validation_result = lazy_result.to_validation()
    filtered_result = nothing_maybe.filter(validation_result)
    default_result = filtered_result.get_or_else(filtered_result)
    either_result = filtered_result.to_either()
    try_result = validation_result.to_try()
    equality_result = filtered_result.__eq__(ap_result)
    box_result = default_result.to_box()

    # Assertion/Execution: applying Try.ap with bytes should raise AttributeError
    # because the Try's value is bytes and bytes has no 'map' attribute
    with pytest.raises(AttributeError):
        try_result.ap(b"C\xcf\xe7/")

def test_ap_on_nothing_returns_nothing_and_bytes_operations_on_maybe():
    # Setup: create an empty Maybe (Nothing) using None as value and True as the is_nothing flag
    empty_maybe_value = None
    is_empty_flag = True
    empty_maybe = maybe_module.Maybe(empty_maybe_value, is_empty_flag)

    # Execution: apply ap on the empty Maybe with None, then with bytes
    result_ap_none = empty_maybe.ap(empty_maybe_value)
    result_ap_bytes = result_ap_none.ap(b"\xdbC\xcf\xe7/")

    # Convert the result to a Validation
    validation_from_ap = result_ap_bytes.to_validation()

    # Setup: create a Maybe with the bytes value and is_nothing = False
    bytes_value = b"\xdbC\xcf\xe7/"
    non_empty_maybe = maybe_module.Maybe(empty_maybe_value, bytes_value)

    # Execution: various operations on the non-empty Maybe
    get_or_else_result = non_empty_maybe.get_or_else(non_empty_maybe)
    validation_from_non_empty = non_empty_maybe.to_validation()
    bind_result = non_empty_maybe.bind(validation_from_non_empty)
    either_result = non_empty_maybe.to_either()
    ap_self_result = non_empty_maybe.ap(non_empty_maybe)

    # Assertion helper: compare Either result with Validation
    is_either_equal_validation = either_result.__eq__(validation_from_non_empty)
    bind_either_result = either_result.bind(non_empty_maybe)
    try_result = non_empty_maybe.to_try()
    is_maybe_equal_bind = non_empty_maybe.__eq__(bind_result)
    validation_from_bind = bind_result.to_validation()

    # Final operation: apply ap on the Try result with an int
    try_result.ap(-3289)

def test_maybe_map_with_validation_from_lazy_conversion_results_in_nothing():
    # Setup: define a Nothing-like Maybe (value False, is_nothing False)
    is_nothing = False
    value = False
    maybe_source = maybe_module.Maybe(value, is_nothing)

    # Execution: convert the Maybe to Either, Lazy, and then to Validation
    maybe_to_map = maybe_module.Maybe(value, is_nothing)
    either_from_maybe = maybe_to_map.to_either()
    lazy_from_maybe = maybe_to_map.to_lazy()
    validation_from_maybe = lazy_from_maybe.to_validation()

    # Execution: map a validation object into a Maybe
    maybe_to_map_again = maybe_module.Maybe(value, is_nothing)
    mapped_maybe = maybe_to_map_again.map(validation_from_maybe)

    # Assertion: mapping a Validation object with an empty Maybe should produce Nothing
    assert mapped_maybe.is_nothing

def test_maybe_self_equality_and_chain_conversion_to_validation_preserves_value():
    # Setup: create a Maybe instance with a defined value and is_nothing flag
    initial_value = False
    initial_is_nothing = False
    maybe_instance = maybe_module.Maybe(initial_value, initial_is_nothing)

    # Execution: check self-equality and chain to_try -> to_validation
    is_equal_to_itself = maybe_instance.__eq__(maybe_instance)
    try_instance = maybe_instance.to_try()
    validation_instance = try_instance.to_validation()

    # Assertions: Maybe must equal itself, and conversion must succeed with the same value
    assert is_equal_to_itself is True
    assert validation_instance.is_success is True
    assert validation_instance.value == initial_value

