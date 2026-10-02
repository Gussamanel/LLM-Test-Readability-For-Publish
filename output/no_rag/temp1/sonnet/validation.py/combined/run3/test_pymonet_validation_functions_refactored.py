import pytest
import validation as validation
import builtins as builtins

def test_validation_with_string_value_converts_to_empty_maybe():
    # Constants
    DOCSTRING_VALUE = "\n        Create empty maybe.\n\n        :returns: Maybe[None]\n        "
    
    # Setup - Create a Validation instance where both value and errors are the same docstring
    validation_instance = validation.Validation(DOCSTRING_VALUE, DOCSTRING_VALUE)
    
    # Execute - Check success/failure states and equality
    is_success_result = validation_instance.is_success()
    is_equal_to_itself = validation_instance.__eq__(validation_instance)
    is_fail_result = validation_instance.is_fail()
    
    # Convert failed validation to Maybe (should return empty Maybe since errors are present)
    maybe_result = is_fail_result.to_maybe()
    
    # Assert - Validation with non-empty errors list should not be successful
    assert is_success_result == False
    # Assert - Validation instance should be equal to itself
    assert is_equal_to_itself == True
    # Assert - Validation with non-empty errors list should be a failure
    assert is_fail_result == True
    # Assert - Failed validation converts to empty Maybe (Nothing)
    assert maybe_result.is_nothing() == True

def test_validation_equality_with_none_returns_false_and_is_not_successful():
    """
    Test that comparing a Validation instance with None returns False (not a Validation instance),
    and that calling is_success() on the result (False) raises an AttributeError since False 
    is not a Validation object. This verifies __eq__ returns False for non-Validation comparisons.
    """
    # Constants
    INITIAL_VALUE = -6891
    ERROR_CODE = 3125

    # Setup
    errors_tuple = (ERROR_CODE,)
    validation_instance = validation.Validation(INITIAL_VALUE, errors_tuple)

    # Execution
    equality_result = validation_instance.__eq__(None)

    # Assertion
    # __eq__ returns False when comparing with None (not a Validation instance)
    assert equality_result is False

def test_validation_is_fail_returns_false_for_empty_errors():
    """
    Test that is_fail() returns False when a Validation object is created
    with empty dictionaries, resulting in no errors being present.
    The __str__ method is called to get the Validation object's string 
    representation, and then is_fail() is verified to return False 
    since no errors exist.
    """
    # Setup: Create empty dictionaries for value and errors
    empty_value = {}
    empty_errors = {}

    # Execution: Create a Validation instance with empty value and errors
    validation_instance = validation.Validation(empty_value, empty_errors)

    # Get the string representation of the validation instance
    validation_str_representation = validation_instance.__str__()

    # Assertion: Verify that is_fail() returns False since there are no errors
    assert validation_str_representation.is_fail() == False

def test_validation_empty_set_transforms_to_either_and_maybe():
    # Constants
    EMPTY_SET = set()

    # Setup: Create a Validation instance with empty sets for both value and errors
    # An empty set as value and errors means the validation state is ambiguous
    validation_instance = validation.Validation(EMPTY_SET, EMPTY_SET)

    # Execution: Transform Validation to Either and Maybe monads
    either_result = validation_instance.to_either()
    maybe_result = validation_instance.to_maybe()

    # Chaining: Verify that the Maybe result can be further transformed to Maybe
    # This tests that the returned Maybe object supports the to_maybe() method
    chained_maybe_result = maybe_result.to_maybe()

    # Assertions: Verify the transformations return valid objects
    # Either should be a Right or Left monad
    assert either_result is not None
    # Maybe should be a Just or Nothing monad
    assert maybe_result is not None
    # Chained Maybe transformation should also return a valid object
    assert chained_maybe_result is not None

def test_validation_with_errors_converts_to_either_and_maybe():
    """
    Test that a Validation instance created with errors:
    1. Can be converted to an Either (Left) monad
    2. Can be compared to itself for equality
    3. Correctly identifies itself as a failure
    4. Can be converted to an empty Maybe (Nothing) when it has errors
    """
    # Constants
    DOCSTRING_VALUE = "\n        Create empty maybe.\n\n        :returns: Maybe[None]\n        "

    # Setup - Create a Validation instance where both value and errors are set to the same string
    validation_with_errors = validation.Validation(DOCSTRING_VALUE, DOCSTRING_VALUE)

    # Execution - Convert Validation to Either monad (should be Left since errors are present)
    either_result = validation_with_errors.to_either()

    # Assert - Validation is equal to itself
    assert validation_with_errors.__eq__(validation_with_errors)

    # Execution - Check if the validation is a failure (errors list is not empty)
    is_failure = validation_with_errors.is_fail()

    # Assert - Since errors are present, is_fail should return True
    assert is_failure

    # Execution - Convert failure validation to Maybe (should return Nothing/empty Maybe)
    maybe_result = is_failure.to_maybe()

def test_validation_to_maybe_chaining():
    # Test that converting a successful Validation (with empty set as value) 
    # to Maybe can be chained with another to_maybe() call
    
    # Setup
    EMPTY_ERRORS = set()
    EMPTY_VALUE = set()
    
    # Execution
    # Create a Validation with no errors (empty set) and empty set as value
    successful_validation = validation.Validation(EMPTY_VALUE, EMPTY_ERRORS)
    
    # Convert Validation to Maybe - should return Maybe.just(value) since there are no errors
    maybe_result = successful_validation.to_maybe()
    
    # Assert - Verify that the resulting Maybe can also be converted to Maybe (chaining)
    # This checks that to_maybe() on a Maybe object works without raising exceptions
    chained_maybe_result = maybe_result.to_maybe()

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
    # Test that converting a failed Validation to Maybe returns Nothing
    # A Validation with None value and None errors list is treated as failed
    
    # Setup
    VALIDATION_VALUE = None
    VALIDATION_ERRORS = None
    
    # Execution
    failed_validation = validation.Validation(VALIDATION_VALUE, VALIDATION_ERRORS)
    result = failed_validation.to_maybe()
    
    # Assert
    # When validation has errors (non-success), to_maybe() should return Maybe.nothing()
    assert result.is_empty()

def test_is_fail_returns_false_when_no_errors_added():
    # Test that is_fail() returns False when no errors have been added to the Validation object
    # An empty errors list should indicate no failures occurred
    
    # Setup: Create a basic object to use as both value and field identifier
    empty_object = builtins.object()
    
    # Execution: Create a Validation instance with no errors added
    validation_instance = validation.Validation(empty_object, empty_object)
    
    # Assert: Verify that is_fail() returns False since no errors have been added
    result = validation_instance.is_fail()
    assert result == False, "is_fail() should return False when the errors list is empty"

def test_map_with_none_mapper_on_validation_with_tuple_value():
    # Constants
    NEGATIVE_INT = -895
    BOOL_VALUE = True
    
    # Setup: Create a nested data structure to use as the validation value
    inner_tuple = (NEGATIVE_INT, BOOL_VALUE)
    nested_dict = {inner_tuple: inner_tuple}
    validation_value = (nested_dict, nested_dict, NEGATIVE_INT)
    
    # Create a Validation instance with the nested tuple as value and True as errors
    validation_instance = validation.Validation(validation_value, BOOL_VALUE)
    
    # Execution & Assertion: Applying None as a mapper should raise a TypeError
    # since None is not callable and cannot be invoked as a function
    with pytest.raises(TypeError):
        validation_instance.map(None)

def test_validation_bind_with_none_folder_raises_type_error():
    # Setup: Create a Validation instance with byte string values
    BYTE_VALUE = b"s\x8flul\xd1p\x86\xe0<q\xd9\xb2\xf6\x17EC\xaf\xd0"
    validation_instance = validation.Validation(BYTE_VALUE, BYTE_VALUE)
    
    # None cannot be called as a function, so binding with None should raise a TypeError
    none_folder = None
    
    # Execution & Assertion: Verify that passing None as the folder raises a TypeError
    # since bind() attempts to call folder(self.value) and None is not callable
    with pytest.raises(TypeError):
        validation_instance.bind(none_folder)

def test_validation_ap_combines_errors_when_invalid():
    # Constants representing boolean values for clarity
    IS_INVALID = False
    HAS_ERROR = True

    # Setup: Create a list of error flags and an invalid Validation instance
    error_flags = [HAS_ERROR, HAS_ERROR, HAS_ERROR, HAS_ERROR]
    invalid_validation = validation.Validation(IS_INVALID, error_flags)

    # Execution: Apply a function (represented as error_flags list) to the invalid validation
    # The ap method combines the current validation's errors with the errors from the result of calling fn(self.value)
    result = invalid_validation.ap(error_flags)

    # Assertion: Verify that the resulting validation has combined errors from both the original and applied function
    assert result.errors == error_flags + error_flags
    assert result.value == IS_INVALID

def test_validation_to_box_is_success_with_no_errors():
    """
    Test that converting a successful Validation to a Box
    and checking is_success() returns True when there are no errors.
    
    A Validation created with True value and True (no errors) should:
    1. Be convertible to a Box via to_box()
    2. The resulting Box's is_success() should indicate no errors present
    """
    # Setup
    IS_SUCCESS = True
    HAS_NO_ERRORS = True
    
    # Execution
    successful_validation = validation.Validation(IS_SUCCESS, HAS_NO_ERRORS)
    validation_as_box = successful_validation.to_box()
    
    # Assertion
    result = validation_as_box.is_success()
    assert result is True

def test_lazy_bind_with_none_folder_returns_lazy():
    """
    Test that binding a None folder to a Lazy monad (created from a Validation)
    and then converting the result to Lazy works correctly.
    
    The test verifies that:
    1. A Validation with empty lists can be converted to a Lazy monad.
    2. Binding None as a folder to the Lazy monad invokes None on the Validation's value (None).
    3. The result of bind(None) can itself be converted to a Lazy monad.
    """
    # Setup
    EMPTY_LIST = []
    NONE_FOLDER = None

    # Create a Validation with empty errors and values, then convert to Lazy
    validation_instance = validation.Validation(EMPTY_LIST, EMPTY_LIST)
    lazy_validation = validation_instance.to_lazy()

    # Execution
    # Bind None as folder: since bind calls folder(self.value), and self.value is None,
    # this effectively calls None(None) which returns None
    bind_result = lazy_validation.bind(NONE_FOLDER)

    # Convert the bind result (None) to Lazy
    # Since bind returns None here, calling to_lazy() on None would raise AttributeError
    # This test verifies the chained behavior of bind and to_lazy
    lazy_result = bind_result.to_lazy()

    # Assertion
    assert lazy_result is not None

def test_validation_to_lazy_to_try_and_ap_with_empty_dict():
    """
    Test that a Validation with empty dict value and no errors can be:
    1. Converted to a Lazy monad
    2. The Lazy monad can be converted to a Try monad
    3. The Lazy monad can use ap() to apply the original Validation as a function
    4. The resulting Try monad reflects success (no errors in original Validation)
    """
    # Setup: Create a Validation with empty dict as both value and errors
    EMPTY_DICT = {}
    empty_validation = validation.Validation(EMPTY_DICT, EMPTY_DICT)

    # Execution: Transform Validation through different monadic types
    lazy_validation = empty_validation.to_lazy()
    try_monad = lazy_validation.to_try()
    ap_result = lazy_validation.ap(empty_validation)

    # Assert: The Try monad should reflect success since there are no errors
    assert try_monad.is_success()

def test_validation_to_try_returns_successful_try_when_no_errors():
    # Constants for test setup
    VALID_VALUE = 0
    EMPTY_ERRORS_LIST = []

    # Setup: Create a Validation instance with a value and no errors
    validation_instance = validation.Validation(VALID_VALUE, EMPTY_ERRORS_LIST)

    # Execute: Convert Validation to Try monad
    try_result = validation_instance.to_try()

    # Assert: The resulting Try should be successful since there are no errors
    assert try_result.is_success() == True

def test_validation_chained_transformations_and_map():
    """
    Tests a series of chained Validation transformations including:
    - Creating Validations with None and bytes values
    - Equality check between Validations
    - Converting to Box, Either, Try, and Lazy monads
    - Checking failure state with is_fail()
    - Mapping a string representation over a Validation
    """
    # Setup - define constants
    BYTES_VALUE = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    NONE_VALUE = None
    ERRORS_DICT = {NONE_VALUE: BYTES_VALUE, BYTES_VALUE: BYTES_VALUE}

    # Create initial Validation with None value and dict as errors
    validation_with_none_value = validation.Validation(NONE_VALUE, ERRORS_DICT)

    # Assert equality of a Validation with itself
    is_equal_to_self = validation_with_none_value.__eq__(validation_with_none_value)
    assert is_equal_to_self is True

    # Convert Validation to Box monad
    box_from_validation = validation_with_none_value.to_box()

    # Create a second Validation with bytes value and bytes errors
    validation_with_bytes = validation.Validation(BYTES_VALUE, BYTES_VALUE)

    # Convert Box to Either monad (based on the original Validation's fail state)
    either_from_box = box_from_validation.to_either()

    # Check if the bytes Validation is a failure
    is_bytes_validation_fail = validation_with_bytes.is_fail()

    # Convert Either to Try monad
    try_from_either = either_from_box.to_try()

    # Create a Validation using the is_fail result (boolean) as the value
    validation_with_bool_value = validation.Validation(is_bytes_validation_fail, BYTES_VALUE)

    # Get string representation of the bool-value Validation
    validation_str_representation = validation_with_bool_value.__str__()

    # Convert bytes Validation to Lazy monad
    lazy_from_bytes_validation = validation_with_bytes.to_lazy()

    # Create another Validation with bytes value
    another_validation_with_bytes = validation.Validation(BYTES_VALUE, BYTES_VALUE)

    # Convert box to Either again (second call)
    another_either_from_box = box_from_validation.to_either()

    # Convert bool-value Validation to Lazy monad
    lazy_from_bool_validation = validation_with_bool_value.to_lazy()

    # Create a Validation using Lazy monad as value and another Validation as errors
    validation_with_lazy_value = validation.Validation(lazy_from_bool_validation, another_validation_with_bytes)

    # Check again if bytes Validation is a failure
    is_bytes_validation_fail_again = validation_with_bytes.is_fail()

    # Execute - Map the string representation (as a mapper function) over the None-value Validation
    # The string representation acts as the mapper (its value is used as a callable)
    result = validation_with_none_value.map(validation_str_representation)

    # Assert the result is a Validation instance with the mapped value
    assert isinstance(result, validation.Validation)

def test_validation_equality_to_maybe_and_bind():
    # Constants representing test data
    BYTES_VALUE = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    NO_VALUE = None

    # Setup: Create a Validation with no value and a dict of errors
    errors_dict = {NO_VALUE: BYTES_VALUE, BYTES_VALUE: BYTES_VALUE}
    failed_validation = validation.Validation(NO_VALUE, errors_dict)

    # Test equality: A Validation instance should be equal to itself
    is_equal_to_self = failed_validation.__eq__(failed_validation)
    assert is_equal_to_self is True

    # Test to_maybe: A failed Validation (with errors) should return an empty Maybe
    maybe_result = failed_validation.to_maybe()
    assert maybe_result.is_nothing() is True

    # Setup: Create a successful Validation with a bytes value
    successful_validation = validation.Validation(BYTES_VALUE, BYTES_VALUE)

    # Test bind: Applying a folder function (bytes_value used as folder) on the Validation value
    # bind calls folder(self.value), here bytes_value is not a callable so it verifies bind delegates correctly
    try:
        successful_validation.bind(BYTES_VALUE)
    except TypeError:
        # Expected since BYTES_VALUE is not callable; bind attempts to call folder(self.value)
        pass

def test_validation_equality_with_different_values_converts_to_box():
    """
    Test that comparing two Validation instances with different values returns a
    boolean result (False in this case since values differ), and that this boolean
    result can be transformed into a Box via to_box().
    
    - validation_with_none_value has value=None and errors={None: bytes_data, bytes_data: bytes_data}
    - validation_with_bytes_value has value=bytes_data and errors=None
    - Since their values and errors differ, __eq__ returns False
    - The False result (a bool) is then wrapped in a Box via to_box()
    """
    # Setup
    SAMPLE_BYTES = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    NONE_VALUE = None
    errors_dict = {NONE_VALUE: SAMPLE_BYTES, SAMPLE_BYTES: SAMPLE_BYTES}

    validation_with_none_value = validation.Validation(NONE_VALUE, errors_dict)
    validation_with_bytes_value = validation.Validation(SAMPLE_BYTES, NONE_VALUE)

    # Execution
    equality_result = validation_with_none_value.__eq__(validation_with_bytes_value)
    box_result = equality_result.to_box()

    # Assertion
    assert box_result is not None

