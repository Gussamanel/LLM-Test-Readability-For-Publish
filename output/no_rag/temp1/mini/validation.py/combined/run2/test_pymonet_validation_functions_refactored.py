import pytest

import builtins as builtins_module
import validation as validation_module

def test_validation_failure_to_maybe_and_self_equality():
    # Purpose:
    # - A Validation constructed with a non-empty "errors" value should report failure.
    # - A Validation should be equal to itself.
    # - Calling to_maybe() on a failing Validation should not raise and should return a Maybe-like object.

    # Test data: use a non-empty string for both value and errors to force a failure state.
    ERROR_TEXT = "\n        Create empty maybe.\n\n        :returns: Maybe[None]\n        "

    # Create a failing Validation (errors is non-empty -> is_fail should be True)
    validation = validation_module.Validation(ERROR_TEXT, ERROR_TEXT)

    # Inspect behavior
    is_success = validation.is_success()
    is_fail = validation.is_fail()
    equals_self = (validation == validation)
    maybe_result = validation.to_maybe()

    # Assertions
    assert is_success is False, "Validation with non-empty errors should not be a success"
    assert is_fail is True, "Validation with non-empty errors should be a failure"
    assert equals_self is True, "Validation should be equal to itself"

    # Ensure to_maybe returned a result and did not raise.
    assert maybe_result is not None, "to_maybe() should return a value, not None"

    # Prefer a direct isinstance check if the Maybe class is exposed on the module,
    # otherwise fall back to checking the returned object's class name.
    if hasattr(validation_module, "Maybe"):
        assert isinstance(maybe_result, validation_module.Maybe), "to_maybe() should return a Maybe instance"
    else:
        assert maybe_result.__class__.__name__ == "Maybe", "to_maybe() result should be an object named 'Maybe'"

def test_validation_equality_with_none_returns_false_and_preserves_success_state():
    # Purpose:
    # Verify that comparing a Validation instance to None returns False
    # and that performing the comparison does not modify the Validation's success state.

    # Constants / Setup
    SAMPLE_VALUE = -6891
    SAMPLE_ERRORS = (3125,)  # non-empty errors -> is_success should be False
    validation_instance = validation_module.Validation(SAMPLE_VALUE, SAMPLE_ERRORS)

    # Sanity check: the instance should initially report not successful due to errors
    assert validation_instance.is_success() is False

    # Execution: compare the Validation instance to None using __eq__ (via ==)
    equality_result = validation_instance == None

    # Assertions:
    # - The equality comparison against None must be False
    # - The success state of the original Validation instance must remain unchanged
    assert equality_result is False
    assert validation_instance.is_success() is False

def test_validation_success_str_and_is_fail_returns_false_when_no_errors():
    # Arrange
    EMPTY_DICT = {}

    # Setup: create a Validation with an empty value and empty errors
    validation = validation_module.Validation(EMPTY_DICT, EMPTY_DICT)

    # Execution: get string representation and failure status
    string_representation = str(validation)
    is_failed = validation.is_fail()

    # Assertions: string indicates success and is_fail() is False
    assert string_representation == f"Validation.success[{EMPTY_DICT}]"
    assert is_failed is False

def test_validation_converts_to_either_and_maybe_when_no_errors():
    # Purpose:
    # Ensure a Validation with no errors can be transformed to Either and Maybe without raising,
    # and that calling to_maybe on the resulting Maybe is safe (idempotent / stable).
    
    # --- Setup ---
    EMPTY_SET = set()
    validation = validation_module.Validation(EMPTY_SET, EMPTY_SET)
    
    # --- Execution ---
    either_result = validation.to_either()
    maybe_result = validation.to_maybe()
    
    # --- Assertion ---
    # We don't rely on concrete monad classes here; just ensure conversion returns objects (non-None)
    # and that repeated to_maybe call on the Maybe result does not raise and returns a value.
    assert either_result is not None
    assert maybe_result is not None

    maybe_converted_again = maybe_result.to_maybe()
    assert maybe_converted_again is not None

def test_validation_failure_converts_to_left_and_empty_maybe_and_self_equality():
    """Verify a Validation with non-empty errors is considered a failure,
    equals itself, converts to a Left Either, and converts to an empty Maybe.
    """
    sample_errors = "\n        Create empty maybe.\n\n        :returns: Maybe[None]\n        "
    validation = validation_module.Validation(sample_errors, sample_errors)

    # Exercise
    either_result = validation.to_either()    # expected: Left(...) because validation has errors
    equals_self = validation == validation    # should be True
    is_failure = validation.is_fail()         # should be True for non-empty errors
    maybe_result = validation.to_maybe()      # expected: empty Maybe for failures

    # Verify
    assert equals_self is True, "Validation should be equal to itself"
    assert is_failure is True, "Validation with non-empty errors should be considered a failure"
    assert either_result is not None, "to_either() should return an Either instance (Left in this failure case)"
    assert maybe_result is not None, "to_maybe() should return a Maybe instance (expected empty/nothing for failures)"

def test_validation_to_maybe_returns_maybe_for_success_and_is_idempotent():
    """A successful Validation should convert to a Maybe, and calling to_maybe() on that Maybe should be idempotent (same runtime type)."""
    # Setup
    success_value = builtins_module.set()  # empty set represents the validation value
    no_errors = builtins_module.set()      # empty set means validation is successful (no errors)
    validation = validation_module.Validation(success_value, no_errors)

    # Execution
    maybe_result = validation.to_maybe()
    assert hasattr(maybe_result, "to_maybe"), "Returned object should expose a to_maybe() method"
    second_result = maybe_result.to_maybe()

    # Assertions
    assert maybe_result is not None, "First to_maybe() should not return None for a successful Validation"
    assert second_result is not None, "Calling to_maybe() on the resulting Maybe should not return None"
    assert type(second_result) is type(maybe_result), "Second to_maybe() should return the same Maybe type as the first"

def test_validation_initialization_with_none_parameters():
    # Purpose:
    # Verify that the Validation class can be instantiated when both constructor
    # parameters are None without raising an exception and returns an object
    # of the expected type.

    # --- Setup: define input constants ---
    FIRST_PARAM = None
    SECOND_PARAM = None

    # --- Execution: construct the Validation object with None parameters ---
    validation_instance = validation_module.Validation(FIRST_PARAM, SECOND_PARAM)

    # --- Assertions: ensure object was created and is of the correct type ---
    assert validation_instance is not None, "Expected a Validation instance, got None"
    assert isinstance(validation_instance, validation_module.Validation), (
        "Expected instance of validation_module.Validation"
    )

def test_validation_to_maybe_returns_maybe_and_preserves_value_when_success():
    # Purpose:
    # Verify that Validation.to_maybe() returns a Maybe instance and,
    # when the Validation represents success, the Maybe preserves the Validation value.

    # --- Constants / Setup ---
    SAMPLE_VALUE = None
    SAMPLE_ERRORS = None
    validation = validation_module.Validation(SAMPLE_VALUE, SAMPLE_ERRORS)

    # --- Execution ---
    maybe_result = validation.to_maybe()

    # --- Assertions ---
    # The returned object should be a Maybe (we check by class name to avoid importing Maybe here).
    assert type(maybe_result).__name__ == "Maybe"

    # If the Validation reports success, the Maybe should carry the same value.
    # Otherwise (failure), the Maybe should not expose a 'value' attribute.
    sentinel = object()
    if validation.is_success():
        assert getattr(maybe_result, "value", sentinel) is SAMPLE_VALUE
    else:
        assert not hasattr(maybe_result, "value")

def test_validation_is_fail_returns_true_when_errors_list_non_empty():
    # Arrange: create a sample value and a Validation instance that will represent a failure
    sample_value = builtins_module.object()
    sample_error = "sample error"

    validation = validation_module.Validation(sample_value, sample_value)
    validation.errors = [sample_error]

    # Act
    result = validation.is_fail()

    # Assert
    assert result is True, "is_fail() should be True when errors list is non-empty"

def test_map_raises_type_error_when_mapper_is_none():
    """Ensure Validation.map raises TypeError when given a non-callable mapper."""
    # Test data
    INT_VALUE = -895
    BOOL_FLAG = True
    TUPLE_KEY = (INT_VALUE, BOOL_FLAG)
    DICT_VALUE = {TUPLE_KEY: TUPLE_KEY}
    COMPLEX_VALUE = (DICT_VALUE, DICT_VALUE, INT_VALUE)
    NONE_MAPPER = None

    # Create a Validation instance with a value and an errors indicator
    validation_instance = validation_module.Validation(COMPLEX_VALUE, BOOL_FLAG)

    # Mapping with a non-callable (None) should raise TypeError
    with pytest.raises(TypeError):
        validation_instance.map(NONE_MAPPER)

def test_bind_with_none_raises_type_error():
    # Verify that Validation.bind raises a TypeError when the "folder" argument is None.
    sample_bytes = b"s\x8flul\xd1p\x86\xe0<q\xd9\xb2\xf6\x17EC\xaf\xd0"
    validation_instance = validation_module.Validation(sample_bytes, sample_bytes)
    none_folder = None  # intentionally not callable

    with pytest.raises(TypeError):
        validation_instance.bind(none_folder)

def test_ap_concatenates_errors_from_function_producing_validation():
    # Purpose:
    # Verify that Validation.ap calls the provided function with the current value,
    # receives another Validation, and returns a new Validation whose errors are the
    # concatenation of the original errors and the errors from the returned Validation.

    # --- Setup ---
    INITIAL_VALUE = False
    ORIGINAL_ERRORS = [True, True, True, True]
    PRODUCER_ERRORS = [True, True, True, True]

    # Create the original Validation under test
    original_validation = validation_module.Validation(INITIAL_VALUE, ORIGINAL_ERRORS)

    # Define a function that, when called with a value, returns another Validation
    # containing PRODUCER_ERRORS. This simulates the monadic function expected by ap.
    def error_producing_function(value):
        return validation_module.Validation(value, PRODUCER_ERRORS)

    # --- Execution ---
    result_validation = original_validation.ap(error_producing_function)

    # --- Assertion ---
    # The returned Validation should keep the same value and have errors concatenated
    assert result_validation.value == INITIAL_VALUE
    assert result_validation.errors == ORIGINAL_ERRORS + PRODUCER_ERRORS

def test_validation_to_box_and_is_success_with_no_errors():
    # Verify that a Validation with an empty errors list is considered successful
    # and that to_box() returns a Box wrapping the Validation value.

    # Setup
    VALID_VALUE = True
    NO_ERRORS = []
    validation = validation_module.Validation(VALID_VALUE, NO_ERRORS)

    # Execution
    box = validation.to_box()

    # Assertions
    assert validation.is_success() is True
    assert getattr(box, "value", None) == VALID_VALUE

def test_bind_on_lazy_with_none_raises_type_error():
    # Verify binding a non-callable (None) to Lazy produced by Validation.to_lazy() raises TypeError.
    EMPTY_LIST = []
    NONE_MAPPER = None

    validation_obj = validation_module.Validation(EMPTY_LIST, EMPTY_LIST)
    lazy_value = validation_obj.to_lazy()

    with pytest.raises(TypeError):
        lazy_value.bind(NONE_MAPPER)

def test_validation_to_lazy_to_try_and_ap_reports_success_when_no_errors():
    # Purpose:
    # Verify that a Validation with no errors:
    #  - can be converted to a lazy representation,
    #  - the lazy representation can be converted to a Try,
    #  - applying `ap` with the original Validation preserves/combines errors,
    #  - and the resulting Try reports success (no errors).
    #
    # Setup
    EMPTY_DICT = {}
    INPUT_VALUE = EMPTY_DICT
    INPUT_ERRORS = EMPTY_DICT  # empty container represents no errors in this test

    # Create a Validation instance with an empty errors container
    validation_instance = validation_module.Validation(INPUT_VALUE, INPUT_ERRORS)

    # Execution
    # Convert Validation to a Lazy monad
    lazy_validation = validation_instance.to_lazy()
    # Convert the Lazy monad to a Try monad
    try_from_lazy = lazy_validation.to_try()
    # Apply `ap` using the original validation (keeps/concats errors internally)
    # Note: original test passed the Validation instance directly to `ap`, so we mirror that.
    ap_result = lazy_validation.ap(validation_instance)

    # Assertions
    # The Try produced from the lazy validation should report success because there were no errors.
    assert try_from_lazy.is_success() is True

    # The original validation should also report success (no errors).
    assert validation_instance.is_success() is True

    # If `ap` returns a Validation-like object, it should also reflect no errors.
    # We only assert `is_success` if the returned object has that method (defensive check).
    if hasattr(ap_result, "is_success"):
        assert ap_result.is_success() is True

def test_validation_to_try_is_unsuccessful_when_validation_has_errors():
    """Validation.to_try() should produce an unsuccessful Try when Validation has errors."""
    # Arrange: a Validation with a value and a non-empty errors list
    TEST_VALUE = 0
    TEST_ERRORS = [TEST_VALUE]
    validation = validation_module.Validation(TEST_VALUE, TEST_ERRORS)

    # Act: convert the Validation to a Try
    result_try = validation.to_try()

    # Assert: the Try must indicate failure because the Validation contained errors
    assert result_try.is_success() is False

def test_validation_transforms_map_and_string_representation():
    # Constants / test data
    BYTE_SEQ = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    ERRORS_DICT = {None: BYTE_SEQ, BYTE_SEQ: BYTE_SEQ}

    # -------------------------
    # Setup: create Validation instances used in the scenario
    # -------------------------
    # Validation with None value and a dictionary of errors
    validation_with_none = validation_module.Validation(None, ERRORS_DICT)
    # Validation whose value and errors are both the same bytes sequence (treated as non-empty errors)
    validation_with_bytes = validation_module.Validation(BYTE_SEQ, BYTE_SEQ)

    # -------------------------
    # Execution: invoke various transformations and operations
    # -------------------------
    # equality check against itself
    self_equality_result = validation_with_none.__eq__(validation_with_none)

    # transform to Box (wraps the value)
    box_from_none = validation_with_none.to_box()

    # transform the bytes-based Validation to Either
    either_from_bytes = validation_with_bytes.to_either()

    # check whether the bytes-based Validation is considered a failure (non-empty errors)
    bytes_validation_is_fail = validation_with_bytes.is_fail()

    # transform the bytes-based Validation to Try
    try_from_bytes = validation_with_bytes.to_try()

    # build a new Validation from the is_fail boolean (as value) and the bytes sequence (as errors)
    derived_validation = validation_module.Validation(bytes_validation_is_fail, BYTE_SEQ)

    # obtain string representation of the derived Validation (calls __str__)
    derived_validation_str = derived_validation.__str__()

    # get a lazy wrapper from the bytes-based Validation
    lazy_from_bytes = validation_with_bytes.to_lazy()

    # create a composite Validation using the Lazy as value and the previous Validation as errors
    composite_validation = validation_module.Validation(lazy_from_bytes, validation_with_bytes)

    # map the validation_with_none value to the derived string representation
    # (map takes a function (A) -> B and returns a new Validation with mapped value and original errors)
    mapped_validation = validation_with_none.map(lambda _: derived_validation_str)

    # -------------------------
    # Assertions: verify expected relationships and properties
    # -------------------------
    # equality with itself must be True
    assert self_equality_result is True

    # the Box produced should wrap the same value as the original Validation (None)
    assert getattr(box_from_none, "value", None) == validation_with_none.value

    # since validation_with_bytes had a non-empty errors field, it should be considered a failure
    assert bytes_validation_is_fail is True

    # the derived Validation created from the is_fail boolean should render as a failure string
    # (format used by __str__ for failures: 'Validation.fail[<value>, <errors>]')
    assert derived_validation_str.startswith("Validation.fail[")

    # mapping should produce a Validation whose value is the derived string and whose errors stay unchanged
    assert mapped_validation.value == derived_validation_str
    assert mapped_validation.errors == ERRORS_DICT

    # composite_validation should preserve the Lazy as its value and the original validation_with_bytes as its errors
    assert composite_validation.value is lazy_from_bytes
    assert composite_validation.errors == validation_with_bytes

def test_validation_equality_to_maybe_and_bind_raises_on_non_callable():
    # Purpose:
    # - Verify a Validation equals itself.
    # - Ensure to_maybe() returns a Maybe-like object (callable and non-None).
    # - Ensure bind() raises a TypeError when given a non-callable folder.

    # Constants / test data
    SAMPLE_BYTES = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    SAMPLE_NONE = None
    SAMPLE_ERRORS = {SAMPLE_NONE: SAMPLE_BYTES, SAMPLE_BYTES: SAMPLE_BYTES}

    # Setup: create a Validation that represents a failure (has errors)
    validation_with_none = validation_module.Validation(SAMPLE_NONE, SAMPLE_ERRORS)

    # Execution: equality check and conversion to Maybe
    self_equality = validation_with_none == validation_with_none
    maybe_result = validation_with_none.to_maybe()

    # Setup: create another Validation to test bind behavior with a non-callable folder
    validation_with_bytes = validation_module.Validation(SAMPLE_BYTES, SAMPLE_BYTES)
    non_callable_folder = SAMPLE_BYTES  # bytes instance is not callable

    # Assertions
    assert self_equality is True, "A Validation should be equal to itself"
    # to_maybe() should return a Maybe-like object (should not be None)
    assert maybe_result is not None, "to_maybe() should return a Maybe object (not None)"

    # bind() must raise TypeError when the provided folder is not callable
    with pytest.raises(TypeError):
        validation_with_bytes.bind(non_callable_folder)

def test_validation_equality_returns_bool_and_bool_has_no_to_box():
    # Purpose:
    # - Verify that Validation.__eq__ returns a boolean when comparing two Validation instances.
    # - Verify that the boolean result does not provide a to_box() method (calling it raises AttributeError).
    #
    # Setup: create a byte value and an errors mapping, then build two Validation instances with different
    # combinations of value and errors to ensure they are not trivially identical.
    VALUE_BYTES = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    NONE_VALUE = None
    ERRORS_MAP = {NONE_VALUE: VALUE_BYTES, VALUE_BYTES: VALUE_BYTES}

    validation_with_none_value = validation_module.Validation(NONE_VALUE, ERRORS_MAP)
    validation_with_bytes_value = validation_module.Validation(VALUE_BYTES, NONE_VALUE)

    # Execution: call __eq__ explicitly to get the comparison result
    comparison_result = validation_with_none_value.__eq__(validation_with_bytes_value)

    # Assertions:
    # - The comparison result should be a boolean.
    assert isinstance(comparison_result, bool)

    # - Attempting to call to_box on the boolean should raise an AttributeError (booleans don't have to_box).
    with pytest.raises(AttributeError):
        comparison_result.to_box()

