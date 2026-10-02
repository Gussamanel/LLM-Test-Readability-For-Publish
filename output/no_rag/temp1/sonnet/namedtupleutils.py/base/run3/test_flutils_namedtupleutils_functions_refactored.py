import pytest
import namedtupleutils as namedtuple_utils
import collections as collections

def test_to_namedtuple_raises_error_for_float_input():
    # Test that to_namedtuple raises an error when given a float,
    # since floats are not a supported type for conversion
    # (only dict, list, tuple, OrderedDict, and SimpleNamespace are supported)
    
    # Setup
    INVALID_FLOAT_INPUT = -476.66
    
    # Execution & Assertion
    with pytest.raises(Exception):
        namedtuple_utils.to_namedtuple(INVALID_FLOAT_INPUT)

def test_to_namedtuple_with_tuple_containing_set_and_direct_set():
    """
    Test that to_namedtuple handles a tuple containing mixed types (float and set)
    and also handles a direct set input.
    
    - When given a tuple containing a float and a set, the function should convert
      the tuple to a namedtuple (or return it with recursively processed contents).
    - When given a plain set directly, the function should handle it without errors,
      as sets are not directly convertible to namedtuples but should not raise exceptions.
    """
    # Setup
    FLOAT_VALUE = -67.0
    input_set = {FLOAT_VALUE}  # A set with a single unique float value (duplicates collapse)
    input_tuple = (FLOAT_VALUE, input_set)  # A tuple containing a float and a set

    # Execute: Convert a tuple containing mixed types (float and set)
    result_from_tuple = namedtuple_utils.to_namedtuple(input_tuple)

    # Execute: Convert a plain set (non-convertible type, should not raise)
    result_from_set = namedtuple_utils.to_namedtuple(input_set)

    # Assert: The result from the tuple should be a tuple (since sets inside cannot become namedtuple fields)
    assert isinstance(result_from_tuple, tuple)

    # Assert: The result from the set should be the original set unchanged (sets are not convertible)
    assert result_from_set == input_set

def test_convert_dict_to_namedtuple_and_reconvert():
    """
    Test that converting a dictionary to a namedtuple, and then converting
    the resulting namedtuple back to a namedtuple, produces a valid namedtuple
    with the expected field and value.
    
    This verifies that:
    1. A dictionary with a single unique key-value pair (due to duplicate keys)
       is correctly converted to a namedtuple.
    2. The resulting namedtuple can be passed back into to_namedtuple without error,
       and the output remains a valid namedtuple with the same field and value.
    """
    # Setup: Create a dictionary with duplicate keys (only one unique key-value pair will remain)
    FIELD_NAME = "author"
    input_dict = {FIELD_NAME: FIELD_NAME}

    # Execution: Convert the dictionary to a namedtuple
    namedtuple_from_dict = namedtuple_utils.to_namedtuple(input_dict)

    # Execution: Convert the resulting namedtuple back to a namedtuple
    namedtuple_from_namedtuple = namedtuple_utils.to_namedtuple(namedtuple_from_dict)

    # Assertion: Verify the first conversion produced a namedtuple with the expected field and value
    assert isinstance(namedtuple_from_dict, tuple)
    assert hasattr(namedtuple_from_dict, FIELD_NAME)
    assert getattr(namedtuple_from_dict, FIELD_NAME) == FIELD_NAME

    # Assertion: Verify the second conversion also produced a namedtuple with the same field and value
    assert isinstance(namedtuple_from_namedtuple, tuple)
    assert hasattr(namedtuple_from_namedtuple, FIELD_NAME)
    assert getattr(namedtuple_from_namedtuple, FIELD_NAME) == FIELD_NAME

def test_to_namedtuple_with_bytes_input_raises_error():
    """
    Test that to_namedtuple raises an error when given bytes input.
    
    The function only supports specific types (dict, list, tuple, SimpleNamespace,
    OrderedDict). Passing a bytes object should raise an error as it is not
    an allowed type for conversion.
    """
    # Setup: Create a bytes object which is not a supported type for conversion
    BYTES_INPUT = b"xs&,\x9b\xc2\xf1\x80\xb3y"

    # Execution & Assertion: Verify that passing bytes raises an error
    with pytest.raises(Exception):
        namedtuple_utils.to_namedtuple(BYTES_INPUT)

def test_to_namedtuple_with_empty_tuple_returns_empty_tuple():
    # Test that converting an empty tuple with to_namedtuple returns an empty tuple
    # Since an empty tuple has no items to convert, it should be returned as-is
    
    # Setup
    EMPTY_TUPLE = ()
    
    # Execute
    result = namedtuple_utils.to_namedtuple(EMPTY_TUPLE)
    
    # Assert
    assert result == EMPTY_TUPLE
    assert isinstance(result, tuple)
    assert len(result) == 0

def test_convert_ordered_dict_and_tuple_with_bytes_to_namedtuple():
    """
    Test that to_namedtuple correctly handles:
    1. Converting an empty OrderedDict to a namedtuple
    2. Converting an already-converted namedtuple back to a namedtuple (idempotent behavior)
    3. Converting a tuple containing a namedtuple and bytes to a namedtuple
    """
    # Setup
    empty_ordered_dict = collections.OrderedDict()
    raw_bytes = b"\xe2\xf8\xb9\x01\x8c\xa5\xed\xb1\x0e&rdHE"

    # Execute: Convert empty OrderedDict to namedtuple
    first_namedtuple = namedtuple_utils.to_namedtuple(empty_ordered_dict)

    # Execute: Convert the resulting namedtuple back to namedtuple (idempotent check)
    namedtuple_from_namedtuple = namedtuple_utils.to_namedtuple(first_namedtuple)

    # Execute: Convert empty OrderedDict again to verify consistent results
    second_namedtuple = namedtuple_utils.to_namedtuple(empty_ordered_dict)

    # Execute: Convert the second namedtuple back to namedtuple (idempotent check)
    namedtuple_from_second_namedtuple = namedtuple_utils.to_namedtuple(second_namedtuple)

    # Execute: Convert a tuple containing a namedtuple and bytes
    mixed_tuple = (namedtuple_from_namedtuple, raw_bytes)
    namedtuple_from_mixed_tuple = namedtuple_utils.to_namedtuple(mixed_tuple)

    # Execute: Convert empty OrderedDict one more time for consistency
    third_namedtuple = namedtuple_utils.to_namedtuple(empty_ordered_dict)

    # Assert: Verify empty OrderedDict conversions produce consistent namedtuples
    assert first_namedtuple == second_namedtuple == third_namedtuple

    # Assert: Verify that converting a namedtuple is idempotent
    assert first_namedtuple == namedtuple_from_namedtuple
    assert second_namedtuple == namedtuple_from_second_namedtuple

    # Assert: Verify that the mixed tuple was converted correctly
    assert isinstance(namedtuple_from_mixed_tuple, tuple)
    assert namedtuple_from_mixed_tuple[0] == namedtuple_from_namedtuple
    assert namedtuple_from_mixed_tuple[1] == raw_bytes

def test_convert_ordered_dict_with_special_char_key_to_namedtuple():
    """
    Test that to_namedtuple handles an OrderedDict with special character keys.
    
    Special characters in dictionary keys (like control characters and symbols)
    cannot be used as valid Python identifiers, so the resulting namedtuple
    should handle this gracefully. Also verifies that creating an OrderedDict
    with a None value in the positional argument raises a TypeError.
    """
    # Setup: Create a key with special/control characters that are invalid Python identifiers
    SPECIAL_CHAR_KEY = "wm=-g\ry#\x0b#:*"
    
    # Create a regular dict and then an OrderedDict with the special char key
    source_dict = {SPECIAL_CHAR_KEY: SPECIAL_CHAR_KEY}
    ordered_dict_with_special_keys = collections.OrderedDict(**source_dict)
    
    # Execution: Attempt to convert the OrderedDict with invalid identifier keys to a namedtuple
    result = namedtuple_utils.to_namedtuple(ordered_dict_with_special_keys)
    
    # Assert: Verify that creating an OrderedDict with None as positional arg raises TypeError
    none_value = None
    invalid_positional_args = [none_value]
    with pytest.raises(TypeError):
        collections.OrderedDict(*invalid_positional_args)

def test_to_namedtuple_with_list_containing_empty_list_and_none():
    """
    Test that to_namedtuple handles:
    1. A list containing an empty list as an element - should return the list
       with the empty list preserved as-is (since empty lists can't be converted
       to namedtuples).
    2. A None value - should handle None input gracefully without raising errors.
    """
    # Setup
    EMPTY_LIST = []
    list_containing_empty_list = [EMPTY_LIST]

    # Execution - Convert a list containing an empty list
    result_with_nested_empty_list = namedtuple_utils.to_namedtuple(list_containing_empty_list)

    # Assert - The result should be a list with the empty list preserved inside
    assert isinstance(result_with_nested_empty_list, list)
    assert result_with_nested_empty_list == [[]]

    # Execution & Assertion - Converting None should not raise an error
    none_input = None
    result_with_none = namedtuple_utils.to_namedtuple(none_input)
    assert result_with_none is None

def test_to_namedtuple_with_complex_nested_structures():
    # Test that to_namedtuple handles complex nested structures including
    # dicts with non-identifier keys, nested namedtuples, and boolean values

    # A long docstring used as a dictionary key (non-identifier key)
    DOCSTRING_KEY = "Normalize a given path.\n\n    The given ``path`` will be normalized in the following process.\n\n    #. :obj:`bytes` will be converted to a :obj:`str` using the encoding\n       given by :obj:`getfilesystemencoding() <sys.getfilesystemencoding>`.\n    #. :obj:`PosixPath <pathlib.PosixPath>` and\n       :obj:`WindowsPath <pathlib.WindowsPath>` will be converted\n       to a :obj:`str` using the :obj:`as_posix() <pathlib.PurePath.as_posix>`\n       method.\n    #. An initial component of ``~`` will be replaced by that user's\n       home directory.\n    #. Any environment variables will be expanded.\n    #. Non absolute paths will have the current working directory from\n       :obj:`os.getcwd() <os.cwd>`prepended.  If needed, use\n       :obj:`os.chdir() <os.chdir>` to change the current working directory\n       before calling this function.\n    #. Redundant separators and up-level references will be normalized, so\n       that ``A//B``, ``A/B/``, ``A/./B`` and ``A/foo/../B`` all become\n       ``A/B``.\n\n    Args:\n        path (:obj:`str`, :obj:`bytes` or :obj:`Path <pathlib.Path>`):\n            The path to be normalized.\n\n    :rtype:\n        :obj:`Path <pathlib.Path>`\n\n        * :obj:`PosixPath <pathlib.PosixPath>` or\n          :obj:`WindowsPath <pathlib.WindowsPath>` depending on the system.\n\n        .. Note:: :obj:`Path <pathlib.Path>` objects are immutable. Therefore,\n           any given ``path`` of type :obj:`Path <pathlib.Path>` will not be\n           the same object returned.\n\n    Example:\n\n        >>> from flutils.pathutils import normalize_path\n        >>> normalize_path('~/tmp/foo/../bar')\n        PosixPath('/home/test_user/tmp/bar')\n\n    "

    # Setup: Create a dict with non-identifier string keys (docstring as key)
    # Since the keys are not valid identifiers, the resulting namedtuple will have no attributes
    dict_with_docstring_keys = {DOCSTRING_KEY: DOCSTRING_KEY}

    # Execution: Convert the dict with non-identifier keys to a namedtuple
    namedtuple_from_docstring_key_dict = namedtuple_utils.to_namedtuple(dict_with_docstring_keys)

    # Setup: Convert the same dict again and wrap the result in a tuple
    BOOL_VALUE_FALSE = False
    namedtuple_from_docstring_key_dict_second = namedtuple_utils.to_namedtuple(dict_with_docstring_keys)
    tuple_with_namedtuple = (namedtuple_from_docstring_key_dict_second,)

    # Execution: Convert the tuple containing a namedtuple into a namedtuple
    namedtuple_from_tuple = namedtuple_utils.to_namedtuple(tuple_with_namedtuple)

    # Setup: Create a dict mixing a namedtuple and a boolean as keys,
    # and namedtuples as values
    dict_with_mixed_keys = {namedtuple_from_tuple: namedtuple_from_docstring_key_dict_second,
                            BOOL_VALUE_FALSE: namedtuple_from_docstring_key_dict_second}

    # Execution: Convert the mixed-key dict to a namedtuple
    namedtuple_from_mixed_dict = namedtuple_utils.to_namedtuple(dict_with_mixed_keys)

    # Execution: Convert the already converted namedtuple again (idempotency check)
    namedtuple_from_namedtuple = namedtuple_utils.to_namedtuple(namedtuple_from_mixed_dict)

    # Execution: Convert the mixed dict namedtuple a second time
    namedtuple_from_mixed_dict_second = namedtuple_utils.to_namedtuple(namedtuple_from_mixed_dict)

    # Execution: Convert a plain boolean False value (non-convertible primitive)
    BOOL_VALUE_FALSE_SECOND = False
    result_from_bool = namedtuple_utils.to_namedtuple(BOOL_VALUE_FALSE_SECOND)

    # Assertion: Verify that converting a boolean returns the boolean itself unchanged
    assert result_from_bool == BOOL_VALUE_FALSE_SECOND

    # Assertion: Verify that converting a namedtuple again returns an equivalent namedtuple
    assert namedtuple_from_namedtuple == namedtuple_from_mixed_dict

    # Assertion: Verify that the two conversions of the mixed dict namedtuple are equivalent
    assert namedtuple_from_mixed_dict_second == namedtuple_from_mixed_dict

def test_to_namedtuple_with_nested_structures_and_idempotency():
    """
    Test that to_namedtuple handles nested structures (list containing a tuple with a dict),
    is idempotent when applied multiple times to already-converted namedtuples,
    and gracefully handles non-convertible types like integers.
    """
    # Constants
    SPECIAL_STRING = "\x0cMv"
    INTEGER_VALUE = 2

    # Setup: Create a nested structure: list > tuple > (string, dict)
    # The dict has mixed key types (string and tuple keys), some of which
    # are not valid identifiers and will be ignored during conversion
    empty_tuple = ()
    nested_dict = {SPECIAL_STRING: empty_tuple, empty_tuple: SPECIAL_STRING}
    inner_tuple = (SPECIAL_STRING, nested_dict)
    input_list = [inner_tuple]

    # Execution: Convert the nested list structure to namedtuple
    first_conversion = namedtuple_utils.to_namedtuple(input_list)

    # Apply conversion again to already-converted namedtuple (idempotency check)
    second_conversion = namedtuple_utils.to_namedtuple(first_conversion)

    # Apply conversion a third time to verify stable idempotency
    third_conversion = namedtuple_utils.to_namedtuple(second_conversion)

    # Assertion: Converting an integer should not raise an error
    # (non-convertible types are returned or handled gracefully)
    result_for_integer = namedtuple_utils.to_namedtuple(INTEGER_VALUE)

    # Verify that repeated conversions produce consistent results
    assert second_conversion == third_conversion, (
        "to_namedtuple should be idempotent: applying it twice or three times "
        "should yield the same result"
    )

def test_to_namedtuple_with_dict_having_bytes_keys_and_values():
    """
    Test that to_namedtuple handles a dictionary with bytes keys and values.
    
    Bytes objects cannot be used as valid identifiers for namedtuple attributes,
    so the function should handle this gracefully without raising an exception,
    even though the keys won't become attributes of the resulting namedtuple.
    """
    # Setup: Create a bytes object and a dictionary with bytes as both keys and values.
    # Note: Duplicate keys in the dict literal will result in a single entry.
    BYTES_KEY_AND_VALUE = b"F\xdb\xfdf\x8a\xe4\n\xa2\x1d[\xdc*\xa3\xba\xf6s}"
    dict_with_bytes_keys = {BYTES_KEY_AND_VALUE: BYTES_KEY_AND_VALUE}

    # Execution: Convert the dictionary with bytes keys to a namedtuple.
    result = namedtuple_utils.to_namedtuple(dict_with_bytes_keys)

    # Assertion: Verify the result is a valid namedtuple instance.
    # Since bytes keys are not valid identifiers, the result should be an empty namedtuple.
    assert isinstance(result, tuple)

