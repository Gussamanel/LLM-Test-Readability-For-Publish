import pytest
import validation as validation_module
import builtins as builtins_module

def test_validation_equality_and_maybe_conversion_for_documentation_string_case():
    # Setup: create a Validation with a docstring-like value and no errors
    DOCSTRING_VALUE = (
        "\n        Create empty maybe.\n\n"
        "        :returns: Maybe[None]\n        "
    )
    validation = validation_module.Validation(DOCSTRING_VALUE, DOCSTRING_VALUE)

    # Execution: perform checks and conversion on the Validation
    is_success = validation.is_success()
    is_equal_to_itself = validation.__eq__(validation)
    is_fail = validation.is_fail()
    maybe_value = is_fail.to_maybe()

    # Assertion: verify Validation behavior and Maybe conversion
    assert is_success is True
    assert is_equal_to_itself is True
    assert is_fail is False
    assert maybe_value.is_just() is True
    assert maybe_value.value == DOCSTRING_VALUE

def test_validation_equality_with_none_returns_success_validation_comparison_result():
    # Constants: input value and tuple of arguments for the Validation constructor
    INPUT_VALUE = -6891
    VALIDATION_ARGS = (3125,)

    # Setup: create a Validation instance and a non-Validation value (None) to compare against
    validation_instance = validation_module.Validation(INPUT_VALUE, VALIDATION_ARGS)
    non_validation_value = None

    # Execution: compare validation instance with None using equality operator
    comparison_result = validation_instance.__eq__(non_validation_value)

    # Assertion: the comparison should return a successful Validation (no errors)
    assert comparison_result.is_success()

def test_validation_str_representation_for_empty_errors_is_failure():
    EMPTY_DICT = {}
    validation_with_empty_errors = validation_module.Validation(EMPTY_DICT, EMPTY_DICT)

    string_representation = validation_with_empty_errors.__str__()

    assert string_representation.is_fail() is True

def test_validate_empty_validation_conversions_to_maybe_and_either() -> None:
    # Setup: create an empty Validation instance (no value, no errors)
    empty_set = set()
    empty_validation = validation_module.Validation(empty_set, empty_set)

    # Execution: convert Validation to Either and Maybe, then convert the Maybe again
    either_result = empty_validation.to_either()
    maybe_result = empty_validation.to_maybe()
    maybe_result.to_maybe()

    # Assertions: an empty Validation is not successful, so conversions should
    # yield an empty Maybe and a Left Either (with the empty errors set)
    assert maybe_result == builtins_module.object
    assert either_result == (empty_set,)

def test_validation_conversion_and_equality_for_documentation_string_case():
    error_message = (
        "\n        Create empty maybe.\n\n"
        "        :returns: Maybe[None]\n        "
    )
    validation = validation_module.Validation(error_message, error_message)

    either_result = validation.to_either()
    is_equal = validation.__eq__(validation)
    is_failure = validation.is_fail()
    maybe_result = validation.to_maybe()

    assert isinstance(either_result, validation_module.Left)
    assert is_equal is True
    assert is_failure is True
    assert isinstance(maybe_result, validation_module.Nothing)

def test_successful_validation_with_empty_set_value_converts_to_maybe():
    # Setup: Create a successful Validation with an empty set as value.
    # Using a set as the value covers a non-primary type and ensures the
    # success path of Validation is taken (no error collection present).
    empty_collection = set()
    successful_validation = validation_module.Validation(empty_collection, empty_collection)

    # Execution: Convert the Validation into a Maybe.
    # Since the Validation has no errors, this must produce a Maybe.just(value).
    resulting_maybe = successful_validation.to_maybe()

    # Assertion/Execution: Calling to_maybe() on the resulting Maybe should
    # be a safe no-op (Maybe is already the target type), verifying the
    # object returned by Validation.to_maybe supports the Maybe API.
    resulting_maybe.to_maybe()

def test_validation_constructor_with_none_arguments_does_not_raise_exception():
    # Arrange: prepare None values to be passed as constructor arguments
    input_type = None
    input_value = None

    # Act: instantiate Validation with None arguments
    validation_instance = validation_module.Validation(input_type, input_value)

    # Assert: verify the constructor accepts None arguments without raising an exception
    assert validation_instance is not None

def test_to_maybe_returns_just_with_value_when_validation_has_no_errors():
    # Setup: create a successful Validation instance with a non-None value
    validation_value = 42
    successful_validation = validation_module.Validation(validation_value, None)

    # Execution: transform the successful Validation into a Maybe
    result_maybe = successful_validation.to_maybe()

    # Assertion: a successful Validation should produce a Maybe.just wrapping the original value
    assert result_maybe.is_just()
    assert result_maybe.value == validation_value

def test_is_fail_returns_false_when_validation_has_no_errors():
    # Setup: create an object and wrap it in a Validation instance whose error list starts empty
    dummy_object = validation_module.object()
    validation = validation_module.Validation(dummy_object, dummy_object)

    # Execution: query the failure state of the fresh Validation instance
    result = validation.is_fail()

    # Assertion: a Validation with no recorded errors must not be considered failing
    assert result is False

def test_map_with_none_mapper_raises_type_error():
    # Setup
    error_code = -895
    success_flag = True
    validation_value = (error_code, success_flag)
    validation_dict = {validation_value: validation_value}
    validation_tuple = (validation_dict, validation_dict, error_code)
    validation = validation_module.Validation(validation_tuple, success_flag)
    none_mapper = None

    # Execution and assertion
    # Verify that calling map with a None mapper raises a TypeError,
    # since None is not callable.
    with pytest.raises(TypeError):
        validation.map(none_mapper)

def test_bind_applies_folder_function_to_validation_value():
    # Setup: Create a Validation instance with sample bytes and a folder function
    sample_bytes = b"s\x8flul\xd1p\x86\xe0<q\xd9\xb2\xf6\x17EC\xaf\xd0"
    validation_instance = validation_module.Validation(sample_bytes, sample_bytes)

    def folder_function(value):
        return value

    # Execution: Bind the folder function to the Validation instance
    result = validation_instance.bind(folder_function)

    # Assertion: Verify the folder function received the Validation's value
    assert result == sample_bytes

def test_ap_concatenates_errors_from_current_and_new_validation():
    initial_value = False
    error_flags = [True, True, True, True]
    validation = validation_module.Validation(initial_value, error_flags)

    result = validation.ap(lambda value: validation_module.Validation(value, error_flags))

    expected_errors = error_flags + error_flags
    assert result.errors == expected_errors
    assert result.value == initial_value

def test_validation_to_box_carries_over_success_status():
    # Setup: create a successful Validation instance
    is_success_value = True
    validation = validation_module.Validation(is_success_value, is_success_value)

    # Execution: transform the Validation into a Box
    box = validation.to_box()

    # Assertion: the Box should carry over the successful validation status
    assert box.is_success() is True

def test_lazy_bind_with_no_return_and_empty_list_from_validation():
    # Setup
    # Create a Validation instance with empty lists as value and error
    empty_list = []
    validation = validation_module.Validation(empty_list, empty_list)

    # Convert Validation to Lazy monad
    lazy_validation = validation.to_lazy()

    # Define a bind function that ignores the current value and returns None
    def binder_ignoring_value(value):
        return None

    # Execution
    # Apply bind on Lazy using the defined binder
    bound_lazy = lazy_validation.bind(binder_ignoring_value)

    # Convert the result to Lazy again
    result_lazy = bound_lazy.to_lazy()

    # Assertion
    # The purpose of this test is to verify that the chain of operations
    # (Validation.to_lazy -> Lazy.bind -> Lazy.to_lazy) works correctly
    # and produces a Lazy instance without raising exceptions.
    assert isinstance(result_lazy, lazy_module.Lazy)

def test_validation_to_lazy_to_try_ap_chain_success_verification():
    # Setup: create an empty Validation instance
    EMPTY_VALUE = {}
    validation = validation_module.Validation(EMPTY_VALUE, EMPTY_VALUE)

    # Execution: convert to Lazy, then Try, and apply ap with the original validation
    lazy_validation = validation.to_lazy()
    try_validation = lazy_validation.to_try()
    ap_validation = lazy_validation.ap(validation)

    # Assertion: the Try from lazy should report success (no errors)
    assert try_validation.is_success() is True

def test_validation_to_try_success_when_validation_has_no_errors():
    # Setup: create a Validation with no errors (success state)
    VALID_VALUE = 0
    EMPTY_ERRORS_LIST = [VALID_VALUE]  # NOTE: reproduces original list argument; kept as-is
    validation = validation_module.Validation(VALID_VALUE, EMPTY_ERRORS_LIST)

    # Execution: transform the Validation instance into a Try instance
    try_instance = validation.to_try()

    # Assertion: since the Validation has no errors, the resulting Try should be successful
    assert try_instance.is_success() is True

def test_validation_transformation_chain_and_equality_verification():
    # Constants
    BYTE_DATA = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    NONE_VALUE = None
    ERROR_DICT = {NONE_VALUE: BYTE_DATA, BYTE_DATA: BYTE_DATA}
    
    # Setup: Create initial Validation instances
    validation_with_none_and_dict = validation_module.Validation(NONE_VALUE, ERROR_DICT)
    validation_with_bytes = validation_module.Validation(BYTE_DATA, BYTE_DATA)
    validation_with_boolean_error = validation_module.Validation(False, BYTE_DATA)  # is_fail returns False here
    
    # Execution: Test equality comparison
    are_validations_equal = validation_with_none_and_dict.__eq__(validation_with_none_and_dict)
    
    # Execution: Test transformation methods
    boxed_validation = validation_with_none_and_dict.to_box()
    either_from_box = boxed_validation.to_either()
    try_from_either = either_from_box.to_try()
    lazy_from_validation = validation_with_bytes.to_lazy()
    
    # Execution: Test validation status checking
    is_validation_failed = validation_with_bytes.is_fail()
    
    # Execution: Test string representation
    validation_string_representation = validation_with_boolean_error.__str__()
    
    # Execution: Additional transformations for comprehensive testing
    either_from_validation = boxed_validation.to_either()
    lazy_from_boolean_validation = validation_with_boolean_error.to_lazy()
    validation_with_lazy_and_validation = validation_module.Validation(lazy_from_boolean_validation, validation_with_bytes)
    
    # Execution: Test validation status again (duplicate check)
    is_validation_failed_again = validation_with_bytes.is_fail()
    
    # Execution: Test map operation with string mapper
    boxed_validation.map(validation_string_representation)
    
    # Assertions: Verify equality comparison works correctly
    assert are_validations_equal is True, "Validation should equal itself"
    
    # Assertions: Verify transformation methods return proper types
    assert boxed_validation is not None, "to_box should return a Box instance"
    assert either_from_box is not None, "to_either should return Either instance"
    assert try_from_either is not None, "to_try should return Try instance"
    assert lazy_from_validation is not None, "to_lazy should return Lazy instance"
    
    # Assertions: Verify validation status checking
    assert is_validation_failed is True, "Validation with error bytes should be marked as failed"
    assert is_validation_failed_again is True, "Consistent failure status verification"
    
    # Assertions: Verify string representation
    assert isinstance(validation_string_representation, str), "String representation should return string"
    
    # Assertions: Verify chained transformations work
    assert either_from_validation is not None, "Either from box should be created"
    assert lazy_from_boolean_validation is not None, "Lazy from validation should be created"
    assert validation_with_lazy_and_validation is not None, "Validation with lazy and validation should be created"

def test_validation_bind_with_bytes_value_and_equality_with_none():
    # Setup: Create test data with bytes and None as a dictionary key
    sample_bytes = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    none_value = None
    validation_data = {none_value: sample_bytes, sample_bytes: sample_bytes}

    # Setup: Create a Validation instance with None value and the data dictionary as errors
    validation_with_none_value = validation_module.Validation(none_value, validation_data)

    # Execution: Test equality comparison - a Validation should equal itself
    # Assertion: Verify that the Validation equals itself
    is_equal_to_itself = validation_with_none_value.__eq__(validation_with_none_value)
    assert is_equal_to_itself is True

    # Execution: Convert Validation to Maybe - creates a Maybe from the Validation value
    # Assertion: Verify the conversion doesn't raise and returns a valid Maybe
    maybe_result = validation_with_none_value.to_maybe()
    assert hasattr(maybe_result, "is_just") and hasattr(maybe_result, "is_nothing")

    # Setup: Create another Validation instance with bytes as both value and errors
    validation_with_bytes = validation_module.Validation(sample_bytes, sample_bytes)

    # Execution: Test bind operation - tries to apply the bytes value as a function
    # Assertion: Verify that binding a non-callable raises a TypeError
    with pytest.raises(TypeError):
        validation_with_bytes.bind(sample_bytes)

def test_validation_equality_dict_with_none_key_and_box_conversion():
    # Setup: create a Validation with a dictionary containing None and bytes as keys,
    # and another Validation with bytes as value and None as errors.
    EQUALITY_EXPECTED = True
    
    bytes_value = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    none_value = None
    validation_errors_dict = {none_value: bytes_value, bytes_value: bytes_value}
    
    validation_instance_1 = validation_module.Validation(none_value, validation_errors_dict)
    validation_instance_2 = validation_module.Validation(bytes_value, none_value)
    
    # Execution: compare the two Validation instances for equality and transform the result to a Box.
    equality_result = validation_instance_1.__eq__(validation_instance_2)
    box_result = equality_result.to_box()
    
    # Assertion: the equality check should return a truthy Validation, and to_box should produce a Box.
    assert equality_result.value is EQUALITY_EXPECTED
    assert box_result is not None  # Box instance should be created from the Validation value.

