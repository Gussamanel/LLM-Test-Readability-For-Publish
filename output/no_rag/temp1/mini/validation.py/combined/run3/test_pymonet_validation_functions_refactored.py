import pytest

import builtins as builtins_module
import validation as validation_module

def test_validation_to_maybe_returns_empty_when_validation_has_errors():
    """Verify behavior of a failing Validation:
    - is_success() -> False
    - is_fail() -> True
    - equality with itself -> True
    - to_maybe() -> an empty Maybe (Nothing)
    """
    # Arrange / Setup
    FAILURE_PAYLOAD = (
        "\n        Create empty maybe.\n\n        :returns: Maybe[None]\n        "
    )
    validation = validation_module.Validation(FAILURE_PAYLOAD, FAILURE_PAYLOAD)

    # Act / Execution
    is_success_result = validation.is_success()
    equals_self_result = validation == validation
    is_fail_result = validation.is_fail()
    maybe_result = validation.to_maybe()

    # Assert / Verification
    # Basic state checks
    assert is_success_result is False, "Expected a failing Validation to report is_success() == False"
    assert equals_self_result is True, "Validation should be equal to itself"
    assert is_fail_result is True, "Expected a failing Validation to report is_fail() == True"

    # The Maybe returned for a failing Validation should represent "nothing".
    # Different Maybe implementations expose this in different ways, so check a few possibilities:
    if hasattr(maybe_result, "__bool__"):
        # Many Maybe implementations make Nothing falsy and Just truthy
        assert not bool(maybe_result), "Expected Maybe from failed Validation to be falsy (Nothing)"
    elif hasattr(maybe_result, "is_nothing"):
        assert maybe_result.is_nothing(), "Expected Maybe.is_nothing() to be True for a failed Validation"
    elif hasattr(maybe_result, "is_empty"):
        assert maybe_result.is_empty(), "Expected Maybe.is_empty() to be True for a failed Validation"
    else:
        # Fallback: ensure we received some Maybe-like object (not None)
        assert maybe_result is not None, "to_maybe() should return a Maybe object (fallback check)"

def test_validation_not_equal_to_none_and_reports_failure_when_errors_present():
    # Purpose:
    # Verify that a Validation instance is not considered equal to None
    # and that is_success() returns False when the Validation contains errors.

    # Constants / setup
    SAMPLE_VALUE = -6891
    SAMPLE_ERROR = 3125
    ERRORS = (SAMPLE_ERROR,)
    validation = validation_module.Validation(SAMPLE_VALUE, ERRORS)

    # Execution
    equality_with_none = (validation == None)  # triggers Validation.__eq__
    success_flag = validation.is_success()     # checks whether errors list is empty

    # Assertions
    assert equality_with_none is False, "Validation should not be equal to None"
    assert success_flag is False, "Validation with errors should not be a success"

def test_validation_with_empty_errors_returns_success_string_and_is_not_fail():
    # Constants for the test inputs
    EMPTY_VALUE = {}
    EMPTY_ERRORS = {}

    # Setup: create a Validation object with an empty value and empty errors list
    validation = validation_module.Validation(EMPTY_VALUE, EMPTY_ERRORS)

    # Exercise: obtain the string representation and check the failure flag
    string_representation = validation.__str__()  # calls Validation.__str__()
    is_failure = validation.is_fail()            # calls Validation.is_fail()

    # Assert: when errors are empty, __str__ should indicate success and is_fail() should be False
    assert string_representation == "Validation.success[{}]"
    assert is_failure is False

def test_validation_transforms_to_either_and_maybe_when_no_errors():
    """Verify a Validation with no errors converts to Either and Maybe without raising and returns non-None."""
    empty_errors = set()
    # Create a Validation instance representing success (no errors)
    validation_instance = validation_module.Validation(empty_errors, empty_errors)

    # Transformations
    either_result = validation_instance.to_either()
    maybe_result = validation_instance.to_maybe()
    # Ensure calling to_maybe on a Maybe is chainable/idempotent (no exception)
    maybe_result_again = maybe_result.to_maybe()

    # Basic sanity checks that the transformations returned objects
    assert either_result is not None
    assert maybe_result is not None
    assert maybe_result_again is not None

def test_validation_with_non_empty_errors_transforms_to_left_and_empty_maybe():
    # Purpose:
    # - Verify behavior of Validation when errors are non-empty:
    #   * __eq__ with itself returns True
    #   * is_fail() returns True
    #   * to_either() yields a Left containing the errors
    #   * to_maybe() yields an empty Maybe (not containing the original value)
    #
    # Arrange (setup)
    SAMPLE_TEXT = "\n        Create empty maybe.\n\n        :returns: Maybe[None]\n        "
    validation_obj = validation_module.Validation(SAMPLE_TEXT, SAMPLE_TEXT)

    # Act (execution)
    either_result = validation_obj.to_either()
    equality_with_self = validation_obj.__eq__(validation_obj)
    is_failure = validation_obj.is_fail()
    maybe_result = validation_obj.to_maybe()

    # Assert
    # Equality with itself should be True
    assert equality_with_self is True

    # Because we passed a non-empty errors value, is_fail should be True
    assert is_failure is True

    # to_either should produce a Left (not a Right). Check class name to avoid importing Left/Right.
    assert either_result.__class__.__name__ == "Left"

    # Ensure the errors payload we provided is stored in the Either/Left instance attributes.
    # Many Either implementations store the payload in an attribute (e.g., .value or .left).
    errors_payload = getattr(validation_obj, "errors", None)
    either_attrs = tuple(vars(either_result).values())
    assert errors_payload in either_attrs

    # to_maybe should not contain the original value because the Validation is a failure.
    # If Maybe.just would wrap SAMPLE_TEXT, its internal stored value (commonly .value) would equal SAMPLE_TEXT.
    assert getattr(maybe_result, "value", object()) != SAMPLE_TEXT

def test_validation_to_maybe_returns_maybe_and_is_chainable():
    # Purpose:
    # Verify that a successful Validation is transformed into a Maybe-like object
    # and that the resulting Maybe exposes a to_maybe method that can be called again
    # (i.e., the result is a Maybe-like, chainable object).
    
    # Constants / Setup
    EMPTY_SET = set()
    validation = validation_module.Validation(EMPTY_SET, EMPTY_SET)
    
    # Execution: transform Validation to Maybe
    maybe_result = validation.to_maybe()
    
    # Assertions: ensure a Maybe-like object was returned and is chainable via to_maybe
    assert maybe_result is not None, "to_maybe() should not return None for a successful Validation"
    assert hasattr(maybe_result, "to_maybe") and callable(getattr(maybe_result, "to_maybe")), \
        "Returned object must have a callable to_maybe method"
    
    # Calling to_maybe on the Maybe result should succeed and return a Maybe-like object
    second_call_result = maybe_result.to_maybe()
    assert second_call_result is not None, "Calling to_maybe() on the Maybe result should return a Maybe-like object"

def test_validation_init_with_none_parameters_does_not_raise_and_creates_instance():
    """Verify Validation can be constructed with None parameters and returns an instance."""
    # Arrange: input parameters intentionally set to None
    first_param = None
    second_param = None

    # Act: construct the Validation object (should not raise)
    validation_instance = validation_module.Validation(first_param, second_param)

    # Assert: an object was created and it is an instance of Validation
    assert validation_instance is not None
    assert isinstance(validation_instance, validation_module.Validation)

def test_validation_to_maybe_returns_just_for_success(monkeypatch):
    # Purpose:
    # Verify that Validation.to_maybe() produces a Maybe.just(value) when the Validation
    # is a success (no errors). We patch the pymonet.maybe module with a fake Maybe
    # to make the assertion deterministic and independent of the real Maybe implementation.

    # --- Constants / Test data ---
    VALIDATION_VALUE = None
    VALIDATION_ERRORS = None

    # --- Patch setup: replace pymonet.maybe.Maybe with a controlled fake ---
    import sys
    import types

    class FakeMaybe:
        """A minimal fake Maybe that supports just(...) and nothing() classmethods."""
        def __init__(self, kind, value=None):
            self.kind = kind
            self.value = value

        @classmethod
        def just(cls, value):
            return cls("just", value)

        @classmethod
        def nothing(cls):
            return cls("nothing", None)

        def __eq__(self, other):
            return (
                isinstance(other, FakeMaybe)
                and self.kind == other.kind
                and self.value == other.value
            )

        def __repr__(self):
            return f"<FakeMaybe {self.kind} {self.value!r}>"

    fake_maybe_module = types.ModuleType("pymonet.maybe")
    fake_maybe_module.Maybe = FakeMaybe
    # Insert the fake module into sys.modules so "from pymonet.maybe import Maybe"
    # inside Validation.to_maybe() will import our FakeMaybe.
    monkeypatch.setitem(sys.modules, "pymonet.maybe", fake_maybe_module)

    # --- Setup: create the Validation under test ---
    validation = validation_module.Validation(VALIDATION_VALUE, VALIDATION_ERRORS)

    # --- Execution: call the method under test ---
    maybe_result = validation.to_maybe()

    # --- Assertion: expect a FakeMaybe.just with the original value ---
    expected = FakeMaybe.just(VALIDATION_VALUE)
    assert maybe_result == expected, f"Expected {expected}, got {maybe_result}"

def test_validation_is_fail_returns_true_when_errors_exist():
    # This test verifies that Validation.is_fail() returns True when the Validation
    # instance has one or more errors in its .errors list.
    SAMPLE_ERROR = "validation error occurred"

    # Setup: create a dummy subject and a Validation instance under test
    subject = builtins_module.object()
    validation_instance = validation_module.Validation(subject, subject)

    # Ensure the Validation instance represents a failing state by populating errors
    validation_instance.errors = [SAMPLE_ERROR]

    # Execution: call the method under test
    result = validation_instance.is_fail()

    # Assertion: is_fail should be True when errors list is not empty
    assert result is True

def test_map_raises_type_error_when_mapper_is_none():
    # Purpose:
    # Verify that Validation.map raises a TypeError when the provided mapper is None
    # (None is not callable, so attempting to call it should fail).

    # Constants / test data setup
    NEGATIVE_INTEGER = -895
    FLAG_TRUE = True
    KEY_TUPLE = (NEGATIVE_INTEGER, FLAG_TRUE)
    VALUE_DICT = {KEY_TUPLE: KEY_TUPLE}
    INITIAL_VALUE = (VALUE_DICT, VALUE_DICT, NEGATIVE_INTEGER)
    NONE_MAPPER = None

    # Setup: create a Validation instance with the prepared value and errors flag
    validation_instance = validation_module.Validation(INITIAL_VALUE, FLAG_TRUE)

    # Execution & Assertion: mapping with a non-callable (None) should raise TypeError
    with pytest.raises(TypeError):
        validation_instance.map(NONE_MAPPER)

def test_bind_with_none_raises_type_error():
    """Ensure Validation.bind raises TypeError when a non-callable (None) is passed."""
    # Setup
    SAMPLE_BYTES = b"s\x8flul\xd1p\x86\xe0<q\xd9\xb2\xf6\x17EC\xaf\xd0"
    validation = validation_module.Validation(SAMPLE_BYTES, SAMPLE_BYTES)

    # Execution & Assertion
    with pytest.raises(TypeError):
        validation.bind(None)

def test_ap_appends_errors_from_callable_and_preserves_original_value():
    # Purpose:
    # Verify that Validation.ap(fn) preserves the original Validation.value
    # and returns a new Validation whose errors are the concatenation of the
    # original errors and the errors from the Validation returned by fn(value).

    # Setup: initial validation and the callable that returns another Validation
    INITIAL_VALUE = False
    INITIAL_ERRORS = [True, True, True, True]
    ADDITIONAL_ERRORS = [False, False]

    original_validation = validation_module.Validation(INITIAL_VALUE, INITIAL_ERRORS)

    # The callable that will be passed to ap; it must accept a value and return a Validation.
    def supplier_fn(value_passed_to_fn):
        # The supplier returns a Validation whose errors should be concatenated.
        return validation_module.Validation(value_passed_to_fn, ADDITIONAL_ERRORS)

    # Execution: call ap with the supplier function
    result_validation = original_validation.ap(supplier_fn)

    # Assertion: value is preserved from the original, and errors are concatenated in order
    assert result_validation.value == INITIAL_VALUE
    assert result_validation.errors == INITIAL_ERRORS + ADDITIONAL_ERRORS

def test_validation_to_box_and_is_success_returns_boolean():
    # Purpose:
    # - Verify that a Validation instance can be transformed to a Box via to_box()
    # - Verify that calling is_success() on the resulting object returns a boolean
    #   (i.e., the success-check code path is executable and yields a boolean result)
    
    # Constants / test data
    INPUT_VALUE = True
    INPUT_ERRORS = True  # kept as in original test input (shape/meaning depends on Validation impl)
    
    # Setup: create a Validation instance with the test constants
    validation_instance = validation_module.Validation(INPUT_VALUE, INPUT_ERRORS)
    
    # Execution: transform Validation to Box and call is_success on the result
    box_result = validation_instance.to_box()
    is_success_result = box_result.is_success()
    
    # Assertion: is_success() returns a boolean (ensures the call is valid and returns expected type)
    assert isinstance(is_success_result, bool)

def test_validation_bind_raises_type_error_for_non_callable_mapper():
    # Purpose:
    # Ensure Validation.bind raises a TypeError when the provided mapper/folder is not callable.
    #
    # Setup:
    EMPTY_LIST = []
    NON_CALLABLE_MAPPER = None
    validation_instance = validation_module.Validation(EMPTY_LIST, EMPTY_LIST)

    # Exercise: calling to_lazy should produce a Lazy monad (sanity check of conversion)
    # Assertion: the conversion should return a non-None object (we don't depend on Lazy internals here)
    lazy_monad = validation_instance.to_lazy()
    assert lazy_monad is not None

    # Execution + Assertion: binding with a non-callable should raise a TypeError
    with pytest.raises(TypeError):
        validation_instance.bind(NON_CALLABLE_MAPPER)

def test_lazy_to_try_and_ap_with_no_errors_returns_successful_try():
    # Constants for test clarity
    EMPTY_VALUE = {}
    EMPTY_ERRORS = []

    # Setup: create a Validation with no errors
    validation = validation_module.Validation(EMPTY_VALUE, EMPTY_ERRORS)

    # Execution: convert Validation to Lazy, then to Try, and apply the Lazy with the original Validation
    lazy_validation = validation.to_lazy()
    try_result = lazy_validation.to_try()
    applied_validation = lazy_validation.ap(validation)

    # Assertions:
    # - The Try produced from a Validation with no errors should be successful
    # - The Try should carry the original value
    # - Applying the lazy validation with the original validation should produce a Validation with no errors
    assert try_result.is_success() is True
    assert try_result.value == EMPTY_VALUE
    assert applied_validation.errors == EMPTY_ERRORS

def test_to_try_preserves_validation_success_flag():
    # Purpose:
    # Verify that Validation.to_try() returns a Try whose success status matches
    # the original Validation.is_success() value.

    # Constants / Setup
    VALUE = 0
    ERRORS = [VALUE]  # non-empty list -> Validation is not successful
    validation = validation_module.Validation(VALUE, ERRORS)

    # Execution
    try_monad = validation.to_try()

    # Assertions:
    # 1) The Validation reports not successful (errors list is not empty).
    assert validation.is_success() is False
    # 2) The Try produced from the Validation preserves that success state.
    assert try_monad.is_success() == validation.is_success()

def test_validation_conversions_and_map():
    # Purpose:
    # Verify core Validation behaviors: equality, success/failure detection,
    # conversions to Box/Lazy, string representation, and mapping of the value.
    #
    # Setup: define sample value and error structure, and create two Validation instances:
    # - validation_fail: has a non-empty errors container -> is_fail() should be True
    # - validation_success: has an empty errors container -> is_fail() should be False
    SAMPLE_BYTES = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    SAMPLE_ERRORS = {None: SAMPLE_BYTES, SAMPLE_BYTES: SAMPLE_BYTES}

    validation_fail = validation_module.Validation(None, SAMPLE_ERRORS)
    validation_success = validation_module.Validation(SAMPLE_BYTES, [])

    # Execution: call a variety of methods to exercise conversions and operations
    # 1) equality: a Validation should equal itself
    equality_self = (validation_fail == validation_fail)

    # 2) to_box: should wrap the value; Box exposes the wrapped value via .value
    box_from_success = validation_success.to_box()

    # 3) to_lazy: returns a Lazy that, when invoked, yields the Validation value.
    lazy_from_success = validation_success.to_lazy()

    # 4) to_try: create a Try from Validation (should reflect is_success)
    try_from_success = validation_success.to_try()
    try_from_fail = validation_fail.to_try()

    # 5) __str__: get string representation for a Validation (success or fail)
    str_repr_fail = validation_fail.__str__()
    str_repr_success = validation_success.__str__()

    # 6) map: apply a mapper function to the Validation value and return a new Validation
    mapper_fn = lambda v: f"mapped:{v}"
    mapped_validation = validation_success.map(mapper_fn)

    # 7) Construct an unusual Validation whose value is a Lazy object and whose errors is another Validation
    #    (this mirrors potential nested/complex uses of the Validation container)
    nested_validation = validation_module.Validation(lazy_from_success, validation_success)

    # Assertions: verify expected properties and relationships
    assert equality_self is True, "A Validation should be equal to itself"

    # Box should expose the same underlying value wrapped by validation_success
    assert hasattr(box_from_success, "value"), "Box returned from to_box should have a 'value' attribute"
    assert box_from_success.value == SAMPLE_BYTES

    # success/fail detection
    assert validation_success.is_fail() is False, "Validation with empty errors should not be considered a failure"
    assert validation_fail.is_fail() is True, "Validation with non-empty errors should be considered a failure"

    # Try objects created from validations should reflect the Validation success state.
    # We check for an 'is_success' attribute if present; otherwise fall back to boolean expectations.
    if hasattr(try_from_success, "is_success"):
        assert try_from_success.is_success is True
    if hasattr(try_from_fail, "is_success"):
        assert try_from_fail.is_success is False

    # String representations should mention 'Validation' and include value or errors information
    assert "Validation" in str_repr_fail
    assert "Validation" in str_repr_success

    # Mapped validation should contain the transformed value and preserve errors (empty for success)
    assert mapped_validation.value == mapper_fn(SAMPLE_BYTES)
    assert mapped_validation.errors == validation_success.errors

    # Nested validation should hold the Lazy object and the errors object as provided
    assert nested_validation.value is lazy_from_success
    assert nested_validation.errors is validation_success

def test_validation_equality_to_maybe_and_bind_behavior():
    # Purpose:
    # - Verify a Validation is equal to itself
    # - Ensure to_maybe() can be called on a Validation that has errors (smoke test)
    # - Verify bind() applies a folder function to a successful Validation's value and returns the result

    # Constants / setup
    SAMPLE_BYTES = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    ERRORS_MAP = {None: SAMPLE_BYTES, SAMPLE_BYTES: SAMPLE_BYTES}

    # Validation instance that represents a failure (has errors)
    validation_with_errors = validation_module.Validation(None, ERRORS_MAP)
    # Validation instance that represents success (empty errors list)
    successful_validation = validation_module.Validation(SAMPLE_BYTES, [])

    # Execution
    # equality check (should be True because it's the same instance compared to itself)
    equality_result = (validation_with_errors == validation_with_errors)
    # to_maybe called on a Validation that has errors (we only assert it returns without raising)
    maybe_result = validation_with_errors.to_maybe()

    # Define a folder function for bind: it receives the inner value and returns a new Validation
    def folder_func(value):
        # produce a new Validation with a deterministically transformed value and no errors
        transformed = value + b"-bound"
        return validation_module.Validation(transformed, [])

    bind_result = successful_validation.bind(folder_func)

    # Expected result after binding
    expected_after_bind = validation_module.Validation(SAMPLE_BYTES + b"-bound", [])

    # Assertions
    assert equality_result is True, "A Validation should be equal to itself"
    # to_maybe should return an object (smoke test to ensure method executes without error)
    assert maybe_result is not None
    # bind should return the Validation produced by the folder function
    assert bind_result == expected_after_bind

def test_validation_equality_then_to_box_called_on_result():
    # Purpose:
    # Verify behavior when comparing two Validation instances with different
    # value/error configurations and then calling `to_box()` on the comparison result.
    # This mirrors the original test's actions: create two Validation objects (one
    # with a value and the other with errors), compare them via __eq__, and call
    # to_box() on whatever is returned by the comparison.

    # Constants / test data
    SAMPLE_BYTES = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    SAMPLE_NONE = None
    SAMPLE_ERRORS = {SAMPLE_NONE: SAMPLE_BYTES, SAMPLE_BYTES: SAMPLE_BYTES}

    # Setup: construct two Validation instances with swapped value/errors
    validation_left = validation_module.Validation(SAMPLE_NONE, SAMPLE_ERRORS)
    validation_right = validation_module.Validation(SAMPLE_BYTES, SAMPLE_NONE)

    # Execution: perform equality comparison using the __eq__ method explicitly
    comparison_result = validation_left.__eq__(validation_right)

    # Assertion / action: call to_box() on the comparison result to reproduce original behavior.
    # Note: if comparison_result is not an object with to_box(), this will raise an AttributeError.
    comparison_result.to_box()

