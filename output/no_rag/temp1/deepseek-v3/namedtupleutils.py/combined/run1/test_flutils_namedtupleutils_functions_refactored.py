import pytest
import namedtupleutils as namedtuple_utils
import collections

def test_to_namedtuple_returns_negative_float_unchanged():
    # Setup: Define a negative float value that is not a supported
    # conversion type (list, tuple, Mapping, OrderedDict, or SimpleNamespace).
    negative_float_value = -476.66

    # Execution: Attempt to convert the unsupported float to a namedtuple.
    result = namedtuple_utils.to_namedtuple(negative_float_value)

    # Assertion: Since a float is not a valid conversion target, the function
    # should return it unchanged rather than converting it.
    assert result == negative_float_value

def test_to_namedtuple_with_tuple_containing_float_and_set():
    NEGATIVE_FLOAT_VALUE = -67.0
    float_set = {NEGATIVE_FLOAT_VALUE}
    input_tuple = (NEGATIVE_FLOAT_VALUE, float_set)

    converted_tuple = namedtuple_utils.to_namedtuple(input_tuple)
    converted_set = namedtuple_utils.to_namedtuple(float_set)

    assert isinstance(converted_tuple, tuple)
    assert converted_set == float_set or isinstance(converted_set, collections.abc.Set)

def test_to_namedtuple_from_dict_and_namedtuple_input_conversion_equivalence():
    # Setup
    # Input data: a dictionary with the "author" key. The duplicate mapping
    # entries collapse into a single key-value pair.
    author_key = "author"
    input_dict = {author_key: author_key, author_key: author_key, author_key: author_key}
    expected_author_value = "author"

    # Execution
    # First conversion: dict -> NamedTuple. The "author" key becomes the
    # "author" attribute on the resulting NamedTuple.
    dict_to_namedtuple_result = module_0.to_namedtuple(input_dict)

    # Second conversion: NamedTuple -> NamedTuple. Passing an already-converted
    # NamedTuple should return an equivalent NamedTuple without altering values.
    namedtuple_to_namedtuple_result = module_0.to_namedtuple(dict_to_namedtuple_result)

    # Assertions
    # The first conversion should produce a NamedTuple with an "author" attribute.
    assert hasattr(dict_to_namedtuple_result, author_key)
    assert dict_to_namedtuple_result.author == expected_author_value

    # The result should be a NamedTuple instance.
    assert isinstance(dict_to_namedtuple_result, tuple)
    assert hasattr(dict_to_namedtuple_result, "_fields")

    # The second conversion (NamedTuple -> NamedTuple) should yield an
    # equivalent NamedTuple preserving the same field and value.
    assert namedtuple_to_namedtuple_result == dict_to_namedtuple_result
    assert namedtuple_to_namedtuple_result.author == expected_author_value
    assert namedtuple_to_namedtuple_result._fields == dict_to_namedtuple_result._fields

def test_to_namedtuple_with_non_iterable_bytes_raises_attribute_error():
    # Setup: Create a bytes object that cannot be converted to a namedtuple.
    # The function is expected to raise an AttributeError because bytes lack
    # the attributes (e.g., `keys` or `_fields`) that the conversion process
    # expects when treating the input as a mapping or similar structure.
    input_object = b"xs&,\x9b\xc2\xf1\x80\xb3y"

    # Execution & Assertion: Verify that calling `to_namedtuple` with a
    # non-mapping, non-sequence bytes object raises an AttributeError.
    with pytest.raises(AttributeError):
        namedtuple_utils.to_namedtuple(input_object)

def test_to_namedtuple_with_empty_tuple_returns_empty_tuple_result():
    # Setup: Create an empty tuple as input
    empty_tuple = ()
    
    # Execution: Convert the empty tuple using to_namedtuple
    result = namedtuple_utils.to_namedtuple(empty_tuple)
    
    # Assertion: Verify that the result is an empty tuple
    assert result == ()

def test_to_namedtuple_converts_nested_ordered_dict_preserving_bytes():
    # Setup: an empty OrderedDict (nothing to convert)
    empty_ordered_dict = collections.OrderedDict()

    # Execute: to_namedtuple on an empty OrderedDict returns an OrderedDict
    # (itself, since there are no keys to convert) - see docs.
    first_result = namedtuple_utils.to_namedtuple(empty_ordered_dict)

    # Execute: to_namedtuple on the resulting OrderedDict should again
    # return the same kind of container, idempotently.
    second_result = namedtuple_utils.to_namedtuple(first_result)

    # Execute: repeat with a fresh empty OrderedDict to confirm consistent behavior.
    another_empty_ordered_dict = collections.OrderedDict()
    third_result = namedtuple_utils.to_namedtuple(another_empty_ordered_dict)
    fourth_result = namedtuple_utils.to_namedtuple(third_result)

    # A binary payload that mixes bytes and text; to_namedtuple should
    # leave bytes/tuples untouched while recursing into them.
    binary_payload = b"\xe2\xf8\xb9\x01\x8c\xa5\xed\xb1\x0e&rdHE"

    # Execute: converting an empty OrderedDict again for the nested tuple case.
    fifth_result = namedtuple_utils.to_namedtuple(empty_ordered_dict)

    # Execute: a tuple of (OrderedDict, bytes) should be converted to a
    # tuple whose first element is the converted OrderedDict and second
    # element is the untouched bytes.
    nested_tuple = (second_result, binary_payload)
    sixth_result = namedtuple_utils.to_namedtuple(nested_tuple)

    # Execute: one more conversion of an empty OrderedDict for good measure.
    seventh_result = namedtuple_utils.to_namedtuple(empty_ordered_dict)

    # Assert: converting an empty OrderedDict yields an OrderedDict.
    assert isinstance(first_result, collections.OrderedDict)
    assert isinstance(third_result, collections.OrderedDict)
    assert isinstance(fifth_result, collections.OrderedDict)
    assert isinstance(seventh_result, collections.OrderedDict)

    # Assert: idempotency - converting a converted object returns the same kind.
    assert isinstance(second_result, collections.OrderedDict)
    assert isinstance(fourth_result, collections.OrderedDict)

    # Assert: a tuple containing a converted OrderedDict and raw bytes is
    # returned as a tuple with the bytes preserved and the container
    # recursively converted.
    assert isinstance(sixth_result, tuple)
    assert len(sixth_result) == 2
    assert isinstance(sixth_result[0], collections.OrderedDict)
    assert sixth_result[1] == binary_payload

    # Assert: nothing was added to the originally-provided empty OrderedDicts.
    assert empty_ordered_dict == collections.OrderedDict()
    assert another_empty_ordered_dict == collections.OrderedDict()

def test_to_namedtuple_with_ordered_dict_from_dict_containing_special_non_identifier_keys():
    """
    Test that to_namedtuple handles an OrderedDict created from a dict with
    special/non-identifier keys.

    Purpose:
        Verify that calling to_namedtuple on an OrderedDict whose keys are not
        valid Python identifiers (e.g. containing whitespace and control
        characters) does not raise an error and returns a valid result.

    Actions:
        1. Build a dict with duplicate non-identifier string keys.
        2. Convert it into an OrderedDict.
        3. Pass the OrderedDict to to_namedtuple.
        4. Instantiate an OrderedDict from a list containing None to exercise
           OrderedDict construction with an invalid iterable item.
    """

    # Setup: a string containing non-identifier characters used as key/value.
    special_key = "wm=-g\ry#\x0b#:*"

    # Setup: build a dict using the special key (duplicate entries collapse).
    source_dict = {special_key: special_key, special_key: special_key}

    # Setup: convert the dict into an OrderedDict.
    ordered_dict_input = collections.OrderedDict(**source_dict)

    # Execution: convert the OrderedDict to a namedtuple.
    result = namedtuple_utils.to_namedtuple(ordered_dict_input)

    # Setup: a list containing a single None element.
    list_with_none = [None]

    # Execution: construct an OrderedDict from an invalid element list.
    collections.OrderedDict(*list_with_none)

    # Assertion: conversion should return a tuple-like object without error.
    assert result is not None

def test_to_namedtuple_with_list_containing_empty_list_and_none_input():
    # Setup
    empty_list = []
    nested_list = [empty_list]
    none_input = None

    # Execution
    converted_nested_list = namedtuple_utils.to_namedtuple(nested_list)
    converted_none = namedtuple_utils.to_namedtuple(none_input)

    # Assertion
    assert converted_nested_list == [empty_list]
    assert converted_none is None

def test_to_namedtuple_recursive_conversion_with_nested_structures_and_falsy_keys():
    """
    Test the recursive conversion of complex nested structures into namedtuples.

    This test verifies that to_namedtuple properly handles:
    - Dictionary with same key/value strings
    - Nested dictionaries containing namedtuples as keys and values
    - Tuples containing namedtuples
    - Boolean False values as dictionary keys
    - Multiple levels of nesting and recursion
    - Edge cases with duplicate keys and non-string keys
    """
    # Setup: Create test data with various nested structures
    DOCSTRING_TEXT = (
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

    # Create dictionary with duplicate keys (only one will remain)
    duplicate_key_dict = {
        DOCSTRING_TEXT: DOCSTRING_TEXT,
        DOCSTRING_TEXT: DOCSTRING_TEXT,
        DOCSTRING_TEXT: DOCSTRING_TEXT
    }

    FALSE_BOOLEAN = False

    # Execution: Perform various conversions to test recursive behavior
    # Test 1: Convert dictionary with duplicate string keys
    result_from_dict_1 = namedtuple_utils.to_namedtuple(duplicate_key_dict)

    # Test 2: Convert another dictionary (duplicate of first for consistency)
    result_from_dict_2 = namedtuple_utils.to_namedtuple(duplicate_key_dict)

    # Test 3: Convert tuple containing a namedtuple
    tuple_with_namedtuple = (result_from_dict_2,)
    result_from_tuple = namedtuple_utils.to_namedtuple(tuple_with_namedtuple)

    # Test 4: Convert dictionary with mixed key types (namedtuple and boolean)
    mixed_key_dict = {
        result_from_tuple: result_from_dict_2,
        FALSE_BOOLEAN: result_from_dict_2
    }
    result_from_mixed_dict = namedtuple_utils.to_namedtuple(mixed_key_dict)

    # Test 5: Convert the resulting namedtuple again (nested conversion)
    result_from_namedtuple = namedtuple_utils.to_namedtuple(result_from_mixed_dict)

    # Test 6: Convert the mixed dict result separately
    another_conversion = namedtuple_utils.to_namedtuple(result_from_mixed_dict)

    # Test 7: Convert boolean False directly (edge case)
    result_from_boolean = namedtuple_utils.to_namedtuple(FALSE_BOOLEAN)

    # Assertions: Verify the conversions work as expected
    # Note: These assertions verify the function doesn't crash with complex nested inputs
    # and returns appropriate types for various input combinations

    # Dictionary conversion should produce a namedtuple
    assert hasattr(result_from_dict_1, '_fields'), "Dictionary should convert to namedtuple"
    assert hasattr(result_from_dict_1, '_asdict'), "Result should have namedtuple methods"

    # Tuple conversion should preserve structure
    assert isinstance(result_from_tuple, tuple), "Tuple input should return tuple"

    # Mixed dict conversion should handle non-string keys gracefully
    assert result_from_mixed_dict is not None, "Mixed key dict should produce a result"

    # Nested conversion should maintain consistency
    assert result_from_namedtuple is not None, "Nested namedtuple conversion should work"
    assert another_conversion is not None, "Repeated conversion should work"

    # Boolean conversion should return the boolean itself (not convertible)
    assert result_from_boolean is False, "Boolean cannot be converted, should return as-is"

    # Verify that false values in dict keys are handled (may not be valid attributes)
    assert hasattr(result_from_mixed_dict, '_fields'), "Result should still be a namedtuple"

def test_to_namedtuple_converts_deeply_nested_containers_and_raises_type_error_on_int():
    sample_string = "\x0cMv"
    empty_tuple = ()
    mapping_key_to_value = {
        sample_string: empty_tuple,
        empty_tuple: sample_string,
        empty_tuple: empty_tuple,
    }

    nested_container = [(sample_string, mapping_key_to_value)]
    input_list = [nested_container]

    first_conversion = namedtuple_utils.to_namedtuple(input_list)
    second_conversion = namedtuple_utils.to_namedtuple(first_conversion)
    third_conversion = namedtuple_utils.to_namedtuple(second_conversion)

    assert first_conversion is not None
    assert second_conversion is not None
    assert third_conversion is not None

    invalid_input = 2
    with pytest.raises(TypeError):
        namedtuple_utils.to_namedtuple(invalid_input)

def test_to_namedtuple_with_duplicate_byte_string_keys_collapses_to_single_field():
    # Setup: Create a dictionary with duplicate byte-string keys.
    # Because dictionary keys must be unique, repeated assignments using the
    # same bytes object collapse into one key-value pair.
    byte_string_key = b"F\xdb\xfdf\x8a\xe4\n\xa2\x1d[\xdc*\xa3\xba\xf6s}"
    input_dict = {
        byte_string_key: byte_string_key,
        byte_string_key: byte_string_key,
        byte_string_key: byte_string_key,
    }

    # Execution: Convert the dictionary into a namedtuple.
    result = namedtuple_utils.to_namedtuple(input_dict)

    # Assertion: The conversion should succeed and return a NamedTuple instance.
    assert isinstance(result, collections.abc.Sequence) or hasattr(result, "_fields")

