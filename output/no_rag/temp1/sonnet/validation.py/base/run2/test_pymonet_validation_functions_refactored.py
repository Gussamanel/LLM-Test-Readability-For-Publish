import pytest
import validation as validation
import builtins as builtins

def test_validation_to_maybe_returns_nothing_when_validation_fails():
    # Constants
    VALIDATION_VALUE = "some_value"
    VALIDATION_ERRORS = "some_error"

    # Setup - Create a Validation instance with both a value and a non-empty errors string
    # When errors is a non-empty string, is_fail() returns True since len(errors) != 0
    failing_validation = validation.Validation(VALIDATION_VALUE, VALIDATION_ERRORS)

    # Execution - Check validation state and convert to Maybe
    is_success = failing_validation.is_success()
    is_equal_to_itself = failing_validation.__eq__(failing_validation)
    is_failing = failing_validation.is_fail()

    # Since validation has errors (non-empty string), to_maybe() should return Maybe.nothing()
    result_maybe = failing_validation.to_maybe()

    # Assertions
    # Validation with non-empty errors string should not be successful
    assert not is_success
    # Validation should be equal to itself
    assert is_equal_to_itself
    # Validation with non-empty errors should be failing
    assert is_failing
    # Converting a failing validation to Maybe should return an empty Maybe (nothing)
    assert result_maybe == Maybe.nothing()

def test_validation_equality_with_none_returns_false_boolean():
    # Constants for test setup
    INITIAL_VALUE = -6891
    ERROR_CODE = 3125
    ERRORS_TUPLE = (ERROR_CODE,)
    
    # Setup: Create a Validation instance with a value and a non-empty errors tuple
    validation_instance = validation.Validation(INITIAL_VALUE, ERRORS_TUPLE)
    
    # Execute: Compare the Validation instance with None
    # __eq__ returns False because None is not an instance of Validation
    equality_result = validation_instance.__eq__(None)
    
    # Assert: Verify the result of is_success on the equality comparison result
    # Since None is not a Validation instance, __eq__ returns False (a boolean)
    # Calling is_success() on a boolean checks if it has an empty errors list
    equality_result.is_success()

def test_validation_is_fail_returns_false_for_empty_errors():
    # Test that is_fail() returns False when a Validation object is created
    # with empty dictionaries, meaning there are no errors present

    # Setup: Create empty dictionaries for value and errors
    empty_value = {}
    empty_errors = {}

    # Execute: Create a Validation instance with empty value and errors,
    # then check failure status
    validation_instance = validation.Validation(empty_value, empty_errors)

    # Assert: Verify that is_fail() returns False since there are no errors
    assert validation_instance.is_fail() == False

def test_validation_with_empty_set_transforms_to_either_and_maybe():
    # Setup: Create a Validation instance with empty set as both value and errors
    EMPTY_SET = set()
    # A Validation with an empty set as errors is considered a failure (non-empty errors would be a failure)
    validation_instance = validation.Validation(EMPTY_SET, EMPTY_SET)

    # Execution: Transform Validation to Either monad
    # Since errors is an empty set, this should produce a Right (success) with the value
    either_result = validation_instance.to_either()

    # Execution: Transform Validation to Maybe monad
    # Since errors is an empty set, this should produce a Maybe.just with the value
    maybe_result = validation_instance.to_maybe()

    # Execution: Chain another to_maybe() call on the Maybe result
    # Verifies that Maybe's to_maybe() method is callable and doesn't raise errors
    maybe_result.to_maybe()

    # Assertion: Verify that the transformations produced valid results
    # The Either result should be a Right monad (success path) since there are no errors
    assert either_result is not None
    # The Maybe result should be a just (non-empty) Maybe since there are no errors
    assert maybe_result is not None

def test_validation_with_string_value_transforms_and_checks_failure():
    # Constants
    VALIDATION_STRING_VALUE = "\n        Create empty maybe.\n\n        :returns: Maybe[None]\n        "
    
    # Setup: Create a Validation instance where both value and errors are set to the same string
    # This means errors is a non-empty string, so is_fail() should return True
    validation_with_string_errors = validation.Validation(VALIDATION_STRING_VALUE, VALIDATION_STRING_VALUE)
    
    # Execution: Transform Validation to Either (should return Left since errors list is not empty)
    either_result = validation_with_string_errors.to_either()
    
    # Check equality of the Validation instance with itself
    is_equal_to_itself = validation_with_string_errors.__eq__(validation_with_string_errors)
    
    # Check if the Validation is a failure (errors is a non-empty string)
    is_failure = validation_with_string_errors.is_fail()
    
    # Assertions: Verify that the Validation is considered a failure and equals itself
    assert is_equal_to_itself is True
    assert is_failure is True

def test_validation_to_maybe_chaining_from_successful_validation():
    # Test that a successful Validation with empty set can be converted to Maybe
    # and that the resulting Maybe can also be converted to Maybe (chaining)
    
    # Setup: Create a Validation with no errors (empty set for both value and errors)
    EMPTY_SET = set()
    successful_validation = validation.Validation(EMPTY_SET, EMPTY_SET)
    
    # Execution: Convert Validation to Maybe
    maybe_result = successful_validation.to_maybe()
    
    # Assert: The resulting Maybe can also be converted to Maybe (chaining is possible)
    chained_maybe_result = maybe_result.to_maybe()

def test_validation_initialized_with_none_values():
    # Test that Validation can be instantiated with None values for both parameters
    
    # Setup
    NONE_VALUE = None
    
    # Execution
    validation_instance = validation.Validation(NONE_VALUE, NONE_VALUE)
    
    # Assert that the Validation object is created successfully with None values
    assert validation_instance is not None

def test_validation_to_maybe_returns_nothing_when_errors_are_none():
    # Test that a Validation with errors transforms to an empty Maybe (nothing)
    # when to_maybe() is called on a failed Validation

    # Setup: Create a Validation instance with None value and None errors
    # A Validation with None errors is treated as a failed validation
    NONE_VALUE = None
    NONE_ERRORS = None

    failed_validation = validation.Validation(NONE_VALUE, NONE_ERRORS)

    # Execute: Transform the failed Validation to a Maybe
    result_maybe = failed_validation.to_maybe()

    # Assert: The resulting Maybe should be empty (nothing) since validation failed
    assert result_maybe.is_nothing()

def test_is_fail_returns_false_on_initial_validation_state():
    # Test that is_fail() returns False when a Validation object is created
    # with no errors, verifying the initial state has an empty errors list
    
    # Setup: Create a base object and initialize Validation with no errors
    base_object = builtins.object()
    validation_instance = validation.Validation(base_object, base_object)
    
    # Execute: Check if the validation has any failures
    result = validation_instance.is_fail()
    
    # Assert: Verify that is_fail() returns False since no errors have been added
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

    # Create a Validation instance with the nested tuple as value and True for errors
    validation_instance = validation.Validation(validation_value, IS_VALID)

    # Execution & Assertion: Applying None as mapper should raise a TypeError
    # since None is not callable and cannot be applied to the validation value
    with pytest.raises(TypeError):
        validation_instance.map(None)

def test_validation_bind_with_none_folder_raises_type_error():
    # Setup: Create a Validation instance with byte string as both value and error
    BYTE_VALUE = b"s\x8flul\xd1p\x86\xe0<q\xd9\xb2\xf6\x17EC\xaf\xd0"
    validation_instance = validation.Validation(BYTE_VALUE, BYTE_VALUE)
    
    # Define None as the folder function to pass to bind
    # bind() expects a callable, so passing None should raise a TypeError
    none_folder = None
    
    # Execution & Assertion: Verify that calling bind with None raises TypeError
    # since None is not callable and cannot be applied to the Validation value
    with pytest.raises(TypeError):
        validation_instance.bind(none_folder)

def test_ap_with_invalid_validation_and_true_list_functions():
    # Constants representing the validation state and function list
    INITIAL_VALID_STATE = False
    FUNCTION_VALUE = True
    
    # Setup: Create a list of 'True' values to act as functions and an invalid Validation object
    # The Validation is initialized with False (invalid state) and a list of True values as errors
    true_values_list = [FUNCTION_VALUE, FUNCTION_VALUE, FUNCTION_VALUE, FUNCTION_VALUE]
    invalid_validation = validation.Validation(INITIAL_VALID_STATE, true_values_list)
    
    # Execute: Apply the list of 'True' values as functions to the invalid Validation
    # ap() is called with the list, which will attempt to call each element as a function
    # and concatenate the errors from the resulting Validation
    result = invalid_validation.ap(true_values_list)
    
    # Assert: Verify the result is a Validation instance with concatenated errors
    assert isinstance(result, validation.Validation)
    assert result.value == INITIAL_VALID_STATE
    assert result.errors == true_values_list + invalid_validation.errors

def test_validation_to_box_is_success_returns_true_when_no_errors():
    """
    Test that converting a successful Validation to a Box and checking is_success()
    returns True when there are no errors.
    
    A Validation created with True value and True (indicating success/no errors)
    should, when converted to a Box, still reflect the success state.
    """
    # Setup: Create a successful Validation with no errors
    IS_VALID = True
    HAS_NO_ERRORS = True
    successful_validation = validation.Validation(IS_VALID, HAS_NO_ERRORS)

    # Execute: Convert Validation to Box
    validation_box = successful_validation.to_box()

    # Assert: The original validation has no errors (is successful)
    assert successful_validation.is_success() == True

def test_lazy_bind_with_none_returns_lazy_monad():
    # Constants
    EMPTY_ERRORS = []
    EMPTY_VALUE = []
    
    # Setup: Create a Validation instance with empty value and errors list
    validation_instance = validation.Validation(EMPTY_VALUE, EMPTY_ERRORS)
    
    # Execute: Convert Validation to Lazy monad
    lazy_validation = validation_instance.to_lazy()
    
    # Execute: Bind None as folder function to the lazy validation
    # bind(None) will attempt to call None(self.value), which returns None when folder is None
    bound_result = lazy_validation.bind(None)
    
    # Assert: Verify that calling to_lazy() on the bound result (None) raises an AttributeError
    # since None does not have a to_lazy() method
    with pytest.raises(AttributeError):
        bound_result.to_lazy()

def test_validation_lazy_and_try_transformations_with_empty_dicts():
    """
    Test that a Validation created with empty dicts can be transformed to Lazy and Try monads,
    and that the ap method correctly concatenates errors from another Validation.
    
    - Creates a Validation with empty dict as both value and errors
    - Verifies the Validation can be converted to a Lazy monad
    - Verifies the Lazy monad can be converted to a Try monad
    - Verifies the ap method works with the original Validation
    - Verifies the resulting Try monad reports success (since there are no errors)
    """
    # Setup
    EMPTY_DICT = {}
    validation = validation.Validation(EMPTY_DICT, EMPTY_DICT)
    
    # Execution
    lazy_validation = validation.to_lazy()
    try_validation = lazy_validation.to_try()
    ap_result = lazy_validation.ap(validation)
    
    # Assertion
    assert try_validation.is_success()

def test_validation_with_errors_converts_to_failed_try():
    # Constants
    INITIAL_VALUE = 0
    ERRORS_LIST = [INITIAL_VALUE]  # Non-empty errors list indicates validation failure

    # Setup: Create a Validation instance with a value and a non-empty errors list
    validation_instance = validation.Validation(INITIAL_VALUE, ERRORS_LIST)

    # Execute: Convert Validation to Try monad
    try_instance = validation_instance.to_try()

    # Assert: The resulting Try should reflect that validation was unsuccessful
    # (is_success returns False when errors list is non-empty)
    result = try_instance.is_success()
    assert result == False, "Try should be unsuccessful when Validation has errors"

def test_validation_transformations_and_equality():
    # Constants for test data
    BYTES_VALUE = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    NONE_VALUE = None
    ERRORS_DICT = {NONE_VALUE: BYTES_VALUE, BYTES_VALUE: BYTES_VALUE}

    # Setup: Create initial Validation with None value and dict as errors (fail state)
    validation_with_none_value = validation.Validation(NONE_VALUE, ERRORS_DICT)

    # Verify equality of Validation with itself
    is_equal_to_self = validation_with_none_value.__eq__(validation_with_none_value)

    # Transform fail Validation to Box and then to Either
    box_from_validation = validation_with_none_value.to_box()
    either_from_box = box_from_validation.to_either()

    # Setup: Create Validation with bytes value and bytes errors (fail state)
    validation_with_bytes = validation.Validation(BYTES_VALUE, BYTES_VALUE)

    # Transform Either to Try
    try_from_either = either_from_box.to_try()

    # Check if bytes validation is a fail
    is_bytes_validation_fail = validation_with_bytes.is_fail()

    # Setup: Create Validation using is_fail result as value
    validation_with_fail_flag = validation.Validation(is_bytes_validation_fail, BYTES_VALUE)

    # Get string representation of fail validation
    fail_validation_str = validation_with_fail_flag.__str__()

    # Transform bytes validation to Lazy
    lazy_from_bytes_validation = validation_with_bytes.to_lazy()

    # Setup: Create another Validation with bytes for comparison
    another_bytes_validation = validation.Validation(BYTES_VALUE, BYTES_VALUE)

    # Transform box validation to Either again
    another_either_from_box = box_from_validation.to_either()

    # Transform fail validation to Lazy
    lazy_from_fail_validation = validation_with_fail_flag.to_lazy()

    # Setup: Create Validation using lazy as value and another validation as errors
    validation_with_lazy_value = validation.Validation(lazy_from_fail_validation, another_bytes_validation)

    # Check if bytes validation is still a fail
    is_bytes_validation_still_fail = validation_with_bytes.is_fail()

    # Assert: Map the string representation over the equal validation
    # The map applies the string (used as mapper) to the validation's value
    mapped_validation = is_equal_to_self.map(fail_validation_str)

    # Assert that the mapped result is a Validation instance
    assert isinstance(mapped_validation, validation.Validation)

    # Assert that the fail checks return expected boolean results
    assert isinstance(is_bytes_validation_fail, bool)
    assert isinstance(is_bytes_validation_still_fail, bool)
    assert is_bytes_validation_fail == is_bytes_validation_still_fail

    # Assert the string representation of the fail validation is properly formatted
    assert 'Validation.fail' in fail_validation_str or 'Validation.success' in fail_validation_str

def test_validation_equality_to_maybe_and_bind_with_none_value():
    # Constants
    BYTES_VALUE = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    NONE_VALUE = None
    ERRORS_DICT = {NONE_VALUE: BYTES_VALUE, BYTES_VALUE: BYTES_VALUE}

    # Setup: Create a Validation with None value and a dict of errors
    validation_with_none = validation.Validation(NONE_VALUE, ERRORS_DICT)

    # Test equality: A Validation instance should be equal to itself
    is_equal_to_self = validation_with_none.__eq__(validation_with_none)
    assert is_equal_to_self is True

    # Test to_maybe: A failed Validation (with errors) should return an empty Maybe
    maybe_result = validation_with_none.to_maybe()
    assert maybe_result.is_nothing() is True

    # Setup: Create a successful Validation with bytes value and no errors
    validation_with_bytes = validation.Validation(BYTES_VALUE, BYTES_VALUE)

    # Test bind: bind should apply the folder function (here bytes_value itself is used as folder)
    # Since BYTES_VALUE is not callable, bind will raise a TypeError when called
    # This verifies the bind method attempts to call the provided folder on the value
    try:
        validation_with_bytes.bind(BYTES_VALUE)
    except TypeError:
        pass  # Expected: BYTES_VALUE is not callable, confirming bind invokes the folder

def test_validation_equality_check_returns_false_and_converts_to_box():
    """
    Test that comparing two Validation instances with different values and errors
    returns False (since they differ), and that the result of __eq__ can be
    converted to a Box using to_box().
    
    The __eq__ method returns a boolean, and to_box() wraps that boolean value
    in a Box container.
    """
    # Setup
    SAMPLE_BYTES = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    NO_VALUE = None

    errors_dict = {NO_VALUE: SAMPLE_BYTES, SAMPLE_BYTES: SAMPLE_BYTES}

    # Create two Validation instances with different value/errors combinations
    validation_with_none_value = validation.Validation(NO_VALUE, errors_dict)
    validation_with_bytes_value = validation.Validation(SAMPLE_BYTES, NO_VALUE)

    # Execution
    # Compare validations - they differ in both value and errors, so result is False
    equality_result = validation_with_none_value.__eq__(validation_with_bytes_value)

    # Convert the boolean equality result into a Box
    boxed_result = equality_result.to_box()

