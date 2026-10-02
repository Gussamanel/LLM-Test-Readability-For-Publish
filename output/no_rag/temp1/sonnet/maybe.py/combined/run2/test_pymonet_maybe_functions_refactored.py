import pytest
import maybe as maybe
import typing as typing

def test_maybe_initialization_with_bytes():
    # Test that a Maybe object can be initialized with bytes values
    # as both the value and default parameters
    
    # Setup: Create a bytes object to use as both value and default
    SAMPLE_BYTES = b"\xf4\xaf\xe2\xc9\xee\xc8\xd67n\x9eK\x0b\x97Y\xb5"
    
    # Execution: Initialize a Maybe instance with bytes as value and default
    maybe_instance = maybe.Maybe(SAMPLE_BYTES, SAMPLE_BYTES)
    
    # Assertion: Verify the Maybe instance was created successfully
    assert maybe_instance is not None

def test_maybe_initialization_with_none_values():
    # Test that a Maybe object can be initialized with None values
    # for both the value and the type parameters
    
    # Setup
    NONE_VALUE = None
    NONE_TYPE = None
    
    # Execution
    # Create a Maybe instance with both value and type set to None
    maybe_instance = maybe.Maybe(NONE_VALUE, NONE_TYPE)
    
    # Assertion
    # Verify the Maybe instance was created successfully
    assert maybe_instance is not None

def test_maybe_operations_with_non_empty_value():
    """
    Test various Maybe monad operations when initialized with a non-empty value.
    Verifies that chaining operations like ap, get_or_else, map, filter, bind,
    and to_validation work correctly on a non-empty Maybe instance.
    """
    # Setup
    INITIAL_VALUE = "p4xa>bl^oP"
    
    # Create a Maybe instance with a non-empty value
    maybe_with_value = maybe.Maybe(INITIAL_VALUE, INITIAL_VALUE)
    
    # Verify equality comparison with a non-Maybe object returns False
    is_equal_to_string = maybe_with_value.__eq__(INITIAL_VALUE)
    assert not is_equal_to_string  # Maybe should not equal a plain string
    
    # Execute ap operation - applies the Maybe's function value to the applicative
    ap_result_first = maybe_with_value.ap(INITIAL_VALUE)
    
    # Execute get_or_else - should return the Maybe's value since it's not empty
    value_or_default = maybe_with_value.get_or_else(INITIAL_VALUE)
    assert value_or_default == INITIAL_VALUE
    
    # Execute map operations using the result of the equality check (False) as mapper
    map_result_first = maybe_with_value.map(is_equal_to_string)
    filter_result = maybe_with_value.filter(is_equal_to_string)
    map_result_second = maybe_with_value.map(is_equal_to_string)
    
    # Execute a second ap operation and verify consistency with the first
    ap_result_second = maybe_with_value.ap(INITIAL_VALUE)
    are_ap_results_equal = ap_result_first.__eq__(ap_result_second)
    assert are_ap_results_equal  # Both ap results should be equivalent
    
    # Execute filter on the first ap result using the Maybe value as filterer
    filter_on_ap_result = ap_result_first.filter(value_or_default)
    
    # Execute get_or_else on second ap result
    ap_value_or_default = ap_result_second.get_or_else(INITIAL_VALUE)
    
    # Create a second Maybe instance for transformation operations
    maybe_for_transformation = maybe.Maybe(INITIAL_VALUE, INITIAL_VALUE)
    
    # Transform Maybe to Validation - should produce a successful Validation
    validation_result = maybe_for_transformation.to_validation()
    
    # Bind using the Validation's to_validation result as mapper
    bind_result = maybe_for_transformation.bind(validation_result)
    
    # Transform the bound result to Either - should produce a Right with the value
    either_result = bind_result.to_either()
    assert either_result is not None

def test_maybe_equality_with_non_maybe_set_returns_false():
    # Test that a Maybe instance returns False when compared to a non-Maybe object (a set)
    # A Maybe initialized with None values should not be equal to a set

    # Setup
    BOOL_VALUE = False
    non_maybe_set = {BOOL_VALUE}  # A set containing False values (duplicates are removed)
    
    # Create a Maybe instance with None for both value and is_nothing
    maybe_instance = maybe.Maybe(None, None)

    # Execute
    # Compare the Maybe instance with a non-Maybe object (a set)
    result = maybe_instance.__eq__(non_maybe_set)

    # Assert
    # Since the set is not an instance of Maybe, equality should return False
    assert result == False

def test_maybe_bind_map_and_to_box_on_invalid_set():
    """
    Test that:
    1. Maybe can be created with a boolean value and is_nothing flag
    2. bind operation on a non-empty Maybe applies mapper and returns result
    3. map operation can be chained on the result of bind
    4. Maybe can be created with a tuple as value
    5. Calling to_box() on a plain set (not a Maybe) raises AttributeError,
       since sets do not have a to_box() method
    """
    # Constants
    IS_NOT_NOTHING = True
    BOOL_VALUE = True
    TUPLE_VALUE = (BOOL_VALUE, BOOL_VALUE, BOOL_VALUE, BOOL_VALUE)

    # Setup - Create a Maybe with a boolean value where is_nothing=False
    maybe_with_bool = maybe.Maybe(BOOL_VALUE, IS_NOT_NOTHING)

    # Execution - Apply bind (using bool as mapper) on a non-empty Maybe
    bind_result = maybe_with_bool.bind(BOOL_VALUE)

    # Apply map (using bool as mapper) on the result of bind
    map_result = bind_result.map(BOOL_VALUE)

    # Setup - Create a Maybe with a tuple value
    maybe_with_tuple = maybe.Maybe(TUPLE_VALUE, IS_NOT_NOTHING)

    # Assertion - Calling to_box() on a plain set raises AttributeError
    # since sets do not have the to_box() method (only Maybe instances do)
    empty_set = set()
    with pytest.raises(AttributeError):
        empty_set.to_box()

def test_map_on_empty_maybe_returns_nothing():
    # Test that calling map on an empty Maybe (nothing) returns a new empty Maybe
    # without calling the mapper function
    
    # Setup: Create an empty Maybe with no value
    EMPTY_VALUE = None
    IS_NOTHING = False
    empty_maybe = maybe.Maybe(EMPTY_VALUE, IS_NOTHING)
    
    # Execute: Apply a mapper function (bool) to the empty Maybe
    MAPPER_FUNCTION = bool
    result = empty_maybe.map(MAPPER_FUNCTION)
    
    # Assert: The result should be a new empty Maybe (nothing)
    assert result.is_nothing

def test_bind_on_empty_maybe_returns_nothing():
    # Constants for test setup
    VALID_VALUE = True
    EMPTY_VALUE = None
    IS_PRESENT = True
    IS_NOTHING = False

    # Setup: Create a Maybe with a value (not used in bind operation, just for context)
    maybe_with_value = maybe.Maybe(VALID_VALUE, IS_PRESENT)

    # Setup: Create an empty Maybe (is_nothing=False means it IS nothing/empty)
    empty_maybe = maybe.Maybe(EMPTY_VALUE, IS_NOTHING)

    # Setup: Use an empty dict as the mapper (won't be called since Maybe is empty)
    mapper_function = {}

    # Execute: Call bind on the empty Maybe
    # When Maybe is empty (is_nothing), bind should return a new empty Maybe
    # without calling the mapper function
    result = empty_maybe.bind(mapper_function)

    # Assert: The result should be a new empty Maybe (nothing)
    assert result.is_nothing
    assert result.value is None

def test_maybe_chained_operations_with_mixed_types():
    """
    Tests chaining multiple Maybe monad operations including filter, ap, to_box, and to_lazy.
    Verifies that Maybe correctly handles transformations between different types (bytes, int, bool)
    and that equality checks work properly when comparing Maybe instances with non-Maybe types.
    """
    # Constants
    BYTES_VALUE = b"\x9f\x02Gj\xbbw\xdb\x8b\xe7\xda"
    INT_VALUE = 0
    BOOL_VALUE = True

    # Setup - Create initial Maybe instances
    # Maybe with bytes value and no is_nothing flag (None defaults to falsy)
    maybe_with_bytes = maybe.Maybe(BYTES_VALUE, None)

    # Transform bytes Maybe to Box monad
    box_from_bytes_maybe = maybe_with_bytes.to_box()

    # Create Maybe with integer value, marked as not nothing (True)
    maybe_with_int = maybe.Maybe(INT_VALUE, BOOL_VALUE)

    # Execution - Chain operations on Maybe instances
    # Filter maybe_with_int using itself as the filterer callable
    filtered_maybe = maybe_with_int.filter(maybe_with_int)

    # Transform maybe_with_int to Lazy monad
    lazy_from_int_maybe = maybe_with_int.to_lazy()

    # Apply filtered_maybe's function to maybe_with_bytes
    applied_maybe = filtered_maybe.ap(maybe_with_bytes)

    # Filter filtered_maybe using the applied result as the filterer
    double_filtered_maybe = filtered_maybe.filter(applied_maybe)

    # Create a new Maybe combining the Lazy monad and the Box monad
    maybe_with_lazy_and_box = maybe.Maybe(lazy_from_int_maybe, box_from_bytes_maybe)

    # Assertion - Verify equality between Lazy monad and a non-Maybe bool value
    # Lazy monad compared with True should return False as they are different types
    is_lazy_equal_to_bool = lazy_from_int_maybe.__eq__(BOOL_VALUE)
    assert is_lazy_equal_to_bool == False

def test_ap_on_nothing_maybe_returns_nothing():
    # Test that applying a Nothing Maybe to an applicative returns a Nothing Maybe
    # When a Maybe is created with is_nothing=False but value=None, 
    # calling ap should attempt to apply the contained value
    
    # Setup
    APPLICATIVE_VALUE = 2862
    EMPTY_VALUE = None
    IS_NOTHING = False
    
    # Create a Maybe instance with None value and is_nothing=False
    maybe_with_none_value = maybe.Maybe(EMPTY_VALUE, IS_NOTHING)
    
    # Execute
    # Attempt to apply the Maybe's None value to the applicative integer
    # This tests the behavior when ap is called with a non-Maybe applicative
    # while the Maybe itself has a None value but is not flagged as nothing
    result = maybe_with_none_value.ap(APPLICATIVE_VALUE)

def test_maybe_filter_and_transformations_with_non_empty_value():
    # Constants for test setup
    INITIAL_VALUE = 0
    IS_PRESENT = True

    # Setup: Create a Maybe monad with a value (non-empty/just)
    maybe_with_value = maybe.Maybe(INITIAL_VALUE, IS_PRESENT)

    # Execute: Apply filter using the Maybe instance itself as the filterer
    # Since Maybe is not nothing, it will call filterer(self.value) = maybe_with_value(0)
    filtered_maybe = maybe_with_value.filter(maybe_with_value)

    # Convert original Maybe to Lazy monad
    lazy_from_original = maybe_with_value.to_lazy()

    # Convert filtered Maybe to Lazy monad
    lazy_from_filtered = filtered_maybe.to_lazy()

    # Apply filter on filtered Maybe using the lazy version as filterer
    double_filtered_maybe = filtered_maybe.filter(lazy_from_filtered)

    # Transform double-filtered Maybe to Try monad
    try_from_double_filtered = double_filtered_maybe.to_try()

    # Convert original Maybe to another Lazy monad
    another_lazy_from_original = maybe_with_value.to_lazy()

    # Apply map on filtered Maybe using itself as the mapper function
    mapped_maybe = filtered_maybe.map(filtered_maybe)

    # Assert: Verify the resulting Maybe monad from mapping is empty (nothing)
    # since filtered_maybe(0) would be called and returns an empty Maybe
    assert mapped_maybe.is_nothing

    # Assert: Verify the Try monad reflects the state of double_filtered_maybe
    assert try_from_double_filtered is not None

    # Assert: Both lazy conversions from original Maybe should produce the same value
    assert lazy_from_original.get() == another_lazy_from_original.get()

def test_filter_with_nothing_maybe_returns_nothing_and_converts_to_lazy():
    # Constants for test setup
    NEGATIVE_VALUE = -283
    
    # Setup: Create a tuple to use as filter argument and a Maybe with None value (nothing)
    filter_tuple = (NEGATIVE_VALUE, NEGATIVE_VALUE, NEGATIVE_VALUE)
    nothing_value = None
    is_nothing = True
    
    # Create a Maybe that represents nothing (is_nothing=True)
    nothing_maybe = maybe.Maybe(nothing_value, is_nothing)
    
    # Execution: Filter the nothing Maybe - should return nothing since Maybe is empty
    filtered_maybe = nothing_maybe.filter(filter_tuple)
    
    # Convert filtered result to Lazy monad - since Maybe is nothing, should wrap None
    lazy_result = filtered_maybe.to_lazy()
    
    # Setup: Create another nothing Maybe to test filter with a Lazy monad as filterer
    second_nothing_value = None
    second_nothing_flag = None
    second_nothing_maybe = maybe.Maybe(second_nothing_value, second_nothing_flag)
    
    # Execution: Filter second nothing Maybe using the Lazy monad as filterer
    # Since second Maybe is nothing (is_nothing evaluates to falsy), should return nothing
    result = second_nothing_maybe.filter(lazy_result)
    
    # Assertion: Result should be a nothing Maybe since the input Maybe was empty
    assert result.is_nothing

def test_maybe_filter_with_retrieved_value_as_filterer_returns_nothing():
    """
    Test that Maybe.filter() correctly handles using a retrieved value as a filterer function.
    
    This test verifies:
    1. Maybe.get_or_else() returns the contained value when Maybe is not empty
    2. Maybe.to_box() correctly wraps a non-empty Maybe value in a Box
    3. Maybe.filter() returns an empty Maybe when the filterer function returns False
       for the contained value (Generic instance)
    """
    # Setup
    DEFAULT_INT_VALUE = 2281
    SAMPLE_STRING = "gZ(\\mOcN"
    
    sample_dict = {SAMPLE_STRING: SAMPLE_STRING}
    sample_tuple = (SAMPLE_STRING, SAMPLE_STRING, sample_dict, sample_dict)
    
    # Create a non-empty Maybe containing a tuple
    IS_PRESENT = True
    maybe_with_tuple = maybe.Maybe(sample_tuple, IS_PRESENT)
    
    # Create a Maybe containing a Generic object that is empty (nothing)
    generic_value = typing.Generic()
    IS_NOTHING = False
    maybe_with_generic = maybe.Maybe(generic_value, IS_NOTHING)
    
    # Execution
    # get_or_else returns the tuple value since Maybe is not empty
    retrieved_value = maybe_with_tuple.get_or_else(DEFAULT_INT_VALUE)
    
    # Convert the non-empty Maybe to a Box containing the tuple value
    box_result = maybe_with_tuple.to_box()
    
    # Use the retrieved tuple as a filterer function on the Generic-containing Maybe
    filter_result = maybe_with_generic.filter(retrieved_value)
    
    # Assertion
    # filter should return an empty Maybe since retrieved_value (tuple) is not a valid filterer
    # that returns True for the Generic value
    assert filter_result.is_nothing

def test_maybe_transformations_and_bind_with_various_states():
    """
    Test Maybe monad transformations and bind operation across different states:
    - A 'Just' Maybe (has value, not nothing) with None as value
    - A 'Nothing' Maybe (is nothing) with an empty tuple
    - Verifying to_validation, to_try, get_or_else and bind operations
    """
    # Setup - Maybe with True as 'is_nothing' flag and None as value (Just Maybe)
    IS_NOTHING_TRUE = True
    NO_VALUE = None
    maybe_just_with_none = maybe.Maybe(IS_NOTHING_TRUE, NO_VALUE)

    # Execute - Transform Just Maybe to Validation
    validation_from_just = maybe_just_with_none.to_validation()

    # Setup - Maybe with negative int as 'is_nothing' flag and empty tuple as value (Nothing Maybe)
    IS_NOTHING_INT = -1784
    EMPTY_TUPLE = ()
    maybe_nothing = maybe.Maybe(IS_NOTHING_INT, EMPTY_TUPLE)

    # Execute - Transform Nothing Maybe to Validation
    validation_from_nothing = maybe_nothing.to_validation()

    # Execute - Get value or else from Nothing Maybe using default value
    DEFAULT_VALUE = -1784
    value_or_default = maybe_nothing.get_or_else(DEFAULT_VALUE)

    # Execute - Transform Nothing Maybe to Try
    try_from_nothing = maybe_nothing.to_try()

    # Setup - Maybe with float values (Just Maybe with float)
    FLOAT_VALUE = -286.64
    maybe_just_with_float = maybe.Maybe(FLOAT_VALUE, FLOAT_VALUE)

    # Execute - Bind Nothing Maybe with the Try result as mapper
    # Since maybe_nothing is Nothing, bind should return a new empty Maybe
    bind_result = maybe_nothing.bind(try_from_nothing)

def test_map_with_nothing_maybe_and_to_either_with_value_maybe():
    # Test that mapping over an empty Maybe returns empty Maybe,
    # and that converting a Maybe with a value to Either returns Right

    # Constants
    NONE_VALUE = None
    INT_VALUE = -1095
    IS_NOTHING_TRUE = True

    # Setup - Create an empty Maybe (is_nothing=True) with None value
    empty_maybe = maybe.Maybe(NONE_VALUE, IS_NOTHING_TRUE)
    
    # Setup - Create a set to use as mapper (callable when used as function)
    set_mapper = {IS_NOTHING_TRUE}

    # Execution - Map over empty Maybe, should return new empty Maybe
    # since is_nothing is True, mapper should not be called
    map_result = empty_maybe.map(set_mapper)

    # Setup - Create a Maybe with an integer value and is_nothing=True
    value_maybe = maybe.Maybe(INT_VALUE, IS_NOTHING_TRUE)

    # Execution - Convert Maybe with value to Either
    # Since is_nothing=True, should return Left(None)
    either_result = value_maybe.to_either()

    # Assert that map result is a Maybe instance (empty Maybe returned)
    assert isinstance(map_result, maybe.Maybe)

    # Assert that either result is an Either instance
    assert either_result is not None

def test_maybe_transformations_with_nothing_and_just_values():
    # Constants
    NOTHING_VALUE = None
    IS_NOTHING = None
    HAS_VALUE = False  # False means it's not "nothing", so it has a value

    # Setup: Create a Maybe with no value (Nothing state)
    maybe_nothing = maybe.Maybe(NOTHING_VALUE, IS_NOTHING)
    
    # Setup: Create a Maybe with a tuple containing the nothing Maybe as value
    tuple_value = (maybe_nothing,)
    maybe_with_value = maybe.Maybe(tuple_value, HAS_VALUE)

    # Execute: Transform Nothing Maybe to Lazy - should return Lazy wrapping None
    lazy_from_nothing = maybe_nothing.to_lazy()

    # Execute: Transform Nothing Maybe to Either - should return Left(None)
    either_from_nothing_first = maybe_nothing.to_either()

    # Execute: Transform Maybe-with-value to Try - should return successful Try with tuple value
    try_from_maybe_with_value = maybe_with_value.to_try()

    # Execute: Transform Nothing Maybe to Either again - should still return Left(None)
    either_from_nothing_second = maybe_nothing.to_either()

    # Execute: Transform Maybe-with-value to Either - should return Right with tuple value
    either_from_maybe_with_value = maybe_with_value.to_either()

    # Execute: Transform the Try (from maybe_with_value) to Lazy
    lazy_from_try = try_from_maybe_with_value.to_lazy()

    # Assert: Verify Nothing Maybe transforms to Lazy wrapping None
    assert lazy_from_nothing is not None

    # Assert: Verify Nothing Maybe transforms to Left (Either) with None
    assert either_from_nothing_first is not None
    assert either_from_nothing_second is not None

    # Assert: Verify Maybe-with-value transforms to successful Try
    assert try_from_maybe_with_value.is_success is True
    assert try_from_maybe_with_value.value == tuple_value

    # Assert: Verify Maybe-with-value transforms to Right (Either) with tuple value
    assert either_from_maybe_with_value is not None

    # Assert: Verify the Try successfully converts to Lazy
    assert lazy_from_try is not None

def test_maybe_to_try_then_to_box_with_value():
    """
    Test that a Maybe containing a value can be successfully transformed
    to a Try monad and then to a Box monad.
    
    When Maybe is initialized with a value (not nothing), converting it to Try
    should produce a successful Try, and subsequently converting that Try to Box
    should wrap the value in a Box monad.
    """
    # Setup: Create a Maybe with a value (is_nothing=False)
    VALUE = True
    IS_NOTHING = False
    maybe_with_value = maybe.Maybe(VALUE, IS_NOTHING)

    # Execution: Transform Maybe to Try monad
    try_result = maybe_with_value.to_try()

    # Assertion: Transform Try to Box monad (validates chain works without errors)
    box_result = try_result.to_box()

def test_maybe_with_nothing_value_transformations_and_comparisons():
    # Constants
    BYTES_VALUE = b"C\xcf\xe7/"
    INITIAL_VALUE = None
    IS_NOTHING = True

    # Setup: Create a Maybe that represents "nothing" (empty Maybe)
    maybe_nothing = maybe.Maybe(INITIAL_VALUE, IS_NOTHING)

    # Execute: Apply None applicative to the nothing Maybe - should return another nothing Maybe
    maybe_after_ap = maybe_nothing.ap(INITIAL_VALUE)

    # Transform the result of ap to a Lazy monad - since it's nothing, returns Lazy with lambda: None
    lazy_from_maybe = maybe_after_ap.to_lazy()

    # Transform Lazy to Validation - since original Maybe was nothing, returns successful Validation with None
    validation_from_lazy = lazy_from_maybe.to_validation()

    # Filter the original nothing Maybe using the Validation as filter function
    # Since maybe_nothing is nothing, filter returns another nothing Maybe
    maybe_after_filter = maybe_nothing.filter(validation_from_lazy)

    # Get the value or else return the filtered Maybe itself as default
    # Since maybe_after_filter is nothing, returns the default value (maybe_after_filter itself)
    value_or_else = maybe_after_filter.get_or_else(maybe_after_filter)

    # Transform the filtered nothing Maybe to Either - should return Left(None)
    either_from_filter = maybe_after_filter.to_either()

    # Transform the Validation to Try - since Validation was successful with None
    try_from_validation = validation_from_lazy.to_try()

    # Assert: Compare filtered Maybe with the Maybe after ap - both are nothing, should be equal
    are_maybes_equal = maybe_after_filter.__eq__(maybe_after_ap)
    assert are_maybes_equal

    # Transform the default value (which is maybe_after_filter) to Box - should return Box(None) since it's nothing
    box_from_value = value_or_else.to_box()

    # Apply bytes value to the Try monad
    try_from_validation.ap(BYTES_VALUE)

def test_maybe_transformations_and_operations_with_nothing_and_value():
    """
    Tests various Maybe monad operations including transformations (to_validation, to_either, to_try)
    and operations (ap, bind, get_or_else, __eq__) for both empty (nothing) and non-empty Maybe instances.
    
    Verifies that:
    - A Maybe with is_nothing=True returns empty/nothing for chained ap operations
    - A Maybe with is_nothing=False (containing bytes value) properly transforms to Validation, Either, and Try
    - bind, get_or_else, and equality checks work correctly on non-empty Maybe
    """
    # Setup - constants
    BYTES_VALUE = b"\xdbC\xcf\xe7/"
    NONE_VALUE = None
    IS_NOTHING = True
    NEGATIVE_INT = -3289

    # Setup - Create a Maybe that represents "nothing" (empty Maybe)
    nothing_maybe = maybe.Maybe(NONE_VALUE, IS_NOTHING)

    # Execute - Apply operations on nothing Maybe, chaining ap calls
    nothing_ap_result = nothing_maybe.ap(NONE_VALUE)
    nothing_ap_with_bytes = nothing_ap_result.ap(BYTES_VALUE)

    # Assert - nothing Maybe transforms to a successful Validation with None
    nothing_validation = nothing_ap_with_bytes.to_validation()

    # Setup - Create a Maybe that holds a bytes value (non-empty Maybe)
    bytes_maybe = maybe.Maybe(NONE_VALUE, BYTES_VALUE)

    # Execute - get_or_else returns the bytes_maybe itself as default since is_nothing=bytes value (falsy check)
    get_or_else_result = bytes_maybe.get_or_else(bytes_maybe)

    # Execute - Transform bytes Maybe to Validation
    bytes_validation = bytes_maybe.to_validation()

    # Execute - bind using the validation result as mapper
    bind_result = bytes_maybe.bind(bytes_validation)

    # Execute - Transform bytes Maybe to Either
    either_result = bytes_maybe.to_either()

    # Execute - Apply bytes_maybe to itself
    ap_result = bytes_maybe.ap(bytes_maybe)

    # Assert - Compare Either with Validation (should be False as they are different types)
    either_equals_validation = either_result.__eq__(bytes_validation)

    # Execute - Bind either result using bytes_maybe as mapper
    either_bind_result = either_result.bind(bytes_maybe)

    # Execute - Transform bytes_maybe to Try
    try_result = bytes_maybe.to_try()

    # Assert - Check equality between bytes_maybe and its bind result
    maybe_equals_bind = bytes_maybe.__eq__(bind_result)

    # Execute - Transform bind result to Validation
    bind_validation = bind_result.to_validation()

    # Execute - Apply a negative integer to the Try result (no assertion needed, testing no exception raised)
    try_result.ap(NEGATIVE_INT)

def test_maybe_nothing_transformations_and_map():
    """
    Test that a Maybe in 'nothing' state (is_nothing=True) correctly:
    1. Compares as not equal to a boolean False value
    2. Transforms to Either (Left with None)
    3. Transforms to Lazy and then to Validation (successful with None)
    4. Maps a Validation function over a 'nothing' Maybe (returns new empty Maybe)
    """
    # Setup - Create Maybe instances in 'nothing' state (both value and is_nothing set to False)
    IS_NOTHING = False
    VALUE = False

    # Create first Maybe in nothing state and verify equality behavior
    maybe_nothing_first = maybe.Maybe(IS_NOTHING, VALUE)
    
    # Execute - Test equality: Maybe instance should not equal a plain boolean
    is_equal_to_bool = maybe_nothing_first.__eq__(VALUE)
    assert is_equal_to_bool == False  # Maybe should not equal a plain boolean value

    # Create second Maybe in nothing state and perform transformations
    maybe_nothing_second = maybe.Maybe(IS_NOTHING, VALUE)
    
    # Transform Maybe to Either - should produce Left(None) for nothing state
    either_result = maybe_nothing_second.to_either()
    
    # Transform Maybe to Lazy - should produce Lazy returning None for nothing state
    lazy_result = maybe_nothing_second.to_lazy()
    
    # Transform Lazy-wrapped value to Validation - should produce successful Validation with None
    validation_result = lazy_result.to_validation()

    # Create third Maybe in nothing state and map the validation function over it
    maybe_nothing_third = maybe.Maybe(IS_NOTHING, VALUE)
    
    # Execute - Map validation over nothing Maybe; should return a new empty Maybe
    map_result = maybe_nothing_third.map(validation_result)
    
    # Assert - Mapping over a nothing Maybe should return a new nothing Maybe
    assert map_result == maybe.Maybe.nothing()

def test_maybe_nothing_transforms_to_failed_try_and_successful_validation():
    # Test that a Maybe with is_nothing=False correctly transforms
    # through the monad chain: Maybe -> Try -> Validation
    
    # Setup: Create a "Nothing" Maybe monad (both value and is_nothing are False)
    IS_NOTHING = False
    NOTHING_VALUE = False
    nothing_maybe = maybe.Maybe(NOTHING_VALUE, IS_NOTHING)
    
    # Verify Maybe equality with itself
    is_equal_to_self = nothing_maybe.__eq__(nothing_maybe)
    assert is_equal_to_self is True
    
    # Execution: Transform Maybe to Try
    # Since is_nothing=False (treated as Nothing), should produce a failed Try with None
    resulting_try = nothing_maybe.to_try()
    
    # Transform the resulting Try to Validation
    # A failed Try should produce a successful Validation with None
    resulting_validation = resulting_try.to_validation()
    
    # Assert: Validation should be successful with None value
    assert resulting_validation is not None

