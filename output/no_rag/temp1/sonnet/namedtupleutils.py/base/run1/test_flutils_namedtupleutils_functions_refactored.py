import pytest
import namedtupleutils as named_tuple_utils
import collections as collections

def test_to_namedtuple_with_float_input():
    # Test that to_namedtuple handles a float input value
    # Floats are not a supported type (Mapping, list, tuple, or SimpleNamespace)
    # so the function should process it without raising an exception
    
    # Setup
    FLOAT_INPUT = -476.66
    
    # Execute
    result = named_tuple_utils.to_namedtuple(FLOAT_INPUT)
    
    # Assert
    # The float value should be returned as-is since it cannot be converted to a namedtuple
    assert result == FLOAT_INPUT

def test_to_namedtuple_with_tuple_containing_set_and_direct_set():
    """
    Test that to_namedtuple handles:
    1. A tuple containing a float and a set - the tuple should be converted
       with its contents processed recursively.
    2. A plain set passed directly - sets are not in the allowed types for
       full conversion, so it should be returned as-is or handled gracefully.
    """
    # Setup
    FLOAT_VALUE = -67.0
    # A set with duplicate float values (duplicates are ignored in a set)
    input_set = {FLOAT_VALUE}
    # A tuple containing the float and the set
    input_tuple = (FLOAT_VALUE, input_set)

    # Execution: convert tuple containing a float and a set to namedtuple
    result_from_tuple = named_tuple_utils.to_namedtuple(input_tuple)

    # Execution: convert a plain set directly (sets are not a Mapping or list/tuple)
    result_from_set = named_tuple_utils.to_namedtuple(input_set)

    # Assertions: the tuple input should return a tuple with its elements processed
    assert isinstance(result_from_tuple, tuple), (
        "Expected result from tuple input to be a tuple type"
    )
    # The float value inside the tuple should remain unchanged
    assert result_from_tuple[0] == FLOAT_VALUE, (
        "Expected first element of result tuple to be the original float value"
    )
    # The set inside the tuple should remain as a set (sets cannot be converted)
    assert result_from_tuple[1] == input_set, (
        "Expected second element of result tuple to remain as the original set"
    )
    # A raw set passed directly should be returned unchanged
    assert result_from_set == input_set, (
        "Expected result from direct set input to be the original set unchanged"
    )

def test_convert_dict_to_namedtuple_and_reconvert():
    # Test that converting a dict to a namedtuple, and then converting
    # the resulting namedtuple again, produces a valid namedtuple both times.

    # Setup: Create a dictionary with a single unique key-value pair
    # (duplicate keys collapse to one entry in Python dicts)
    AUTHOR_KEY = "author"
    input_dict = {AUTHOR_KEY: AUTHOR_KEY}

    # Execution: Convert the dictionary to a namedtuple
    namedtuple_from_dict = named_tuple_utils.to_namedtuple(input_dict)

    # Assert: The result is a namedtuple with the 'author' attribute set correctly
    assert isinstance(namedtuple_from_dict, tuple)
    assert hasattr(namedtuple_from_dict, AUTHOR_KEY)
    assert getattr(namedtuple_from_dict, AUTHOR_KEY) == AUTHOR_KEY

    # Execution: Convert the already-converted namedtuple again
    namedtuple_from_namedtuple = named_tuple_utils.to_namedtuple(namedtuple_from_dict)

    # Assert: Re-converting a namedtuple produces an equivalent namedtuple
    assert isinstance(namedtuple_from_namedtuple, tuple)
    assert hasattr(namedtuple_from_namedtuple, AUTHOR_KEY)
    assert getattr(namedtuple_from_namedtuple, AUTHOR_KEY) == AUTHOR_KEY
    assert namedtuple_from_dict == namedtuple_from_namedtuple

def test_to_namedtuple_raises_error_for_bytes_input():
    # Test that to_namedtuple raises an error when given a bytes object,
    # as bytes is not a supported type for conversion to namedtuple.
    # Supported types are: dict, OrderedDict, list, tuple, and SimpleNamespace.

    # Setup: Create a bytes object as input
    BYTES_INPUT = b"xs&,\x9b\xc2\xf1\x80\xb3y"

    # Execution & Assertion: Verify that passing bytes raises a TypeError
    # since bytes is not an allowed type for namedtuple conversion
    with pytest.raises(TypeError):
        named_tuple_utils.to_namedtuple(BYTES_INPUT)

def test_to_namedtuple_with_empty_tuple():
    # Test that converting an empty tuple returns an empty tuple unchanged
    # since there are no elements to convert to a namedtuple
    
    # Setup
    EMPTY_TUPLE = ()
    
    # Execution
    result = named_tuple_utils.to_namedtuple(EMPTY_TUPLE)
    
    # Assertion
    # An empty tuple has no items to convert, so it should be returned as an empty tuple
    assert result == EMPTY_TUPLE
    assert isinstance(result, tuple)
    assert len(result) == 0

def test_convert_empty_ordered_dict_and_tuple_with_bytes():
    """
    Test that to_namedtuple correctly handles:
    1. Converting an empty OrderedDict to a namedtuple multiple times
    2. Converting an already-converted namedtuple (idempotent behavior)
    3. Converting a tuple containing a namedtuple and bytes object
    """
    # Setup
    BYTES_DATA = b"\xe2\xf8\xb9\x01\x8c\xa5\xed\xb1\x0e&rdHE"
    empty_ordered_dict = collections.OrderedDict()

    # Execute: Convert empty OrderedDict to namedtuple
    first_namedtuple = named_tuple_utils.to_namedtuple(empty_ordered_dict)

    # Execute: Convert already-converted namedtuple again (idempotent check)
    namedtuple_from_namedtuple = named_tuple_utils.to_namedtuple(first_namedtuple)

    # Execute: Convert empty OrderedDict again to verify consistency
    second_namedtuple = named_tuple_utils.to_namedtuple(empty_ordered_dict)

    # Execute: Convert second namedtuple again (idempotent check)
    namedtuple_from_second = named_tuple_utils.to_namedtuple(second_namedtuple)

    # Execute: Convert empty OrderedDict once more
    third_namedtuple = named_tuple_utils.to_namedtuple(empty_ordered_dict)

    # Execute: Convert a tuple containing a namedtuple and a bytes object
    mixed_tuple = (namedtuple_from_namedtuple, BYTES_DATA)
    namedtuple_from_mixed_tuple = named_tuple_utils.to_namedtuple(mixed_tuple)

    # Execute: Convert empty OrderedDict one final time
    fourth_namedtuple = named_tuple_utils.to_namedtuple(empty_ordered_dict)

    # Assert: All conversions of the empty OrderedDict should yield equivalent results
    assert first_namedtuple == second_namedtuple
    assert second_namedtuple == third_namedtuple
    assert third_namedtuple == fourth_namedtuple

    # Assert: Converting an already-converted namedtuple should be idempotent
    assert first_namedtuple == namedtuple_from_namedtuple
    assert second_namedtuple == namedtuple_from_second

    # Assert: The mixed tuple conversion should return a tuple with the bytes preserved
    assert isinstance(namedtuple_from_mixed_tuple, tuple)
    assert BYTES_DATA in namedtuple_from_mixed_tuple

def test_convert_ordered_dict_with_special_key_to_namedtuple():
    """
    Test that to_namedtuple handles an OrderedDict with a special character key
    that cannot be used as a valid Python identifier.
    
    Since the key "wm=-g\ry#\x0b#:*" is not a valid Python identifier,
    it should be excluded from the resulting namedtuple attributes.
    Additionally, verifies that creating an OrderedDict with None as a
    positional argument raises a TypeError, confirming expected behavior.
    """
    # Setup: Define a key with special characters that is not a valid identifier
    SPECIAL_CHAR_KEY = "wm=-g\ry#\x0b#:*"
    
    # Setup: Create a regular dict and an OrderedDict using the special character key
    source_dict = {SPECIAL_CHAR_KEY: SPECIAL_CHAR_KEY}
    ordered_dict_with_special_key = collections.OrderedDict(**source_dict)
    
    # Execute: Convert the OrderedDict to a namedtuple
    # Since the key is not a valid identifier, the result should be an empty namedtuple
    result_namedtuple = named_tuple_utils.to_namedtuple(ordered_dict_with_special_key)
    
    # Assert: The result is a namedtuple with no fields (due to invalid identifier key)
    assert isinstance(result_namedtuple, tuple)
    assert result_namedtuple._fields == ()
    
    # Verify: Creating an OrderedDict with None as positional argument raises TypeError
    none_value = None
    args_with_none = [none_value]
    with pytest.raises(TypeError):
        collections.OrderedDict(*args_with_none)

def test_to_namedtuple_with_list_containing_empty_list_and_none():
    """
    Test that to_namedtuple handles:
    1. A list containing an empty list as an element - should return a list with the empty list preserved
    2. None as input - should handle None input without errors
    """
    # Setup
    EMPTY_LIST = []
    list_containing_empty_list = [EMPTY_LIST]
    NONE_VALUE = None

    # Execution: Convert a list containing an empty list to namedtuple
    result_with_nested_empty_list = named_tuple_utils.to_namedtuple(list_containing_empty_list)

    # Assert: The result should be a list containing the empty list
    assert isinstance(result_with_nested_empty_list, list)
    assert result_with_nested_empty_list == [EMPTY_LIST]

    # Execution & Assertion: Converting None should not raise an exception
    result_with_none = named_tuple_utils.to_namedtuple(NONE_VALUE)
    assert result_with_none is None

def test_to_namedtuple_with_complex_nested_structures():
    # Test that to_namedtuple handles complex nested structures including
    # dicts with long string keys, tuples containing namedtuples, and
    # mixed-key dicts (namedtuple and bool keys), as well as passing
    # a namedtuple back into to_namedtuple and handling a boolean input.

    # Constants
    LONG_DOC_STRING_KEY = (
        "Normalize a given path.\n\n    The given ``path`` will be normalized in the following process.\n\n"
        "    #. :obj:`bytes` will be converted to a :obj:`str` using the encoding\n"
        "       given by :obj:`getfilesystemencoding() <sys.getfilesystemencoding>`.\n"
        "    #. :obj:`PosixPath <pathlib.PosixPath>` and\n"
        "       :obj:`WindowsPath <pathlib.WindowsPath>` will be converted\n"
        "       to a :obj:`str` using the :obj:`as_posix() <pathlib.PurePath.as_posix>`\n"
        "       method.\n"
        "    #. An initial component of ``~`` will be replaced by that user's\n"
        "       home directory.\n"
        "    #. Any environment variables will be expanded.\n"
        "    #. Non absolute paths will have the current working directory from\n"
        "       :obj:`os.getcwd() <os.cwd>`prepended.  If needed, use\n"
        "       :obj:`os.chdir() <os.chdir>` to change the current working directory\n"
        "       before calling this function.\n"
        "    #. Redundant separators and up-level references will be normalized, so\n"
        "       that ``A//B``, ``A/B/``, ``A/./B`` and ``A/foo/../B`` all become\n"
        "       ``A/B``.\n\n"
        "    Args:\n"
        "        path (:obj:`str`, :obj:`bytes` or :obj:`Path <pathlib.Path>`):\n"
        "            The path to be normalized.\n\n"
        "    :rtype:\n"
        "        :obj:`Path <pathlib.Path>`\n\n"
        "        * :obj:`PosixPath <pathlib.PosixPath>` or\n"
        "          :obj:`WindowsPath <pathlib.WindowsPath>` depending on the system.\n\n"
        "        .. Note:: :obj:`Path <pathlib.Path>` objects are immutable. Therefore,\n"
        "           any given ``path`` of type :obj:`Path <pathlib.Path>` will not be\n"
        "           the same object returned.\n\n"
        "    Example:\n\n"
        "        >>> from flutils.pathutils import normalize_path\n"
        "        >>> normalize_path('~/tmp/foo/../bar')\n"
        "        PosixPath('/home/test_user/tmp/bar')\n\n"
        "    "
    )
    BOOL_KEY = False

    # Setup: Create a dict with a long doc string as both key and value
    # (duplicate keys collapse to one entry in Python dicts)
    dict_with_string_keys = {LONG_DOC_STRING_KEY: LONG_DOC_STRING_KEY}

    # Execution 1: Convert dict with string keys to namedtuple
    namedtuple_from_string_keyed_dict = named_tuple_utils.to_namedtuple(dict_with_string_keys)

    # Execution 2: Convert the same dict again to get a namedtuple for nesting
    namedtuple_from_string_keyed_dict_copy = named_tuple_utils.to_namedtuple(dict_with_string_keys)

    # Execution 3: Wrap the namedtuple in a tuple and convert to namedtuple
    tuple_containing_namedtuple = (namedtuple_from_string_keyed_dict_copy,)
    namedtuple_from_tuple = named_tuple_utils.to_namedtuple(tuple_containing_namedtuple)

    # Setup: Create a dict with mixed keys (namedtuple and bool)
    dict_with_mixed_keys = {
        namedtuple_from_tuple: namedtuple_from_string_keyed_dict_copy,
        BOOL_KEY: namedtuple_from_string_keyed_dict_copy,
    }

    # Execution 4: Convert mixed-key dict to namedtuple
    namedtuple_from_mixed_key_dict = named_tuple_utils.to_namedtuple(dict_with_mixed_keys)

    # Execution 5: Pass the resulting namedtuple back into to_namedtuple
    namedtuple_from_namedtuple = named_tuple_utils.to_namedtuple(namedtuple_from_mixed_key_dict)

    # Execution 6: Convert the mixed-key dict namedtuple again
    namedtuple_from_mixed_key_dict_again = named_tuple_utils.to_namedtuple(namedtuple_from_mixed_key_dict)

    # Execution 7: Pass a boolean False into to_namedtuple (non-convertible type)
    result_from_bool = named_tuple_utils.to_namedtuple(BOOL_KEY)

    # Assertions: Verify that conversion results are namedtuple or basic types as expected
    assert isinstance(namedtuple_from_string_keyed_dict, tuple), (
        "Expected a namedtuple (tuple subclass) from a dict with string keys"
    )
    assert isinstance(namedtuple_from_tuple, tuple), (
        "Expected a namedtuple (tuple subclass) from a tuple containing a namedtuple"
    )
    assert isinstance(namedtuple_from_namedtuple, tuple), (
        "Expected a namedtuple (tuple subclass) when passing a namedtuple back in"
    )
    assert result_from_bool == BOOL_KEY, (
        "Expected the boolean value to be returned unchanged since booleans cannot be converted"
    )

def test_convert_nested_list_with_dict_to_namedtuple_multiple_times():
    """
    Test that to_namedtuple can handle nested structures with mixed types
    (list containing tuple with dict) and that converting an already
    converted namedtuple multiple times is idempotent. Also verifies that
    converting a plain integer (non-convertible type) works without error.
    """
    # Setup: Create a nested structure with a special character string key,
    # empty tuple, and a dict containing mixed key-value types
    SPECIAL_CHAR_KEY = "\x0cMv"
    EMPTY_TUPLE = ()

    # Dict with both string and tuple keys (tuple keys will be ignored as
    # they can't be valid identifiers)
    nested_dict = {SPECIAL_CHAR_KEY: EMPTY_TUPLE, EMPTY_TUPLE: EMPTY_TUPLE}

    # Create a tuple containing the special string and the dict,
    # then wrap it in a list
    tuple_with_dict = (SPECIAL_CHAR_KEY, nested_dict)
    list_with_tuple = [tuple_with_dict]

    # Execution: Convert the nested list structure to namedtuple
    first_conversion = named_tuple_utils.to_namedtuple(list_with_tuple)

    # Convert the already-converted result again (should be idempotent)
    second_conversion = named_tuple_utils.to_namedtuple(first_conversion)

    # Convert one more time to verify stability of repeated conversions
    third_conversion = named_tuple_utils.to_namedtuple(second_conversion)

    # Verify that converting a plain integer (non-convertible type) does not raise an error
    NON_CONVERTIBLE_INT = 2
    int_conversion_result = named_tuple_utils.to_namedtuple(NON_CONVERTIBLE_INT)

    # Assertions: Verify that conversions produce list and tuple types correctly
    assert isinstance(first_conversion, list), (
        "Converting a list should return a list"
    )
    assert isinstance(second_conversion, list), (
        "Re-converting a converted list should still return a list"
    )
    assert isinstance(third_conversion, list), (
        "Third conversion of a converted list should still return a list"
    )
    assert int_conversion_result == NON_CONVERTIBLE_INT, (
        "Converting a plain integer should return the integer unchanged"
    )

def test_to_namedtuple_with_dict_containing_bytes_keys_and_values():
    """
    Test that to_namedtuple handles a dictionary where both keys and values
    are bytes objects. Since bytes objects cannot be used as proper identifiers
    (valid attribute names), the conversion should handle this gracefully.
    The dictionary has duplicate byte keys which means only one key-value pair
    will be present in the dict.
    """
    # Setup: Create bytes object and dictionary with bytes as keys and values
    BYTES_KEY_VALUE = b"F\xdb\xfdf\x8a\xe4\n\xa2\x1d[\xdc*\xa3\xba\xf6s}"
    dict_with_bytes_keys = {BYTES_KEY_VALUE: BYTES_KEY_VALUE}

    # Execute: Attempt to convert the dict with bytes keys to a namedtuple
    result = named_tuple_utils.to_namedtuple(dict_with_bytes_keys)

    # Assert: Verify that the result is a namedtuple (bytes keys are not valid
    # identifiers, so they cannot become attributes; the result should still
    # be a valid namedtuple, potentially with no fields)
    assert isinstance(result, tuple)

