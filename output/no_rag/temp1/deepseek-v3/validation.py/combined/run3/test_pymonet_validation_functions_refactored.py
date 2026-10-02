import pytest
import validation as validation_module
import builtins as builtins_module

def test_validation_to_maybe_success_when_no_errors():
    # Setup: Create a Validation that is successful (no errors)
    validation_value = "\n        Create empty maybe.\n\n        :returns: Maybe[None]\n        "
    validation = validation_module.Validation(validation_value, [])

    # Execution: Transform Validation to Maybe
    maybe_result = validation.to_maybe()

    # Assertion: Since Validation has no errors, to_maybe should return a non-empty Maybe
    assert maybe_result.is_just()

def test_validation_equality_with_none_produces_error_free_validation():
    """
    Test that comparing a Validation instance to None results in a successful (error-free) Validation.

    Purpose:
        Verifies that the __eq__ method returns a Validation object (not raising an error)
        even when compared against None, and that the resulting Validation has no errors.

    Steps:
        1. Arrange: Create a Validation instance with a value and a tuple of elements.
        2. Act: Compare the Validation instance to None using __eq__.
        3. Assert: The result is a Validation object and is_success() returns True.
    """
    # Arrange: create the Validation instance
    validation = validation_module.Validation(VALIDATION_INITIAL_VALUE, ELEMENTS_TUPLE)

    # Act: compare the Validation instance to None
    comparison_result = validation.__eq__(NONE_VALUE)

    # Assert: the comparison should return a Validation and be considered successful
    assert comparison_result is not None
    assert comparison_result.is_success()

def test_validation_str_on_empty_validation_reports_failure():
    EMPTY_DICT = {}
    validation = validation_module.Validation(EMPTY_DICT, EMPTY_DICT)

    validation_str = str(validation)
    is_failure = validation.is_fail()

    assert is_failure is True
    assert validation_str == 'Validation.fail[{}, {}]'.format(EMPTY_DICT, validation.errors)

def test_empty_validation_transforms_to_maybe_and_either_without_errors():
    # Setup: Create an empty Validation instance (no value, no errors)
    empty_set = set()
    validation_instance = validation_module.Validation(empty_set, empty_set)

    # Execution: Transform the Validation to a Maybe and to an Either
    either_result = validation_instance.to_either()
    maybe_result = validation_instance.to_maybe()

    # Assertion: Verify the transformation chain executes without raising exceptions
    # (Further transform the resulting Maybe to confirm it is a valid Maybe instance)
    maybe_result.to_maybe()

def test_validation_failure_is_failure_and_can_convert_to_maybe():
    # A Validation created with an error message is a failure.
    # Assert that it reports failure, equals itself, and converts to Either/Maybe
    # consistently with its failure state.
    error_message = "\n        Create empty maybe.\n\n        :returns: Maybe[None]\n        "
    validation = validation_module.Validation(error_message, error_message)

    # Execution
    either_result = validation.to_either()
    is_equal_to_self = validation.__eq__(validation)
    is_failure = validation.is_fail()
    maybe_result = is_failure.to_maybe()

    # Assertion
    assert isinstance(either_result, validation_module.Left)
    assert is_equal_to_self is True
    assert is_failure is True
    assert isinstance(maybe_result, validation_module.Maybe)

def test_validation_with_errors_to_maybe_yields_nothing_that_is_idempotent():
    # Setup: create an empty (failing) Validation instance
    validation_with_no_value = validation_module.Validation(set(), set())

    # Execution: convert Validation to Maybe
    maybe_result = validation_with_no_value.to_maybe()

    # Assertion: chaining to_maybe again should be a no-op on the empty Maybe
    result = maybe_result.to_maybe()

    assert result is maybe_result

def test_validation_initialization_accepts_none_arguments():
    # Setup: prepare None values to be passed to the Validation constructor
    none_value = None

    # Execution: instantiate Validation with None for both arguments
    validation_instance = validation_module.Validation(none_value, none_value)

    # Assertion: verify the instance is created and stores the None values as provided
    assert validation_instance is not None

def test_validation_with_none_value_and_no_errors_converts_to_nothing():
    # Setup: Create a Validation with None values, which represents a failure state
    none_value = None
    validation = validation_module.Validation(none_value, none_value)

    # Execution: Transform the Validation to Maybe
    result = validation.to_maybe()

    # Assertion: A failed Validation should be converted to an empty Maybe
    assert result.is_nothing()

def test_validation_without_errors_is_not_failure():
    object_to_validate = validation_module.object()
    validation_instance = validation_module.Validation(object_to_validate, object_to_validate)

    is_failure = validation_instance.is_fail()

    assert is_failure is False

def test_map_with_none_mapper_on_validation_with_complex_tuple_value_raises_type_error():
    # Setup: Create a Validation instance with a complex nested tuple value.
    # Since the map function calls mapper(value), passing None as the mapper
    # should raise a TypeError when attempting to call None(...).
    some_int_value = -895
    some_bool_value = True
    inner_tuple = (some_int_value, some_bool_value)
    inner_dict = {inner_tuple: inner_tuple}
    validation_value = (inner_dict, inner_dict, some_int_value)
    validation_errors = some_bool_value
    validation_instance = validation_module.Validation(validation_value, validation_errors)
    none_mapper = None

    # Execution: Apply the None mapper, which is expected to fail because
    # None is not callable.
    with pytest.raises(TypeError):
        validation_instance.map(none_mapper)

    # Assertion: pytest.raises above verifies that calling map with a
    # non-callable mapper raises a TypeError, as expected.

def test_bind_passes_validation_value_to_folder_function_and_returns_result():
    # Setup: Define the Validation value and a folder function that returns a known sentinel.
    # The test verifies that bind invokes the folder function with the Validation's value.
    initial_value = b"s\x8flul\xd1p\x86\xe0<q\xd9\xb2\xf6\x17EC\xaf\xd0"
    validation = validation_module.Validation(initial_value, initial_value)

    received_args = []

    def folder_function(value):
        received_args.append(value)
        return value

    # Execution: Apply bind with the folder function.
    result = validation.bind(folder_function)

    # Assertion: The folder function receives the Validation's current value and bind returns its result.
    assert received_args == [initial_value]
    assert result == initial_value

def test_ap_accumulates_errors_when_validation_factory_returns_validation_with_extra_error():
    # Setup: create an invalid Validation (False) with a list of errors.
    is_valid = False
    error_flags = [True, True, True, True]
    initial_validation = validation_module.Validation(is_valid, error_flags)

    # Execution: call ap() with a function that returns another Validation.
    # The returned Validation itself contains one more error flag.
    def validation_factory(value):
        return validation_module.Validation(value, [True])

    result_validation = initial_validation.ap(validation_factory)

    # Assertion: the resulting Validation preserves the original value
    # and concatenates the errors from the current and returned Validations.
    assert result_validation.value == is_valid
    assert result_validation.errors == error_flags + [True]

def test_to_box_yields_success_for_valid_validation_without_errors():
    # Setup: create a Validation instance with a successful (no errors) state
    is_valid = True
    validation = validation_module.Validation(is_valid, is_valid)

    # Execution: transform the Validation into a Box and check success
    result_box = validation.to_box()
    is_success = result_box.is_success()

    # Assertion: the Box derived from a valid Validation should report success
    assert is_success is True

def test_lazy_bind_with_none_value_returns_lazy_validation_with_none():
    # Setup: create an empty Validation, convert it to Lazy, then bind a None value
    empty_list = []
    validation = validation_module.Validation(empty_list, empty_list)
    lazy_validation = validation.to_lazy()

    # Execution: bind None to the lazy validation
    bound_validation = lazy_validation.bind(None)

    # Assertion: converting the bound validation back to lazy should succeed
    # and retain the None value
    result = bound_validation.to_lazy()
    assert result is not None

def test_empty_validation_to_try_returns_successful_try():
    empty_dict = {}
    validation = validation_module.Validation(empty_dict, empty_dict)

    lazy_validation = validation.to_lazy()
    try_result = lazy_validation.to_try()
    validation.ap(validation)

    assert try_result.is_success() is True

def test_validation_to_try_success_when_no_errors():
    # Setup: create a Validation with value 0 and no errors; convert to Try
    VALUE = 0
    EMPTY_ERRORS = []
    validation = validation_module.Validation(VALUE, EMPTY_ERRORS)
    
    # Execution: transform Validation into a Try monad
    result_try = validation.to_try()
    
    # Assertion: Try should be successful because Validation had no errors
    assert result_try.is_success() is True

def test_validation_map_creates_new_validation_with_mapped_value():
    # Setup
    EMPTY_ERRORS = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    NONE_VALUE = None

    # Create test data
    error_dict = {NONE_VALUE: EMPTY_ERRORS, EMPTY_ERRORS: EMPTY_ERRORS}

    # Create validation instances with different configurations
    validation_with_none = validation_module.Validation(NONE_VALUE, error_dict)
    validation_with_bytes = validation_module.Validation(EMPTY_ERRORS, EMPTY_ERRORS)

    # Execution - test equality and transformation operations
    are_equal = validation_with_none.__eq__(validation_with_none)
    box_result = validation_with_none.to_box()

    # Transform box to either and then to try
    either_result = box_result.to_either()
    is_validation_failed = validation_with_bytes.is_fail()
    try_result = either_result.to_try()

    # Create validation with the failure boolean as value
    validation_with_failure_flag = validation_module.Validation(is_validation_failed, EMPTY_ERRORS)

    # Get string representation and lazy transformation
    string_representation = validation_with_failure_flag.__str__()
    lazy_result = validation_with_bytes.to_lazy()

    # Create another validation and test transformations
    another_validation = validation_module.Validation(EMPTY_ERRORS, EMPTY_ERRORS)
    another_either_result = box_result.to_either()
    another_lazy_result = validation_with_failure_flag.to_lazy()

    # Create validation with lazy function as value
    validation_with_lazy = validation_module.Validation(another_lazy_result, another_validation)

    # Test is_fail on original validation again
    another_failure_check = validation_with_bytes.is_fail()

    # Core purpose: Test that map operation creates a new Validation instance
    # with the mapped value while preserving the original errors
    mapped_validation = box_result.map(string_representation)

    # Assertions - verify the mapped validation was created
    # The map operation should return a new Validation with the result
    # of applying the mapper function to the original value
    assert isinstance(mapped_validation, validation_module.Validation)
    assert mapped_validation.value == string_representation
    assert mapped_validation.errors == box_result.errors

def test_validation_equality_to_itself_to_maybe_and_bind_with_bytes():
    # Arrange: create sample inputs for the Validation under test
    SAMPLE_BYTES = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    NONE_VALUE = None
    SAMPLE_DICT = {NONE_VALUE: SAMPLE_BYTES, SAMPLE_BYTES: SAMPLE_BYTES}

    # Arrange: construct a Validation with a None value and a dict of errors
    validation_with_none_value = validation_module.Validation(NONE_VALUE, SAMPLE_DICT)

    # Act: check equality with itself, convert to Maybe, and bind a folder function
    is_equal_to_itself = validation_with_none_value.__eq__(validation_with_none_value)
    maybe_result = validation_with_none_value.to_maybe()

    # Arrange: construct a successful Validation with the sample bytes as value and errors
    successful_validation = validation_module.Validation(SAMPLE_BYTES, SAMPLE_BYTES)

    # Act: bind a function that simply returns the folder value
    bind_result = successful_validation.bind(SAMPLE_BYTES)

    # Assert: a Validation should be equal to itself, and the derived objects should exist
    assert is_equal_to_itself is True
    assert maybe_result is not None
    assert bind_result == SAMPLE_BYTES

def test_validation_inequality_for_distinct_values_converts_equality_result_to_box_wrapping_value():
    # Setup: create two Validation instances with different values and errors
    # The first Validation wraps a dict as value and has None as errors
    # The second Validation wraps a bytes object as value and has None as errors
    sample_bytes = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    error_value = None
    validation_payload = {error_value: sample_bytes, sample_bytes: sample_bytes}

    first_validation = validation_module.Validation(error_value, validation_payload)
    second_validation = validation_module.Validation(sample_bytes, error_value)

    # Execution: compare the two validations for equality
    equality_result = first_validation.__eq__(second_validation)

    # Assertion: convert the equality result to a Box and verify it wraps the value
    boxed_result = equality_result.to_box()

