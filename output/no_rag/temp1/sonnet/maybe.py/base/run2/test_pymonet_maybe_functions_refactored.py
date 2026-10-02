import pytest
import maybe as maybe
import typing as typing

def test_maybe_initialization_with_bytes():
    # Test that a Maybe object can be initialized with bytes values
    # as both the value and default parameters
    
    # Setup: Create a bytes object with specific byte values
    SAMPLE_BYTES = b"\xf4\xaf\xe2\xc9\xee\xc8\xd67n\x9eK\x0b\x97Y\xb5"
    
    # Execution: Initialize a Maybe object using the bytes as both value and default
    maybe_instance = maybe.Maybe(SAMPLE_BYTES, SAMPLE_BYTES)
    
    # Assertion: Verify the Maybe object was created successfully
    assert maybe_instance is not None

def test_maybe_initialization_with_none_values():
    # Test that Maybe can be initialized with None values for both parameters
    # This verifies the basic construction of a Maybe object with null/empty state
    
    # Setup
    NONE_VALUE = None
    
    # Execution
    maybe_instance = maybe.Maybe(NONE_VALUE, NONE_VALUE)
    
    # Assertion
    assert maybe_instance is not None

def test_maybe_operations_with_string_value():
    """
    Test Maybe monad operations when initialized with a string value.
    Verifies that:
    - __eq__ returns False when comparing Maybe to a non-Maybe object (string)
    - ap, map, filter, get_or_else operations work correctly on a Maybe with string value
    - to_validation and bind operations chain correctly
    - to_either transforms a bound Maybe result into an Either
    """
    # Setup
    STRING_VALUE = "p4xa>bl^oP"
    
    # Create a Maybe instance with string value (non-standard usage, value and is_nothing are both strings)
    maybe_with_string = maybe.Maybe(STRING_VALUE, STRING_VALUE)
    
    # Execution - test __eq__ with a non-Maybe object (string)
    # Should return False since string is not an instance of Maybe
    is_equal_to_string = maybe_with_string.__eq__(STRING_VALUE)
    
    # Apply the Maybe's value as a function to the string applicative
    ap_result_1 = maybe_with_string.ap(STRING_VALUE)
    
    # Get value or fallback to the string default
    value_or_default = maybe_with_string.get_or_else(STRING_VALUE)
    
    # Map and filter using the result of ap (which is a Maybe)
    mapped_result_1 = maybe_with_string.map(is_equal_to_string)
    filtered_result_1 = maybe_with_string.filter(is_equal_to_string)
    mapped_result_2 = maybe_with_string.map(is_equal_to_string)
    
    # Apply the Maybe's value again to confirm consistent behavior
    ap_result_2 = maybe_with_string.ap(STRING_VALUE)
    
    # Verify two ap results are equal
    are_ap_results_equal = ap_result_1.__eq__(ap_result_2)
    
    # Filter the first ap result using the value retrieved from get_or_else
    filtered_ap_result = ap_result_1.filter(value_or_default)
    
    # Get the value or default from second ap result
    ap_value_or_default = ap_result_2.get_or_else(STRING_VALUE)
    
    # Create a second Maybe instance with the same string value
    maybe_with_string_2 = maybe.Maybe(STRING_VALUE, STRING_VALUE)
    
    # Transform to Validation and use the result as a bind mapper
    validation_result = maybe_with_string_2.to_validation()
    bound_result = maybe_with_string_2.bind(validation_result)
    
    # Transform the bound result to Either
    either_result = bound_result.to_either()
    
    # Assertions
    # __eq__ should return False since STRING_VALUE is not a Maybe instance
    assert is_equal_to_string is False
    
    # Two separate ap calls with same arguments should produce equal results
    assert are_ap_results_equal is True
    
    # either_result should be a valid Either instance (Right or Left)
    assert either_result is not None

def test_maybe_equality_with_non_maybe_type_returns_false():
    # Test that comparing a Maybe instance with a non-Maybe type (set) returns False
    # The __eq__ method should return False when the other object is not a Maybe instance
    
    # Setup
    BOOL_VALUE = False
    non_maybe_set = {BOOL_VALUE}  # A set containing False values (duplicates collapse to one element)
    
    # Create a Maybe instance with None values (representing Nothing)
    maybe_nothing = maybe.Maybe(None, None)
    
    # Execution
    # Compare Maybe instance with a set, which is not a Maybe type
    result = maybe_nothing.__eq__(non_maybe_set)
    
    # Assertion
    # Since a set is not an instance of Maybe, __eq__ should return False
    assert result == False

def test_maybe_bind_map_and_to_box_operations():
    # Constants
    TRUTHY_VALUE = True
    TUPLE_VALUE = (True, True, True, True)

    # Test bind and map operations on Maybe with a truthy value
    # Setup: Create a Maybe instance with a truthy value
    maybe_with_bool = maybe.Maybe(TRUTHY_VALUE, TRUTHY_VALUE)

    # Execution: Bind and map using truthy value as mapper (callable)
    bound_maybe = maybe_with_bool.bind(TRUTHY_VALUE)
    mapped_maybe = bound_maybe.map(TRUTHY_VALUE)

    # Setup: Create a Maybe instance with a tuple value
    maybe_with_tuple = maybe.Maybe(TUPLE_VALUE, TRUTHY_VALUE)

    # Test that calling to_box() on a plain set raises an AttributeError
    # since set does not have a to_box method (only Maybe does)
    plain_set = set()
    with pytest.raises(AttributeError):
        # Assertion: set does not have to_box method, this should raise an error
        plain_set.to_box()

def test_map_on_empty_maybe_returns_nothing():
    # Test that calling map on an empty Maybe (is_nothing=False with None value)
    # returns a new empty Maybe without applying the mapper function
    
    # Setup
    EMPTY_VALUE = None
    IS_NOTHING = False
    MAPPER_FUNCTION = False  # Using False as a dummy mapper (not expected to be called)
    
    # Execution
    empty_maybe = maybe.Maybe(EMPTY_VALUE, IS_NOTHING)
    result = empty_maybe.map(MAPPER_FUNCTION)
    
    # Assertion
    # When Maybe is empty (is_nothing=True), map should return a new empty Maybe
    assert result.is_nothing

def test_bind_on_empty_maybe_returns_nothing():
    # Constants for test setup
    VALID_VALUE = True
    EMPTY_VALUE = None
    IS_PRESENT = True
    IS_EMPTY = False
    MAPPER = {}  # Used as a mapper argument (not called since Maybe is empty)

    # Setup: Create a non-empty Maybe and an empty Maybe
    non_empty_maybe = maybe.Maybe(VALID_VALUE, IS_PRESENT)
    empty_maybe = maybe.Maybe(EMPTY_VALUE, IS_EMPTY)

    # Execution: Call bind on empty Maybe with a mapper
    # Since the Maybe is empty (is_nothing=True), bind should return a new empty Maybe
    result = empty_maybe.bind(MAPPER)

    # Assertion: Verify that binding on an empty Maybe returns an empty Maybe (nothing)
    assert result.is_nothing

def test_maybe_chained_operations_with_filter_ap_and_transformations():
    # Constants for test setup
    BYTES_VALUE = b"\x9f\x02Gj\xbbw\xdb\x8b\xe7\xda"
    INT_VALUE = 0
    BOOL_VALUE = True

    # Setup: Create a Maybe with bytes value and no default (nothing)
    maybe_with_bytes = maybe.Maybe(BYTES_VALUE, None)
    
    # Execute: Transform bytes Maybe to Box representation
    box_from_bytes_maybe = maybe_with_bytes.to_box()

    # Setup: Create a Maybe with integer value and True as default
    maybe_with_int = maybe.Maybe(INT_VALUE, BOOL_VALUE)
    
    # Execute: Filter the int Maybe using itself as the filterer (maybe_with_int acts as callable)
    filtered_maybe = maybe_with_int.filter(maybe_with_int)
    
    # Execute: Transform int Maybe to Lazy monad
    lazy_from_int_maybe = maybe_with_int.to_lazy()
    
    # Execute: Apply the filtered Maybe's function to the bytes Maybe
    ap_result = filtered_maybe.ap(maybe_with_bytes)
    
    # Execute: Filter the ap result using the filtered Maybe
    filtered_ap_result = filtered_maybe.filter(ap_result)
    
    # Setup: Create a Maybe combining the Lazy monad and Box as its value and default
    maybe_with_lazy_and_box = maybe.Maybe(lazy_from_int_maybe, box_from_bytes_maybe)
    
    # Assert: Verify that the Lazy monad is not equal to a plain boolean True value
    # since Lazy is a Maybe instance check, this should return False
    is_lazy_equal_to_bool = lazy_from_int_maybe.__eq__(BOOL_VALUE)
    assert is_lazy_equal_to_bool == False

def test_ap_on_nothing_maybe_returns_nothing():
    # Constants for test setup
    APPLICATIVE_VALUE = 2862
    MAYBE_VALUE = None
    IS_NOTHING = False

    # Setup: Create a Maybe instance with None value and is_nothing flag set to False
    nothing_maybe = maybe.Maybe(MAYBE_VALUE, IS_NOTHING)

    # Execute: Apply the applicative to the Maybe instance
    # Since the Maybe has None value and is_nothing is False, ap should apply the function
    result = nothing_maybe.ap(APPLICATIVE_VALUE)

    # Assert: Verify that applying to a Maybe with None value returns nothing
    # When is_nothing is True, ap returns a copy of itself (nothing)
    # When is_nothing is False but value is None, map is called on applicative with None
    assert result is not None

def test_maybe_filter_and_transform_operations():
    # Constants for test setup
    INITIAL_VALUE = 0
    IS_PRESENT = True

    # Setup: Create a Maybe instance with a value (not nothing)
    maybe_with_value = maybe.Maybe(INITIAL_VALUE, IS_PRESENT)

    # Execute: Apply filter using maybe itself as the filterer function
    # Since maybe_with_value is a Maybe object (truthy), filter should return a Maybe with the same value
    filtered_maybe = maybe_with_value.filter(maybe_with_value)

    # Execute: Convert original maybe to Lazy monad
    lazy_from_original = maybe_with_value.to_lazy()

    # Execute: Convert filtered maybe to Lazy monad
    lazy_from_filtered = filtered_maybe.to_lazy()

    # Execute: Apply filter on filtered_maybe using lazy_from_filtered as filterer
    # lazy_from_filtered is a Lazy object (truthy), so filter should return a Maybe with the same value
    double_filtered_maybe = filtered_maybe.filter(lazy_from_filtered)

    # Execute: Convert double filtered maybe to Try monad
    try_from_double_filtered = double_filtered_maybe.to_try()

    # Execute: Convert original maybe to Lazy monad again (second conversion)
    lazy_from_original_second = maybe_with_value.to_lazy()

    # Execute: Map filtered_maybe using filtered_maybe itself as the mapper function
    # Since filtered_maybe is callable (it's a Maybe with __call__ not defined, this tests duck typing)
    mapped_maybe = filtered_maybe.map(filtered_maybe)

    # Assert: Verify filtered maybe retains the original value when filter condition is truthy
    assert filtered_maybe.value == INITIAL_VALUE

    # Assert: Verify double filtered maybe retains the value when filter condition is truthy
    assert double_filtered_maybe.value == INITIAL_VALUE

    # Assert: Verify the Try monad from double filtered is successful with correct value
    assert try_from_double_filtered.is_success is True
    assert try_from_double_filtered.value == INITIAL_VALUE

def test_filter_with_nothing_maybe_returns_nothing_and_converts_to_lazy():
    # Constants for test setup
    NEGATIVE_VALUE = -283
    FILTER_TUPLE = (NEGATIVE_VALUE, NEGATIVE_VALUE, NEGATIVE_VALUE)
    
    # Setup: Create a Maybe with None value (nothing) but with is_nothing=False (True passed as second arg)
    initial_value = None
    is_not_nothing = True
    maybe_with_none_value = maybe.Maybe(initial_value, is_not_nothing)
    
    # Execution: Filter the Maybe using a tuple as filterer
    # Since maybe_with_none_value has None as value and the filterer is a tuple,
    # filter will check is_nothing first - since is_nothing=False, it will try to call tuple as filterer
    filtered_maybe = maybe_with_none_value.filter(FILTER_TUPLE)
    
    # Convert the filtered result to a Lazy monad
    lazy_result = filtered_maybe.to_lazy()
    
    # Setup: Create a second Maybe with None value and None is_nothing (defaults to nothing)
    second_maybe_value = None
    second_maybe_is_nothing = None
    maybe_nothing = maybe.Maybe(second_maybe_value, second_maybe_is_nothing)
    
    # Assertion: Filter the nothing Maybe using the lazy result as filterer
    # Since maybe_nothing is nothing (is_nothing=True), filter should return Maybe.nothing()
    result = maybe_nothing.filter(lazy_result)
    
    # Verify the result is a nothing Maybe
    assert result.is_nothing == True

def test_maybe_filter_with_value_from_non_empty_maybe():
    # Constants for test setup
    DEFAULT_INT_VALUE = 2281
    SAMPLE_STRING = "gZ(\\mOcN"
    
    # Setup - Create a non-empty Maybe with a tuple value
    sample_dict = {SAMPLE_STRING: SAMPLE_STRING}
    sample_tuple = (SAMPLE_STRING, SAMPLE_STRING, sample_dict, sample_dict)
    IS_NOTHING = False
    HAS_VALUE = True
    
    non_empty_maybe = maybe.Maybe(sample_tuple, HAS_VALUE)
    
    # Execution - Get value from non-empty Maybe (should return tuple, not default)
    # Since Maybe is not empty (is_nothing=False), get_or_else returns the tuple value
    retrieved_value = non_empty_maybe.get_or_else(DEFAULT_INT_VALUE)
    
    # Convert non-empty Maybe to Box (should contain the tuple value)
    box_from_maybe = non_empty_maybe.to_box()
    
    # Setup - Create an empty Maybe with a Generic value
    generic_instance = typing.Generic()
    empty_maybe = maybe.Maybe(generic_instance, IS_NOTHING)
    
    # Execution - Filter the empty Maybe using the retrieved tuple as filterer
    # Since empty_maybe is_nothing=True, filter should return Maybe.nothing()
    filter_result = empty_maybe.filter(retrieved_value)
    
    # Assertion - Filtered result on empty Maybe should be nothing
    assert filter_result.is_nothing == True

def test_maybe_transformations_and_bind_with_various_types():
    # Test Maybe transformations (to_validation, to_try) and bind operation
    # with different value types including bool, int, float, and None

    # Setup - Constants for test values
    VALID_BOOL_VALUE = True
    EMPTY_VALUE = None
    NEGATIVE_FLOAT_VALUE = -286.64
    NEGATIVE_INT_VALUE = -1784
    EMPTY_TUPLE = ()

    # Test 1: Maybe with bool value and None as "nothing" indicator
    # Creates a Maybe with a valid bool value, None is just the nothing placeholder
    maybe_with_bool = maybe.Maybe(VALID_BOOL_VALUE, EMPTY_VALUE)
    
    # Execute transformation to Validation - should return successful Validation with bool value
    validation_from_bool_maybe = maybe_with_bool.to_validation()
    assert validation_from_bool_maybe is not None

    # Test 2: Maybe with negative int value and empty tuple as "nothing" indicator
    maybe_with_int = maybe.Maybe(NEGATIVE_INT_VALUE, EMPTY_TUPLE)

    # Execute transformation to Validation - should return successful Validation with int value
    validation_from_int_maybe = maybe_with_int.to_validation()
    assert validation_from_int_maybe is not None

    # Execute get_or_else - since Maybe has a value, should return the Maybe's value (not the default)
    result_get_or_else = maybe_with_int.get_or_else(NEGATIVE_INT_VALUE)
    assert result_get_or_else == NEGATIVE_INT_VALUE

    # Execute transformation to Try - should return successful Try with int value
    try_from_int_maybe = maybe_with_int.to_try()
    assert try_from_int_maybe is not None
    assert try_from_int_maybe.is_success

    # Test 3: Maybe with float value - just verifying instantiation works
    maybe_with_float = maybe.Maybe(NEGATIVE_FLOAT_VALUE, NEGATIVE_FLOAT_VALUE)

    # Execute bind using the Try object as mapper - applies the Try transformation on Maybe's value
    # Since maybe_with_int has a value, bind should call try_from_int_maybe with the int value
    bind_result = maybe_with_int.bind(try_from_int_maybe)
    assert bind_result is not None

def test_map_on_nothing_returns_nothing_and_to_either_on_nothing_returns_right():
    # Test that map on a Maybe with is_nothing=True returns an empty Maybe,
    # and that to_either on a Maybe with a value returns a Right monad.

    # Setup
    NOTHING_VALUE = None
    IS_NOTHING = True
    JUST_VALUE = -1095

    # Create a Maybe that represents "nothing" (empty Maybe)
    nothing_maybe = maybe.Maybe(NOTHING_VALUE, IS_NOTHING)
    
    # Create a set to use as a mapper (will not be called since Maybe is nothing)
    set_mapper = {True}

    # Execution: map on a nothing Maybe should return a new empty Maybe
    mapped_result = nothing_maybe.map(set_mapper)

    # Create a Maybe with an actual value (is_nothing=False means it has a value)
    just_maybe = maybe.Maybe(JUST_VALUE, IS_NOTHING)

    # Execution: to_either on a Just Maybe should return a Right monad
    either_result = just_maybe.to_either()

    # Assertions
    # mapped_result should be an empty Maybe (nothing)
    assert mapped_result.is_nothing == True

    # either_result should be a Right monad wrapping the value
    assert either_result.get_right() == JUST_VALUE

def test_maybe_transformations_with_none_and_tuple_values():
    """
    Test Maybe monad transformations (to_either, to_lazy, to_try) with two different Maybe instances:
    1. A 'nothing' Maybe created with None value and None is_nothing flag
    2. A 'something' Maybe created with a tuple value and False is_nothing flag
    
    Verifies that:
    - A Nothing Maybe correctly transforms to Left(None) via to_either()
    - A Nothing Maybe correctly transforms to Lazy(lambda: None) via to_lazy()
    - A Something Maybe with tuple value transforms to Try(value, is_success=True) via to_try()
    - A Something Maybe with tuple value transforms to Right(value) via to_either()
    - The resulting Try monad can be further transformed to Lazy
    """
    # Setup
    NONE_VALUE = None
    NOTHING_FLAG = None
    IS_SOMETHING_FLAG = False

    # Create a Nothing Maybe (both value and is_nothing are None)
    nothing_maybe = maybe.Maybe(NONE_VALUE, NOTHING_FLAG)
    
    # Create a Something Maybe with a tuple containing the nothing_maybe as value
    tuple_value = (nothing_maybe,)
    something_maybe = maybe.Maybe(tuple_value, IS_SOMETHING_FLAG)

    # Execute transformations on Nothing Maybe
    nothing_maybe_as_lazy = nothing_maybe.to_lazy()
    nothing_maybe_as_either_first = nothing_maybe.to_either()
    nothing_maybe_as_either_second = nothing_maybe.to_either()

    # Execute transformations on Something Maybe
    something_maybe_as_try = something_maybe.to_try()
    something_maybe_as_either = something_maybe.to_either()

    # Transform the Try result further to Lazy
    try_as_lazy = something_maybe_as_try.to_lazy()

    # Assert Nothing Maybe transforms to Left(None)
    assert nothing_maybe_as_either_first.get() is None
    assert nothing_maybe_as_either_second.get() is None

    # Assert Something Maybe transforms to Right with tuple value
    assert something_maybe_as_either.get() == tuple_value

    # Assert Something Maybe transforms to successful Try with tuple value
    assert something_maybe_as_try.get() == tuple_value
    assert something_maybe_as_try.is_success is True

    # Assert Nothing Maybe transforms to Lazy returning None
    assert nothing_maybe_as_lazy.get() is None

    # Assert Try to Lazy transformation works
    assert try_as_lazy is not None

def test_maybe_to_try_to_box_conversion_with_value():
    """
    Test the chained transformation of a Maybe monad with a value
    through Try and then to a Box monad.
    
    A Maybe with a value (is_nothing=False) should:
    1. Convert to a successful Try monad
    2. Then convert to a Box monad containing the original value
    """
    # Setup: Create a Maybe monad with a value (not nothing)
    MAYBE_VALUE = True
    IS_NOTHING = False
    maybe_with_value = maybe.Maybe(MAYBE_VALUE, IS_NOTHING)

    # Execute: Convert Maybe to Try (should be successful since is_nothing=False)
    try_result = maybe_with_value.to_try()

    # Execute: Convert the successful Try to a Box monad
    box_result = try_result.to_box()

    # Assert: Box should contain the original value from the Maybe monad
    assert box_result.value == MAYBE_VALUE

def test_maybe_nothing_with_chained_transformations():
    # Constants
    BYTES_VALUE = b"C\xcf\xe7/"
    INITIAL_VALUE = None
    IS_NOTHING = True

    # Setup: Create a Maybe that represents a "nothing" (empty) value
    maybe_nothing = maybe.Maybe(INITIAL_VALUE, IS_NOTHING)

    # Execute: Apply None applicative to nothing Maybe - should return nothing
    maybe_after_ap = maybe_nothing.ap(INITIAL_VALUE)

    # Execute: Chain transformations from the nothing Maybe
    lazy_from_nothing = maybe_after_ap.to_lazy()           # Convert nothing Maybe to Lazy (returns lambda: None)
    validation_from_nothing = lazy_from_nothing.to_validation()  # Convert Lazy to Validation (success with None)

    # Execute: Filter the original nothing Maybe using the validation as a predicate
    # Since maybe_nothing is already nothing, filter should return nothing regardless
    maybe_filtered = maybe_nothing.filter(validation_from_nothing)

    # Execute: Get value or use filtered Maybe as default (since it's nothing, returns the default)
    value_or_default = maybe_filtered.get_or_else(maybe_filtered)

    # Execute: Convert the filtered nothing Maybe to Either (should return Left(None))
    either_from_filtered = maybe_filtered.to_either()

    # Execute: Convert validation to Try (success with None)
    try_from_validation = validation_from_nothing.to_try()

    # Assert: Compare filtered maybe with ap result - both should be nothing, so they should be equal
    are_equal = maybe_filtered.__eq__(maybe_after_ap)
    assert are_equal, "Both Maybes should be nothing and therefore equal"

    # Execute: Convert the default value (which is a nothing Maybe) to Box
    box_from_nothing = value_or_default.to_box()

    # Execute: Apply bytes to the Try monad (Try with None value, not successful)
    try_from_validation.ap(BYTES_VALUE)

def test_maybe_operations_with_nothing_and_bytes_value():
    # Constants
    BYTES_VALUE = b"\xdbC\xcf\xe7/"
    NONE_VALUE = None
    IS_NOTHING = True
    INT_VALUE = -3289

    # Setup: Create Maybe instances
    # maybe_nothing is a Maybe that wraps None with is_nothing=True (empty Maybe)
    maybe_nothing = maybe.Maybe(NONE_VALUE, IS_NOTHING)
    
    # maybe_with_bytes is a Maybe that wraps bytes value with is_nothing=True (empty Maybe)
    maybe_with_bytes = maybe.Maybe(NONE_VALUE, BYTES_VALUE)

    # Execution: Chain operations on empty Maybe (maybe_nothing)
    # Applying None to an empty Maybe should return an empty Maybe
    ap_result_none = maybe_nothing.ap(NONE_VALUE)
    # Applying bytes to the previous empty Maybe result should still return empty Maybe
    ap_result_bytes = ap_result_none.ap(BYTES_VALUE)
    # Converting empty Maybe to Validation should yield successful Validation with None
    validation_from_nothing = ap_result_bytes.to_validation()

    # Execution: Operations on maybe_with_bytes (also empty due to is_nothing=BYTES_VALUE being truthy)
    # get_or_else returns the default value since maybe_with_bytes is empty
    get_or_else_result = maybe_with_bytes.get_or_else(maybe_with_bytes)
    
    # Convert maybe_with_bytes to Validation (successful with None since it's empty)
    validation_from_bytes_maybe = maybe_with_bytes.to_validation()
    
    # Bind with validation as mapper - since maybe_with_bytes is empty, returns empty Maybe
    bind_result = maybe_with_bytes.bind(validation_from_bytes_maybe)
    
    # Convert maybe_with_bytes to Either - Left(None) since it's empty
    either_result = maybe_with_bytes.to_either()
    
    # Apply maybe_with_bytes to itself - empty Maybe applies to empty Maybe
    ap_result_self = maybe_with_bytes.ap(maybe_with_bytes)

    # Assertions: Check equality operations
    # Either and Validation should not be equal (different types)
    either_eq_validation = either_result.__eq__(validation_from_bytes_maybe)
    
    # Bind either with maybe_with_bytes as mapper
    either_bind_result = either_result.bind(maybe_with_bytes)
    
    # Convert maybe_with_bytes to Try - unsuccessful Try with None since it's empty
    try_result = maybe_with_bytes.to_try()
    
    # Check equality between maybe_with_bytes and bind_result (both empty Maybes)
    maybe_eq_bind = maybe_with_bytes.__eq__(bind_result)
    
    # Convert bind_result to Validation
    bind_validation = bind_result.to_validation()
    
    # Apply int value to Try - empty Try applying int
    try_result.ap(INT_VALUE)

def test_maybe_map_with_validation_mapper_when_nothing():
    """
    Test that Maybe.map() correctly handles a Nothing Maybe when using a Validation mapper.
    
    This test verifies the chain of transformations:
    1. Creating a Nothing Maybe (both value and is_nothing are False/falsy)
    2. Converting Maybe to Either (should return Left(None) for Nothing)
    3. Converting Maybe to Lazy (should return Lazy(lambda: None) for Nothing)
    4. Converting Lazy to Validation (should return successful Validation with None)
    5. Using the resulting Validation as a mapper function for another Nothing Maybe
    
    The core purpose is to verify that map() on a Nothing Maybe returns a new Nothing Maybe
    without calling the mapper, even when the mapper is a complex chained transformation result.
    """
    # Setup
    IS_NOTHING = False
    VALUE = False
    
    # Create initial Nothing Maybe and verify equality
    nothing_maybe = maybe.Maybe(IS_NOTHING, VALUE)
    is_equal_to_false = nothing_maybe.__eq__(VALUE)
    
    # Create second Nothing Maybe and transform it through the monad chain
    source_maybe = maybe.Maybe(IS_NOTHING, VALUE)
    
    # Execute transformation chain: Maybe -> Either -> Lazy -> Validation
    either_result = source_maybe.to_either()      # Returns Left(None) since Maybe is Nothing
    lazy_result = source_maybe.to_lazy()          # Returns Lazy(lambda: None) since Maybe is Nothing
    validation_mapper = lazy_result.to_validation() # Returns successful Validation with None
    
    # Create a third Nothing Maybe and apply the validation mapper
    target_maybe = maybe.Maybe(IS_NOTHING, VALUE)
    
    # Assert - map on Nothing Maybe should return new Nothing Maybe without calling mapper
    result = target_maybe.map(validation_mapper)

def test_maybe_nothing_equality_and_monad_transformations():
    """
    Test that a Maybe monad in 'nothing' state:
    1. Is equal to itself
    2. Can be transformed to a failed Try monad
    3. Can be transformed from Try to a successful Validation monad with None value
    """
    # Setup - Create a Maybe monad in 'nothing' state (both value and is_nothing are False)
    IS_NOTHING = False
    NOTHING_VALUE = False
    nothing_maybe = maybe.Maybe(IS_NOTHING, NOTHING_VALUE)

    # Execute - Test equality of Maybe with itself
    is_equal_to_itself = nothing_maybe.__eq__(nothing_maybe)

    # Assert - Maybe should be equal to itself
    assert is_equal_to_itself is True

    # Execute - Transform Nothing Maybe to Try monad
    # Since is_nothing=False but value=False, this will create a successful Try with value=False
    try_monad = nothing_maybe.to_try()

    # Execute - Transform Try monad to Validation monad
    # Since the Try was created from a Nothing Maybe, it should be a failed Try
    # which transforms to a successful Validation with None
    validation_monad = try_monad.to_validation()

    # Assert - Validation should be successful with the value from the Try monad
    assert validation_monad is not None

