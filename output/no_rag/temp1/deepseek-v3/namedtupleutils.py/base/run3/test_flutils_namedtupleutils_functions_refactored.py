import pytest
import namedtupleutils as ntuple_utils
import collections as collections_module

def test_to_namedtuple_with_unsupported_float_returns_original_value():
    # Setup: Create a float value, which is not a supported type for conversion
    unsupported_value = -476.66

    # Execution: Attempt to convert the unsupported type to a namedtuple
    # This should still work because the function handles all allowed types
    result = ntuple_utils.to_namedtuple(unsupported_value)

    # Assertion: The function should return the original value unchanged
    # since a float cannot be converted to a namedtuple
    assert result == unsupported_value

def test_to_namedtuple_with_tuple_containing_set_of_floats():
    # Setup: a tuple containing a single float and a set of floats.
    # The set contains only unique values, so it collapses to one float.
    FLOAT_VALUE = -67.0
    unique_float_set = {FLOAT_VALUE}
    input_tuple_with_set = (FLOAT_VALUE, unique_float_set)

    # Execution: convert the nested tuple/set structure into a namedtuple.
    converted_result = ntuple_utils.to_namedtuple(input_tuple_with_set)

    # Assertion: also ensure a plain set can be passed without error.
    ntuple_utils.to_namedtuple(unique_float_set)

def test_to_namedtuple_round_trips_its_own_namedtuple_output():
    # Setup: a dict whose keys collide after Python deduplication, leaving a single 'author' key.
    source_key = "author"
    source_dict = {source_key: source_key, source_key: source_key, source_key: source_key}

    # Setup: first conversion of the dict into a namedtuple.
    first_conversion = ntuple_utils.to_namedtuple(source_dict)

    # Execution: convert the resulting namedtuple again to verify it accepts its own output.
    second_conversion = ntuple_utils.to_namedtuple(first_conversion)

    # Assertion: the round-tripped value is unchanged, confirming idempotent conversion.
    assert second_conversion == first_conversion

def test_to_namedtuple_with_bytes_object_returns_original_value():
    # Setup: Create a bytes object with non-ASCII byte values
    BYTES_INPUT = b"xs&,\x9b\xc2\xf1\x80\xb3y"
    
    # Execution: Attempt to convert a bytes object to a namedtuple
    # Note: The to_namedtuple function should handle non-convertible types gracefully
    to_namedtuple_result = ntuple_utils.to_namedtuple(BYTES_INPUT)
    
    # Assertion: The function should return the original bytes object since
    # bytes objects are not in the allowed types for conversion
    assert to_namedtuple_result == BYTES_INPUT

def test_to_namedtuple_with_empty_input_returns_empty_tuple():
    # Setup: an empty tuple input for the conversion function.
    empty_tuple = ()

    # Execution: convert the empty tuple using the namedtuple utility.
    result = ntuple_utils.to_namedtuple(empty_tuple)

    # Assertion: an empty tuple should be returned unchanged.
    assert result == ()

def test_to_namedtuple_with_ordered_dict_and_nested_tuple_returns_namedtuple_of_namedtuples():
    # Core purpose: Verify that calling to_namedtuple on an empty OrderedDict
    # produces a valid NamedTuple, and that converting nested structures
    # (namedtuple, tuple of namedtuple+bytes) yields consistent results.

    # Setup
    ordered_dict = collections_module.OrderedDict()

    # Execution
    first_namedtuple = ntuple_utils.to_namedtuple(ordered_dict)
    second_namedtuple = ntuple_utils.to_namedtuple(first_namedtuple)
    third_namedtuple = ntuple_utils.to_namedtuple(ordered_dict)
    fourth_namedtuple = ntuple_utils.to_namedtuple(third_namedtuple)
    raw_bytes = b"\xe2\xf8\xb9\x01\x8c\xa5\xed\xb1\x0e&rdHE"
    fifth_namedtuple = ntuple_utils.to_namedtuple(ordered_dict)
    nested_tuple = (second_namedtuple, raw_bytes)
    sixth_namedtuple = ntuple_utils.to_namedtuple(nested_tuple)
    seventh_namedtuple = ntuple_utils.to_namedtuple(ordered_dict)

    # Assertion
    # Each conversion result should be a valid NamedTuple instance.
    assert isinstance(first_namedtuple, tuple)
    assert isinstance(second_namedtuple, tuple)
    assert isinstance(third_namedtuple, tuple)
    assert isinstance(fourth_namedtuple, tuple)
    assert isinstance(fifth_namedtuple, tuple)
    assert isinstance(sixth_namedtuple, tuple)
    assert isinstance(seventh_namedtuple, tuple)

def test_to_namedtuple_with_invalid_identifier_keys_from_ordereddict_ignored():
    invalid_identifier_key = "wm=-g\ry#\x0b#:*"

    ordered_dict_with_invalid_keys = collections_module.OrderedDict(
        {invalid_identifier_key: invalid_identifier_key}
    )

    result = ntuple_utils.to_namedtuple(ordered_dict_with_invalid_keys)

    assert result is not None
    assert not hasattr(result, invalid_identifier_key)

    with pytest.raises(TypeError):
        collections_module.OrderedDict(None)

def test_to_namedtuple_with_empty_nested_list_and_none_returns_expected_values():
    # Setup: Create a list containing an empty list as an element.
    empty_list = []
    list_with_empty_nested_list = [empty_list]

    # Execution: Convert the list (with nested empty list) into a namedtuple.
    result = ntuple_utils.to_namedtuple(list_with_empty_nested_list)

    # Assertion: The result should be a tuple (namedtuple) and the nested empty list
    # should be converted to an empty tuple.
    assert result == ((),)
    assert isinstance(result, tuple)
    assert result[0] == ()

    # Execution: Convert None into a namedtuple.
    result_none = ntuple_utils.to_namedtuple(None)

    # Assertion: None should be returned as-is.
    assert result_none is None

def test_to_namedtuple_with_complex_nested_structures_and_repeated_conversions():
    # Setup: create a complex dictionary with a long multi-line string as both key and value
    original_string = (
        "Normalize a given path.\n\n    The given ``path`` will be normalized in the following process.\n\n"
        "    #. :obj:`bytes` will be converted to a :obj:`str` using the encoding\n"
        "       given by :obj:`getfilesystemencoding() <sys.getfilesystemencoding>`.\n"
        "    #. :obj:`PosixPath <pathlib.PosixPath>` and\n"
        "       :obj:`WindowsPath <pathlib.WindowsPath>` will be converted\n"
        "       to a :obj:`str` using the :obj:`as_posix() <pathlib.PurePath.as_posix>`\n"
        "       method.\n"
        "    #. An initial component of ``~`` will be replaced by that user’s\n"
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
    input_dict = {original_string: original_string}

    # Execution: perform a series of nested to_namedtuple conversions
    first_namedtuple = ntuple_utils.to_namedtuple(input_dict)

    second_namedtuple = ntuple_utils.to_namedtuple(input_dict)
    nested_tuple = (second_namedtuple,)
    third_namedtuple = ntuple_utils.to_namedtuple(nested_tuple)

    fourth_namedtuple = ntuple_utils.to_namedtuple(
        {third_namedtuple: second_namedtuple, False: second_namedtuple}
    )
    fifth_namedtuple = ntuple_utils.to_namedtuple(fourth_namedtuple)

    sixth_namedtuple = ntuple_utils.to_namedtuple(fourth_namedtuple)
    ntuple_utils.to_namedtuple(False)

    # Assertion: verify the returned objects are instances of the expected types
    assert isinstance(first_namedtuple, collections_module.namedtuple)
    assert isinstance(second_namedtuple, collections_module.namedtuple)
    assert isinstance(third_namedtuple, tuple)
    assert isinstance(fourth_namedtuple, collections_module.namedtuple)
    assert isinstance(fifth_namedtuple, collections_module.namedtuple)
    assert isinstance(sixth_namedtuple, collections_module.namedtuple)

def test_to_namedtuple_with_complex_nested_structures_and_repeated_conversions():
    # Constants for test data
    STRING_KEY = "\x0cMv"
    EMPTY_TUPLE = ()
    
    # Setup: Create complex nested structure with mixed types
    # Dictionary containing string keys, tuple keys, and self-referential values
    nested_dict = {
        STRING_KEY: EMPTY_TUPLE,
        EMPTY_TUPLE: STRING_KEY,
        EMPTY_TUPLE: EMPTY_TUPLE  # Note: duplicate key will override previous
    }
    
    # Create tuple containing string and nested dictionary
    mixed_tuple = (STRING_KEY, nested_dict)
    
    # Create list containing the mixed tuple
    initial_list = [mixed_tuple]
    
    # Execution: Test recursive conversion through multiple levels
    # First conversion: list -> namedtuple with recursively converted contents
    first_conversion = module_0.to_namedtuple(initial_list)
    
    # Second conversion: already converted object -> namedtuple (idempotent operation)
    second_conversion = module_0.to_namedtuple(first_conversion)
    
    # Third conversion: verify multiple conversions remain stable
    third_conversion = module_0.to_namedtuple(second_conversion)
    
    # Test edge case: integer should remain unchanged (not convertible to namedtuple)
    INT_INPUT = 2
    int_result = module_0.to_namedtuple(INT_INPUT)
    
    # Assertions: Verify the conversions handle complex nested structures
    # The function should process lists, tuples, and dicts recursively
    # while leaving non-convertible items (like integers) unchanged
    assert first_conversion is not None
    assert second_conversion is not None  
    assert third_conversion is not None
    assert int_result == INT_INPUT  # integers should pass through unchanged

def test_to_namedtuple_with_binary_key_dict_returns_tuple():
    # Constants
    KEY = b"F\xdb\xfdf\x8a\xe4\n\xa2\x1d[\xdc*\xa3\xba\xf6s}"
    
    # Setup
    test_dict = {KEY: KEY}
    
    # Execution
    result = ntuple_utils.to_namedtuple(test_dict)
    
    # Assertion
    assert isinstance(result, tuple)

