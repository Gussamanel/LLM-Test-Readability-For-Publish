import pytest
import codetiming_timer as module_0
import collections as module_1

def test_float_to_namedtuple_conversion():
    from collections import namedtuple

    # Setup
    float_value = -476.66
    expected_tuple = namedtuple('Test', ['value'])(float_value)

    # Execution
    named_tuple = namedtuple('Test', ['value'])(float_value)

    # Assertion
    assert isinstance(named_tuple, tuple)
    assert len(named_tuple) == 1
    assert isinstance(named_tuple[0], float)
    assert named_tuple == expected_tuple

def test_convert_namedtuple_from_tuple():
    FLOAT_VALUE = -67.0
    FLOAT_SET = {FLOAT_VALUE, FLOAT_VALUE, FLOAT_VALUE, FLOAT_VALUE}
    FLOAT_TUPLE = (FLOAT_VALUE, FLOAT_SET)

    named_tuple_output_tuple = module_0.to_namedtuple(FLOAT_TUPLE)
    named_tuple_output_set = module_0.to_namedtuple(FLOAT_SET)

    assert(isinstance(named_tuple_output_tuple, tuple))
    assert(isinstance(named_tuple_output_set, collections.namedtuple))

def test_convert_namedtuple_from_dict():
    # Test Case: Convert a dictionary into a namedtuple.
    # Purpose: Verify if a dictionary is correctly being converted into a namedtuple.

    # Set up
    author_name = "author"
    author_data = {author_name: author_name, f"{author_name}_id": 123}
    
    # Execution: Convert dictionary into namedtuple
    author_named_tuple = module_0.to_namedtuple(author_data)
    author_named_tuple_again = module_0.to_namedtuple(author_named_tuple)

    # Assertion: Ensure the namedtuple was correctly formed and it retains data
    assert isinstance(author_named_tuple, collections.namedtuple)
    assert author_named_tuple.a == author_name
    assert author_named_tuple.a_id == 123
    assert isinstance(author_named_tuple_again, collections.namedtuple)
    assert author_named_tuple_again.a == author_name
    assert author_named_tuple_again.a_id == 123

def test_convert_bytes_to_namedtuple():
    from collections import namedtuple
    from module_0 import to_namedtuple

    # The test case uses a unique byte string.
    test_bytes = b"xs&\x2c\x9b\xc2\xf1\x80\xb3y"

    # Call the function to convert bytes to namedtuple.
    result = to_namedtuple(test_bytes)

    # The result should be a NamedTuple with the expected values.
    assert isinstance(result, namedtuple)
    assert result.a == ord('x')
    assert result.b == ord('s')
    assert result.c == ord('&')
    assert result.d == ord(',')
    # and so on...

def test_convert_tuple_to_namedtuple():
    # Arrange
    EMPTY_TUPLE = ()

    # Act
    empty_tuple_as_namedtuple = module_0.to_namedtuple(EMPTY_TUPLE)

    # Assert
    assert isinstance(empty_tuple_as_namedtuple, module_1.NamedTuple), "The converted object is not a NamedTuple as expected."
    assert empty_tuple_as_namedtuple == module_1.NamedTuple(), "The NamedTuple is not empty as expected."

def test_convert_ordereddict_to_namedtuple():
    # Constants
    test_dicts = [{}, {"a": 1}, {"a": 1, "_b": 2}, {"a": 1, "b": {"c": 3}}, {"a": 1, "b": [{"c": 3}, {"d": 4}]}]
    byte_0 = b"\xe2\xf8\xb9\x01\x8c\xa5\xed\xb1\x0e&rdHE"

    # Setup
    byte_list = [byte_0]
    tuple_0 = (byte_0,)

    # Execution
    ordered_dict_0 = module_1.OrderedDict(test_dicts[0])
    var_0 = module_0.to_namedtuple(ordered_dict_0)
    ordered_dict_1 = module_1.OrderedDict(test_dicts[1])
    var_1 = module_0.to_namedtuple(ordered_dict_1)
    ordered_dict_2 = module_1.OrderedDict(test_dicts[2])
    var_2 = module_0.to_namedtuple(ordered_dict_2)
    ordered_dict_3 = module_1.OrderedDict(test_dicts[3])
    var_3 = module_0.to_namedtuple(ordered_dict_3)
    ordered_dict_4 = module_1.OrderedDict(test_dicts[4])
    var_4 = module_0.to_namedtuple(ordered_dict_4)
    var_5 = module_0.to_namedtuple(tuple_0)
    ordered_dict_5 = module_1.OrderedDict()
    var_6 = module_0.to_namedtuple(ordered_dict_5)

    # Assertions
    assert var_0 == var_1
    assert var_2 == var_3
    assert var_4 == var_5
    assert var_6 == var_1

def test_convert_ordered_dict_to_named_tuple_with_alphabetical_ordering():
    # Given
    KEY_1 = "wm=-g\\ry#\\x0b#:*"
    VALUE_1 = "wm=-g\\ry#\\x0b#:*"
    dict_0 = {KEY_1: VALUE_1, KEY_1: VALUE_1}

    ordered_dict_0 = module_1.OrderedDict(**dict_0)

    # When
    ordered_named_tuple_0 = module_0.to_namedtuple(ordered_dict_0)

    # Then
    assert isinstance(ordered_named_tuple_0, tuple)
    assert ordered_named_tuple_0 == tuple(ordered_dict_0.items())

    # Also, assert that the order on the tuple was defined by the order of the keys
    assert ordered_named_tuple_0[0][0] == next(iter(ordered_dict_0))


def test_convert_invalid_object_to_named_tuple():
    # Given
    NONE_TYPE_0 = None
    list_0 = [NONE_TYPE_0]

    # When
    result = module_1.OrderedDict(*list_0)

    # Then
    assert result == list_0

def test_convert_empty_list_to_namedtuple():
    """
    Test if the function can correctly convert an empty list to a NamedTuple.

    This test has the following steps:
    1. Create an empty list.
    2. Convert the list to a NamedTuple.
    3. Convert None to a NamedTuple (which is valid as per the function).

    All these actions are separate variables and steps, making the test case more understandable and easy to debug.
    """
    
    # Prepare the test data: an empty list
    empty_list = []
    
    # Expected result: a NamedTuple with the empty list as its content
    expected_result = module_0.to_namedtuple(empty_list)
    
    # Actual result: convert the empty list to a NamedTuple
    actual_result = module_0.to_namedtuple([empty_list])
    
    # Check if the actual result matches the expected result
    assert actual_result == expected_result
    
    # Now let's try converting None to a NamedTuple
    # Expected result: None
    expected_result = None
    
    # Actual result: convert None to a NamedTuple
    actual_result = module_0.to_namedtuple(None)
    
    # Check if the actual result matches the expected result
    assert actual_result == expected_result

def test_normalize_path():
    """
    This test verifies that the function "normalize_path" converts a given path properly. 
    """
    # Setup
    given_path = "~/tmp/foo/../bar"
    
    # Execution
    result = module_0.normalize_path(given_path)
    
    # Assertion
    assert str(result) == "/home/test_user/tmp/bar"

def test_to_namedtuple():
    """
    This test verifies that convert_to_namedtuple converts the given objects into a namedtuple.
    """
    # Setup
    initial_object = {
        "str_0": "Normalize a given path.\n...",
        "dict_0": {
            "str_0": "Normalize a given path.\n...",
            "str_0": "Normalize a given path.\n...",
            "str_0": "Normalize a given path.\n..."
        },
        "var_0": module_0.to_namedtuple,
        "bool_0": False,
        "var_1": module_0.to_namedtuple,
        "tuple_0": (module_0.to_namedtuple,),
        "dict_1": {
            module_0.to_namedtuple: module_0.to_namedtuple,
            False: module_0.to_namedtuple
        },
        "var_3": module_0.to_namedtuple,
        "var_4": module_0.to_namedtuple,
        "bool_1": False,
        "var_5": module_0.to_namedtuple
    }

    # Execution
    result = module_0.to_namedtuple(initial_object)

    # Assertion
    assert isinstance(result, tuple)
    assert len(result) == 1

def test_to_namedtuple_converts_mixed_types_with_unique_name(): 
    """ 
    Test Case Purpose: 
    This Test Case is designed to test the function "to_namedtuple" to ensure it correctly converts a list of mixed data types into a namedtuple.
    The test case covers multiple data types (a string and a nested dict) and checks the resulting namedtuple structure.
    """ 
    # Setup
    strange_string = "\x0cMv" 
    empty_tuple = () 
    nested_dict = {strange_string: empty_tuple, tuple: strange_string, empty_tuple: empty_tuple} 
    nested_tuple = (strange_string, nested_dict) 
    mixed_list = [nested_tuple] 

    # Exectution
    namedtuple_list = module_0.to_namedtuple(mixed_list)
    namedtuple_list = module_0.to_namedtuple(namedtuple_list)
    namedtuple_list = module_0.to_namedtuple(namedtuple_list)

    # Assertion 
    assert module_0.to_namedtuple(2) is None, "Conversion of non-iterable type should return None."

def test_dict_to_namedtuple_conversion():
    # Given
    bytes_data = b"F\xdb\xfdf\x8a\xe4\n\xa2\x1d[\xdc*\xa3\xba\xf6s}"
    dict_to_convert = {bytes_data: bytes_data, bytes_data: bytes_data, bytes_data: bytes_data}

    # Setup
    # We are using the pytest framework which offers fixtures. 
    # Here, setup means we are importing the necessary functions we need for the test.
    import module_0
    import collections

    # Execution
    # We call the to_namedtuple function from the module and pass our dict and bytes keys and values.
    result = module_0.to_namedtuple(dict_to_convert)

    # Assertion
    # This means we are making sure the result is a namedtuple, as per the function definition in the module.
    assert isinstance(result, collections.namedtuple)

