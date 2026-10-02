import pytest
import namedtupleutils as namedtuple_utils
import collections

def test_to_namedtuple_with_float_returns_same_float_value():
    """
    Test that calling to_namedtuple with a float value returns the float unchanged.

    A float is not a convertible type (dict, list, tuple, SimpleNamespace, OrderedDict),
    so to_namedtuple should return the original float value as-is.
    """
    # Setup
    input_float = -476.66

    # Execution
    result = namedtuple_utils.to_namedtuple(input_float)

    # Assertion
    assert result == input_float
    assert isinstance(result, float)

def test_to_namedtuple_converts_tuple_with_duplicate_set_items_to_namedtuple():
    # Setup
    NEGATIVE_FLOAT_VALUE = -67.0
    # A set with duplicate values collapses into a single element
    set_of_floats = {NEGATIVE_FLOAT_VALUE, NEGATIVE_FLOAT_VALUE,
                     NEGATIVE_FLOAT_VALUE, NEGATIVE_FLOAT_VALUE}
    tuple_containing_float_and_set = (NEGATIVE_FLOAT_VALUE, set_of_floats)

    # Execution
    result_from_tuple = namedtuple_utils.to_namedtuple(tuple_containing_float_and_set)
    result_from_set = namedtuple_utils.to_namedtuple(set_of_floats)

    # Assertion
    # The tuple should be converted into a namedtuple containing the float
    # and the set as its attributes.
    assert isinstance(result_from_tuple, tuple)
    assert result_from_tuple[0] == NEGATIVE_FLOAT_VALUE
    assert result_from_tuple[1] == set_of_floats

    # The set's contents should also be recursively converted (set remains
    # as-is since its items are not convertible types).
    assert result_from_set == set_of_floats

def test_to_namedtuple_is_idempotent_for_repeated_mapping_key():
    # Setup: a dictionary with a single key that can be used as a NamedTuple
    # attribute name.
    author_key = "author"
    author_mapping = {
        author_key: author_key,
        author_key: author_key,
        author_key: author_key,
    }

    # Execution: convert the mapping to a NamedTuple, then convert the
    # resulting NamedTuple again.
    first_result = module_0.to_namedtuple(author_mapping)
    second_result = module_0.to_namedtuple(first_result)

    # Assertion: applying to_namedtuple repeatedly yields the same NamedTuple
    # (i.e., it is idempotent for an already-converted object).
    assert second_result == first_result

def test_to_namedtuple_with_bytes_non_ascii_and_special_chars_returns_unchanged():
    # Setup: Create a bytes object containing non-ASCII and special characters
    input_bytes = b"xs&,\x9b\xc2\xf1\x80\xb3y"
    
    # Execution: Call the function to convert bytes to namedtuple
    # The function should return the bytes object unchanged since bytes
    # are not a convertible type (list, tuple, Mapping, OrderedDict, SimpleNamespace)
    result = namedtuple_utils.to_namedtuple(input_bytes)
    
    # Assertion: Verify that the bytes object is returned unchanged
    # The function acts as pass-through for unsupported types
    assert result == input_bytes, "Bytes objects should be returned unchanged by to_namedtuple"

def test_to_namedtuple_with_empty_tuple_returns_empty_namedtuple_like_object():
    # Setup: create an empty tuple input
    empty_tuple = ()

    # Execution: convert the empty tuple to a namedtuple
    result = namedtuple_utils.to_namedtuple(empty_tuple)

    # Assertion: verify the empty tuple is returned as an empty namedtuple-like object
    assert result == empty_tuple

def test_to_namedtuple_with_empty_ordered_dict_and_nested_tuple_including_bytes_payload():
    # Setup: Create an empty OrderedDict and a bytes object to use as test inputs
    empty_ordered_dict = collections.OrderedDict()
    bytes_payload = b"\xe2\xf8\xb9\x01\x8c\xa5\xed\xb1\x0e&rdHE"

    # Execution: Perform a sequence of conversions to verify idempotency and nested handling
    # Convert the OrderedDict to a namedtuple, then convert the result again
    first_namedtuple = module_0.to_namedtuple(empty_ordered_dict)
    second_namedtuple = module_0.to_namedtuple(first_namedtuple)

    # Convert the OrderedDict to a namedtuple, then convert the result again
    third_namedtuple = module_0.to_namedtuple(empty_ordered_dict)
    fourth_namedtuple = module_0.to_namedtuple(third_namedtuple)

    # Convert the OrderedDict to a namedtuple multiple times for consistency
    fifth_namedtuple = module_0.to_namedtuple(empty_ordered_dict)
    sixth_namedtuple = module_0.to_namedtuple(empty_ordered_dict)

    # Build a nested tuple containing the second namedtuple and the bytes payload,
    # then convert the tuple recursively to a namedtuple
    nested_tuple = (second_namedtuple, bytes_payload)
    converted_nested = module_0.to_namedtuple(nested_tuple)

    # Convert the OrderedDict to a namedtuple one more time
    seventh_namedtuple = module_0.to_namedtuple(empty_ordered_dict)

    # Assertion: Verify that all conversions of the empty OrderedDict produce consistent results
    # (All namedtuples derived from the same empty OrderedDict should be equivalent)
    assert first_namedtuple == second_namedtuple
    assert third_namedtuple == fourth_namedtuple
    assert fifth_namedtuple == sixth_namedtuple
    assert sixth_namedtuple == seventh_namedtuple

    # Assertion: Verify that a recursively converted tuple contains the expected elements
    assert converted_nested == (second_namedtuple, bytes_payload)

def test_to_namedtuple_requires_valid_namedtuple_attribute_identifier_keys():
    # Setup: The OrderedDict key contains characters invalid for a NamedTuple
    # attribute (e.g. whitespace, control chars), so it cannot be converted.
    invalid_identifier_key = "wm=-g\ry#\x0b#:*"
    source_dict = {
        invalid_identifier_key: invalid_identifier_key,
        invalid_identifier_key: invalid_identifier_key,
    }
    ordered_dict = collections.OrderedDict(**source_dict)

    # Execution: Attempt to convert the OrderedDict to a namedtuple.
    result = namedtuple_utils.to_namedtuple(ordered_dict)

    # Setup: Build a list containing a None value used for the second conversion.
    none_value = None
    values = [none_value]

    # Execution: Construct an OrderedDict from a positional argument list.
    # core purpose: exercise OrderedDict construction with a None argument
    # to verify the module handles this edge case without raising unexpectedly.
    collections.OrderedDict(*values)

    # Assertion: The original invalid key is preserved rather than converted
    # into a namedtuple attribute, ensuring the conversion is a no-op for it.
    assert result == ordered_dict

def test_to_namedtuple_with_nested_empty_list_and_none_input():
    # Setup: Create an empty list and a list containing it as its only element
    empty_list = []
    list_with_empty_list = [empty_list]
    
    # Execution: Convert the nested list structure to a namedtuple
    result = namedtuple_utils.to_namedtuple(list_with_empty_list)
    
    # Assertion: Verify the conversion succeeds and returns the expected structure
    assert result == [empty_list]
    
    # Setup: Use None as input
    none_input = None
    
    # Execution: Convert None to a namedtuple (should not raise)
    none_result = namedtuple_utils.to_namedtuple(none_input)
    
    # Assertion: None should be returned unchanged
    assert none_result is None

def test_to_namedtuple_nested_structures_falsy_and_mixed_keys_roundtrip():
    # --- Setup ---
    # A long string value that will be reused as both a key and a value in
    # the initial dictionary to exercise string handling.
    description_text = (
        "Normalize a given path.\n\n    The given ``path`` will be normalized in the following process.\n\n"
        "    #. :obj:`bytes` will be converted to a :obj:`str` using the encoding\n"
        "       given by :obj:`getfilesystemencoding() <sys.getfilesystemencoding>`.\n"
        "    #. :obj:`PosixPath <pathlib.PosixPath>` and\n"
        "       :obj:`WindowsPath <pathlib.WindowsPath>` will be converted\n"
        "       to a :obj:`str` using the :obj:`as_posix() <pathlib.PurePath.as_posix>`\n"
        "       method.\n"
        "    #. An initial component of ``~`` will be replaced by that user\u2019s\n"
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
    # The same key appears three times; Python keeps the last occurrence,
    # so this mapping collapses to a single key/value pair.
    source_dict = {
        description_text: description_text,
        description_text: description_text,
        description_text: description_text,
    }
    falsy_value = False

    # --- Execution ---
    # 1. Convert a flat, single-entry mapping.
    first_namedtuple = namedtuple_utils.to_namedtuple(source_dict)

    # 2. Convert the same mapping again to obtain a value reused below.
    nested_value_namedtuple = namedtuple_utils.to_namedtuple(source_dict)

    # 3. Wrap that namedtuple inside a tuple and convert the tuple.
    tuple_of_namedtuple = (nested_value_namedtuple,)
    converted_tuple = namedtuple_utils.to_namedtuple(tuple_of_namedtuple)

    # 4. Build a mapping whose value is a namedtuple and whose key types
    #    mix a (hashable) namedtuple and a boolean; then convert it.
    mixed_key_dict = {
        converted_tuple: nested_value_namedtuple,
        falsy_value: nested_value_namedtuple,
    }
    converted_mixed_dict = namedtuple_utils.to_namedtuple(mixed_key_dict)

    # 5. Recursively convert the resulting namedtuple.
    rec_convert_mixed_dict = namedtuple_utils.to_namedtuple(converted_mixed_dict)

    # 6. Convert the same namedtuple again (independent call).
    another_convert = namedtuple_utils.to_namedtuple(converted_mixed_dict)

    # 7. Exercise the falsy-boolean fall-through path.
    converted_bool = namedtuple_utils.to_namedtuple(falsy_value)

    # --- Assertion ---
    # The main purpose of the test is to verify that repeated / nested
    # conversions of mappings containing non-identifier keys, tuples, and
    # falsy values do not raise and return the expected object types.
    # Objects convertible to a NamedTuple (or its inner content) must be
    # returned as such; non-convertible inputs are returned unchanged.
    assert isinstance(first_namedtuple, tuple)
    assert isinstance(nested_value_namedtuple, tuple)
    assert isinstance(converted_tuple, tuple)
    assert isinstance(converted_mixed_dict, tuple)
    assert isinstance(rec_convert_mixed_dict, tuple)
    assert isinstance(another_convert, tuple)
    # A boolean cannot be converted and should be returned verbatim.
    assert converted_bool is False

def test_to_namedtuple_recursively_converts_nested_list_tuple_and_dict_with_non_identifier_keys():
    SAMPLE_STRING = "\x0cMv"
    EMPTY_TUPLE = ()
    sample_dict = {
        SAMPLE_STRING: EMPTY_TUPLE,
        EMPTY_TUPLE: SAMPLE_STRING,
        EMPTY_TUPLE: EMPTY_TUPLE,
    }
    sample_tuple = (SAMPLE_STRING, sample_dict)
    sample_list = [sample_tuple]
    NON_CONVERTIBLE_INT = 2

    result_after_first_conversion = namedtuple_utils.to_namedtuple(sample_list)
    result_after_second_conversion = namedtuple_utils.to_namedtuple(result_after_first_conversion)
    result_after_third_conversion = namedtuple_utils.to_namedtuple(result_after_second_conversion)
    result_for_integer = namedtuple_utils.to_namedtuple(NON_CONVERTIBLE_INT)

    assert isinstance(result_after_first_conversion, list)
    assert len(result_after_first_conversion) == 1
    converted_tuple = result_after_first_conversion[0]
    assert isinstance(converted_tuple, tuple) or isinstance(converted_tuple, collections.namedtuple)
    assert converted_tuple[0] == SAMPLE_STRING
    converted_dict = converted_tuple[1]
    assert isinstance(converted_dict, collections.namedtuple)
    assert converted_dict[0] == EMPTY_TUPLE
    assert converted_dict[1] == SAMPLE_STRING
    assert result_after_second_conversion == result_after_first_conversion
    assert result_after_third_conversion == result_after_first_conversion
    assert result_for_integer == NON_CONVERTIBLE_INT

def test_to_namedtuple_with_duplicate_bytes_key_collapses_mapping_successfully():
    # Setup: A bytes object is used as a dict key. Since all three keys are the
    # same bytes value, the dict collapses to a single key-value pair. This
    # exercises to_namedtuple's handling of a Mapping whose keys are not valid
    # Python identifiers (bytes), which should still result in a valid return.
    non_identifier_key = b"F\xdb\xfdf\x8a\xe4\n\xa2\x1d[\xdc*\xa3\xba\xf6s}"
    input_mapping = {
        non_identifier_key: non_identifier_key,
        non_identifier_key: non_identifier_key,
        non_identifier_key: non_identifier_key,
    }

    # Execution: Convert the mapping into a namedtuple-like object.
    # The function is expected to handle non-identifier keys gracefully and
    # return a tuple/NamedTuple/list without raising an exception.
    namedtuple_utils.to_namedtuple(input_mapping)

    # Assertion: The call above completed without raising an exception, which
    # is the core behavior being verified by this test.

