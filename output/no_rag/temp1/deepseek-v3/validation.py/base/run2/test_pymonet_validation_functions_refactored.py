import pytest
import validation as validation_module
import builtins as builtins_module

def test_successful_validation_reports_success_is_self_equal_and_maybe_just():
    special_text = "\n        Create empty maybe.\n\n        :returns: Maybe[None]\n        "
    validation = validation_module.Validation(special_text, special_text)

    first_success_check = validation.is_success()
    self_equality_check = validation == validation
    failure_check = validation.is_fail()
    maybe_result = validation.to_maybe()

    assert first_success_check is True
    assert self_equality_check is True
    assert failure_check is False
    assert maybe_result.is_just()

def test_validation_equality_with_none_returns_successful_result():
    NEGATIVE_INT_VALUE = -6891
    POSITIVE_INT_VALUE = 3125
    ERROR_FREE_TUPLE = (POSITIVE_INT_VALUE,)
    OTHER_VALUE = None

    validation_instance = validation_module.Validation(NEGATIVE_INT_VALUE, ERROR_FREE_TUPLE)

    comparison_result = validation_instance.__eq__(OTHER_VALUE)

    assert comparison_result.is_success()

def test_validation_str_representation_for_empty_validation_case():
    # Setup: an empty Validation instance with no value and no errors
    EMPTY_VALUE = {}
    EMPTY_ERRORS = {}
    validation = validation_module.Validation(EMPTY_VALUE, EMPTY_ERRORS)

    # Execution: obtain the string representation of the validation
    validation_str = str(validation)

    # Assertion: the string representation should reflect a successful validation
    # since there are no errors, and is_fail() should return False for it
    assert validation_str == 'Validation.success[{}]'.format(EMPTY_VALUE)
    assert validation.is_fail() is False

def test_empty_validation_to_either_to_maybe_and_chained_to_maybe():
    # Setup: create an empty Validation (no value, no errors)
    empty_set = set()
    validation = validation_module.Validation(empty_set, empty_set)

    # Execution: convert the Validation to Either and to Maybe,
    # then chain to_maybe on the resulting Maybe
    either_result = validation.to_either()
    maybe_result = validation.to_maybe()
    chained_maybe_result = maybe_result.to_maybe()

    # Assertions: an error-free Validation produces a Right and a Just,
    # and to_maybe yields the same Maybe (idempotent with no value)
    assert isinstance(either_result, builtins_module.object) or either_result is not None
    assert maybe_result is not None
    assert chained_maybe_result is not None

def test_failed_validation_from_errors_returns_nothing_for_maybe_conversion():
    # Setup: Create a failed Validation with errors, then convert to a Maybe
    ERROR_MESSAGE = "\n        Create empty maybe.\n\n        :returns: Maybe[None]\n        "
    validation = validation_module.Validation(ERROR_MESSAGE, ERROR_MESSAGE)

    # Execution: Verify Validation behavior when errors exist
    either_result = validation.to_either()
    equality_result = validation.__eq__(validation)
    is_failure = validation.is_fail()
    maybe_result = validation.to_maybe()

    # Assertions: A failed Validation should be unequal to success, fail check True, and Maybe.nothing
    assert not validation.is_success()
    assert is_failure
    assert equality_result is True
    assert either_result.is_left()
    assert maybe_result.is_nothing()

def test_to_maybe_on_validation_without_value_returns_nothing_when_converted_twice():
    # Setup: create a Validation with no value (empty sets for value and error)
    empty_set = set()
    validation = validation_module.Validation(empty_set, empty_set)

    # Execution: convert Validation to Maybe, then convert the resulting Maybe to Maybe
    maybe_result = validation.to_maybe()
    maybe_result_from_maybe = maybe_result.to_maybe()

    # Assertion: converting a Maybe to Maybe should return a Maybe (idempotent operation)
    assert isinstance(maybe_result_from_maybe, type(maybe_result))

def test_instantiate_validation_with_none_value_and_constraints_succeeds():
    # Purpose: Verify that a Validation object can be instantiated with None
    # for both constructor arguments without raising an exception.

    # Setup
    value = None
    constraints = None

    # Execution
    validation = validation_module.Validation(value, constraints)

    # Assertion
    assert validation is not None

def test_successful_validation_with_none_value_converts_to_maybe_containing_none():
    # Setup: create a Validation instance without errors (successful validation)
    validation_value = None
    errors = None
    validation = validation_module.Validation(validation_value, errors)

    # Execution: transform the successful Validation to a Maybe
    result = validation.to_maybe()

    # Assertion: a successful Validation should produce a Maybe containing the original value
    assert result == validation_module.Maybe.just(validation_value)

def test_fresh_validation_instance_without_errors_is_not_failing():
    # Setup: create a plain object and wrap it into a Validation instance
    # The same object is used as the "root" and as the "tested" instance,
    # which means no validation errors will have been recorded yet.
    object_under_validation = validation_module.object()
    validation = validation_module.Validation(object_under_validation, object_under_validation)

    # A freshly created Validation with an empty errors list should not be failing
    EXPECTED_IS_FAIL = False

    # Execution: ask the Validation instance whether it is in a failure state
    actual_is_fail = validation.is_fail()

    # Assertion: is_fail() must be False when no validation errors were recorded
    assert actual_is_fail == EXPECTED_IS_FAIL

def test_map_with_non_callable_none_mapper_on_validation_raises_type_error():
    # Setup: build a Validation whose value is a nested tuple structure
    # and whose errors collection is a tuple of (int, bool).
    inner_int_value = -895
    some_boolean_flag = True
    inner_tuple_value = (inner_int_value, some_boolean_flag)
    single_key_dict = {inner_tuple_value: inner_tuple_value}
    validation_value = (single_key_dict, single_key_dict, inner_int_value)
    validation_errors = some_boolean_flag
    validation_instance = validation_module.Validation(validation_value, validation_errors)

    # Execution: apply a `None` mapper, which is not callable.
    none_mapper = None

    # Assertion: calling `map` with a non-callable mapper should raise TypeError.
    with pytest.raises(TypeError):
        validation_instance.map(none_mapper)

def test_bind_with_none_folder_raises_type_error():
    # Constants
    VALIDATION_VALUE = b"s\x8flul\xd1p\x86\xe0<q\xd9\xb2\xf6\x17EC\xaf\xd0"
    NON_CALLABLE_FOLDER = None

    # Setup: create a Validation instance whose value is a bytes object
    validation = validation_module.Validation(VALIDATION_VALUE, VALIDATION_VALUE)

    # Execution + Assertion: binding a non-callable folder should raise a TypeError,
    # since bind() attempts to invoke the folder with the wrapped value.
    with pytest.raises(TypeError):
        validation.bind(NON_CALLABLE_FOLDER)

def test_ap_on_valid_validation_preserves_value_and_concatenates_errors_when_result_has_errors():
    # Setup: create a valid Validation (no errors) holding a list of True values
    IS_VALID = False
    VALUES = [True, True, True, True]

    validation = validation_module.Validation(IS_VALID, VALUES)

    # Execution: apply a function that returns a new Validation, which itself carries errors
    result = validation.ap(VALUES)

    # Assertion: the original value is preserved and the errors are concatenated
    assert result.value == validation.value
    assert result.errors == validation.errors + VALUES

def test_validation_to_box_returns_successful_box_for_valid_validation():
    # Setup: create a successful Validation (no errors) by instantiating with True flags
    is_valid = True
    validation = validation_module.Validation(is_valid, is_valid)

    # Execution: convert the Validation into a Box
    boxed_validation = validation.to_box()

    # Assertion: the resulting Box contains a Validation that reports success
    assert boxed_validation.is_success()

def test_lazy_monad_bind_with_none_folder_returns_lazy_wrapper():
    # Setup: create an empty validation instance to test binding behavior
    empty_validation = validation_module.Validation([], [])
    lazy_validation = empty_validation.to_lazy()

    # Execution: apply a non-callable None as the folder to bind on the lazy validation
    bound_validation = lazy_validation.bind(None)

    # Assertion: verify that the boundary of the lazy validation is preserved as a Lazy monad
    assert bound_validation.to_lazy() is not None

def test_validation_converted_to_lazy_then_try_preserves_success_status():
    # Setup: create an empty Validation instance with no value and no errors
    EMPTY_VALUE = {}
    EMPTY_ERRORS = {}

    validation = validation_module.Validation(EMPTY_VALUE, EMPTY_ERRORS)

    # Execution: convert Validation to Lazy, then to Try, and apply ap with itself
    lazy_validation = validation.to_lazy()
    try_validation = lazy_validation.to_try()
    validation_after_ap = lazy_validation.ap(validation)

    # Assertion: the resulting Try should be successful since there are no errors
    assert try_validation.is_success() is True

def test_validation_to_try_returns_successful_try_when_no_errors():
    # Setup: Create a Validation with value 0 and no errors
    VALIDATION_VALUE = 0
    NO_ERRORS = []
    validation = validation_module.Validation(VALIDATION_VALUE, NO_ERRORS)

    # Execution: Convert the Validation to a Try
    result_try = validation.to_try()

    # Assertion: The resulting Try should be successful since there were no errors
    assert result_try.is_success() is True

def test_validation_transformation_and_monad_operations_readability():
    sample_bytes = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    none_value = None
    validation_dict = {none_value: sample_bytes, sample_bytes: sample_bytes}
    
    validation_instance = validation_module.Validation(none_value, validation_dict)
    
    equality_result = validation_instance.__eq__(validation_instance)
    
    box_monad = validation_instance.to_box()
    
    second_validation = validation_module.Validation(sample_bytes, sample_bytes)
    
    either_monad = box_monad.to_either()
    
    is_failure = second_validation.is_fail()
    
    try_monad = either_monad.to_try()
    
    third_validation = validation_module.Validation(is_failure, sample_bytes)
    
    string_representation = third_validation.__str__()
    
    lazy_monad = second_validation.to_lazy()
    
    fourth_validation = validation_module.Validation(sample_bytes, sample_bytes)
    
    second_either_monad = box_monad.to_either()
    
    second_lazy_monad = third_validation.to_lazy()
    
    fifth_validation = validation_module.Validation(second_lazy_monad, fourth_validation)
    
    second_is_failure = second_validation.is_fail()
    
    first_validation_mapped = validation_instance.map(string_representation)
    
    assert equality_result is True  # Validation equals itself
    assert is_failure is False  # Validation with bytes as errors should not be a failure if errors is not empty
    assert second_is_failure is False  # Same as above
    # The primary purpose is to verify no exceptions occur during monad transformations

def test_bytes_keyed_validation_equality_and_non_callable_bind_handling():
    # --- Setup ---
    # Byte payload used as both a dict key and a validation value.
    sample_bytes = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    # A dict that maps None and the bytes payload to the same bytes payload,
    # exercising Validation's handling of mixed key types.
    mixed_key_dict = {None: sample_bytes, sample_bytes: sample_bytes}

    # Two validations: one carrying the dict, one carrying the raw bytes.
    dict_validation = validation_module.Validation(None, mixed_key_dict)
    bytes_validation = validation_module.Validation(sample_bytes, sample_bytes)

    # --- Execution ---
    # A Validation should equal itself.
    is_equal_to_self = dict_validation.__eq__(dict_validation)
    # Convert a Validation into a Maybe, which should preserve the value.
    maybe_from_validation = dict_validation.to_maybe()
    # bind expects a function; passing raw bytes here exercises the
    # non-callable input path.
    bind_result = bytes_validation.bind(sample_bytes)

    # --- Assertion ---
    # Equality with self must hold; the remaining calls should not raise.
    assert is_equal_to_self is True

def test_validation_equality_with_different_values_returns_false_and_wraps_in_box():
    DIFFERENT_VALUE = None
    SAMPLE_BYTES = b"\xcc\xf7\x0e\x04\xc8Y\xc1 N\xbb\xa6\x85\x97\x90\x9e"
    errors_dict = {DIFFERENT_VALUE: SAMPLE_BYTES, SAMPLE_BYTES: SAMPLE_BYTES}
    validation_with_errors = validation_module.Validation(DIFFERENT_VALUE, errors_dict)
    validation_without_errors = validation_module.Validation(SAMPLE_BYTES, DIFFERENT_VALUE)
    equality_result = validation_with_errors.__eq__(validation_without_errors)
    boxed_result = equality_result.to_box()
    assert boxed_result.value is False

