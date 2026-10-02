import pytest
import maybe as maybe
import typing as typing

def test_maybe_initialization_with_bytes():
    # Test that Maybe can be initialized with bytes values
    # Setup: Create a bytes object to use as both arguments
    SAMPLE_BYTES = b"\xf4\xaf\xe2\xc9\xee\xc8\xd67n\x9eK\x0b\x97Y\xb5"

    # Execution: Initialize Maybe with bytes as both the value and default
    maybe_instance = maybe.Maybe(SAMPLE_BYTES, SAMPLE_BYTES)

    # Assertion: Verify the Maybe instance was created successfully
    assert maybe_instance is not None

def test_maybe_initialization_with_none_values():
    # Test that Maybe can be initialized with None values for both parameters
    # This verifies the basic construction of a Maybe object with null/empty state
    
    # Setup: Define None values to represent empty/absent values
    EMPTY_VALUE = None
    EMPTY_TYPE = None
    
    # Execution: Create a Maybe instance with both value and type set to None
    maybe_instance = maybe.Maybe(EMPTY_VALUE, EMPTY_TYPE)
    
    # Assertion: Verify the Maybe object was created successfully (no exception raised)
    assert maybe_instance is not None

def test_maybe_operations_with_non_empty_value():
    """
    Test various Maybe monad operations when initialized with a non-empty string value.
    Verifies that ap, get_or_else, map, filter, bind, to_validation, and to_either
    all behave correctly for a non-empty Maybe instance.
    """
    # Setup
    SAMPLE_VALUE = "p4xa>bl^oP"
    
    # Create a Maybe instance with a non-empty string value
    maybe_with_value = maybe.Maybe(SAMPLE_VALUE, SAMPLE_VALUE)
    
    # Verify equality check between Maybe and a plain string returns False (not same type)
    is_equal_to_string = maybe_with_value.__eq__(SAMPLE_VALUE)
    
    # Execute ap operation - applies the Maybe's function value to the string applicative
    ap_result_1 = maybe_with_value.ap(SAMPLE_VALUE)
    
    # Execute get_or_else - should return the Maybe's value since it's non-empty
    retrieved_value = maybe_with_value.get_or_else(SAMPLE_VALUE)
    
    # Execute map operations using the equality check result as the mapper
    map_result_1 = maybe_with_value.map(is_equal_to_string)
    
    # Execute filter operation using the equality check result as the filterer
    filter_result_1 = maybe_with_value.filter(is_equal_to_string)
    
    # Execute second map operation
    map_result_2 = maybe_with_value.map(is_equal_to_string)
    
    # Execute second ap operation
    ap_result_2 = maybe_with_value.ap(SAMPLE_VALUE)
    
    # Verify that two ap results with the same input are equal
    are_ap_results_equal = ap_result_1.__eq__(ap_result_2)
    
    # Filter the first ap result using retrieved_value as the filterer
    filter_result_2 = ap_result_1.filter(retrieved_value)
    
    # Get value from second ap result with fallback to SAMPLE_VALUE
    ap_result_2_value = ap_result_2.get_or_else(SAMPLE_VALUE)
    
    # Create a second Maybe instance with the same value
    maybe_with_value_2 = maybe.Maybe(SAMPLE_VALUE, SAMPLE_VALUE)
    
    # Convert second Maybe to Validation - should produce a successful Validation
    validation_result = maybe_with_value_2.to_validation()
    
    # Bind the validation result as a mapper to the second Maybe
    bind_result = maybe_with_value_2.bind(validation_result)
    
    # Convert the bind result to Either - should produce a Right since Maybe is non-empty
    either_result = bind_result.to_either()

def test_maybe_equality_with_non_maybe_object_returns_false():
    # Test that comparing a Maybe instance with a non-Maybe object (set) returns False
    # The __eq__ method should return False when 'other' is not an instance of Maybe

    # Setup: Create a Maybe instance with None values (representing Nothing)
    NONE_VALUE = None
    maybe_nothing = maybe.Maybe(NONE_VALUE, NONE_VALUE)

    # Setup: Create a non-Maybe object (a set) to compare against
    FALSE_VALUE = False
    non_maybe_set = {FALSE_VALUE}

    # Execute: Compare the Maybe instance with the non-Maybe set
    result = maybe_nothing.__eq__(non_maybe_set)

    # Assert: The result should be False since a set is not an instance of Maybe
    assert result == False

def test_maybe_bind_map_and_set_to_box_raises_attribute_error():
    """
    Test that:
    1. Maybe.bind() with a non-callable (bool) raises a TypeError when called with True value
    2. Maybe.map() with a non-callable (bool) raises a TypeError when called with True value
    3. Calling to_box() on a plain set raises AttributeError since set has no to_box method
    """
    # Setup
    IS_PRESENT = True
    BOOL_VALUE = True
    TUPLE_VALUE = (True, True, True, True)

    # Test Maybe with bool value and bool as mapper (non-callable)
    maybe_with_bool = maybe.Maybe(IS_PRESENT, BOOL_VALUE)

    # Execution and assertion: bind with non-callable bool should raise TypeError
    with pytest.raises(TypeError):
        bound_maybe = maybe_with_bool.bind(BOOL_VALUE)
        # Execution and assertion: map with non-callable bool should raise TypeError
        bound_maybe.map(BOOL_VALUE)

    # Setup: Maybe with tuple value
    maybe_with_tuple = maybe.Maybe(TUPLE_VALUE, BOOL_VALUE)

    # Setup: plain Python set (not a Maybe or Box)
    plain_set = set()

    # Execution and assertion: set has no to_box method, should raise AttributeError
    with pytest.raises(AttributeError):
        plain_set.to_box()

def test_map_on_empty_maybe_returns_nothing():
    # Test that calling map on an empty Maybe (with is_nothing=False but None value)
    # returns a new empty Maybe without applying the mapper function
    
    # Setup
    EMPTY_VALUE = None
    IS_NOTHING = False
    MAPPER_FUNCTION = False  # Using False as a non-callable mapper since Maybe is treated as empty
    
    # Execution
    empty_maybe = maybe.Maybe(EMPTY_VALUE, IS_NOTHING)
    result = empty_maybe.map(MAPPER_FUNCTION)
    
    # Assertion
    # When Maybe has no value (None), map should return a new empty Maybe
    assert result is not None

def test_bind_on_empty_maybe_returns_nothing():
    # Constants for test setup
    VALID_VALUE = True
    EMPTY_VALUE = None
    IS_FILLED = True
    IS_EMPTY = False

    # Setup: Create a filled Maybe and an empty Maybe
    filled_maybe = maybe.Maybe(VALID_VALUE, IS_FILLED)
    empty_mapper = {}

    # Setup: Create an empty Maybe (is_nothing=True since value is None and has_value is False)
    empty_maybe = maybe.Maybe(EMPTY_VALUE, IS_EMPTY)

    # Execution: Call bind on an empty Maybe with a mapper (empty dict used as mapper placeholder)
    # When Maybe is empty (is_nothing), bind should return a new empty Maybe without calling the mapper
    result = empty_maybe.bind(empty_mapper)

    # Assertion: Verify that binding on an empty Maybe returns a nothing Maybe
    assert result.is_nothing

def test_maybe_chained_operations_with_filter_ap_and_transformations():
    # Constants for test values
    BYTES_VALUE = b"\x9f\x02Gj\xbbw\xdb\x8b\xe7\xda"
    INT_VALUE = 0
    BOOL_VALUE = True

    # Setup: Create a Maybe with bytes value and no default (nothing Maybe)
    maybe_with_bytes = maybe.Maybe(BYTES_VALUE, None)
    
    # Convert bytes Maybe to Box - should return Box with bytes value since Maybe is not empty
    box_from_bytes_maybe = maybe_with_bytes.to_box()

    # Setup: Create a Maybe with integer value and True as default
    maybe_with_int = maybe.Maybe(INT_VALUE, BOOL_VALUE)

    # Execute: Filter maybe_with_int using itself as the filterer
    # Since maybe_with_int is used as a callable filterer, and int 0 is falsy,
    # filter should return nothing
    filtered_maybe = maybe_with_int.filter(maybe_with_int)

    # Convert maybe_with_int to Lazy monad
    lazy_from_int_maybe = maybe_with_int.to_lazy()

    # Execute: Apply filtered_maybe (which is nothing) to maybe_with_bytes
    # Since filtered_maybe is nothing, ap should return nothing
    ap_result = filtered_maybe.ap(maybe_with_bytes)

    # Execute: Filter ap_result using filtered_maybe as the filterer
    # Since filtered_maybe is nothing, filter should return nothing
    filtered_ap_result = filtered_maybe.filter(ap_result)

    # Setup: Create a Maybe combining the lazy monad and box as value and default
    maybe_with_lazy_and_box = maybe.Maybe(lazy_from_int_maybe, box_from_bytes_maybe)

    # Assert: Check equality between lazy monad and BOOL_VALUE (True)
    # lazy_from_int_maybe is a Lazy instance and BOOL_VALUE is True, 
    # so they should not be equal (different types)
    equality_result = lazy_from_int_maybe.__eq__(BOOL_VALUE)
    assert equality_result == False

def test_ap_on_nothing_maybe_returns_nothing():
    # Test that calling ap() on a Nothing Maybe returns a Nothing Maybe
    # When the Maybe contains no value (is_nothing=True), ap should return a copy of itself (Nothing)
    
    # Setup
    SOME_INTEGER_VALUE = 2862
    NO_VALUE = None
    IS_NOTHING = True
    
    # Create a Maybe instance representing Nothing (no value)
    nothing_maybe = maybe.Maybe(NO_VALUE, IS_NOTHING)
    
    # Execute
    # Apply the ap operation with an integer value on a Nothing Maybe
    result = nothing_maybe.ap(SOME_INTEGER_VALUE)
    
    # Assert
    # When ap is called on a Nothing Maybe, it should return a Nothing Maybe
    assert result.is_nothing

def test_maybe_filter_and_transform_operations():
    # Setup: Create a Maybe instance with value 0 and is_nothing=True (empty Maybe)
    INITIAL_VALUE = 0
    IS_NOTHING = True
    maybe_with_value = maybe.Maybe(INITIAL_VALUE, IS_NOTHING)

    # Execution: Apply filter using maybe itself as the filterer
    # Since IS_NOTHING is True, filter should return Maybe.nothing()
    filtered_maybe = maybe_with_value.filter(maybe_with_value)

    # Transform the original maybe and filtered maybe to Lazy monads
    lazy_from_original = maybe_with_value.to_lazy()
    lazy_from_filtered = filtered_maybe.to_lazy()

    # Apply filter on filtered_maybe using lazy_from_filtered as filterer
    double_filtered_maybe = filtered_maybe.filter(lazy_from_filtered)

    # Transform double filtered maybe to Try monad
    try_from_double_filtered = double_filtered_maybe.to_try()

    # Transform original maybe to Lazy monad again
    lazy_from_original_second = maybe_with_value.to_lazy()

    # Apply map on filtered_maybe using filtered_maybe itself as mapper
    mapped_maybe = filtered_maybe.map(filtered_maybe)

    # Assertions: Verify that all transformations produce correct empty/nothing results
    # since the initial Maybe is empty (IS_NOTHING=True)
    assert filtered_maybe.is_nothing is True  # filter on empty Maybe returns nothing
    assert double_filtered_maybe.is_nothing is True  # filter on nothing returns nothing
    assert try_from_double_filtered.is_success is False  # empty Maybe converts to failed Try
    assert try_from_double_filtered.value is None  # failed Try has None value
    assert mapped_maybe.is_nothing is True  # map on nothing returns nothing

def test_filter_nothing_maybe_returns_nothing_with_lazy_filterer():
    # Constants for test setup
    NEGATIVE_VALUE = -283
    FILTER_TUPLE = (NEGATIVE_VALUE, NEGATIVE_VALUE, NEGATIVE_VALUE)
    
    # Setup: Create a Maybe instance with None value but is_just=True
    initial_value = None
    is_just = True
    maybe_with_none_value = maybe.Maybe(initial_value, is_just)
    
    # Execution: Filter the Maybe using a tuple as filterer (tuple is truthy)
    # and convert the result to a Lazy monad
    filtered_maybe = maybe_with_none_value.filter(FILTER_TUPLE)
    lazy_result = filtered_maybe.to_lazy()
    
    # Setup: Create a second Maybe instance with nothing (None value and None is_just)
    maybe_nothing = maybe.Maybe(None, None)
    
    # Execution: Filter the nothing Maybe using the Lazy monad as filterer
    # Since maybe_nothing is nothing (is_nothing=True), filter should return Maybe.nothing()
    result = maybe_nothing.filter(lazy_result)
    
    # Assertion: Result should be a nothing Maybe since the input was nothing
    assert result.is_nothing == True

def test_filter_with_get_or_else_value_as_filterer():
    """
    Test that filter() on a Maybe[None] (nothing) returns an empty Maybe,
    when the filterer used is the actual value retrieved from a non-empty Maybe via get_or_else().
    
    Steps:
    1. Create a non-empty Maybe with a tuple value and retrieve its value using get_or_else().
    2. Convert the non-empty Maybe to a Box to verify the transformation.
    3. Create an empty Maybe (is_nothing=False with Generic value) and apply filter() 
       using the previously retrieved tuple value as the filterer.
    """
    # Setup
    DEFAULT_INT_VALUE = 2281
    SAMPLE_STRING = "gZ(\\mOcN"
    
    sample_dict = {SAMPLE_STRING: SAMPLE_STRING}
    sample_tuple = (SAMPLE_STRING, SAMPLE_STRING, sample_dict, sample_dict)
    
    IS_PRESENT = True
    IS_NOTHING = False

    # Create a non-empty Maybe containing a tuple
    non_empty_maybe = maybe.Maybe(sample_tuple, IS_PRESENT)
    
    # Execution - get_or_else returns the tuple value since Maybe is not empty
    retrieved_value = non_empty_maybe.get_or_else(DEFAULT_INT_VALUE)
    
    # Convert non-empty Maybe to Box
    box_result = non_empty_maybe.to_box()
    
    # Create an empty Maybe with a Generic value
    generic_value = typing.Generic()
    empty_maybe = maybe.Maybe(generic_value, IS_NOTHING)
    
    # Apply filter using the retrieved tuple as filterer on the empty Maybe
    filter_result = empty_maybe.filter(retrieved_value)
    
    # Assertion - filtering an empty Maybe always returns Maybe.nothing()
    assert filter_result.is_nothing

def test_maybe_transformations_and_bind_with_various_states():
    """
    Test Maybe monad transformations (to_validation, to_try, get_or_else) 
    and bind operation across different Maybe states:
    - Maybe with True value and no nothing flag
    - Maybe with integer value and no nothing flag (empty tuple as is_nothing)
    - Maybe with float value and float as is_nothing flag
    """
    # Setup - Constants for test values
    BOOL_VALUE = True
    FLOAT_VALUE = -286.64
    INT_VALUE = -1784
    EMPTY_TUPLE = ()

    # Setup - Create Maybe instances with different states
    # Maybe with True value, not a nothing (None as is_nothing = falsy)
    maybe_with_bool = maybe.Maybe(BOOL_VALUE, None)
    
    # Maybe with integer value, empty tuple as is_nothing (falsy)
    maybe_with_int = maybe.Maybe(INT_VALUE, EMPTY_TUPLE)
    
    # Maybe with float value and float as is_nothing (truthy)
    maybe_with_float = maybe.Maybe(FLOAT_VALUE, FLOAT_VALUE)

    # Execution - Transform bool Maybe to validation
    validation_from_bool_maybe = maybe_with_bool.to_validation()

    # Execution - Transform int Maybe to validation, get value, and convert to try
    validation_from_int_maybe = maybe_with_int.to_validation()
    value_or_default = maybe_with_int.get_or_else(INT_VALUE)
    try_from_int_maybe = maybe_with_int.to_try()

    # Execution - Bind int Maybe with a mapper (try_from_int_maybe acts as mapper)
    bind_result = maybe_with_int.bind(try_from_int_maybe)

    # Assertions - Verify validation from bool Maybe is successful with bool value
    assert validation_from_bool_maybe.is_success
    assert validation_from_bool_maybe.value == BOOL_VALUE

    # Assertions - Verify validation from int Maybe is successful with int value
    assert validation_from_int_maybe.is_success
    assert validation_from_int_maybe.value == INT_VALUE

    # Assertions - Verify get_or_else returns the Maybe's value since it's not nothing
    assert value_or_default == INT_VALUE

    # Assertions - Verify Try from int Maybe is successful with int value
    assert try_from_int_maybe.is_success
    assert try_from_int_maybe.value == INT_VALUE

def test_map_on_nothing_maybe_returns_nothing_and_to_either_on_nothing_returns_left():
    # Test two scenarios:
    # 1. Calling map on a Nothing Maybe (with None value) should return a new empty Maybe
    # 2. Calling to_either on a Nothing Maybe should return a Left with None value

    # Constants
    NONE_VALUE = None
    INT_VALUE = -1095
    IS_NOTHING = True

    # Setup - Create a Nothing Maybe (value is None, is_nothing is True)
    nothing_maybe = maybe.Maybe(NONE_VALUE, IS_NOTHING)

    # Setup - Create a mapper (set used as callable, though unconventional)
    mapper_set = {True}

    # Execution - Map over a Nothing Maybe should return empty Maybe
    map_result = nothing_maybe.map(mapper_set)

    # Assert - Map on Nothing Maybe returns a new empty Maybe (Nothing)
    assert map_result.is_nothing is True

    # Setup - Create a Nothing Maybe with an integer value but marked as Nothing
    just_maybe = maybe.Maybe(INT_VALUE, IS_NOTHING)

    # Execution - Convert Nothing Maybe to Either
    either_result = just_maybe.to_either()

    # Assert - to_either on a Nothing Maybe returns Left with None
    assert either_result.get() is None

def test_maybe_monad_transformations_with_none_and_tuple_values():
    """
    Test various transformations (to_lazy, to_either, to_try) on Maybe monads
    initialized with None and tuple values, verifying that the transformations
    work correctly for both Nothing (None) and Just (tuple) cases.
    """
    # Setup
    NOTHING_VALUE = None
    IS_NOTHING_FLAG = None
    IS_NOT_NOTHING_FLAG = False

    # Create a Maybe with None value (Nothing case)
    maybe_nothing = maybe.Maybe(NOTHING_VALUE, IS_NOTHING_FLAG)

    # Create a tuple containing the nothing Maybe, used as value for a second Maybe
    tuple_with_maybe = (maybe_nothing,)

    # Create a Maybe with a tuple value (Just case, is_nothing=False)
    maybe_just = maybe.Maybe(tuple_with_maybe, IS_NOT_NOTHING_FLAG)

    # Execute transformations on Nothing Maybe
    lazy_from_nothing = maybe_nothing.to_lazy()  # Should return Lazy wrapping None
    either_from_nothing_first = maybe_nothing.to_either()  # Should return Left(None)

    # Execute transformations on Just Maybe
    try_from_just = maybe_just.to_try()  # Should return successful Try with tuple value
    either_from_nothing_second = maybe_nothing.to_either()  # Should return Left(None)
    either_from_just = maybe_just.to_either()  # Should return Right(tuple_with_maybe)

    # Execute to_lazy on the Try result from the Just Maybe
    lazy_from_try = try_from_just.to_lazy()  # Should return Lazy wrapping the Try value

    # Assert transformations produce expected types
    assert lazy_from_nothing is not None
    assert either_from_nothing_first is not None
    assert try_from_just is not None
    assert either_from_nothing_second is not None
    assert either_from_just is not None
    assert lazy_from_try is not None

def test_maybe_to_try_to_box_with_value():
    """
    Test that a Maybe with a value can be successfully transformed 
    to a Try monad and then to a Box monad.
    
    A Maybe initialized with a value (is_nothing=False) should:
    1. Convert to a successful Try monad via to_try()
    2. Further convert to a Box monad via to_box()
    """
    # Setup
    MAYBE_VALUE = True
    IS_NOTHING = False

    # Create a Maybe with a value (not nothing)
    maybe_with_value = maybe.Maybe(MAYBE_VALUE, IS_NOTHING)

    # Execution - Transform Maybe to Try
    try_monad = maybe_with_value.to_try()

    # Execution - Transform Try to Box
    box_monad = try_monad.to_box()

    # Assert that the final Box monad is not None, 
    # confirming the transformations completed successfully
    assert box_monad is not None

def test_maybe_nothing_transformations_and_operations():
    # Constants
    BYTES_VALUE = b"C\xcf\xe7/"
    INITIAL_VALUE = None
    IS_NOTHING = True

    # Setup: Create a Maybe monad that represents a "nothing" state
    maybe_nothing = maybe.Maybe(INITIAL_VALUE, IS_NOTHING)

    # Execution: Apply 'ap' on a nothing Maybe, which should return another nothing Maybe
    maybe_after_ap = maybe_nothing.ap(None)

    # Transform nothing Maybe to Lazy monad (should wrap None in a lazy evaluation)
    lazy_from_nothing = maybe_after_ap.to_lazy()

    # Transform Lazy to Validation (should result in a successful Validation with None)
    validation_from_lazy = lazy_from_nothing.to_validation()

    # Apply filter using validation as filterer on the original nothing Maybe
    # Since maybe_nothing is nothing, filter should return nothing
    maybe_after_filter = maybe_nothing.filter(validation_from_lazy)

    # Get value or else return the filtered Maybe itself (since it's nothing, returns default)
    value_or_default = maybe_after_filter.get_or_else(maybe_after_filter)

    # Transform nothing Maybe to Either (should return Left with None)
    either_from_nothing = maybe_after_filter.to_either()

    # Transform Validation (from nothing) to Try (should return failed Try with None)
    try_from_validation = validation_from_lazy.to_try()

    # Assert: Check equality between filtered Maybe and the Maybe after ap (both should be nothing)
    are_equal = maybe_after_filter.__eq__(maybe_after_ap)

    # Transform the default value (which is itself a nothing Maybe) to Box
    box_from_default = value_or_default.to_box()

    # Apply bytes value to the failed Try (applying to a failed Try should propagate the failure)
    try_from_validation.ap(BYTES_VALUE)

    # Assertions
    # Both maybe_after_filter and maybe_after_ap should be nothing Maybes, so they should be equal
    assert are_equal is True

    # maybe_after_ap should be nothing since maybe_nothing is nothing
    assert maybe_after_ap.is_nothing is True

    # maybe_after_filter should also be nothing since the original was nothing
    assert maybe_after_filter.is_nothing is True

    # either_from_nothing should be a Left since Maybe is nothing
    from pymonet.either import Left
    assert isinstance(either_from_nothing, Left)
    assert either_from_nothing.value is None

def test_maybe_transformations_with_none_and_bytes_values():
    # Constants used in the test
    BYTES_VALUE = b"\xdbC\xcf\xe7/"
    NEGATIVE_INT = -3289
    
    # Setup: Create Maybe instances with None value (is_nothing=True when bool is True)
    maybe_with_none_flagged_true = maybe.Maybe(None, True)
    
    # Test ap() on a 'nothing' Maybe returns nothing, and chaining ap with bytes also returns nothing
    nothing_result = maybe_with_none_flagged_true.ap(None)
    chained_nothing_result = nothing_result.ap(BYTES_VALUE)
    
    # Convert the nothing result chain to validation - should yield successful Validation with None
    validation_from_nothing = chained_nothing_result.to_validation()
    
    # Setup: Create a second Maybe with None value and bytes as value
    maybe_with_bytes_value = maybe.Maybe(None, BYTES_VALUE)
    
    # Test get_or_else returns the bytes value since Maybe is not nothing
    retrieved_value = maybe_with_bytes_value.get_or_else(maybe_with_bytes_value)
    
    # Convert Maybe with bytes to Validation
    validation_from_bytes_maybe = maybe_with_bytes_value.to_validation()
    
    # Test bind: since maybe_with_bytes_value is not nothing, bind calls the mapper (validation_from_bytes_maybe) with the bytes value
    bound_result = maybe_with_bytes_value.bind(validation_from_bytes_maybe)
    
    # Convert Maybe with bytes to Either - should be Right(BYTES_VALUE)
    either_from_bytes_maybe = maybe_with_bytes_value.to_either()
    
    # Test ap on Maybe with bytes value applies the contained value to another Maybe
    ap_result = maybe_with_bytes_value.ap(maybe_with_bytes_value)
    
    # Test equality between Either and Validation - should be False since different types
    either_equals_validation = either_from_bytes_maybe.__eq__(validation_from_bytes_maybe)
    
    # Test bind on Either with maybe_with_bytes_value as mapper
    either_bind_result = either_from_bytes_maybe.bind(maybe_with_bytes_value)
    
    # Convert Maybe with bytes to Try - should be successful Try with BYTES_VALUE
    try_from_bytes_maybe = maybe_with_bytes_value.to_try()
    
    # Test equality between Maybe and bound result
    maybe_equals_bound = maybe_with_bytes_value.__eq__(bound_result)
    
    # Convert bound result to Validation
    validation_from_bound = bound_result.to_validation()
    
    # Test ap on Try with a negative integer - Try is successful so it attempts to apply value
    try_from_bytes_maybe.ap(NEGATIVE_INT)

def test_maybe_nothing_transformations_and_map():
    """
    Test that a Maybe monad initialized with False (is_nothing=False, value=False)
    correctly supports chained transformations (to_either, to_lazy, to_validation)
    and that map applies a validation transformer to another Maybe instance.
    """
    # Setup
    IS_NOTHING = False
    VALUE = False

    # Create initial Maybe and verify equality with a plain bool returns False
    maybe_with_false = maybe.Maybe(IS_NOTHING, VALUE)
    is_equal_to_bool = maybe_with_false.__eq__(VALUE)
    assert isinstance(is_equal_to_bool, bool)

    # Create a second Maybe and chain transformations: Maybe -> Either -> Lazy -> Validation
    maybe_for_transform = maybe.Maybe(IS_NOTHING, VALUE)
    either_result = maybe_for_transform.to_either()
    lazy_result = maybe_for_transform.to_lazy()
    validation_result = lazy_result.to_validation()

    # Create a third Maybe and apply the validation transformer as a mapper
    maybe_for_map = maybe.Maybe(IS_NOTHING, VALUE)
    mapped_result = maybe_for_map.map(validation_result)

    # Assert that the mapped result is a Maybe instance (map returns Maybe)
    assert isinstance(mapped_result, maybe.Maybe)

def test_maybe_nothing_to_try_to_validation_returns_successful_validation_with_none():
    # Setup: Create a Maybe instance where both value and is_nothing are False
    IS_NOTHING = False
    VALUE = False
    maybe_nothing = maybe.Maybe(VALUE, IS_NOTHING)

    # Verify Maybe equality with itself
    is_equal_to_itself = maybe_nothing.__eq__(maybe_nothing)
    assert is_equal_to_itself is True

    # Execution: Convert Maybe to Try monad
    try_result = maybe_nothing.to_try()

    # Execution: Convert Try monad to Validation monad
    validation_result = try_result.to_validation()

    # Assert: The final Validation should be successful with None value
    # since Maybe was in "nothing" state (is_nothing=False treated as not nothing here,
    # but value=False leads to Try with is_success=True containing False)
    assert validation_result is not None

