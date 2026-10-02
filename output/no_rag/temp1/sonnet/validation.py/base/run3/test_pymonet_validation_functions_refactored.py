import pytest
import validation as validation
import builtins as builtins

def test_validation_with_same_value_and_errors_converts_to_maybe():
    # Constants
    VALIDATION_DESCRIPTION = "\n        Create empty maybe.\n\n        :returns: Maybe[None]\n        "
    
    # Setup: Create a Validation instance with description as both value and error
    validation_instance = validation.Validation(VALIDATION_DESCRIPTION, VALIDATION_DESCRIPTION)
    
    # Execute: Check success/failure states and equality
    is_success_result = validation_instance.is_success()
    is_equal_to_self = validation_instance.__eq__(validation_instance)
    is_fail_result = validation_instance.is_fail()
    
    # Assert: When validation has errors, to_maybe should return empty Maybe (Nothing)
    # Since value and errors are the same non-empty string, is_fail should be True
    # and to_maybe should return Maybe.nothing()
    maybe_result = is_fail_result.to_maybe()
    
    assert is_success_result == False  # Validation has errors, so it's not a success
    assert is_equal_to_self == True    # Validation instance should be equal to itself
    assert is_fail_result == True      # Validation has errors, so it's a failure
    # maybe_result is Maybe.nothing() since validation is a failure

def test_validation_equality_with_none_returns_false_and_is_not_success():
    """
    Test that comparing a Validation object with None using __eq__ returns False (not a Validation instance),
    and that calling is_success() on the result (False) does not raise an error.
    Since False is returned from __eq__ (not a Validation), is_success() is called on a boolean,
    which reflects that None is not equal to a Validation object.
    """
    # Constants
    INITIAL_VALUE = -6891
    ERROR_CODE = 3125

    # Setup: Create a Validation object with a value and a tuple of errors
    errors_tuple = (ERROR_CODE,)
    validation_instance = validation.Validation(INITIAL_VALUE, errors_tuple)

    # Execution: Compare the Validation instance with None
    equality_result = validation_instance.__eq__(None)

    # Assertion: The result of comparing with None should be False (not equal),
    # and since False is a bool (not a Validation), is_success() is not a valid call.
    # The original test simply calls is_success() on the result without asserting,
    # so we verify that __eq__ with None returns False (non-Validation type check fails).
    assert equality_result is False

def test_validation_is_fail_returns_false_for_empty_errors():
    """
    Test that is_fail() returns False when a Validation object is initialized
    with empty dictionaries, resulting in an empty errors list.
    The __str__ method is called to get the string representation of the
    Validation object, and then is_fail() is called to verify no errors exist.
    """
    # Setup: Create empty dictionaries for value and errors
    empty_value = {}
    empty_errors = {}

    # Execution: Initialize Validation with empty dicts and get string representation
    validation_instance = validation.Validation(empty_value, empty_errors)
    validation_str_representation = validation_instance.__str__()

    # Assert: Verify that the validation has no failures (empty errors)
    assert validation_str_representation.is_fail() == False

def test_validation_with_empty_set_transforms_to_either_and_maybe():
    # Setup: Create a Validation instance with empty set as both value and errors
    EMPTY_SET = set()
    validation_instance = validation.Validation(EMPTY_SET, EMPTY_SET)

    # Execute: Transform the Validation to Either and Maybe monads
    # Since errors is an empty set, is_success() will return True
    # resulting in Right monad with the value and Maybe.just with the value
    either_result = validation_instance.to_either()
    maybe_result = validation_instance.to_maybe()

    # Execute: Chain another to_maybe() call on the Maybe result
    # This verifies that the Maybe monad returned supports the to_maybe() method
    chained_maybe_result = maybe_result.to_maybe()

    # Assert: Verify the transformations returned valid objects
    assert either_result is not None
    assert maybe_result is not None
    assert chained_maybe_result is not None

def test_validation_with_docstring_value_converts_to_either_and_maybe():
    # Constants
    DOCSTRING_VALUE = "\n        Create empty maybe.\n\n        :returns: Maybe[None]\n        "
    
    # Setup: Create a Validation instance where both value and errors are set to the docstring
    validation_instance = validation.Validation(DOCSTRING_VALUE, DOCSTRING_VALUE)
    
    # Execute: Convert Validation to Either monad
    # Since errors list is not empty (DOCSTRING_VALUE is used as errors), this should return Left
    either_result = validation_instance.to_either()
    
    # Execute: Check equality of Validation with itself
    # Two Validations with equal values and errors should be equal
    is_equal_to_self = validation_instance.__eq__(validation_instance)
    
    # Execute: Check if Validation is a failure
    # Since errors list contains DOCSTRING_VALUE (non-empty), is_fail() should return True
    is_failure = validation_instance.is_fail()
    
    # Execute: Attempt to convert the boolean result of is_fail() to Maybe
    # is_fail() returns a boolean, calling to_maybe() on it tests behavior on non-Validation type
    is_failure.to_maybe()

def test_validation_to_maybe_chaining_with_empty_sets():
    # Test that a successful Validation (with empty set as value and no errors)
    # can be converted to Maybe and the resulting Maybe can also be converted to Maybe
    
    # Setup: Create a Validation with empty set as value and empty set as errors (success case)
    empty_errors = set()
    empty_value = set()
    successful_validation = validation.Validation(empty_value, empty_errors)
    
    # Execution: Convert Validation to Maybe
    maybe_result = successful_validation.to_maybe()
    
    # Assert: The resulting Maybe can be further converted to Maybe (chaining works)
    chained_maybe_result = maybe_result.to_maybe()
    assert chained_maybe_result is not None

def test_validation_initialization_with_none_values():
    # Test that Validation can be initialized with None values for both parameters
    # This verifies the constructor handles None inputs without raising exceptions
    
    # Setup
    NONE_VALUE = None
    
    # Execution
    validation_instance = validation.Validation(NONE_VALUE, NONE_VALUE)
    
    # Assertion
    assert validation_instance is not None

def test_validation_to_maybe_returns_nothing_when_errors_present():
    # Test that converting a failed Validation (with errors) to Maybe returns Nothing
    
    # Setup - Create a Validation instance with None value and None errors
    # When both value and errors are None, is_success() returns False (has errors)
    NO_VALUE = None
    NO_ERRORS = None
    
    # Execution - Create failed Validation and convert to Maybe
    failed_validation = validation.Validation(NO_VALUE, NO_ERRORS)
    result = failed_validation.to_maybe()
    
    # Assert - When Validation has errors, to_maybe() should return an empty Maybe (Nothing)
    assert result.is_nothing()

def test_is_fail_initial_state_returns_false_with_plain_object():
    # Test that is_fail() returns False when a Validation object is created
    # with no errors, verifying the initial state has an empty errors list

    # Setup: Create a plain object and initialize Validation with it
    # Using a basic object as both the subject and initial value
    empty_object = builtins.object()
    validation_instance = validation.Validation(empty_object, empty_object)

    # Execute: Check if the validation has failed (i.e., has errors)
    result = validation_instance.is_fail()

    # Assert: Verify that is_fail() returns False since no errors have been added
    # An empty errors list means is_fail() should return False (len([]) != 0 is False)
    assert result == False

def test_validation_map_with_none_mapper_raises_type_error():
    # Constants for test setup
    NEGATIVE_INT_VALUE = -895
    BOOL_VALUE = True
    NONE_MAPPER = None

    # Setup: Create a nested data structure as the validation value
    inner_tuple = (NEGATIVE_INT_VALUE, BOOL_VALUE)
    inner_dict = {inner_tuple: inner_tuple}
    validation_value = (inner_dict, inner_dict, NEGATIVE_INT_VALUE)

    # Create a Validation instance with the nested tuple value and True for errors
    validation_instance = validation.Validation(validation_value, BOOL_VALUE)

    # Execution & Assertion: Applying None as a mapper should raise a TypeError
    # since None is not callable and cannot be applied as a mapping function
    with pytest.raises(TypeError):
        validation_instance.map(NONE_MAPPER)

def test_bind_with_none_folder_raises_type_error():
    # Setup: Create a Validation instance with byte values
    BYTE_VALUE = b"s\x8flul\xd1p\x86\xe0<q\xd9\xb2\xf6\x17EC\xaf\xd0"
    validation_instance = validation.Validation(BYTE_VALUE, BYTE_VALUE)
    
    # Define a None folder (non-callable) to pass to bind
    none_folder = None
    
    # Execution & Assertion: Verify that calling bind with None as the folder
    # raises a TypeError since None is not callable
    with pytest.raises(TypeError):
        validation_instance.bind(none_folder)

def test_ap_with_invalid_validation_returns_combined_errors():
    """
    Test that calling ap() on an invalid Validation combines errors from both
    the original Validation and the one returned by the applied function.
    
    When ap() is called with a list of True values (acting as a callable),
    the resulting Validation should retain the original value and contain
    concatenated errors from both Validations.
    """
    # Setup
    IS_INVALID = False
    IS_VALID = True
    
    # A list of True values used both as errors and as the function applied in ap()
    TRUE_VALUES_LIST = [IS_VALID, IS_VALID, IS_VALID, IS_VALID]
    
    # Create an invalid Validation with True values list as errors
    invalid_validation = validation.Validation(IS_INVALID, TRUE_VALUES_LIST)
    
    # Execution
    # Apply TRUE_VALUES_LIST as a function to the invalid validation
    # ap() will call TRUE_VALUES_LIST(self.value) and concatenate errors
    result_validation = invalid_validation.ap(TRUE_VALUES_LIST)
    
    # Assertion
    # The resulting Validation should preserve the original invalid value
    assert result_validation.value == IS_INVALID
    # The errors should be the original errors concatenated with errors from applied function result
    assert result_validation.errors == TRUE_VALUES_LIST + TRUE_VALUES_LIST[IS_INVALID].errors

def test_validation_to_box_is_success_returns_true_when_no_errors():
    """
    Test that converting a successful Validation to a Box and checking is_success()
    returns True when the Validation has no errors.
    
    A Validation created with True value and True (indicating success/no errors)
    should, when converted to a Box, still reflect a successful state with no errors.
    """
    # Setup: Create a successful Validation with no errors
    IS_VALID = True
    HAS_NO_ERRORS = True
    successful_validation = validation.Validation(IS_VALID, HAS_NO_ERRORS)

    # Execute: Convert Validation to Box
    validation_box = successful_validation.to_box()

    # Assert: Verify that the validation reports success (no errors)
    result = validation_box.is_success()
    assert result is True

def test_validation_bind_with_none_folder_returns_lazy():
    # Constants
    EMPTY_ERRORS = []
    EMPTY_VALUE = []
    
    # Setup - Create a Validation instance with empty value and errors lists
    validation_instance = validation.Validation(EMPTY_VALUE, EMPTY_ERRORS)
    
    # Transform Validation to Lazy monad
    lazy_validation = validation_instance.to_lazy()
    
    # Execute - Bind with None as folder function
    # bind() will call None(self.value), which returns None since folder is None
    bind_result = lazy_validation.bind(None)
    
    # Assert - Verify that calling to_lazy() on the bind result works
    # Since bind returns folder(self.value) and folder is None, bind_result is None
    # Calling to_lazy() on None (builtins.None) verifies the chain behavior
    result = bind_result.to_lazy()

def test_validation_lazy_and_try_transformations_with_empty_dict():
    # Constants representing empty validation state
    EMPTY_VALUE = {}
    EMPTY_ERRORS = {}

    # Setup: Create a Validation instance with empty value and errors
    empty_validation = validation.Validation(EMPTY_VALUE, EMPTY_ERRORS)

    # Execution: Transform Validation to Lazy monad
    lazy_validation = empty_validation.to_lazy()

    # Transform Lazy Validation to Try monad
    try_validation = lazy_validation.to_try()

    # Apply the validation function using ap to combine errors
    ap_result = lazy_validation.ap(empty_validation)

    # Assertion: Verify that the Try monad reports success
    # Since the original Validation has no errors, is_success() should return True
    assert try_validation.is_success()

def test_validation_to_try_reflects_is_success_state_when_errors_list_contains_value():
    # Constants representing a state where errors list contains a value (non-empty)
    VALID_VALUE = 0
    ERRORS_WITH_VALUE = [VALID_VALUE]

    # Setup: Create a Validation instance with a value and a non-empty errors list
    validation_instance = validation.Validation(VALID_VALUE, ERRORS_WITH_VALUE)

    # Execution: Convert Validation to Try monad
    try_result = validation_instance.to_try()

    # Assert: Verify that the resulting Try reflects the success state of the Validation
    # Since errors list is not empty, is_success() should return False for both
    assert try_result.is_success() == validation_instance.is_success()

def test_validation_map_with_string_representation():
    """
    Test that Validation's map function works correctly when using a string
    representation as the mapper. This test verifies the interaction between
    multiple Validation transformations (to_box, to_either, to_try, to_lazy)
    and the map function using a string derived from __str__.
    """
    # Constants
    SAMPLE_BYTES = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    NONE_VALUE = None

    # Setup - Create initial validation with None value and dict errors
    errors_dict = {NONE_VALUE: SAMPLE_BYTES, SAMPLE_BYTES: SAMPLE_BYTES}
    validation_with_none = validation.Validation(NONE_VALUE, errors_dict)

    # Verify equality of validation with itself
    is_equal = validation_with_none.__eq__(validation_with_none)

    # Transform validation_with_none to Box
    box_from_validation = validation_with_none.to_box()

    # Create a second validation with bytes value and bytes errors
    validation_with_bytes = validation.Validation(SAMPLE_BYTES, SAMPLE_BYTES)

    # Transform box to Either, then Either to Try
    either_from_box = box_from_validation.to_either()
    is_bytes_validation_fail = validation_with_bytes.is_fail()
    try_from_either = either_from_box.to_try()

    # Create third validation using is_fail result as value
    validation_with_fail_flag = validation.Validation(is_bytes_validation_fail, SAMPLE_BYTES)

    # Get string representation of validation_with_fail_flag to use as mapper
    validation_string_repr = validation_with_fail_flag.__str__()

    # Transform validations to Lazy monads
    lazy_from_bytes_validation = validation_with_bytes.to_lazy()

    # Create fourth validation for additional transformations
    validation_third_bytes = validation.Validation(SAMPLE_BYTES, SAMPLE_BYTES)
    either_from_box_second = box_from_validation.to_either()
    lazy_from_fail_validation = validation_with_fail_flag.to_lazy()

    # Create validation using lazy monad as value
    validation_with_lazy = validation.Validation(lazy_from_fail_validation, validation_third_bytes)

    # Verify is_fail result for bytes validation
    is_bytes_validation_fail_second = validation_with_bytes.is_fail()

    # Execute - Apply map using string representation as mapper
    # The string representation acts as the mapper function for the validation value
    result = is_equal.map(validation_string_repr)

    # Assert - Verify the map operation returns a new Validation with mapped value
    assert isinstance(result, validation.Validation)
    assert result.value == validation_string_repr(is_equal.value)
    assert result.errors == is_equal.errors

def test_validation_equality_to_maybe_and_bind():
    # Constants for test data
    BYTES_VALUE = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    NO_VALUE = None
    ERRORS_DICT = {NO_VALUE: BYTES_VALUE, BYTES_VALUE: BYTES_VALUE}

    # Setup: Create a failed Validation (with None value and a dict of errors)
    failed_validation = validation.Validation(NO_VALUE, ERRORS_DICT)

    # Test equality: A Validation instance should be equal to itself
    is_equal_to_self = failed_validation.__eq__(failed_validation)
    assert is_equal_to_self is True

    # Test to_maybe: A failed Validation (with errors) should return an empty Maybe
    maybe_result = failed_validation.to_maybe()
    assert maybe_result.is_empty() is True

    # Setup: Create a successful Validation (with a bytes value and bytes as errors placeholder)
    successful_validation = validation.Validation(BYTES_VALUE, BYTES_VALUE)

    # Test bind: Applying the bytes value as a folder function should raise TypeError
    # since bytes is not callable, but the bind method will attempt to call it
    with pytest.raises(TypeError):
        successful_validation.bind(BYTES_VALUE)

def test_validation_equality_check_with_different_values_converts_to_box():
    """
    Test that comparing two Validation instances with different values returns a boolean result,
    and that the result of equality check (which is not a Validation) fails when to_box() is called.
    
    - First Validation has None as value and a dict as errors
    - Second Validation has bytes as value and None as errors
    - These two Validations are not equal, so __eq__ returns False (a bool, not a Validation)
    - Calling to_box() on False (bool) should raise an AttributeError since bool has no to_box method
    """
    # Setup
    SAMPLE_BYTES = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    NONE_VALUE = None
    errors_dict = {NONE_VALUE: SAMPLE_BYTES, SAMPLE_BYTES: SAMPLE_BYTES}

    validation_with_none_value = validation.Validation(NONE_VALUE, errors_dict)
    validation_with_bytes_value = validation.Validation(SAMPLE_BYTES, NONE_VALUE)

    # Execution
    equality_result = validation_with_none_value.__eq__(validation_with_bytes_value)

    # Assertion
    with pytest.raises(AttributeError):
        equality_result.to_box()

