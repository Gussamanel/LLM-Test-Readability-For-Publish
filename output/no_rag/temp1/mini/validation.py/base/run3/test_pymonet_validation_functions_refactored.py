import pytest

import validation as validation_module
import builtins as builtins_module

def test_validation_failure_reports_and_converts_to_maybe():
    # Purpose:
    # - Verify a Validation constructed with non-empty errors reports failure (is_success False, is_fail True)
    # - Verify a Validation equals itself
    # - Verify converting a failing Validation to a Maybe yields a Maybe object (nothing)
    #
    # Note: This test intentionally constructs a failing Validation (non-empty errors list).

    # Setup
    VALUE = "Create empty maybe."
    ERRORS = ["some error occurred"]  # non-empty errors to make the Validation a failure
    validation = validation_module.Validation(VALUE, ERRORS)

    # Execute
    success_flag = validation.is_success()
    failure_flag = validation.is_fail()
    equality_with_self = validation == validation  # uses Validation.__eq__
    maybe_result = validation.to_maybe()  # should produce a Maybe (likely nothing for failing Validation)

    # Assert
    assert success_flag is False, "Validation with errors should not be successful"
    assert failure_flag is True, "Validation with errors should report failure"
    assert equality_with_self is True, "A Validation should be equal to itself"
    # to_maybe() should return a Maybe instance (not None). We don't rely on Maybe internals here.
    assert maybe_result is not None, "to_maybe() should return a Maybe object even for failing Validation"
    assert maybe_result.__class__.__name__ == "Maybe", "to_maybe() should return an instance of Maybe"

def test_validation_equality_with_none_and_is_success_returns_false():
    # Purpose:
    # Verify that a Validation instance is not equal to None and that
    # is_success() correctly reports False when the errors list is non-empty.

    # Setup: create a Validation with a non-empty errors list
    SAMPLE_VALUE = -6891
    SAMPLE_ERROR = 3125
    ERRORS = (SAMPLE_ERROR,)
    validation_instance = validation_module.Validation(SAMPLE_VALUE, ERRORS)

    # Execution: compare the Validation to None and check its success state
    equality_with_none = validation_instance == None  # explicit comparison to None
    success_flag = validation_instance.is_success()

    # Assertion: equality should be False and is_success should be False for non-empty errors
    assert equality_with_none is False
    assert success_flag is False

def test_validation_with_empty_errors_reports_success_and_string_representation():
    """
    Verify that a Validation created with an empty errors collection is considered a success
    and its string representation reflects the successful state.
    """
    # Setup
    empty = {}
    validation_obj = validation_module.Validation(empty, empty)

    # Execution
    string_representation = str(validation_obj)
    is_failure = validation_obj.is_fail()

    # Assertions
    assert is_failure is False
    assert string_representation == f'Validation.success[{empty}]'

def test_validation_to_either_and_to_maybe_with_empty_successful_value():
    # Purpose:
    # Verify that a Validation constructed with no errors (success case)
    # can be converted to an Either and to a Maybe, and that calling to_maybe()
    # on the resulting Maybe does not raise and returns a value.

    # Constants / Test data
    EMPTY_VALUE = set()
    EMPTY_ERRORS = set()  # no errors -> validation should be considered success

    # Setup: create a Validation instance representing a successful validation
    validation = validation_module.Validation(EMPTY_VALUE, EMPTY_ERRORS)

    # Execution: perform conversions from Validation -> Either and Validation -> Maybe
    either_result = validation.to_either()
    maybe_result = validation.to_maybe()

    # Exercise: call to_maybe() on the Maybe returned (should be safe / idempotent)
    maybe_result_second = maybe_result.to_maybe()

    # Assertions: conversions completed and returned objects (no exceptions; results are not None)
    assert either_result is not None
    assert maybe_result is not None
    assert maybe_result_second is not None

def test_validation_with_non_empty_errors_behaves_as_failure_and_converts_cleanly():
    # Constants: a non-empty string used both as the value and as the "errors" argument.
    # Using a non-empty string ensures Validation.is_fail() returns True (errors length != 0).
    SAMPLE_TEXT = "Create empty maybe.\n\n:returns: Maybe[None]\n"

    # Setup: construct a Validation instance with a non-empty "errors" argument.
    validation = validation_module.Validation(SAMPLE_TEXT, SAMPLE_TEXT)

    # Execution: call the various API methods under test.
    either_result = validation.to_either()          # should produce an Either (Left with errors)
    equality_with_self = validation.__eq__(validation)  # should be True for same instance/content
    is_failure = validation.is_fail()               # expected to be True because errors is non-empty
    maybe_result = validation.to_maybe()            # should produce a Maybe (expected empty/nothing)

    # Assertions: verify core expectations and that conversions execute without raising.
    # - Validation equals itself.
    assert equality_with_self is True

    # - The Validation is considered a failure since errors are non-empty.
    assert is_failure is True

    # - Conversion methods return objects (verifies no exceptions and basic return).
    #   Detailed type/value checks are done in other, more specific tests.
    assert either_result is not None
    assert maybe_result is not None

def test_validation_to_maybe_returns_maybe_and_allows_subsequent_to_maybe_calls():
    """
    Purpose:
    - Verify that Validation.to_maybe() returns a Maybe-like object.
    - Verify that calling to_maybe() on the resulting Maybe object is valid (idempotent-like behavior)
      and does not raise an exception (returns a non-None object).

    Actions:
    - Setup a Validation instance using the same empty set for value and errors to mirror the original test.
    - Convert the Validation to a Maybe.
    - Call to_maybe() on the resulting Maybe and assert both results are non-None.
    """

    # --- Setup ---
    EMPTY_SET = builtins_module.set()
    validation_obj = validation_module.Validation(EMPTY_SET, EMPTY_SET)

    # --- Execution ---
    maybe_result = validation_obj.to_maybe()
    # Call to_maybe() again on the Maybe returned above
    maybe_result_second = maybe_result.to_maybe()

    # --- Assertions ---
    assert maybe_result is not None
    assert maybe_result_second is not None

def test_validation_init_with_none_arguments_creates_instance():
    # Purpose: Verify Validation can be instantiated when both constructor args are None.
    none_arg = None
    # Sanity check: none_arg is indeed NoneType
    assert isinstance(none_arg, builtins_module.type(None))

    # Execution
    validation_instance = validation_module.Validation(none_arg, none_arg)

    # Assertion: instance was created and is of the Validation type
    assert validation_instance is not None
    assert isinstance(validation_instance, validation_module.Validation)

def test_validation_to_maybe_returns_maybe_just_when_successful(monkeypatch):
    # Purpose:
    # Verify that Validation.to_maybe() transforms a successful Validation (no errors)
    # into a Maybe by calling Maybe.just with the Validation value.

    # Constants (arrange)
    TEST_VALUE = None
    TEST_ERRORS = None

    # Setup: create a Validation instance that represents success (no errors)
    validation_instance = validation_module.Validation(TEST_VALUE, TEST_ERRORS)

    # Replace the real pymonet.maybe.Maybe with a fake to observe which factory is used.
    # Using monkeypatch on sys.modules ensures the import inside to_maybe() picks up this fake.
    import types
    import sys

    fake_maybe_module = types.ModuleType("pymonet.maybe")

    class FakeMaybe:
        last_called = None
        last_arg = None

        @classmethod
        def just(cls, value):
            cls.last_called = "just"
            cls.last_arg = value
            return ("just", value)

        @classmethod
        def nothing(cls):
            cls.last_called = "nothing"
            cls.last_arg = None
            return ("nothing", None)

    fake_maybe_module.Maybe = FakeMaybe
    monkeypatch.setitem(sys.modules, "pymonet.maybe", fake_maybe_module)

    # Execution: call the method under test
    maybe_result = validation_instance.to_maybe()

    # Assertion: ensure Maybe.just was invoked with the Validation value and the returned object matches
    assert FakeMaybe.last_called == "just", "Expected Maybe.just to be called for a successful Validation"
    assert FakeMaybe.last_arg is TEST_VALUE
    assert maybe_result == ("just", TEST_VALUE)

def test_validation_is_fail_is_false_on_new_instance():
    """Verify Validation.is_fail() returns False for a newly created Validation with no errors."""
    subject = builtins_module.object()
    validation_instance = validation_module.Validation(subject, subject)
    assert validation_instance.is_fail() is False

def test_map_with_non_callable_mapper_raises_type_error():
    # Purpose:
    # Verify that Validation.map raises a TypeError when given a non-callable mapper (e.g., None).
    #
    # Setup: create a Validation instance with a composite value and an "errors" flag.
    SAMPLE_INT = -895
    SAMPLE_BOOL = True
    SAMPLE_TUPLE = (SAMPLE_INT, SAMPLE_BOOL)
    SAMPLE_DICT = {SAMPLE_TUPLE: SAMPLE_TUPLE}
    VALIDATION_VALUE = (SAMPLE_DICT, SAMPLE_DICT, SAMPLE_INT)
    NON_CALLABLE_MAPPER = None

    validation_instance = validation_module.Validation(VALIDATION_VALUE, SAMPLE_BOOL)

    # Sanity check: ensure the mapper provided is indeed not callable
    assert not builtins_module.callable(NON_CALLABLE_MAPPER)

    # Execution & Assertion: calling map with a non-callable should raise TypeError
    with pytest.raises(TypeError):
        validation_instance.map(NON_CALLABLE_MAPPER)

def test_bind_raises_type_error_when_folder_is_none():
    # Purpose:
    # Verify that Validation.bind raises a TypeError when the provided folder is None
    # (None is not callable, so attempting to call it should fail).

    # Setup: create a Validation with some bytes value
    SAMPLE_BYTES = b"s\x8flul\xd1p\x86\xe0<q\xd9\xb2\xf6\x17EC\xaf\xd0"
    validation = validation_module.Validation(SAMPLE_BYTES, SAMPLE_BYTES)

    # Execution & Assertion: binding with None should raise a TypeError because None is not callable
    folder = None
    with pytest.raises(TypeError):
        validation.bind(folder)

def test_ap_combines_original_and_function_errors():
    # This test verifies that Validation.ap calls the provided function with the
    # current Validation.value and returns a new Validation with the same value
    # and errors that are the concatenation of the original errors and the
    # errors from the Validation returned by the function.
    
    # Constants / setup
    initial_value = False
    initial_errors = [True, True, True, True]
    validation_instance = validation_module.Validation(initial_value, initial_errors)

    # The function passed to ap must accept a value and return another Validation.
    # Return a Validation that carries the same errors list to simulate the monadic function.
    def function_returning_validation(value):
        return validation_module.Validation(value, initial_errors)

    # Execution
    result = validation_instance.ap(function_returning_validation)

    # Assertion: value is preserved and errors are concatenated (original + function's)
    expected_errors = initial_errors + initial_errors
    assert isinstance(result, validation_module.Validation)
    assert result.value == initial_value
    assert result.errors == expected_errors

def test_validation_to_box_and_is_success_with_no_errors():
    # Purpose:
    # - Verify that a Validation with an empty errors list reports success.
    # - Verify that to_box() wraps the Validation value in a Box-like object
    #   exposing the original value via a `.value` attribute (or equivalent).

    # Constants / Test data
    VALID_VALUE = True
    EMPTY_ERRORS = []

    # Setup: create a Validation instance with a value and no errors
    validation_instance = validation_module.Validation(VALID_VALUE, EMPTY_ERRORS)

    # Execution: check success flag and convert the validation to a box
    is_success_result = validation_instance.is_success()
    boxed_result = validation_instance.to_box()

    # Assertion: Validation without errors should be successful
    assert is_success_result is True

    # Assertion: the boxed result should expose the original value.
    # We try to read a common attribute name used by Box implementations.
    if hasattr(boxed_result, "value"):
        boxed_value = boxed_result.value
    elif hasattr(boxed_result, "get"):
        # Some Box implementations use .get() to retrieve the inner value
        boxed_value = boxed_result.get()
    else:
        # Fallback: try indexing or attribute access that may exist on custom boxes
        boxed_value = getattr(boxed_result, "__wrapped__", None)

    assert boxed_value == VALID_VALUE

def test_validation_to_lazy_bind_with_none_returns_lazy_like():
    # Verify that converting a Validation to a Lazy and binding with None
    # does not raise and yields an object that can be converted to a lazy-like representation.
    EMPTY_LIST = []
    NONE_FOLDER = None

    validation = validation_module.Validation(EMPTY_LIST, EMPTY_LIST)

    lazy_from_validation = validation.to_lazy()
    bound_result = lazy_from_validation.bind(NONE_FOLDER)

    lazy_like = bound_result.to_lazy()

    assert lazy_like is not None, "Calling to_lazy() on the bind result should produce a lazy-like object"

def test_validation_transforms_to_lazy_then_try_and_ap_combines_errors():
    # Constants for test inputs
    EMPTY_VALUE = {}
    EMPTY_ERRORS = []

    # Setup: create a Validation with no errors (represents a successful validation)
    source_validation = validation_module.Validation(EMPTY_VALUE, EMPTY_ERRORS)

    # Execution:
    # 1. Transform Validation to a Lazy monad (lazy wrapper around the value)
    lazy_monad = source_validation.to_lazy()
    # 2. Transform the Lazy (or resulting monad) into a Try monad
    try_monad = lazy_monad.to_try()
    # 3. Apply ap using the original validation as the function-source for additional errors
    ap_result = lazy_monad.ap(source_validation)

    # Assertions:
    # - The Try produced from the Validation with no errors should be successful.
    assert try_monad.is_success() is True
    # - The result of ap should be a Validation instance.
    assert isinstance(ap_result, validation_module.Validation)
    # - The ap operation should combine errors from both validations (here both are empty lists).
    assert ap_result.errors == source_validation.errors + source_validation.errors

def test_validation_to_try_returns_failed_try_for_non_empty_errors():
    # Converting a Validation that has errors should yield a failed Try.
    SAMPLE_VALUE = 0
    SAMPLE_ERRORS = [SAMPLE_VALUE]  # non-empty -> validation is a failure

    validation_instance = validation_module.Validation(SAMPLE_VALUE, SAMPLE_ERRORS)
    try_result = validation_instance.to_try()

    assert try_result.is_success() is False

def test_validation_transforms_map_and_equality():
    # Purpose:
    # - Verify key Validation behaviors: equality, conversions (to_box, to_either, to_try, to_lazy),
    #   is_fail(), string representation, and map().
    # - Keep setup / execution / assertions clearly separated and use descriptive names.

    # Constants / Setup
    SAMPLE_BYTES = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    # A failing Validation uses a non-empty errors list; a successful one uses an empty list.
    failing_errors = [SAMPLE_BYTES]
    success_errors = []

    failing_validation = validation_module.Validation(None, failing_errors)
    successful_validation = validation_module.Validation(SAMPLE_BYTES, success_errors)

    # Execution: exercise various Validation API methods
    # 1) Equality check (explicit __eq__ call) with itself
    self_equality_result = failing_validation.__eq__(failing_validation)

    # 2) Convert failing validation to a Box and inspect contained value
    box_from_failing = failing_validation.to_box()

    # 3) Convert both validations to Either (Right when success, Left when fail)
    either_from_success = successful_validation.to_either()
    either_from_failure = failing_validation.to_either()

    # 4) Check is_fail for success and failure cases
    is_success_fail_flag = successful_validation.is_fail()
    is_failure_fail_flag = failing_validation.is_fail()

    # 5) Convert to Try (won't be executed here, just ensure conversion works)
    try_from_success = successful_validation.to_try()
    try_from_failure = failing_validation.to_try()

    # 6) String representations for both cases
    str_success = str(successful_validation)
    str_failure = str(failing_validation)

    # 7) Obtain lazy wrappers (returning the value when evaluated)
    lazy_from_success = successful_validation.to_lazy()
    lazy_from_failure = failing_validation.to_lazy()

    # 8) Map the successful validation's value using a small mapper function
    def prefix_mapper(value):
        if isinstance(value, (bytes, bytearray)):
            return b"mapped:" + value
        return value

    mapped_validation = successful_validation.map(prefix_mapper)

    # Assertions: verify expected outcomes from the above operations
    assert self_equality_result is True  # validation equals itself
    # Box created from failing_validation should contain the original value (None)
    assert getattr(box_from_failing, "value", object()) is None

    # Either conversions: successful validation should be considered successful (is_fail False)
    assert is_success_fail_flag is False
    assert is_failure_fail_flag is True

    # String representations should reflect success/failure states
    assert str_success.startswith("Validation.success")
    assert "fail" in str_failure

    # Mapping should produce a Validation whose value is the mapped bytes
    assert getattr(mapped_validation, "value", None) == b"mapped:" + SAMPLE_BYTES

    # Lazy conversions should produce an object (do not rely on its concrete API here)
    assert lazy_from_success is not None
    assert lazy_from_failure is not None

    # to_either / to_try should return objects (we don't assert concrete monad internals here)
    assert either_from_success is not None
    assert either_from_failure is not None
    assert try_from_success is not None
    assert try_from_failure is not None

def test_validation_equality_to_maybe_and_bind_raises_on_non_callable():
    # Purpose:
    # - Verify that a Validation equals itself.
    # - Verify that to_maybe() returns a Maybe object (expected empty Maybe when Validation carries errors).
    # - Verify that bind() raises a TypeError when given a non-callable folder.

    # -----------------------
    # Constants / Test data
    # -----------------------
    SAMPLE_BYTES = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    SAMPLE_NONE = None
    ERRORS_MAP = {SAMPLE_NONE: SAMPLE_BYTES, SAMPLE_BYTES: SAMPLE_BYTES}

    # -----------------------
    # Setup
    # -----------------------
    # Validation that carries errors (errors provided as a non-empty mapping)
    validation_with_errors = validation_module.Validation(SAMPLE_NONE, ERRORS_MAP)

    # Validation with a value and a non-empty "errors" payload (used to test bind raising on non-callable)
    validation_with_value_and_error = validation_module.Validation(SAMPLE_BYTES, SAMPLE_BYTES)

    # -----------------------
    # Execution
    # -----------------------
    # Equality check (should be True when comparing the object to itself)
    equality_result = (validation_with_errors == validation_with_errors)

    # Convert to Maybe (should succeed and return a Maybe instance; expected to be "nothing" since validation has errors)
    maybe_result = validation_with_errors.to_maybe()

    # Attempt to call bind with a non-callable (SAMPLE_BYTES is a bytes object, not a function)
    # This should raise a TypeError because bind attempts to call the provided folder.
    # We perform this check in the assertions section using pytest.raises.
    
    # -----------------------
    # Assertions
    # -----------------------
    assert equality_result is True, "A Validation instance should be equal to itself."

    # Ensure to_maybe returned a Maybe instance (import locally to keep test self-contained)
    from pymonet.maybe import Maybe
    assert isinstance(maybe_result, Maybe), "to_maybe() should return a Maybe instance."

    # bind should raise a TypeError when passed a non-callable folder
    with pytest.raises(TypeError):
        validation_with_value_and_error.bind(SAMPLE_BYTES)

def test_validation_equality_result_is_boxable():
    """
    Verify that comparing two Validation instances via __eq__ yields an object
    that can be transformed to a Box using to_box().
    """
    # -- Constants / Test data --
    BYTES_SAMPLE = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    NONE_VALUE = None
    ERRORS_MAP = {NONE_VALUE: BYTES_SAMPLE, BYTES_SAMPLE: BYTES_SAMPLE}

    # -- Setup --
    # validation_with_errors: value is None and has an errors map
    validation_with_errors = validation_module.Validation(NONE_VALUE, ERRORS_MAP)
    # validation_with_value: value is BYTES_SAMPLE and has no errors
    validation_with_value = validation_module.Validation(BYTES_SAMPLE, NONE_VALUE)

    # -- Execution --
    # Call __eq__ explicitly to obtain the comparison result object
    equality_result = validation_with_errors.__eq__(validation_with_value)

    # -- Assertion / Action --
    # Convert the result to a Box and assert the conversion produced a Box-like object.
    boxed_result = equality_result.to_box()
    assert boxed_result is not None
    assert hasattr(boxed_result, "value")

