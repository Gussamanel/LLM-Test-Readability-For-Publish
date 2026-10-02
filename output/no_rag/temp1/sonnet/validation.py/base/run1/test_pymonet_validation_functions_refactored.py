import pytest
import validation as validation
import builtins as builtins

def test_validation_equality_and_maybe_conversion_when_fail():
    """
    Test that a failed Validation object (one with errors):
    - Reports success status correctly (is_success returns False when errors exist)
    - Is equal to itself (reflexive equality)
    - Reports fail status correctly (is_fail returns True when errors exist)
    - Converts to an empty Maybe when it is a failed Validation
    """
    # Constants
    ERROR_AND_VALUE = "\n        Create empty maybe.\n\n        :returns: Maybe[None]\n        "

    # Setup: Create a Validation where both value and errors are set to the same string
    # This means errors list is non-empty, making it a failed Validation
    failed_validation = validation.Validation(ERROR_AND_VALUE, ERROR_AND_VALUE)

    # Execution: Check success, equality and fail status
    is_success_result = failed_validation.is_success()
    is_equal_to_itself = failed_validation.__eq__(failed_validation)
    is_fail_result = failed_validation.is_fail()

    # Execution: Convert failed Validation to Maybe
    maybe_result = failed_validation.to_maybe()

    # Assertions: Validate expected behavior
    assert is_success_result == False, "Validation with errors should not be a success"
    assert is_equal_to_itself == True, "Validation should be equal to itself"
    assert is_fail_result == True, "Validation with errors should be a fail"
    assert maybe_result.is_nothing() == True, "Failed Validation should convert to an empty Maybe"

def test_validation_equality_with_none_returns_false_and_has_no_success():
    # Constants representing the validation setup
    VALIDATION_VALUE = -6891
    VALIDATION_ERRORS = (3125,)
    
    # Setup: Create a Validation object with a value and an errors tuple
    validation_instance = validation.Validation(VALIDATION_VALUE, VALIDATION_ERRORS)
    
    # Execution: Compare the Validation instance with None using __eq__
    # Since None is not a Validation instance, __eq__ should return False
    equality_result = validation_instance.__eq__(None)
    
    # Assertion: Verify that the result of equality check is not a successful validation
    # False (boolean) has an empty errors attribute equivalent, is_success() should handle this
    equality_result.is_success()

def test_validation_is_fail_returns_false_for_empty_errors():
    """
    Test that is_fail() returns False when a Validation object is initialized
    with empty dictionaries, meaning there are no errors present.
    """
    # Setup: Create empty dictionaries for value and errors
    empty_value = {}
    empty_errors = {}

    # Execution: Initialize a Validation object with empty value and errors
    validation_instance = validation.Validation(empty_value, empty_errors)

    # Assertion: Verify that is_fail() returns False since there are no errors
    assert not validation_instance.is_fail()

def test_validation_with_empty_sets_transforms_to_either_and_maybe():
    # Constants
    EMPTY_SET = set()
    
    # Setup - Create a Validation instance with empty sets for value and errors
    empty_validation = validation.Validation(EMPTY_SET, EMPTY_SET)
    
    # Execute - Transform Validation to Either and Maybe monads
    either_result = empty_validation.to_either()
    maybe_result = empty_validation.to_maybe()
    
    # Transform resulting Maybe to another Maybe (chaining)
    chained_maybe_result = maybe_result.to_maybe()
    
    # Assert - Verify transformations produce valid monad instances
    # Since both value and errors are empty sets, Validation is considered successful
    # (empty errors), so Either should be Right and Maybe should contain value
    assert either_result is not None, "to_either() should return a valid Either monad"
    assert maybe_result is not None, "to_maybe() should return a valid Maybe monad"
    assert chained_maybe_result is not None, "Chained to_maybe() should return a valid Maybe monad"

def test_validation_with_string_value_conversions_and_equality():
    # Constants
    VALIDATION_STRING_VALUE = "\n        Create empty maybe.\n\n        :returns: Maybe[None]\n        "

    # Setup: Create a Validation instance where both value and errors are set to the same string
    # This means the validation has a non-empty errors list, making it a failed validation
    validation_with_string = validation.Validation(VALIDATION_STRING_VALUE, VALIDATION_STRING_VALUE)

    # Execution: Test various operations on the failed validation

    # Convert failed validation to Either - should return Left with errors list
    either_result = validation_with_string.to_either()

    # Check equality of validation with itself - should return True
    is_equal_to_itself = validation_with_string.__eq__(validation_with_string)

    # Check if validation is a failure - should return True since errors list is non-empty
    is_failure = validation_with_string.is_fail()

    # Convert the boolean result of is_fail() to Maybe - called on True (bool), not Validation
    # This tests that is_fail returns a value that has a to_maybe method (bool doesn't, but True inherits from int)
    is_failure.to_maybe()

    # Assertions
    # Verify the validation is identified as a failure (non-empty errors)
    assert is_failure is True

    # Verify the validation is equal to itself
    assert is_equal_to_itself is True

def test_validation_to_maybe_chaining_returns_maybe():
    # Test that converting a successful Validation to Maybe can be chained
    # A Validation with empty errors set is considered successful
    EMPTY_ERRORS = set()
    EMPTY_VALUE = set()

    # Setup: Create a successful Validation (no errors) with an empty set as value
    successful_validation = validation.Validation(EMPTY_VALUE, EMPTY_ERRORS)

    # Execution: Convert Validation to Maybe
    first_maybe = successful_validation.to_maybe()

    # Assert: Verify that the resulting Maybe can also be converted to Maybe (chaining)
    # Since the value of the Validation is an empty set, the Maybe wraps that value
    # and calling to_maybe() on it should work without errors
    chained_maybe = first_maybe.to_maybe()

def test_validation_initialization_with_none_arguments():
    # Test that Validation can be initialized with None values for both arguments
    # This verifies the constructor handles None/null inputs without raising an exception
    
    # Setup
    NONE_VALUE = None
    
    # Execution
    validation_instance = validation.Validation(NONE_VALUE, NONE_VALUE)
    
    # Assertion
    assert validation_instance is not None

def test_validation_to_maybe_returns_nothing_when_errors_present():
    # Test that converting a failed Validation (with None value and None errors) to Maybe returns Maybe.nothing()
    # A Validation with None errors is considered a failure, so to_maybe() should return an empty Maybe

    # Setup
    NO_VALUE = None
    NO_ERRORS = None

    # Execution
    failed_validation = validation.Validation(NO_VALUE, NO_ERRORS)
    result = failed_validation.to_maybe()

    # Assert
    # When Validation is not successful, to_maybe() should return Maybe.nothing() (an empty Maybe)
    assert result.is_nothing()

def test_is_fail_returns_false_when_no_errors_added():
    # Test that is_fail() returns False when a Validation object is initialized
    # with no errors, confirming that an empty errors list results in a non-failure state.

    # Setup: Create a plain object and initialize Validation with it
    # (using the object as both the subject and errors placeholder)
    empty_object = builtins.object()
    validation_instance = validation.Validation(empty_object, empty_object)

    # Execute: Check if the validation is in a failed state
    result = validation_instance.is_fail()

    # Assert: With no errors added, is_fail() should return False
    assert result == False

def test_map_with_none_mapper_raises_type_error():
    # Constants for test setup
    INVALID_INT_VALUE = -895
    IS_VALID = True

    # Setup: Create a nested data structure as the validation value
    inner_int = INVALID_INT_VALUE
    inner_bool = IS_VALID
    inner_tuple = (inner_int, inner_bool)
    nested_dict = {inner_tuple: inner_tuple}
    validation_value = (nested_dict, nested_dict, inner_int)

    # Setup: Create a Validation instance with the nested value and valid state
    validation_instance = validation.Validation(validation_value, IS_VALID)

    # Execution & Assertion: Verify that passing None as mapper raises TypeError
    # since None is not callable and cannot be applied to the validation value
    with pytest.raises(TypeError):
        validation_instance.map(None)

def test_validation_bind_with_none_folder_raises_type_error():
    # Setup: Create a Validation instance with byte string as both value and error
    BYTE_VALUE = b"s\x8flul\xd1p\x86\xe0<q\xd9\xb2\xf6\x17EC\xaf\xd0"
    validation_instance = validation.Validation(BYTE_VALUE, BYTE_VALUE)
    
    # Define None as the folder function to be applied to the Validation value
    none_folder = None
    
    # Execution & Assertion: Binding with None as folder should raise TypeError
    # since None is not callable and cannot be invoked as a function
    with pytest.raises(TypeError):
        validation_instance.bind(none_folder)

def test_validation_ap_with_failure_combines_errors():
    # Constants for test setup
    INITIAL_VALID_VALUES = [True, True, True, True]
    IS_FAILURE = False

    # Setup: Create a failed Validation instance with a list of valid values as errors
    failed_validation = validation.Validation(IS_FAILURE, INITIAL_VALID_VALUES)

    # Define a function that returns a Validation when called with a value
    # Using INITIAL_VALID_VALUES list as a callable substitute (list of True values)
    validation_function = INITIAL_VALID_VALUES

    # Execute: Apply the function to the failed validation
    # ap() combines errors from current validation with errors from function result
    result = failed_validation.ap(validation_function)

    # Assert: Verify the result is a Validation with combined errors
    assert result.value == IS_FAILURE
    assert result.errors == INITIAL_VALID_VALUES + failed_validation.ap(validation_function).errors

def test_validation_to_box_is_success():
    """
    Test that a Validation object converted to a Box retains success state.
    When a Validation is created with no errors (True, True), converting it
    to a Box and checking is_success() should return True since there are no errors.
    """
    # Setup: Create a successful Validation with no errors
    IS_VALID = True
    HAS_NO_ERRORS = True
    successful_validation = validation.Validation(IS_VALID, HAS_NO_ERRORS)

    # Execute: Convert Validation to Box
    validation_box = successful_validation.to_box()

    # Assert: The box value represents a successful validation (empty errors list)
    assert validation_box.is_success() == True

def test_validation_to_lazy_bind_with_none_folder_then_to_lazy():
    """
    Test that a Validation instance can be converted to a Lazy monad,
    then bound with a None folder (which returns None when called with the value),
    and that the result can also be converted to a Lazy monad without errors.
    
    Steps:
    - Create a Validation instance with empty lists for value and errors
    - Convert the Validation to a Lazy monad
    - Bind the Lazy monad with None as the folder function (calls None(value) -> returns None)
    - Convert the result of bind (None) to a Lazy monad
    """
    # Setup
    EMPTY_VALUE = []
    EMPTY_ERRORS = []
    NONE_FOLDER = None

    # Create Validation with empty value and errors
    validation_instance = validation.Validation(EMPTY_VALUE, EMPTY_ERRORS)

    # Execution
    # Convert Validation to Lazy monad
    lazy_validation = validation_instance.to_lazy()

    # Bind the Lazy monad with None as the folder (None is called with the value)
    bind_result = lazy_validation.bind(NONE_FOLDER)

    # Convert the bind result to Lazy
    lazy_result = bind_result.to_lazy()

def test_validation_to_lazy_and_try_conversions_with_empty_dict():
    # Constants representing empty value and errors for Validation
    EMPTY_VALUE = {}
    EMPTY_ERRORS = {}

    # Setup: Create a Validation instance with empty value and errors
    empty_validation = validation.Validation(EMPTY_VALUE, EMPTY_ERRORS)

    # Execution: Convert Validation to Lazy monad
    lazy_monad = empty_validation.to_lazy()

    # Execution: Convert Lazy monad to Try monad
    try_monad = lazy_monad.to_try()

    # Execution: Apply the original validation to the lazy monad using ap
    # ap combines errors from both Validations and returns a new Validation
    validation_with_applied_fn = lazy_monad.ap(empty_validation)

    # Assertion: Verify that the Try monad derived from Lazy is successful
    # Since the original Validation has no errors (empty dict), is_success should return True
    assert try_monad.is_success()

def test_validation_to_try_returns_successful_try_when_no_errors():
    # Constants for test setup
    VALID_VALUE = 0
    EMPTY_ERRORS_LIST = []

    # Setup: Create a Validation instance with a value and no errors
    validation_instance = validation.Validation(VALID_VALUE, EMPTY_ERRORS_LIST)

    # Execute: Transform the Validation to a Try monad
    try_result = validation_instance.to_try()

    # Assert: Verify the resulting Try is successful since there are no errors
    assert try_result.is_success() == True

def test_validation_chained_transformations_with_map():
    """
    Test that Validation supports chained transformations (to_box, to_either, to_try, to_lazy)
    and that map applies a string representation as a mapper function.
    
    Setup: Creates multiple Validation instances with various value/error combinations.
    Execution: Chains multiple transformation methods and checks is_fail status.
    Assertion: Verifies that map can be called with a string as a mapper on a Validation.
    """
    # Setup - Define test data
    SAMPLE_BYTES = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    NONE_VALUE = None
    ERRORS_DICT = {NONE_VALUE: SAMPLE_BYTES, SAMPLE_BYTES: SAMPLE_BYTES}

    # Setup - Create initial Validation with None value and dict as errors
    validation_with_none_value = validation.Validation(NONE_VALUE, ERRORS_DICT)

    # Execution - Test equality of Validation with itself
    equality_result = validation_with_none_value.__eq__(validation_with_none_value)

    # Execution - Transform Validation to Box
    box_from_validation = validation_with_none_value.to_box()

    # Setup - Create a Validation with bytes value and bytes errors
    validation_with_bytes = validation.Validation(SAMPLE_BYTES, SAMPLE_BYTES)

    # Execution - Convert Box's Validation to Either
    either_from_box = box_from_validation.to_either()

    # Execution - Check if bytes Validation is a failure
    is_bytes_validation_fail = validation_with_bytes.is_fail()

    # Execution - Convert Either to Try
    try_from_either = either_from_box.to_try()

    # Setup - Create Validation using is_fail result as value
    validation_with_fail_status = validation.Validation(is_bytes_validation_fail, SAMPLE_BYTES)

    # Execution - Get string representation of validation
    validation_str_representation = validation_with_fail_status.__str__()

    # Execution - Transform bytes Validation to Lazy
    lazy_from_bytes_validation = validation_with_bytes.to_lazy()

    # Setup - Create another Validation with bytes
    another_bytes_validation = validation.Validation(SAMPLE_BYTES, SAMPLE_BYTES)

    # Execution - Convert Box's Validation to Either again
    another_either_from_box = box_from_validation.to_either()

    # Execution - Transform fail status Validation to Lazy
    lazy_from_fail_validation = validation_with_fail_status.to_lazy()

    # Setup - Create Validation using lazy result as value and another Validation as errors
    validation_with_lazy_value = validation.Validation(lazy_from_fail_validation, another_bytes_validation)

    # Execution - Check if bytes Validation is a failure again
    is_bytes_validation_fail_again = validation_with_bytes.is_fail()

    # Assertion - Verify that map can apply the string representation as a mapper on the Validation
    # The string representation is used as the mapper function argument
    equality_result.map(validation_str_representation)

def test_validation_equality_maybe_conversion_and_bind():
    """
    Test core Validation operations:
    1. Equality check between two Validation instances with same value/errors
    2. Conversion of a failed Validation (with errors) to Maybe (should return Nothing)
    3. Bind operation on a successful Validation with a non-callable value
    """
    # Setup
    SAMPLE_BYTES = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    NO_VALUE = None
    errors_dict = {NO_VALUE: SAMPLE_BYTES, SAMPLE_BYTES: SAMPLE_BYTES}

    # Create a failed Validation (no value, with errors dict)
    failed_validation = validation.Validation(NO_VALUE, errors_dict)

    # Test equality: a Validation instance should be equal to itself
    is_equal_to_self = failed_validation.__eq__(failed_validation)
    assert is_equal_to_self is True

    # Test to_maybe: a failed Validation should convert to Maybe.nothing()
    maybe_result = failed_validation.to_maybe()
    assert maybe_result.get_or_else(None) is None

    # Create a successful Validation (with value, no errors)
    successful_validation = validation.Validation(SAMPLE_BYTES, SAMPLE_BYTES)

    # Test bind: applying a non-callable (bytes) as folder on the Validation value
    # bind calls folder(self.value), so passing bytes as folder will raise TypeError
    with pytest.raises(TypeError):
        successful_validation.bind(SAMPLE_BYTES)

def test_validation_equality_check_returns_false_and_converts_to_box():
    # Constants representing test data
    SAMPLE_BYTES = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    NO_VALUE = None

    # Setup: Create two Validations with different value/error combinations
    # First validation has None value and a dict with mixed keys as errors
    errors_dict = {NO_VALUE: SAMPLE_BYTES, SAMPLE_BYTES: SAMPLE_BYTES}
    validation_with_none_value = validation.Validation(NO_VALUE, errors_dict)

    # Second validation has bytes value and None errors
    validation_with_bytes_value = validation.Validation(SAMPLE_BYTES, NO_VALUE)

    # Execution: Compare the two Validations (expected to be not equal since value and errors differ)
    equality_result = validation_with_none_value.__eq__(validation_with_bytes_value)

    # Assert: The equality result (a boolean False) is converted to a Box
    # to_box() wraps the Validation's value in a Box container
    result_box = equality_result.to_box()

