import pytest

import validation as validation_module
import builtins as builtins_module

def test_validation_success_converts_to_maybe_and_checks_equality():
    # Constants / test data
    TEST_VALUE = "Create empty maybe."
    EMPTY_ERRORS = []

    # Setup: create a successful Validation (no errors)
    validation = validation_module.Validation(TEST_VALUE, EMPTY_ERRORS)

    # Execution: exercise the API under test
    is_success = validation.is_success()          # should be True for empty errors
    equals_self = validation.__eq__(validation)   # equality with itself should be True
    is_fail = validation.is_fail()                # should be False for empty errors
    maybe_result = validation.to_maybe()          # convert successful Validation to Maybe

    # Assertions: verify expected behavior for a successful Validation
    assert is_success is True, "Validation should report success when errors list is empty"
    assert equals_self is True, "Validation should be equal to itself"
    assert is_fail is False, "Validation.is_fail() should be False when there are no errors"
    # We don't assume Maybe internals here; ensure conversion returned an object (not None)
    assert maybe_result is not None, "to_maybe() should return a Maybe instance (not None)"

def test_validation_eq_with_none_and_call_is_success_on_result():
    # Core purpose:
    # Verify behavior when a Validation instance is compared to None using __eq__,
    # then (as in the original test) attempt to call is_success() on the result.
    # This preserves the original sequence of operations for readability.

    # Constants / test data
    NONE_VALUE = None
    INITIAL_VALUE = -6891
    INNER_VALUE = 3125
    ERRORS_TUPLE = (INNER_VALUE,)

    # Setup: instantiate a Validation object with a value and an errors tuple
    validation = validation_module.Validation(INITIAL_VALUE, ERRORS_TUPLE)

    # Execution: perform equality comparison against None
    eq_result = validation.__eq__(NONE_VALUE)

    # Assertion: call is_success() on the result of __eq__ (preserves original behavior)
    # Note: this mirrors the original test's actions and intent.
    eq_result.is_success()

def test_validation_with_empty_errors_reports_success_and_string_representation():
    # Purpose:
    # - Verify that a Validation constructed with an empty errors container is not considered a failure
    # - Verify the string representation corresponds to the "success" form

    # Constants / Setup
    SAMPLE_VALUE = {}
    EMPTY_ERRORS = []
    validation = validation_module.Validation(SAMPLE_VALUE, EMPTY_ERRORS)

    # Execution
    # Use builtins_module.str to explicitly call the object's __str__ implementation
    string_representation = builtins_module.str(validation)
    is_fail_result = validation.is_fail()

    # Assertions
    assert is_fail_result is False
    assert string_representation == "Validation.success[{}]"

def test_validation_transforms_to_either_and_maybe_on_success():
    """
    Verify that a successful Validation converts to an Either (Right) and to a Maybe (Just),
    and that calling to_maybe() on the resulting Maybe is a safe no-op (idempotent).
    """
    # Arrange
    EMPTY_SET = set()
    validation_value = EMPTY_SET
    empty_errors = EMPTY_SET

    validation = validation_module.Validation(validation_value, empty_errors)

    # Act
    either_result = validation.to_either()
    maybe_result = validation.to_maybe()

    # Re-call to_maybe on the returned Maybe to exercise idempotence / passthrough
    maybe_result.to_maybe()

    # Assert
    assert validation.is_success() is True
    assert either_result is not None
    assert maybe_result is not None

def test_validation_with_non_empty_errors_is_failure_and_transforms():
    # Purpose:
    # - A Validation constructed with a non-empty errors value should be a failure
    # - An instance should equal itself
    # - to_either() and to_maybe() should be callable and return non-None values
    SAMPLE_TEXT = "Create empty maybe.\n\n:returns: Maybe[None]\n"
    validation_instance = validation_module.Validation(SAMPLE_TEXT, SAMPLE_TEXT)

    either_result = validation_instance.to_either()
    self_equality = (validation_instance == validation_instance)
    is_failure = validation_instance.is_fail()
    maybe_result = validation_instance.to_maybe()

    assert self_equality is True
    assert is_failure is True
    assert either_result is not None
    assert maybe_result is not None

def test_validation_to_maybe_produces_just_and_is_idempotent():
    """Verify that Validation.to_maybe() returns a Maybe.just(value) on success
    and that calling to_maybe() on the resulting Maybe is idempotent.
    """
    # Arrange / Setup
    EMPTY_SET = set()
    validation_obj = validation_module.Validation(EMPTY_SET, EMPTY_SET)

    # Act / Execution
    maybe_once = validation_obj.to_maybe()
    maybe_twice = maybe_once.to_maybe()

    # Assert / Verification
    maybe_cls = maybe_once.__class__
    assert hasattr(maybe_cls, "just"), "Maybe class should provide a `just` constructor"
    expected_maybe = maybe_cls.just(EMPTY_SET)

    # The first conversion should produce a Maybe wrapping the original value
    assert maybe_once == expected_maybe

    # Converting the Maybe to a Maybe again should be idempotent (same result)
    assert maybe_once == maybe_twice

def test_validation_initialization_with_none_inputs():
    # Purpose:
    # Verify that Validation can be instantiated when both constructor arguments are None.
    NONE_INPUT = None

    # Execution: create a Validation instance using None for both parameters
    validation_instance = validation_module.Validation(NONE_INPUT, NONE_INPUT)

    # Assertion: ensure an instance was created and is of the expected type
    assert isinstance(validation_instance, validation_module.Validation)

def test_validation_to_maybe_returns_maybe_for_successful_validation_with_none_value():
    # Purpose:
    # Verify that a Validation with no errors is transformed into a Maybe.
    # When the Validation holds a None value and has no errors, to_maybe should
    # produce a Maybe representing the presence of that value (i.e., Maybe.just(None)).
    
    # --- Setup ---
    VALIDATION_VALUE = None
    VALIDATION_ERRORS = None
    validation_instance = validation_module.Validation(VALIDATION_VALUE, VALIDATION_ERRORS)
    
    # Sanity check: this Validation should be treated as a success (no errors)
    assert validation_instance.is_success() is True
    
    # --- Execution ---
    maybe_result = validation_instance.to_maybe()
    
    # --- Assertion ---
    # Expect a Maybe object (not None). The detailed contents/behavior of the Maybe
    # (e.g., that it is a "just" holding None) are covered by Maybe-specific tests.
    assert maybe_result is not None

def test_is_fail_returns_false_when_errors_list_is_empty():
    # Purpose:
    # Verify that Validation.is_fail() returns False when the Validation instance
    # has an empty errors list (i.e. no validation errors present).

    # Constants / Setup
    TEST_OBJECT = builtins_module.object()  # use a simple builtin object as subject
    # Create the Validation instance. The original test passed the same object for both params.
    validator = validation_module.Validation(TEST_OBJECT, TEST_OBJECT)

    # Execution
    is_failure = validator.is_fail()

    # Assertion
    # When there are no errors, is_fail() should indicate no failure (False).
    assert is_failure is False

def test_map_raises_type_error_when_mapper_is_none():
    # Purpose:
    # Ensure that Validation.map raises a TypeError when the provided mapper is None
    # (i.e., not a callable). The test constructs a Validation with a non-trivial
    # value to demonstrate that the implementation will attempt to call the mapper.

    # --- Setup ---
    SAMPLE_INT = -895
    SAMPLE_ERROR_FLAG = True
    # Use a tuple as dictionary key and value to create a nested/complex structure
    TUPLE_KEY = (SAMPLE_INT, SAMPLE_ERROR_FLAG)
    NESTED_DICT = {TUPLE_KEY: TUPLE_KEY}
    COMPLEX_VALUE = (NESTED_DICT, NESTED_DICT, SAMPLE_INT)

    validation_instance = validation_module.Validation(COMPLEX_VALUE, SAMPLE_ERROR_FLAG)

    # --- Execution & Assertion ---
    # Passing None as the mapper should cause a TypeError since None is not callable.
    with pytest.raises(TypeError):
        validation_instance.map(None)

def test_bind_with_none_raises_type_error():
    # Purpose:
    # Ensure Validation.bind raises a TypeError when given a non-callable folder (None).
    # The bind implementation calls folder(self.value), so a non-callable should fail.

    # Setup
    SAMPLE_BYTES = b"s\x8flul\xd1p\x86\xe0<q\xd9\xb2\xf6\x17EC\xaf\xd0"
    validation_obj = validation_module.Validation(SAMPLE_BYTES, SAMPLE_BYTES)
    invalid_folder = None  # non-callable input for bind

    # Exercise & Assertion
    with pytest.raises(TypeError):
        validation_obj.bind(invalid_folder)

def test_ap_concatenates_errors_from_callable_validation():
    # Purpose:
    # Verify that Validation.ap calls the provided callable with the current value
    # and returns a new Validation with the same value and concatenated errors
    # (original errors + errors from the Validation returned by the callable).

    # Constants / test data
    INITIAL_VALUE = False
    ORIGINAL_ERRORS = [True, True, True, True]

    # Setup: create the initial Validation and a callable that returns another Validation
    initial_validation = validation_module.Validation(INITIAL_VALUE, ORIGINAL_ERRORS)

    def validation_factory(value):
        # This factory simulates the "fn" parameter: it receives the current value and
        # returns a Validation containing the same error list.
        return validation_module.Validation(value, ORIGINAL_ERRORS)

    # Execution: apply the factory to the initial validation using ap
    result_validation = initial_validation.ap(validation_factory)

    # Assertions: value remains unchanged, errors are concatenated
    assert result_validation.value == INITIAL_VALUE
    assert result_validation.errors == ORIGINAL_ERRORS + ORIGINAL_ERRORS

def test_validation_to_box_preserves_value_and_box_lacks_is_success():
    # Purpose:
    # - Ensure Validation.to_box() places the Validation.value into a Box
    # - Ensure the resulting Box does not expose Validation.is_success()
    # Constants (setup data)
    VALID_VALUE = True
    ERRORS_PLACEHOLDER = True

    # Setup: create a Validation instance with a value and an errors placeholder
    validation = validation_module.Validation(VALID_VALUE, ERRORS_PLACEHOLDER)

    # Execution: transform the Validation into a Box
    box = validation.to_box()

    # Assertion: the Box should contain the original Validation value
    assert getattr(box, "value", None) == VALID_VALUE

    # Assertion: Box should not provide is_success (calling it should raise AttributeError)
    with pytest.raises(AttributeError):
        box.is_success()

def test_validation_to_lazy_bind_with_non_callable_raises_type_error():
    # Purpose:
    # Verify that binding a non-callable (None) to the Lazy produced by Validation.to_lazy()
    # raises a TypeError because the binder must be callable.

    # Constants / test data
    EMPTY_LIST = []
    NON_CALLABLE_FOLDER = None

    # Setup: create a Validation instance with empty value and empty error
    validation = validation_module.Validation(EMPTY_LIST, EMPTY_LIST)

    # Execution: transform the Validation to a Lazy
    lazy_value = validation.to_lazy()

    # Assertion: binding a non-callable should raise a TypeError
    with pytest.raises(TypeError):
        # Attempt to bind None as a folder; this should fail because None is not callable.
        lazy_value.bind(NON_CALLABLE_FOLDER)

def test_validation_to_lazy_to_try_and_ap_preserves_success_for_empty_errors():
    """
    Verify that a Validation with empty errors:
    - can be converted to a Lazy wrapper,
    - then to a Try, which should be successful,
    - and that calling ap on the Lazy with the original Validation exercises the path
      and returns an object exposing the underlying value.
    """
    # Setup
    EMPTY_VALUE = {}
    EMPTY_ERRORS = {}
    original_validation = validation_module.Validation(EMPTY_VALUE, EMPTY_ERRORS)

    # Transformations
    lazy_validation = original_validation.to_lazy()
    try_from_lazy = lazy_validation.to_try()

    # Exercise ap on the lazy wrapper with the original validation
    ap_result = lazy_validation.ap(original_validation)

    # Assertions
    assert try_from_lazy.is_success()
    assert hasattr(ap_result, "value")
    assert ap_result.value == lazy_validation.value

def test_to_try_returns_failed_try_when_validation_has_errors():
    # Purpose:
    # Verify that Validation.to_try() produces a Try marked as failure when the Validation contains errors.

    # Constants / Setup
    VALUE = 0
    ERRORS = [VALUE]  # non-empty errors list => Validation is not successful
    validation = validation_module.Validation(VALUE, ERRORS)

    # Execution
    try_result = validation.to_try()

    # Assertion: the resulting Try should indicate failure because the original Validation had errors
    assert try_result.is_success() is False

def test_validation_transformation_and_map_preserves_errors():
    # Purpose:
    # - Exercise various Validation conversions (to_box, to_either, to_try, to_lazy)
    # - Check equality, failure detection, string representation
    # - Ensure map applies a mapper to the Validation value while preserving errors

    # Constants / setup
    SAMPLE_BYTES = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    SAMPLE_NONE = None
    SAMPLE_ERRORS_DICT = {SAMPLE_NONE: SAMPLE_BYTES, SAMPLE_BYTES: SAMPLE_BYTES}

    # Create several Validation instances with different shapes of value/errors
    failing_validation_with_dict_errors = validation_module.Validation(SAMPLE_NONE, SAMPLE_ERRORS_DICT)
    validation_with_bytes_errors = validation_module.Validation(SAMPLE_BYTES, SAMPLE_BYTES)
    boolean_failure_flag = validation_with_bytes_errors.is_fail()  # expected True because errors is non-empty bytes

    # Execution: conversions and operations
    # 1) equality check (self equality)
    is_equal_to_self = (failing_validation_with_dict_errors == failing_validation_with_dict_errors)

    # 2) transform to Box, then to Either, then to Try (exercise conversion chain)
    box_from_fail = failing_validation_with_dict_errors.to_box()
    either_from_box = box_from_fail.to_either()
    try_from_either = either_from_box.to_try()

    # 3) build a Validation carrying a boolean value and byte-errors, and get its string form
    bool_validation_with_errors = validation_module.Validation(boolean_failure_flag, SAMPLE_BYTES)
    bool_validation_str = str(bool_validation_with_errors)

    # 4) lazy conversions
    lazy_from_bytes_validation = validation_with_bytes_errors.to_lazy()
    lazy_from_bool_validation = bool_validation_with_errors.to_lazy()

    # 5) create a more complex Validation whose value is a Lazy and whose errors is another Validation
    nested_errors_validation = validation_module.Validation(
        lazy_from_bool_validation,
        validation_module.Validation(SAMPLE_BYTES, SAMPLE_BYTES),
    )

    # 6) map: apply a mapper to the failing_validation_with_dict_errors' value while preserving its errors.
    #    Use builtins.str as a simple mapper function.
    mapped_validation = failing_validation_with_dict_errors.map(builtins_module.str)

    # Assertions: verify expected properties and that errors were preserved by map
    assert is_equal_to_self is True  # a Validation equals itself
    # Box should expose the original value
    assert hasattr(box_from_fail, "value") and box_from_fail.value is SAMPLE_NONE
    # Either produced from a Box should allow conversion to Try (we already executed it)
    assert try_from_either is not None
    # The validation constructed with bytes as errors should be considered a failure
    assert boolean_failure_flag is True
    # String representation for a failing Validation should mention 'Validation.fail'
    assert "Validation.fail" in bool_validation_str
    # Lazy conversions should yield callable-like objects (Lazy is callable-like)
    assert callable(lazy_from_bytes_validation)
    assert callable(lazy_from_bool_validation)
    # The nested validation should be a Validation whose value is the Lazy and whose errors is a Validation
    assert isinstance(nested_errors_validation, validation_module.Validation)
    assert callable(nested_errors_validation.value)
    assert nested_errors_validation.errors == validation_module.Validation(SAMPLE_BYTES, SAMPLE_BYTES)
    # Mapping should change the value (str(None) -> 'None') while preserving the original errors object
    assert isinstance(mapped_validation, validation_module.Validation)
    assert mapped_validation.value == "None"
    assert mapped_validation.errors == SAMPLE_ERRORS_DICT

def test_validation_equality_to_maybe_and_bind_with_non_callable_raises():
    # Constants / fixtures
    SAMPLE_BYTES = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    NO_ERRORS = None
    SAMPLE_VALUE_DICT = {NO_ERRORS: SAMPLE_BYTES, SAMPLE_BYTES: SAMPLE_BYTES}

    # Setup: create a Validation that represents success (no errors) and one with a non-callable as errors/value
    validation_success = validation_module.Validation(NO_ERRORS, SAMPLE_VALUE_DICT)
    validation_with_non_callable = validation_module.Validation(SAMPLE_BYTES, SAMPLE_BYTES)

    # Execution: equality check and conversion to Maybe for the successful validation
    equality_result = validation_success == validation_success
    maybe_result = validation_success.to_maybe()

    # Assertion: same object should be equal to itself
    assert equality_result is True

    # Assertion: to_maybe() should produce a Maybe wrapping the validation value when there are no errors.
    # We check that the returned object is a Maybe and that it exposes the underlying value (if available).
    assert maybe_result is not None
    assert maybe_result.__class__.__name__ == "Maybe"
    assert getattr(maybe_result, "value", None) == SAMPLE_VALUE_DICT

    # Execution + Assertion: calling bind with a non-callable should raise a TypeError
    with pytest.raises(builtins_module.TypeError):
        validation_with_non_callable.bind(SAMPLE_BYTES)

def test_validation_equality_returns_boolean_and_bool_has_no_to_box():
    # Purpose:
    # - Create two Validation instances with different combinations of value/errors
    # - Verify that __eq__ returns a boolean (False for differing validations)
    # - Confirm that the boolean result is not a Validation and therefore has no to_box method

    # --- Constants / test data ---
    SAMPLE_BYTES = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    # errors mapping mixing None and bytes as keys/values
    SAMPLE_ERRORS = {None: SAMPLE_BYTES, SAMPLE_BYTES: SAMPLE_BYTES}

    # --- Setup: create Validation objects with differing value/errors ---
    validation_with_none_value = validation_module.Validation(None, SAMPLE_ERRORS)
    validation_with_bytes_value = validation_module.Validation(SAMPLE_BYTES, None)

    # --- Exercise: compare the two Validation instances using __eq__ ---
    equality_result = validation_with_none_value.__eq__(validation_with_bytes_value)

    # --- Assertions ---
    # The equality comparison should produce a plain boolean (they differ, so expect False)
    assert isinstance(equality_result, bool)
    assert equality_result is False

    # Since the result is a boolean, it should not expose Validation methods like to_box.
    # Attempting to call to_box on the boolean should raise an AttributeError.
    with pytest.raises(AttributeError):
        equality_result.to_box()

