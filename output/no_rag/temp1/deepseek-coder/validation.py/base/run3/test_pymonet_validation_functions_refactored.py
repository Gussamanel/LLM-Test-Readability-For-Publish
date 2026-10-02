import builtins as builtins
import validation as validation

def test_validation_is_success_and_equality():
    """
    This test case covers the functionality of Validation class.
    It checks if a Validation instance is successful and if it can be compared with another Validation instance.
    """

    validation = Validation()

    is_successful = validation.is_success()

    assert is_successful == (validation == validation), "Validation is successful and should equal to itself"

    maybe = validation.to_maybe()

    assert maybe.is_just(), "After converting to Maybe, it should be just"

    validation_no_errors = Validation("", "")
    is_fail = validation_no_errors.is_fail()

    assert is_fail != False, "If Validation has no errors, is_fail should not be False"

def test_validation_eq():
    """
    Test case to verify the equality of two Validation instances.
    
    This test case creates two Validation instances and checks whether they are equal.
    A Validation instance is said to be equal if both their 'value' and 'error' properties are equal.
    """

    from builtins import None as NONE
    from validation import Validation

    # Setup/Constants
    VALID_NUMBER = -6891
    NUMBER = 3125
    VALIDATION_TUPLE = (NUMBER,)

    # Create the first Validation instance.
    first_validation = Validation(VALID_NUMBER, VALIDATION_TUPLE)

    # Create the second Validation instance.
    second_validation = Validation(VALID_NUMBER, VALIDATION_TUPLE)

    # Execution.
    result = (first_validation == second_validation)

    # Assertion.
    assert result, "Expected both Validation instances to be equal but they are not."

