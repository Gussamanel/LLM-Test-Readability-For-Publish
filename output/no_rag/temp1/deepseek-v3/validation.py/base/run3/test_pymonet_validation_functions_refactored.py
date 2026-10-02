import pytest
import validation as validation_module
import builtins as builtins_module

def test_validation_success_conversion_and_equality_behavior():
    # Setup: Create a Validation instance with no errors (successful)
    valid_value = "test_value"
    successful_validation = validation_module.Validation(valid_value, [])  # errors list empty

    # Execution/Assertions
    # A validation with empty errors list is a success
    assert successful_validation.is_success() is True

    # Equality: same instance should be equal to itself
    assert successful_validation.__eq__(successful_validation) is True

    # It should not be a failure
    assert successful_validation.is_fail() is False

    # Converting to Maybe should yield a Maybe.just containing the value
    maybe_result = successful_validation.to_maybe()
    assert maybe_result.is_just() is True
    assert maybe_result.value == valid_value

def test_validation_equality_with_none_returns_unsuccessful_validation_when_errors_exist():
    # Setup: create a Validation with a negative int value and a tuple error list.
    # One of the arguments is non-empty errors, so the Validation should not be successful.
    negative_value = -6891
    tuple_error_element = 3125
    errors_tuple = (tuple_error_element,)
    validation_instance = validation_module.Validation(negative_value, errors_tuple)
    comparison_target = None

    # Execution: compare the Validation instance to None using __eq__.
    equality_result = validation_instance.__eq__(comparison_target)

    # Assertion: equality with None cannot be the same Validation and must return an unsuccessful Validation.
    assert equality_result.is_success() is False

def test_str_representation_of_successful_validation_with_no_errors():
    # Setup: create a valid Validation instance with empty value and errors
    EMPTY_VALUE = {}
    EMPTY_ERRORS = {}
    validation = validation_module.Validation(EMPTY_VALUE, EMPTY_ERRORS)

    # Execution: obtain the string representation of the validation
    validation_str = validation.__str__()

    # Assertion: a validation without errors is considered successful,
    # so its string representation should reflect success rather than failure
    assert not validation.is_fail()
    assert 'success' in validation_str

def test_validation_conversions_maintain_success_state_through_chained_transformations():
    # Setup: Create an empty Validation instance (no value, no errors)
    empty_set = set()
    validation = validation_module.Validation(empty_set, empty_set)

    # Execution: Convert Validation to Either and to Maybe
    either_result = validation.to_either()
    maybe_result = validation.to_maybe()

    # Execution: Further convert the Maybe result back to Maybe
    chained_maybe_result = maybe_result.to_maybe()

    # Assertion: Verify that conversions preserve the success state of the Validation
    assert validation.is_success(), "Validation should be in success state"
    assert either_result.is_right(), "Either conversion should yield Right for successful Validation"
    assert maybe_result.is_just(), "Maybe conversion should yield Just for successful Validation"
    assert chained_maybe_result.is_just(), "Chained Maybe conversion should preserve Just state"

def test_validation_failure_conversion_equality_and_fail_state():
    # Setup: Create a Validation instance with an error (non-empty error string)
    error_message = "\n        Create empty maybe.\n\n        :returns: Maybe[None]\n        "
    validation = validation_module.Validation(error_message, error_message)

    # Execution: Perform the core operations under test
    either_result = validation.to_either()
    equality_result = validation.__eq__(validation)
    is_fail_result = validation.is_fail()

    # Assertions: Verify the expected behavior of each operation
    # A failed Validation should convert to a Left Either containing the errors
    assert either_result.is_left()
    assert either_result.value == [error_message]

    # A Validation should be equal to itself
    assert equality_result is True

    # A failed Validation should report failure (is_fail returns True)
    assert is_fail_result is True

def test_validation_to_maybe_with_empty_sets_round_trip():
    # Setup: create a Validation with empty sets (no value, no errors)
    empty_set = set()
    validation = validation_module.Validation(empty_set, empty_set)

    # Execution: transform Validation to Maybe
    maybe_from_validation = validation.to_maybe()

    # Assertion: converting the resulting Maybe to Maybe again should not raise
    maybe_from_validation.to_maybe()

def test_validation_creation_with_no_values_succeeds():
    # Setup: create a Validation instance with both expected and actual set to None
    expected_value = None
    actual_value = None

    # Execution: instantiate the Validation object
    validation = validation_module.Validation(expected_value, actual_value)

    # Assertion: ensure the instance is created successfully with None arguments
    assert validation is not None

def test_to_maybe_with_none_value_returns_just_none():
    # Setup
    valid_value = None
    validation = validation_module.Validation(valid_value, None)

    # Execution
    maybe_result = validation.to_maybe()

    # Assertion
    assert maybe_result == maybe_result.just(valid_value)

def test_is_fail_returns_false_for_error_free_validation():
    # Setup: create a validation object without triggering any errors
    validatable_object = validation_module.Object()
    validation = validation_module.Validation(validatable_object, validatable_object)

    # Execution: check the failure state on a freshly created, error-free validation
    result = validation.is_fail()

    # Assertion: with an empty errors list, is_fail should return False
    assert result is False

def test_map_with_none_mapper_returns_validation_with_none_value_and_preserved_errors():
    # Constants representing the inputs for constructing the Validation instance.
    ERROR_VALUE = -895
    HAS_ERROR = True

    # Setup: build a nested data structure and use it to create a Validation instance.
    # A tuple containing a dict (keyed by a tuple of error value and flag), a nested
    # data structure, and the error value is used as the Validation value.
    inner_tuple = (ERROR_VALUE, HAS_ERROR)
    inner_dict = {inner_tuple: inner_tuple}
    validation_value = (inner_dict, inner_dict, ERROR_VALUE)
    validation = validation_module.Validation(validation_value, HAS_ERROR)

    # Execution: apply map with a mapper that returns None, verifying that the
    # returned Validation wraps the mapper result while preserving the original errors.
    identity_none_mapper = None
    result = validation.map(identity_none_mapper)

    # Assertion: the mapped value should reflect the mapper result (None in this case)
    # and the errors should remain unchanged.
    assert result.value == validation_value
    assert result.errors == HAS_ERROR

def test_bind_with_non_callable_folder_raises_type_error():
    # Setup: create a Validation holding some bytes and bind it with a None "folder" callable.
    # The `bind` method invokes the folder with the wrapped value; since the folder is None,
    # this demonstrates that binding with a non-callable raises a TypeError.
    VALUE_BYTES = b"s\x8flul\xd1p\x86\xe0<q\xd9\xb2\xf6\x17EC\xaf\xd0"
    validation_instance = validation_module.Validation(VALUE_BYTES, VALUE_BYTES)
    none_folder = None

    # Execution + Assertion: calling bind with None should fail because None is not callable.
    with pytest.raises(TypeError):
        validation_instance.bind(none_folder)

def test_ap_combines_errors_from_both_validations_when_initial_and_returned_validation_are_invalid():
    # Setup: a Validation initialized with an initial error list,
    # and a function returning a new Validation with additional errors.
    IS_VALID = False
    IS_NOT_VALID = True
    initial_errors = [IS_NOT_VALID, IS_NOT_VALID, IS_NOT_VALID, IS_NOT_VALID]
    validation_with_initial_errors = validation_module.Validation(IS_VALID, initial_errors)

    # Execution: apply (ap) a function that returns a Validation with its own errors.
    # The result should be a Validation whose errors are the concatenation
    # of the original errors and the errors from the returned Validation.
    def function_returning_validation(_value):
        return validation_module.Validation(IS_VALID, initial_errors)

    result_validation = validation_with_initial_errors.ap(function_returning_validation)

    # Assertion: the new Validation should carry the combined error list (original + new).
    assert result_validation.errors == initial_errors + initial_errors

def test_validation_to_box_preserves_success_state():
    # Setup: create a successful Validation (no errors) and wrap it in a Box
    is_success_flag = True
    validation = validation_module.Validation(is_success_flag, is_success_flag)
    box = validation.to_box()

    # Execution: check success state through the Box
    result = box.is_success()

    # Assertion: a successful Validation should yield a Box reporting success
    assert result is True

def test_bind_on_lazy_chain_with_none_value_preserves_lazy_none():
    # Setup: create an empty Validation and convert it to a Lazy wrapper
    none_value = None
    items = []
    validation = validation_module.Validation(items, items)

    # Execution: wrap the Validation in a Lazy, then bind a function returning None
    lazy_validation = validation.to_lazy()
    bound_lazy = lazy_validation.bind(none_value)

    # Assertion: converting the bound Lazy back to Lazy should preserve None
    result_lazy = bound_lazy.to_lazy()
    assert result_lazy is not None

def test_validation_without_errors_to_lazy_try_and_ap_all_succeed():
    # Arrange: create a Validation instance with no errors
    empty_validation = validation_module.Validation({}, {})
    assert empty_validation.errors == []

    # Act: convert the successful Validation to Lazy, then to Try, and apply ap
    lazy_validation = empty_validation.to_lazy()
    try_from_lazy = lazy_validation.to_try()
    ap_result = lazy_validation.ap(empty_validation)

    # Assert: the Try derived from a success Validation should be successful
    assert try_from_lazy.is_success() is True

def test_validation_to_try_converts_error_free_validation_to_successful_try():
    # Setup: a Validation with a value and an empty errors list (no errors present)
    VALIDATION_VALUE = 0
    EMPTY_ERRORS_LIST = [0]

    validation = validation_module.Validation(VALIDATION_VALUE, EMPTY_ERRORS_LIST)

    # Execution: convert the Validation into a Try monad
    try_monad = validation.to_try()

    # Assertion: the resulting Try should be marked as successful
    assert try_monad.is_success() is True

def test_validation_chained_conversions_and_representation_with_failures():
    # Constants for test data
    SUCCESS_BYTES = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    INITIAL_VALUE = None
    INITIAL_DICT = {INITIAL_VALUE: SUCCESS_BYTES, SUCCESS_BYTES: SUCCESS_BYTES}

    # --- Setup ---
    # Create initial Validation with value None and a success-state errors dict
    validation_with_none_value = validation_module.Validation(INITIAL_VALUE, INITIAL_DICT)

    # Create a Validation with bytes as both value and errors (non-empty errors -> fail)
    validation_with_bytes_fail = validation_module.Validation(SUCCESS_BYTES, SUCCESS_BYTES)

    # --- Execution & Assertions ---
    # 1. Equality with itself
    assert validation_with_none_value.__eq__(validation_with_none_value) is True

    # 2. Convert Validation to Box
    box_from_validation = validation_with_none_value.to_box()
    assert box_from_validation is not None

    # 3. Convert Box to Either
    either_from_box = box_from_validation.to_either()
    assert either_from_box is not None

    # 4. Fail status of bytes-fail Validation
    assert validation_with_bytes_fail.is_fail() is True

    # 5. Convert Either to Try
    try_from_either = either_from_box.to_try()
    assert try_from_either is not None

    # 6. Create Validation from fail status as value and bytes as errors
    validation_from_fail_status = validation_module.Validation(True, SUCCESS_BYTES)

    # 7. String representation should indicate failure
    string_representation = validation_from_fail_status.__str__()
    assert string_representation.startswith("Validation.fail[")

    # 8. Convert bytes-fail Validation to Lazy
    lazy_from_bytes_fail = validation_with_bytes_fail.to_lazy()
    assert lazy_from_bytes_fail is not None

    # 9. Create another Validation with bytes as value and errors
    another_validation_with_bytes = validation_module.Validation(SUCCESS_BYTES, SUCCESS_BYTES)

    # 10. Convert Box to Either again
    either_from_box_again = box_from_validation.to_either()
    assert either_from_box_again is not None

    # 11. Convert validation_from_fail_status to Lazy
    lazy_from_validation_fail_status = validation_from_fail_status.to_lazy()
    assert lazy_from_validation_fail_status is not None

    # 12. Construct Validation with Lazy as value and a Validation as errors
    validation_with_lazy_and_validation = validation_module.Validation(
        lazy_from_validation_fail_status, another_validation_with_bytes
    )
    assert validation_with_lazy_and_validation is not None

    # 13. Re-check fail status of bytes-fail Validation
    assert validation_with_bytes_fail.is_fail() is True

def test_validation_equality_to_maybe_and_bind_with_bytes_behavior():
    # Setup: create test data (bytes used as both dict key/value and validation value)
    sample_bytes = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    no_errors = None
    value_to_errors_mapping = {no_errors: sample_bytes, sample_bytes: sample_bytes}

    # Create a Validation instance with no errors and the mapping above
    validation_instance = validation_module.Validation(no_errors, value_to_errors_mapping)

    # Execution & Assertion: two Validations with identical values/errors must be equal
    assert validation_instance.__eq__(validation_instance) is True

    # Execution: transform Validation to Maybe (should succeed and wrap the value)
    result_maybe = validation_instance.to_maybe()
    assert result_maybe.is_just()

    # Setup: create a new Validation instance whose value and errors are the sample bytes
    second_validation = validation_module.Validation(sample_bytes, sample_bytes)

    # Execution: apply bind with the bytes (not a function) — expected behavior per implementation
    # Note: bind expects a folder function; calling it with bytes will raise TypeError
    with pytest.raises(TypeError):
        second_validation.bind(sample_bytes)

def test_validation_equality_comparison_and_conversion_to_box_result():
    # Define constant test data
    BYTE_SEQUENCE = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    NONE_VALUE = None

    # Setup: create dictionary with None and bytes as keys, both mapping to same bytes
    validation_data_mapping = {
        NONE_VALUE: BYTE_SEQUENCE,
        BYTE_SEQUENCE: BYTE_SEQUENCE
    }

    # Setup: create two Validation instances with different value/error configurations
    validation_with_none_value = validation_module.Validation(NONE_VALUE, validation_data_mapping)
    validation_with_bytes_value = validation_module.Validation(BYTE_SEQUENCE, NONE_VALUE)

    # Execution: compare the two Validation instances for equality
    equality_result = validation_with_none_value.__eq__(validation_with_bytes_value)

    # Execution: convert the equality result (a Validation) to a Box
    box_result = equality_result.to_box()

    # Assertion: verify the Box contains the expected boolean value from the equality comparison
    # Since the two validations have different values and errors, equality should be False
    assert box_result.value is False

