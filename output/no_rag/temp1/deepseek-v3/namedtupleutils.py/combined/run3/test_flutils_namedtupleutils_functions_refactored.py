import pytest
import namedtupleutils as namedtuple_utils
import collections

def test_to_namedtuple_with_float_input_returns_namedtuple():
    # Setup
    input_value = -476.66  # A float value is provided as input to test the conversion to namedtuple
    
    # Execution
    result = namedtuple_utils.to_namedtuple(input_value)
    
    # Assertion
    # The function should convert the float value to a namedtuple representation
    # Since floats are immutable primitives, the result should be a namedtuple
    # containing the float value as its sole attribute
    assert isinstance(result, collections.namedtuple)
    assert result._fields == ('value',)
    assert result.value == input_value

def test_to_namedtuple_with_tuple_containing_float_and_set():
    initialized_float = -67.0
    initialized_set = {initialized_float}

    input_tuple = (initialized_float, initialized_set)

    converted_tuple = namedtuple_utils.to_namedtuple(input_tuple)

    namedtuple_utils.to_namedtuple(initialized_set)

    assert isinstance(converted_tuple, tuple) or hasattr(converted_tuple, '_fields')

def test_to_namedtuple_dict_and_namedtuple_conversions_are_equivalent():
    # Setup: a dictionary with a single key repeated (dict literal collapses to one "author" key)
    expected_attribute_name = "author"
    expected_attribute_value = "author"
    input_dict = {expected_attribute_name: expected_attribute_value}

    # Execute: convert the dictionary to a namedtuple, then convert that result again
    result_from_dict = namedtuple_utils.to_namedtuple(input_dict)
    result_from_namedtuple = namedtuple_utils.to_namedtuple(result_from_dict)

    # Assertion: both conversions produce equivalent namedtuples with the expected attribute
    assert result_from_dict == result_from_namedtuple
    assert result_from_dict.author == expected_attribute_value
    assert result_from_namedtuple.author == expected_attribute_value
    assert isinstance(result_from_dict, tuple) and hasattr(result_from_dict, "_fields")
    assert isinstance(result_from_namedtuple, tuple) and hasattr(result_from_namedtuple, "_fields")

def test_to_namedtuple_with_bytes_input_returns_bytes_unchanged():
    # Purpose:
    # When to_namedtuple() is called with a value that is not one of the
    # supported container types (e.g., bytes), the value should be returned
    # as-is without raising an error or attempting a conversion.
    #
    # A short, arbitrary byte string is used as the input.

    byte_input = b"xs&,\x9b\xc2\xf1\x80\xb3y"

    result = namedtuple_utils.to_namedtuple(byte_input)

    assert result == byte_input

def test_to_namedtuple_with_empty_tuple_returns_empty_tuple_input():
    # Setup
    empty_tuple = ()
    
    # Execution
    result = namedtuple_utils.to_namedtuple(empty_tuple)
    
    # Assertion
    assert result == ()

def test_to_namedtuple_with_empty_ordered_dict_idempotent_conversion_behavior():
    # Setup: create an empty OrderedDict to convert to namedtuple
    EMPTY_ORDERED_DICT = collections.OrderedDict()
    BYTES_VALUE = b"\xe2\xf8\xb9\x01\x8c\xa5\xed\xb1\x0e&rdHE"
    
    # Execution: convert the empty OrderedDict to a namedtuple (returns empty namedtuple)
    initial_namedtuple = namedtuple_utils.to_namedtuple(EMPTY_ORDERED_DICT)
    
    # Execution: convert the resulting namedtuple to namedtuple again (idempotent)
    re_converted_namedtuple = namedtuple_utils.to_namedtuple(initial_namedtuple)
    
    # Execution: convert empty OrderedDict to namedtuple again (should produce the same empty namedtuple)
    second_namedtuple = namedtuple_utils.to_namedtuple(EMPTY_ORDERED_DICT)
    second_re_converted_namedtuple = namedtuple_utils.to_namedtuple(second_namedtuple)
    
    # Execution: create a tuple containing the re-converted namedtuple and some bytes, then convert it
    TUPLE_WITH_NAMEDTUPLE_AND_BYTES = (re_converted_namedtuple, BYTES_VALUE)
    converted_tuple = namedtuple_utils.to_namedtuple(TUPLE_WITH_NAMEDTUPLE_AND_BYTES)
    
    # Execution: convert empty OrderedDict one more time (ensuring repeated conversion works)
    final_namedtuple = namedtuple_utils.to_namedtuple(EMPTY_ORDERED_DICT)
    
    # Assertion: all conversions should return empty namedtuples (or tuples/lists containing them)
    # The initial empty OrderedDict converts to an empty namedtuple
    assert initial_namedtuple == namedtuple_utils.to_namedtuple(collections.OrderedDict())
    
    # The namedtuple is idempotent: converting it again yields an equivalent empty namedtuple
    assert re_converted_namedtuple == initial_namedtuple
    
    # A fresh empty OrderedDict produces the same empty namedtuple
    assert second_namedtuple == initial_namedtuple
    assert second_re_converted_namedtuple == initial_namedtuple
    
    # Converting a tuple containing an empty namedtuple and bytes returns a tuple of the same length
    assert isinstance(converted_tuple, tuple)
    assert len(converted_tuple) == 2
    assert converted_tuple[0] == initial_namedtuple
    assert converted_tuple[1] == BYTES_VALUE
    
    # The final conversion of an empty OrderedDict again yields an empty namedtuple
    assert final_namedtuple == initial_namedtuple

def test_to_namedtuple_with_ordered_dict_special_keys_and_invalid_ordereddict_construction():
    # Constants representing edge-case string inputs and expected behavior
    SPECIAL_KEY = "wm=-g\ry#\x0b#:*"
    DICTIONARY = {SPECIAL_KEY: SPECIAL_KEY, SPECIAL_KEY: SPECIAL_KEY}

    # Setup: create an OrderedDict whose keys are non-identifier strings
    ordered_dict = collections.OrderedDict(**DICTIONARY)

    # Execution: convert the OrderedDict to a NamedTuple
    result = namedtuple_utils.to_namedtuple(ordered_dict)

    # Assertion: the conversion should succeed and produce a NamedTuple
    assert result is not None
    assert isinstance(result, tuple)

    # Edge-case check: constructing OrderedDict from a list with None should raise
    none_value = None
    value_list = [none_value]
    with pytest.raises(TypeError):
        collections.OrderedDict(*value_list)

def test_to_namedtuple_handles_nested_empty_list_and_none_input():
    """
    Tests the behavior of `to_namedtuple` for two edge cases:
    1. A list containing a single empty list should return a list of the same
       structure with the nested list converted (though an empty list remains
       an empty list).
    2. Passing `None` should be handled gracefully (implementation raises no
       error and returns something sensible, typically `None` itself).
    """
    # Setup
    inner_empty_list = []
    nested_list = [inner_empty_list]
    none_input = None

    # Execution
    result_nested_list = namedtuple_utils.to_namedtuple(nested_list)
    result_none = namedtuple_utils.to_namedtuple(none_input)

    # Assertions
    assert result_nested_list == [inner_empty_list]
    assert result_none is None

def test_to_namedtuple_recursive_conversion_with_docstring_keys_and_mixed_types():
    # Setup - input string with docstring-like content used as a dict key/value
    normalized_path_docs = (
        "Normalize a given path.\n\n"
        "    The given ``path`` will be normalized in the following process.\n\n"
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

    # A dict with duplicate keys (Python collapses to a single entry)
    input_dict_with_duplicate_keys = {
        normalized_path_docs: normalized_path_docs,
        normalized_path_docs: normalized_path_docs,
        normalized_path_docs: normalized_path_docs,
    }

    # Execution - first conversion level
    result_namedtuple = namedtuple_utils.to_namedtuple(input_dict_with_duplicate_keys)
    assert result_namedtuple is not None

    # Build a nested structure to exercise recursive conversion
    second_conversion = namedtuple_utils.to_namedtuple(input_dict_with_duplicate_keys)
    boolean_flag = False

    # Wrap a namedtuple in a tuple and convert again
    tuple_containing_namedtuple = (second_conversion,)
    converted_tuple = namedtuple_utils.to_namedtuple(tuple_containing_namedtuple)

    # Build a dict with non-string (bool) key and namedtuple value to exercise
    # identifier sanitization and recursive value conversion
    dict_with_mixed_keys = {
        converted_tuple: second_conversion,
        boolean_flag: second_conversion,
    }
    converted_dict_namedtuple = namedtuple_utils.to_namedtuple(dict_with_mixed_keys)

    # Recursively convert an already-converted namedtuple
    double_converted = namedtuple_utils.to_namedtuple(converted_dict_namedtuple)

    # Re-convert the same dict-namedtuple with another boolean flag unused value
    another_conversion = namedtuple_utils.to_namedtuple(converted_dict_namedtuple)

    # Convert a bare boolean primitive (non-mapping, non-sequence type)
    primitive_conversion = namedtuple_utils.to_namedtuple(boolean_flag)

    # Assertions - verify recursive conversion behavior
    assert result_namedtuple is not None
    assert second_conversion is not None
    assert converted_tuple is not None
    assert converted_dict_namedtuple is not None
    assert double_converted is not None
    assert another_conversion is not None
    assert primitive_conversion is not None

def test_to_namedtuple_nested_mixed_keys_and_recursive_conversion():
    # Constants used to build the input structures
    STRING_VALUE = "\x0cMv"
    EMPTY_TUPLE = ()
    INTEGER_VALUE = 2

    # Setup: build a dict that mixes string and tuple keys, plus a nested tuple/list
    initial_dict = {
        STRING_VALUE: EMPTY_TUPLE,
        EMPTY_TUPLE: STRING_VALUE,
        EMPTY_TUPLE: EMPTY_TUPLE,
    }
    nested_tuple = (STRING_VALUE, initial_dict)
    input_list = [nested_tuple]

    # Execution: recursively convert the list to a namedtuple and
    # chain further conversions to verify idempotence/recursion behavior.
    first_conversion = namedtuple_utils.to_namedtuple(input_list)
    second_conversion = namedtuple_utils.to_namedtuple(first_conversion)
    third_conversion = namedtuple_utils.to_namedtuple(second_conversion)

    # Execution: convert a non-container primitive to ensure it is handled gracefully.
    namedtuple_utils.to_namedtuple(INTEGER_VALUE)

    # Assertions
    # The list should be converted into a list containing a namedtuple for the nested tuple.
    assert isinstance(first_conversion, list)

    # The nested tuple should become a namedtuple with convertible fields.
    assert isinstance(second_conversion[0], collections.namedtuple)
    assert isinstance(third_conversion[0], collections.namedtuple)

    # The integer cannot be converted, so the result should be the integer itself.
    assert namedtuple_utils.to_namedtuple(INTEGER_VALUE) == INTEGER_VALUE

def test_to_namedtuple_with_bytes_dict_keys_handles_non_identifier_keys():
    """
    Test that `to_namedtuple` handles a dictionary whose keys are bytes.

    Bytes are not valid Python identifiers, so this verifies the function
    does not raise when attempting to build a namedtuple from a dict with
    non-identifier (bytes) keys. All keys map to the same bytes value,
    so the resulting dict has a single entry.
    """
    # Setup
    bytes_key = b"F\xdb\xfdf\x8a\xe4\n\xa2\x1d[\xdc*\xa3\xba\xf6s}"
    input_dict = {bytes_key: bytes_key}

    # Execution
    result = namedtuple_utils.to_namedtuple(input_dict)

    # Assertion
    assert result is not None

