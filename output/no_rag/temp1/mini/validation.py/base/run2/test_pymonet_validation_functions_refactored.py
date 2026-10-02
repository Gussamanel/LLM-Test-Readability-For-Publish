import pytest

import validation as validation_module
import builtins as builtins_module

def test_validation_success_behaviors_and_to_maybe_conversion():
    # Purpose:
    # - Create a Validation that represents success (no errors).
    # - Verify success/failure predicates, equality with itself, and conversion to Maybe.
    #
    # Setup
    test_value = "\n        Create empty maybe.\n\n        :returns: Maybe[None]\n        "
    empty_errors = []  # no errors => Validation should be a success
    validation = validation_module.Validation(test_value, empty_errors)

    # Execution
    is_success = validation.is_success()
    equals_self = validation == validation  # uses __eq__
    is_failure = validation.is_fail()
    maybe_result = validation.to_maybe()  # should produce a Maybe containing test_value for a successful Validation

    # Assertions
    assert is_success is True, "Validation with empty errors should be successful"
    assert equals_self is True, "Validation should be equal to itself"
    assert is_failure is False, "Validation with empty errors should not be a failure"
    # Ensure conversion to Maybe returns an object (implicitly checking no exception and a value returned)
    assert maybe_result is not None, "to_maybe() should return a Maybe instance (not None)"

def test_validation_equality_with_none_and_is_success_behavior():
    """
    Purpose:
    - Ensure a Validation instance is not considered equal to None.
    - Ensure is_success() reflects that the Validation with non-empty errors is not successful.

    This test separates setup, exercise, and assertion phases for clarity.
    """

    # --- Setup ---
    VALUE = -6891
    ERRORS = (3125,)  # non-empty errors indicate validation failure
    validation_instance = validation_module.Validation(VALUE, ERRORS)

    # --- Exercise ---
    are_equal_to_none = validation_instance == None  # compare to None using __eq__
    success_flag = validation_instance.is_success()  # check success based on errors

    # --- Assert ---
    # A Validation should not be equal to None
    assert are_equal_to_none is False

    # Because errors is non-empty, is_success() should be False
    assert success_flag is False

def test_validation_success_representation_and_is_fail_returns_false():
    # This test verifies that a Validation constructed with an empty value
    # and no errors reports not-failed (is_fail() == False) and that its
    # string representation indicates success and includes the value's repr.
    
    # --------------------
    # Setup
    # --------------------
    EMPTY_VALUE = {}
    EMPTY_ERRORS = []  # use an empty list for errors to reflect expected type
    validation = validation_module.Validation(EMPTY_VALUE, EMPTY_ERRORS)
    
    # --------------------
    # Execute
    # --------------------
    string_representation = str(validation)
    is_failure = validation.is_fail()
    
    # --------------------
    # Assert
    # --------------------
    # Validation with no errors should not be considered a failure
    assert is_failure is False
    # The string form should indicate success and include the value representation
    assert "Validation.success" in string_representation
    assert "{}" in string_representation

def test_validation_converts_successful_validation_to_either_and_maybe():
    # Constants: represent an empty successful value and no errors
    EMPTY_VALUE = set()

    # Setup: create a Validation that represents success (no errors)
    validation = validation_module.Validation(EMPTY_VALUE, EMPTY_VALUE)

    # Execution: convert the Validation to an Either and to a Maybe
    either_result = validation.to_either()
    maybe_result = validation.to_maybe()

    # Assertions:
    # - The Validation should be considered a success
    assert validation.is_success() is True

    # - The Either result should expose the original value (Right case)
    if hasattr(either_result, "value"):
        assert either_result.value == EMPTY_VALUE
    else:
        pytest.fail("Expected Either (Right) to expose attribute 'value' with the original value")

    # - The Maybe result should be a Just containing the original value.
    #   Verify by checking it exposes the value and that calling to_maybe() is idempotent.
    if hasattr(maybe_result, "value"):
        assert maybe_result.value == EMPTY_VALUE
    else:
        pytest.fail("Expected Maybe.just to expose attribute 'value' with the original value")

    # Many Maybe implementations return themselves when converted again to Maybe;
    # ensure that calling to_maybe() on the result returns the same object (identity).
    if hasattr(maybe_result, "to_maybe"):
        assert maybe_result.to_maybe() is maybe_result
    else:
        pytest.fail("Expected Maybe instance to implement to_maybe()")

def test_validation_with_non_empty_errors_converts_to_left_and_empty_maybe():
    """Validation with non-empty errors should be a failure, convert to Left(errors), and to an empty Maybe."""
    SAMPLE_TEXT = "Create empty maybe."

    # Create a Validation where both value and errors are the same non-empty string
    validation = validation_module.Validation(SAMPLE_TEXT, SAMPLE_TEXT)

    # Conversions and checks
    either_result = validation.to_either()
    assert validation == validation  # equality to itself
    assert validation.is_fail() is True

    from pymonet.either import Left
    from pymonet.maybe import Maybe

    assert either_result == Left(SAMPLE_TEXT)
    assert validation.to_maybe() == Maybe.nothing()

def test_validation_to_maybe_returns_maybe_for_success_and_allows_reconversion():
    """
    Verify that a successful Validation (no errors) can be transformed to a Maybe,
    and that calling to_maybe on the resulting Maybe is a valid, non-error operation.
    """
    # Setup: create an empty value and an empty errors collection to represent success.
    EMPTY_SET = builtins_module.set()
    validation = validation_module.Validation(EMPTY_SET, EMPTY_SET)

    # Execution: convert Validation -> Maybe, then call to_maybe again on the Maybe.
    maybe_result = validation.to_maybe()
    reconverted_maybe = maybe_result.to_maybe()

    # Assertion: both conversions returned objects (no exceptions were raised and results are not None).
    assert maybe_result is not None
    assert reconverted_maybe is not None

def test_validation_constructor_accepts_none_values():
    # Purpose:
    # Verify that Validation can be constructed with None values without raising
    # an exception and that the resulting object is an instance of Validation.

    # Constants / test data
    NONE_VALUE = None

    # Setup: prepare inputs for the constructor
    first_input = NONE_VALUE
    second_input = NONE_VALUE

    # Execution: construct the Validation object
    validation_instance = validation_module.Validation(first_input, second_input)

    # Assertion: ensure construction succeeded and returned the correct type
    assert isinstance(validation_instance, validation_module.Validation)

def test_validation_to_maybe_with_none_inputs_returns_maybe_object():
    # Purpose:
    # Ensure that Validation.to_maybe() can be called when both the value and errors are None,
    # and that it returns a Maybe object (either Just(None) or Nothing) rather than raising.

    # Constants / Setup
    VALUE_NONE = None
    ERRORS_NONE = None
    validation_instance = validation_module.Validation(VALUE_NONE, ERRORS_NONE)

    # Execution
    maybe_result = validation_instance.to_maybe()

    # Assertion: result is a Maybe-like object (should not be None)
    # The exact shape (Just(None) vs Nothing) depends on Validation.is_success() implementation,
    # this test verifies that a Maybe object is produced and no exception occurs.
    assert maybe_result is not None

def test_is_fail_returns_false_when_errors_list_is_empty():
    # Purpose:
    #   Verify that Validation.is_fail() reports no failure (False) when the errors list is empty.
    # Constants
    EXPECTED_IS_FAIL_RESULT = False

    # Setup: create a target object and a Validation instance initialized with that object
    target_object = builtins_module.object()
    validator = validation_module.Validation(target_object, target_object)

    # Ensure the validator has an explicit empty errors list (defensive setup)
    validator.errors = []

    # Execution: call the method under test
    actual_is_fail = validator.is_fail()

    # Assertion: when there are no errors, is_fail should return False
    assert actual_is_fail == EXPECTED_IS_FAIL_RESULT

def test_map_raises_typeerror_when_mapper_is_none():
    # This test verifies that Validation.map raises a TypeError when the provided mapper is None.
    # Arrange: build a complex value and a Validation instance with that value and some "errors" placeholder.
    ORIGINAL_INT = -895
    ORIGINAL_BOOL = True
    KEY_VALUE_TUPLE = (ORIGINAL_INT, ORIGINAL_BOOL)
    DICT_WITH_TUPLE_KEY = {KEY_VALUE_TUPLE: KEY_VALUE_TUPLE}
    COMPLEX_VALUE = (DICT_WITH_TUPLE_KEY, DICT_WITH_TUPLE_KEY, ORIGINAL_INT)

    validation_instance = validation_module.Validation(COMPLEX_VALUE, ORIGINAL_BOOL)
    mapper_function = None  # Intentionally invalid mapper

    # Act & Assert: calling map with None should raise a TypeError because None is not callable.
    with pytest.raises(TypeError):
        validation_instance.map(mapper_function)

def test_bind_raises_type_error_when_folder_is_none():
    """Verify Validation.bind raises TypeError when folder is None (not callable)."""
    BYTES_VALUE = b"s\x8flul\xd1p\x86\xe0<q\xd9\xb2\xf6\x17EC\xaf\xd0"

    # Setup: create a Validation instance with the same bytes for value and error
    validation_instance = validation_module.Validation(BYTES_VALUE, BYTES_VALUE)
    none_folder = None  # intentionally not a callable to trigger the error

    # Execution & Assertion: bind should try to call the folder and raise TypeError
    with pytest.raises(TypeError):
        validation_instance.bind(none_folder)

def test_ap_concatenates_errors_from_callable_provider():
    # Purpose:
    # Verify that Validation.ap calls the provided function (monad) with the current value,
    # and returns a new Validation preserving the original value and concatenating original
    # errors with the errors from the Validation returned by the function.

    # Constants / Setup
    INITIAL_VALUE = False
    INITIAL_ERRORS = [True, True, True, True]
    NEW_ERRORS = [True, True, True, True]

    # Prepare the initial Validation with a value and initial errors
    initial_validation = validation_module.Validation(INITIAL_VALUE, INITIAL_ERRORS)

    # The provider function simulates the monad: given a value, it returns another Validation
    # whose value will be the same and whose errors are NEW_ERRORS.
    def errors_provider(value):
        return validation_module.Validation(value, NEW_ERRORS)

    # Execution: apply the provider using ap
    result_validation = initial_validation.ap(errors_provider)

    # Assertions: value is preserved; errors are concatenated (initial + new)
    assert result_validation.value is INITIAL_VALUE
    assert result_validation.errors == INITIAL_ERRORS + NEW_ERRORS

def test_validation_with_empty_errors_reports_success_and_transforms_to_box():
    # Constants: a representative value and an explicit empty errors list
    VALID_VALUE = True
    EMPTY_ERRORS = []

    # Setup: create a Validation instance with a value and no errors
    validation = validation_module.Validation(VALID_VALUE, EMPTY_ERRORS)

    # Execution: convert the Validation to a Box and check success status on the Validation
    result_box = validation.to_box()
    success_flag = validation.is_success()

    # Assertions:
    # - Validation should report success when the errors list is empty
    assert success_flag is True
    # - to_box() should wrap the original value into a Box (Box.value should equal the original value)
    assert hasattr(result_box, "value") and result_box.value == VALID_VALUE

def test_validation_to_lazy_bind_with_none_produces_lazy_like_result():
    # Purpose:
    # - Verify that a Validation wrapping an empty list can be transformed to a Lazy,
    #   then bound with a None "folder" argument without raising, and that the
    #   resulting object still exposes a callable to_lazy (returns a non-None value).

    # --- Setup ---
    EMPTY_VALUE = []
    EMPTY_ERRORS = []

    validation = validation_module.Validation(EMPTY_VALUE, EMPTY_ERRORS)
    lazy_from_validation = validation.to_lazy()

    # --- Execution ---
    # Intentionally pass None as the "folder" argument to bind (as in original test).
    folder_argument = None
    bound_result = lazy_from_validation.bind(folder_argument)

    # --- Assertion ---
    # Ensure calling to_lazy on the bound result returns a non-None object and does not raise.
    result_lazy = bound_result.to_lazy()
    assert result_lazy is not None

def test_validation_to_lazy_then_try_and_ap_combines_errors_and_preserves_value():
    # Constants for the test inputs
    EMPTY_VALUE = {}
    EMPTY_ERRORS = []

    # Setup: create a Validation instance with an empty value and no errors
    original_validation = validation_module.Validation(EMPTY_VALUE, EMPTY_ERRORS)

    # Execution:
    # 1) Convert the Validation to a Lazy monad (should wrap the value)
    lazy_monad = original_validation.to_lazy()
    # 2) Convert the Lazy monad to a Try monad (Try should be successful because there are no errors)
    try_monad = lazy_monad.to_try()
    # 3) Call ap on the lazy monad passing the original validation as the function-like argument.
    #    This exercises the applicative behavior where errors from the provided "fn" are concatenated.
    ap_result = lazy_monad.ap(original_validation)

    # Assertions:
    # - The Try monad reports success since the original Validation had no errors.
    assert try_monad.is_success() is True

    # - The result of ap is a Validation instance.
    assert isinstance(ap_result, validation_module.Validation)

    # - The ap result preserves the original value.
    assert ap_result.value == original_validation.value

    # - The errors of the ap result are the concatenation of the original errors with the
    #   errors returned by the provided argument when called with the value.
    #   With both error lists empty this should result in an empty list as well.
    assert ap_result.errors == original_validation.errors + original_validation.errors

def test_to_try_returns_failed_try_when_validation_has_errors():
    # Verify that Validation.to_try() produces a failing Try when the Validation contains errors.
    SAMPLE_VALUE = 0
    SAMPLE_ERRORS = [SAMPLE_VALUE]

    # Arrange
    validation_instance = validation_module.Validation(SAMPLE_VALUE, SAMPLE_ERRORS)

    # Act
    try_result = validation_instance.to_try()

    # Assert
    assert try_result.is_success() is False

def test_validation_mapping_and_conversion_helpers_behavior():
    """
    Purpose:
    - Verify core Validation behavior: equality, success/fail detection, mapping of value,
      and that conversion helpers return objects (to_box, to_either, to_try, to_lazy).
    - Keep assertions limited to Validation internals (value, errors, is_fail, __eq__, __str__)
      and lightweight checks (conversion returns non-None) so the test does not depend on
      internals of the returned monads (Box, Either, Try, Lazy).
    """

    # --- Constants / Setup ---
    SAMPLE_BYTES = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    ERRORS = [SAMPLE_BYTES]

    # A successful Validation (no errors)
    success_validation = validation_module.Validation(SAMPLE_BYTES, [])

    # A failing Validation (non-empty errors list)
    fail_validation = validation_module.Validation(None, ERRORS)

    # --- Execution ---
    # Equality checks
    equals_self = (fail_validation == fail_validation)
    equals_same_content = (fail_validation == validation_module.Validation(None, ERRORS.copy()))

    # Success / failure detection
    success_is_fail = success_validation.is_fail()
    fail_is_fail = fail_validation.is_fail()

    # Mapping: transform the successful validation's value and preserve errors
    def append_exclamation(b: bytes) -> bytes:
        return b + b"!"

    mapped_validation = success_validation.map(append_exclamation)

    # Conversions (we only verify that they return objects, not their internal details)
    box_obj = fail_validation.to_box()
    either_from_success = success_validation.to_either()
    either_from_fail = fail_validation.to_either()
    try_from_success = success_validation.to_try()
    lazy_from_success = success_validation.to_lazy()

    # String representations
    str_success = str(success_validation)
    str_fail = str(fail_validation)

    # --- Assertions ---
    # Equality semantics
    assert equals_self is True, "Validation should be equal to itself"
    assert equals_same_content is True, "Validations with same value and errors should be equal"

    # is_fail semantics
    assert success_is_fail is False, "Validation with empty errors should not be a failure"
    assert fail_is_fail is True, "Validation with non-empty errors should be a failure"

    # map semantics: value transformed, errors preserved
    assert mapped_validation.value == SAMPLE_BYTES + b"!", "Mapped Validation must contain transformed value"
    assert mapped_validation.errors == success_validation.errors, "Mapping should preserve errors list"

    # Conversions should return objects (non-None)
    assert box_obj is not None, "to_box() should return a Box-like object"
    assert either_from_success is not None, "to_either() should return an Either-like object for success"
    assert either_from_fail is not None, "to_either() should return an Either-like object for failure"
    assert try_from_success is not None, "to_try() should return a Try-like object"
    assert lazy_from_success is not None, "to_lazy() should return a Lazy-like object"

    # __str__ should indicate success/fail state
    assert "success" in str_success.lower(), "__str__ of a successful Validation should mention 'success'"
    assert "fail" in str_fail.lower(), "__str__ of a failing Validation should mention 'fail'"

def test_validation_equality_bind_and_to_maybe_behavior():
    # Purpose:
    # - A Validation should compare equal to itself.
    # - to_maybe() should be callable on a Validation that contains errors.
    # - bind() should apply a mapper that returns a Validation and produce a new Validation
    #   with the transformed value.

    # Setup constants
    SAMPLE_BYTES = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    SAMPLE_NONE = None
    ERRORS_MAP = {SAMPLE_NONE: SAMPLE_BYTES, SAMPLE_BYTES: SAMPLE_BYTES}
    EMPTY_ERRORS = []

    # Create Validation instances: one representing an error, one representing success
    validation_with_errors = validation_module.Validation(SAMPLE_NONE, ERRORS_MAP)
    validation_success = validation_module.Validation(SAMPLE_BYTES, EMPTY_ERRORS)

    # Equality: a Validation should equal itself
    assert (validation_with_errors == validation_with_errors) is True

    # Success/failure checks
    assert validation_with_errors.is_success() is False
    assert validation_success.is_success() is True

    # to_maybe() should be callable even when Validation contains errors
    maybe_from_error = validation_with_errors.to_maybe()
    assert maybe_from_error is not None

    # bind: mapper returns a Validation; ensure bind applies it and returns a Validation
    def mapper_return_validation(value):
        return validation_module.Validation(value + b"-mapped", EMPTY_ERRORS)

    mapped_validation = validation_success.bind(mapper_return_validation)
    assert isinstance(mapped_validation, validation_module.Validation)
    assert mapped_validation.value == SAMPLE_BYTES + b"-mapped"

def test_validation_equality_result_and_to_box_call_behavior():
    # Purpose:
    # - Create two Validation objects with different values/errors and verify they are not equal.
    # - Demonstrate that the direct result of __eq__ is a boolean and therefore does not
    #   provide the Validation.to_box() method (calling it should raise AttributeError).
    # Setup (constants and objects):
    SAMPLE_BYTES = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    SAMPLE_NONE = None
    # errors map intentionally includes both None->bytes and bytes->bytes to vary internal state
    SAMPLE_ERRORS = {SAMPLE_NONE: SAMPLE_BYTES, SAMPLE_BYTES: SAMPLE_BYTES}

    left_validation = validation_module.Validation(SAMPLE_NONE, SAMPLE_ERRORS)
    right_validation = validation_module.Validation(SAMPLE_BYTES, SAMPLE_NONE)

    # Execution: call the equality method explicitly (returns a boolean)
    equality_result = left_validation.__eq__(right_validation)

    # Assertions:
    # - The two Validation objects should not be considered equal.
    assert equality_result is False

    # - Since equality_result is a bool, calling to_box on it should raise AttributeError.
    with pytest.raises(AttributeError):
        equality_result.to_box()

