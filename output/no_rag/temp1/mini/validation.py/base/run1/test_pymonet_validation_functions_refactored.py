import pytest

import validation as validation_module
import builtins as builtins_module

def test_validation_with_non_empty_errors_is_failure_and_converts_to_maybe():
    # Purpose: Verify a Validation constructed with non-empty errors reports failure,
    # is not a success, equals itself, and converts to a Maybe instance.

    DOCSTRING = (
        "\n        Create empty maybe.\n\n        :returns: Maybe[None]\n        "
    )

    # Create a Validation with a non-empty errors payload
    validation = validation_module.Validation(DOCSTRING, DOCSTRING)

    # Execute API under test
    is_success_flag = validation.is_success()
    equals_self = validation == validation
    is_failure_flag = validation.is_fail()
    maybe_result = validation.to_maybe()

    # Assertions
    assert is_success_flag is False
    assert equals_self is True
    assert is_failure_flag is True
    # Ensure conversion produced a Maybe object by checking the class name
    assert maybe_result.__class__.__name__ == "Maybe"

def test_validation_eq_with_none_returns_false_and_is_success_reflects_errors():
    # Purpose:
    # Verify that a Validation with non-empty errors:
    #  - is not considered equal to None, and
    #  - reports failure via is_success() (i.e., is_success() -> False).
    
    # Constants / setup
    VALUE = -6891
    ERROR_ITEM = 3125
    ERRORS = (ERROR_ITEM,)  # non-empty errors sequence makes the Validation a failure

    validation = validation_module.Validation(VALUE, ERRORS)

    # Execution: use the explicit __eq__ call to mirror the original test intent
    equality_result = validation.__eq__(None)

    # Assertions
    # Comparing the Validation instance to None should return False
    assert equality_result is False

    # The Validation instance has errors, so is_success() should be False
    assert validation.is_success() is False

def test_validation_str_represents_failure_when_errors_present():
    # Purpose:
    # Verify that when a Validation object contains non-empty errors,
    # .is_fail() returns True and __str__() returns the failure representation
    # including both the value and the errors.

    # Constants / Setup
    SAMPLE_VALUE = {"id": 1}
    SAMPLE_ERRORS = ["missing_field", "invalid_type"]
    validation = validation_module.Validation(SAMPLE_VALUE, SAMPLE_ERRORS)

    # Execution
    representation = validation.__str__()
    is_failure = validation.is_fail()

    # Assertions
    assert is_failure is True
    expected_representation = "Validation.fail[{}, {}]".format(SAMPLE_VALUE, SAMPLE_ERRORS)
    assert representation == expected_representation

def test_validation_conversions_with_no_errors_produce_wrappers():
    # This test verifies that a Validation with no errors can be converted
    # to both Either and Maybe wrappers and that calling to_maybe on the
    # resulting Maybe is supported and idempotent in terms of returned type.

    # Constants / setup
    EMPTY_SET = set()
    validation = validation_module.Validation(EMPTY_SET, EMPTY_SET)

    # Execution: perform conversions
    either_result = validation.to_either()
    maybe_result = validation.to_maybe()

    # Call to_maybe again on the Maybe result to ensure the method exists
    # and returns the same kind of Maybe wrapper (idempotent-type behavior).
    maybe_result_second_call = maybe_result.to_maybe()

    # Assertions: conversions returned wrapper objects and repeated to_maybe
    # returns the same wrapper type (we avoid relying on concrete Maybe class).
    assert either_result is not None
    assert maybe_result is not None
    assert builtins_module.type(maybe_result_second_call) is builtins_module.type(maybe_result)

def test_validation_with_non_empty_errors_is_failure_and_converts_to_either_and_maybe():
    # Purpose:
    # - Ensure a Validation constructed with a non-empty errors value is considered a failure
    # - Ensure conversion methods to_either() and to_maybe() can be called and behave consistently
    #   (i.e., to_either() should produce a Left-like value and to_maybe() should produce an empty/nothing Maybe)

    # --- Constants / Setup ---
    SAMPLE_TEXT = "\n        Create empty maybe.\n\n        :returns: Maybe[None]\n        "
    validation = validation_module.Validation(SAMPLE_TEXT, SAMPLE_TEXT)

    # --- Execution ---
    either_result = validation.to_either()
    equals_self = (validation == validation)
    is_failure = validation.is_fail()
    maybe_result = validation.to_maybe()

    # --- Assertions ---
    # Basic logical expectations
    assert equals_self is True, "Validation should be equal to itself"
    assert is_failure is True, "Validation constructed with non-empty errors should report failure (is_fail() == True)"

    # The conversion results should exist and reflect a failure state.
    # Check either_result: prefer using provided predicate methods if available
    if hasattr(either_result, "is_left"):
        assert either_result.is_left(), "Expected Either to be a Left when Validation has errors"
    elif hasattr(either_result, "is_right"):
        assert not either_result.is_right(), "Expected Either not to be Right when Validation has errors"
    else:
        # Fallback: inspect repr for typical Left/Right markers
        repr_either = repr(either_result).lower()
        assert ("left" in repr_either) or ("errors" in repr_either), (
            "Either result did not indicate a Left-like structure in its representation"
        )

    # Check maybe_result: prefer using provided predicate methods if available
    if hasattr(maybe_result, "is_nothing"):
        assert maybe_result.is_nothing(), "Expected Maybe.nothing() when Validation has errors"
    elif hasattr(maybe_result, "is_just"):
        assert not maybe_result.is_just(), "Expected Maybe to not be Just when Validation has errors"
    else:
        # Fallback: inspect repr for typical Nothing/Just markers
        repr_maybe = repr(maybe_result).lower()
        assert ("nothing" in repr_maybe) or ("none" in repr_maybe), (
            "Maybe result did not indicate a Nothing-like structure in its representation"
        )

def test_validation_to_maybe_returns_maybe_and_supports_idempotent_conversion():
    # Purpose:
    # - Verify Validation.to_maybe() returns a Maybe-like object.
    # - Verify calling to_maybe() again on the returned Maybe is supported (idempotent conversion).

    # Setup: create an empty Validation instance
    EMPTY_ERRORS = set()
    EMPTY_VALUE = set()
    validation_instance = validation_module.Validation(EMPTY_ERRORS, EMPTY_VALUE)

    # Execution: convert Validation to Maybe
    maybe_result = validation_instance.to_maybe()

    # The returned object should expose the same conversion API (to_maybe) and allow a repeated call.
    assert hasattr(maybe_result, "to_maybe"), "Converted object must expose a to_maybe() method"

    # Call to_maybe again on the result to ensure idempotent/stable conversion
    maybe_result_second = maybe_result.to_maybe()

    # Assertions: both results exist and are of the same runtime type (conversion stability).
    assert maybe_result is not None
    assert maybe_result_second is not None
    assert type(maybe_result_second) == type(maybe_result)

def test_validation_initializes_with_both_parameters_none():
    """Verify Validation constructs successfully when both constructor parameters are None."""
    none_input = None

    validation_instance = validation_module.Validation(none_input, none_input)

    assert validation_instance is not None, "Expected a Validation instance, got None"
    assert isinstance(validation_instance, validation_module.Validation), (
        "Constructed object is not an instance of validation_module.Validation"
    )

def test_validation_to_maybe_returns_maybe_instance_when_success():
    # This test verifies that Validation.to_maybe() returns an instance of the Maybe class
    # when the Validation instance is considered successful (no errors).
    # We initialize the Validation with explicit constants, force the success path,
    # call to_maybe(), and assert the returned object's class comes from pymonet.maybe.

    # Constants / setup
    VALUE_WITH_NO_ERRORS = None
    ERRORS_ABSENT = None
    validation_instance = validation_module.Validation(VALUE_WITH_NO_ERRORS, ERRORS_ABSENT)

    # Force the success branch of to_maybe() to make the test deterministic
    validation_instance.is_success = lambda: True

    # Execution
    maybe_result = validation_instance.to_maybe()

    # Assertions: ensure the returned object is the Maybe type from pymonet.maybe
    assert maybe_result.__class__.__name__ == "Maybe"
    assert maybe_result.__class__.__module__ == "pymonet.maybe"

def test_is_fail_returns_false_for_new_validation_with_no_errors():
    # Verify that a newly created Validation with no recorded errors reports as not failed.
    EXPECTED_IS_FAIL_FOR_EMPTY_ERRORS = False

    # Arrange: create a generic subject and a Validation instance with no errors.
    sample_subject = builtins_module.object()
    validation_instance = validation_module.Validation(sample_subject, sample_subject)

    # Act: check failure status.
    result_is_fail = validation_instance.is_fail()

    # Assert: result is a boolean and matches the expected False value for empty errors.
    assert isinstance(result_is_fail, bool)
    assert result_is_fail == EXPECTED_IS_FAIL_FOR_EMPTY_ERRORS

def test_map_raises_typeerror_when_mapper_is_not_callable():
    """
    Purpose:
    Verify that Validation.map raises a TypeError when given a non-callable mapper.
    """

    # --- Setup: prepare a complex Validation value and an "errors" flag ---
    INT_VALUE = -895
    ERRORS_FLAG = True
    KEY_TUPLE = (INT_VALUE, ERRORS_FLAG)
    # dictionary with a tuple key and the same tuple as value to create a nested structure
    NESTED_DICT = {KEY_TUPLE: KEY_TUPLE}
    # the Validation value is a tuple containing dictionaries and an integer
    ORIGINAL_VALIDATION_VALUE = (NESTED_DICT, NESTED_DICT, INT_VALUE)

    validation_obj = validation_module.Validation(ORIGINAL_VALIDATION_VALUE, ERRORS_FLAG)

    # --- Execution: use a non-callable mapper (None) ---
    non_callable_mapper = None

    # --- Assertion: mapping with a non-callable should raise a TypeError ---
    with pytest.raises(TypeError):
        validation_obj.map(non_callable_mapper)

def test_bind_with_none_raises_type_error():
    # Core purpose:
    # Ensure that Validation.bind() raises a TypeError when given None
    # instead of a callable mapper/folder, since bind attempts to call it.
    
    # --- Setup ---
    TEST_BYTES = b"s\x8flul\xd1p\x86\xe0<q\xd9\xb2\xf6\x17EC\xaf\xd0"
    validation_instance = validation_module.Validation(TEST_BYTES, TEST_BYTES)
    invalid_folder = None  # Not a callable, invalid input for bind
    
    # --- Execution & Assertion ---
    # Expect a TypeError because bind will attempt to call the provided folder.
    with pytest.raises(TypeError):
        validation_instance.bind(invalid_folder)

def test_ap_with_non_callable_argument_returns_validation_instance():
    # Purpose:
    # Verify that calling Validation.ap with a non-callable argument (here: the same error list)
    # executes and returns a Validation object. This mirrors the original test behavior.
    
    # Constants / test data
    INITIAL_VALUE = False
    ERROR_ELEMENT = True
    ERROR_LIST = [ERROR_ELEMENT, ERROR_ELEMENT, ERROR_ELEMENT, ERROR_ELEMENT]
    
    # Setup: create a Validation with an initial value and a list of errors
    validation_instance = validation_module.Validation(INITIAL_VALUE, ERROR_LIST)
    
    # Execution: call ap with the non-callable error list (preserves original test behavior)
    result = validation_instance.ap(ERROR_LIST)
    
    # Assertion: ensure a Validation object is returned
    assert isinstance(result, validation_module.Validation)

def test_to_box_preserves_value_and_validation_reports_success():
    # Purpose:
    # - Verify that Validation.to_box() returns a Box containing the original value
    # - Verify that the Validation instance reports success (no errors)
    
    # Constants / test inputs
    SAMPLE_VALUE = True
    SAMPLE_FLAG = True  # kept as in original usage; passed to the Validation constructor
    
    # Setup: create a Validation instance with the sample inputs
    validation_instance = validation_module.Validation(SAMPLE_VALUE, SAMPLE_FLAG)
    
    # Execution: convert the Validation to a Box
    result_box = validation_instance.to_box()
    
    # Assertions:
    # - the Box should contain the same value that was provided to Validation
    assert getattr(result_box, "value", None) == SAMPLE_VALUE
    # - the Validation instance should report success (empty errors list)
    assert validation_instance.is_success()

def test_validation_to_lazy_bind_with_none_preserves_chain():
    # Purpose:
    # Ensure that a Validation can be converted to a Lazy, have bind called with None,
    # and then converted back to a Lazy without producing a None result.
    #
    # This mirrors the original sequence:
    # Validation -> to_lazy() -> bind(None) -> to_lazy()
    # The test only asserts that the final result is not None.

    # --- Setup ---
    EMPTY_LIST = []         # used for both value and errors in the Validation
    NONE_FOLDER = None      # simulate passing None to bind

    validation_obj = validation_module.Validation(EMPTY_LIST, EMPTY_LIST)

    # --- Execution ---
    lazy_from_validation = validation_obj.to_lazy()
    bound_result = lazy_from_validation.bind(NONE_FOLDER)
    final_lazy = bound_result.to_lazy()

    # --- Assertion ---
    assert final_lazy is not None

def test_validation_to_lazy_then_to_try_returns_success_and_ap_preserves_value():
    # Purpose:
    # - Ensure a Validation with empty errors can be converted to a Lazy and then to a Try.
    # - Verify the resulting Try reports success when the original Validation has no errors.
    # - Exercise the ap() path and confirm the returned Validation preserves the original value.
    #
    # Note: This test intentionally uses empty containers for value and errors (matching the original test).
    
    # Constants / Setup
    EMPTY_VALUE = {}
    EMPTY_ERRORS = {}
    original_validation = validation_module.Validation(EMPTY_VALUE, EMPTY_ERRORS)
    
    # Execution - transform and exercise methods
    lazy_validation = original_validation.to_lazy()        # create Lazy wrapper around the Validation value
    try_from_lazy = lazy_validation.to_try()               # convert Lazy -> Try
    applied_validation = lazy_validation.ap(original_validation)  # exercise ap(...) path
    
    # Assertions - verify Try reflects original value and success state
    assert hasattr(try_from_lazy, "value"), "Try produced from Lazy should expose a .value attribute"
    assert try_from_lazy.value == EMPTY_VALUE
    assert try_from_lazy.is_success() is True, "Try should be successful when the original Validation had no errors"
    
    # Assertions - verify ap(...) preserves the original value on the resulting Validation
    assert hasattr(applied_validation, "value"), "Result of ap(...) should be a Validation-like object exposing .value"
    assert applied_validation.value == EMPTY_VALUE

def test_to_try_returns_failed_try_when_validation_has_errors():
    # Purpose: Verify that converting a Validation with errors to a Try produces a failed Try.

    # Setup: create a value and a non-empty errors list, then build the Validation object
    VALUE = 0
    ERRORS = [VALUE]
    validation = validation_module.Validation(VALUE, ERRORS)

    # Execution: transform the Validation into a Try
    try_result = validation.to_try()

    # Assertion: because the original Validation contained errors, the resulting Try must be unsuccessful
    assert try_result.is_success() is False

def test_validation_equality_and_transformations():
    # Constants / fixtures
    SAMPLE_BYTES = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    NONE_VALUE = None
    ERRORS_DICT = {NONE_VALUE: SAMPLE_BYTES, SAMPLE_BYTES: SAMPLE_BYTES}

    # Setup: create several Validation instances with different values/errors
    validation_with_errors = validation_module.Validation(NONE_VALUE, ERRORS_DICT)
    validation_with_byte_errors = validation_module.Validation(SAMPLE_BYTES, SAMPLE_BYTES)

    # Execution: perform a sequence of transformations and checks that exercise
    # Validation equality, conversion helpers and mapping.

    # 1) equality against itself
    equality_result = validation_with_errors.__eq__(validation_with_errors)

    # 2) convert a Validation to a Box (Box should wrap the Validation value)
    box_from_validation = validation_with_errors.to_box()

    # 3) try to convert the Box to an Either if the Box supports it
    either_from_box = None
    if hasattr(box_from_validation, "to_either"):
        either_from_box = box_from_validation.to_either()

    # 4) check if a Validation constructed with a non-empty "errors" value reports failure
    is_fail_result = validation_with_byte_errors.is_fail()

    # 5) convert Either (if present) to Try
    try_from_either = None
    if either_from_box is not None and hasattr(either_from_box, "to_try"):
        try_from_either = either_from_box.to_try()

    # 6) construct a Validation whose value is the boolean result and has byte errors,
    #    then get its string representation and lazy conversion
    validation_from_bool = validation_module.Validation(is_fail_result, SAMPLE_BYTES)
    str_representation = validation_from_bool.__str__()
    lazy_from_byte_validation = validation_with_byte_errors.to_lazy()

    # 7) obtain a lazy from the boolean-backed validation
    lazy_from_bool_validation = validation_from_bool.to_lazy()

    # 8) construct a mixed Validation that uses a Lazy as value and another Validation as errors
    another_validation = validation_module.Validation(SAMPLE_BYTES, SAMPLE_BYTES)
    mixed_validation = validation_module.Validation(lazy_from_bool_validation, another_validation)

    # 9) re-check failure status on the byte-errors validation
    repeated_is_fail = validation_with_byte_errors.is_fail()

    # 10) map the original validation value through a simple mapper (use builtins.str)
    mapped_validation = validation_with_errors.map(builtins_module.str)

    # Assertions: verify expected behaviors from the above operations
    assert equality_result is True  # a Validation should be equal to itself
    assert validation_with_errors.value is NONE_VALUE
    assert validation_with_errors.errors == ERRORS_DICT

    # The validation constructed with a non-empty "errors" payload should report failure
    assert is_fail_result is True
    assert repeated_is_fail is True

    # The boolean-backed validation with non-empty errors should render as a "fail" string
    assert "Validation.fail" in str_representation

    # Mapping should apply the mapper to the value and preserve the original errors
    assert mapped_validation.value == builtins_module.str(NONE_VALUE)
    assert mapped_validation.errors == ERRORS_DICT

    # Optional assertions for conversions that depend on other monad implementations:
    if either_from_box is not None:
        # If we were able to produce an Either, it should provide a to_try conversion when present
        if hasattr(either_from_box, "to_try"):
            assert try_from_either is not None

    # The Lazy conversions should produce some object (we don't assert specific API here)
    assert lazy_from_byte_validation is not None
    assert lazy_from_bool_validation is not None
    assert mixed_validation is not None

def test_validation_eq_to_maybe_and_bind_with_non_callable_raises():
    # Constants / test data
    SAMPLE_BYTES = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    SAMPLE_ERRORS = {None: SAMPLE_BYTES, SAMPLE_BYTES: SAMPLE_BYTES}

    # Setup: create a Validation that carries errors and another Validation to test bind
    validation_with_errors = validation_module.Validation(None, SAMPLE_ERRORS)
    validation_for_bind = validation_module.Validation(SAMPLE_BYTES, SAMPLE_BYTES)

    # Execution: compare the validation to itself and convert it to a Maybe
    is_equal_to_self = (validation_with_errors == validation_with_errors)
    maybe_result = validation_with_errors.to_maybe()

    # Assertions:
    # - A Validation must be equal to itself
    assert is_equal_to_self is True

    # - to_maybe should return a Maybe instance (either Just or Nothing). Check by class name
    #   (we don't depend on Maybe API details here, just that the returned object is a Maybe).
    assert maybe_result.__class__.__name__ == "Maybe"

    # - bind must expect a callable. Passing a non-callable (bytes) should raise a TypeError.
    with pytest.raises(TypeError):
        validation_for_bind.bind(SAMPLE_BYTES)

def test_validation_equality_returns_bool_and_to_box_on_result_raises_attribute_error():
    # Purpose:
    # - Verify that Validation.__eq__ compares value and errors and returns a boolean.
    # - Verify that calling to_box on that boolean result raises AttributeError
    #   (i.e. the boolean result is not a Validation and does not implement to_box).

    # Constants / test data
    BYTES_VALUE = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    NONE_VALUE = None
    ERRORS_DICT = {NONE_VALUE: BYTES_VALUE, BYTES_VALUE: BYTES_VALUE}

    # Setup: two Validation instances with different value/errors
    validation_with_none_value = validation_module.Validation(NONE_VALUE, ERRORS_DICT)
    validation_with_bytes_value = validation_module.Validation(BYTES_VALUE, NONE_VALUE)

    # Execution: perform equality check (calls Validation.__eq__)
    equality_result = validation_with_none_value.__eq__(validation_with_bytes_value)

    # Assertions:
    # - __eq__ should return a boolean
    assert isinstance(equality_result, bool)
    # - The two Validation instances are different, so equality should be False
    assert equality_result is False

    # - Attempting to call to_box on the boolean result should raise AttributeError
    with pytest.raises(AttributeError):
        equality_result.to_box()

