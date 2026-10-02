import pytest

import namedtupleutils as namedtuple_utils
import collections as collections_module

def test_to_namedtuple_returns_primitive_float_unchanged():
    """
    Verify that to_namedtuple does not convert a primitive float into a namedtuple
    or any other collection; it should return the original float value.
    """
    # Arrange: representative negative float value
    NEGATIVE_FLOAT = -476.66

    # Act: call the function under test
    result = namedtuple_utils.to_namedtuple(NEGATIVE_FLOAT)

    # Assert: value and type are preserved
    assert result == NEGATIVE_FLOAT
    assert isinstance(result, float)

def test_to_namedtuple_converts_tuple_containing_number_and_singleton_set():
    """to_namedtuple should accept a tuple with a numeric and a singleton set,
    returning a tuple that preserves both elements, and converting the set
    directly should not raise and should return an equivalent object.
    """
    # Setup
    FLOAT_VALUE = -67.0
    SINGLETON_SET = {FLOAT_VALUE}
    INPUT_TUPLE = (FLOAT_VALUE, SINGLETON_SET)

    # Execution
    result_tuple = namedtuple_utils.to_namedtuple(INPUT_TUPLE)
    result_from_set = namedtuple_utils.to_namedtuple(SINGLETON_SET)

    # Assertions
    assert isinstance(result_tuple, tuple)
    assert result_tuple[0] == FLOAT_VALUE
    assert result_tuple[1] == SINGLETON_SET
    assert result_from_set == SINGLETON_SET

def test_to_namedtuple_converts_simple_dict_and_is_idempotent():
    # Purpose:
    # - Verify that a simple dict with a valid identifier key is converted into a namedtuple
    # - Verify that calling to_namedtuple on an already-converted namedtuple is idempotent
    #
    # Setup: define constants and input dictionary
    KEY = "author"
    VALUE = "author"
    input_mapping = {KEY: VALUE}

    # Execution: convert dict -> namedtuple, then convert the result again
    first_namedtuple = namedtuple_utils.to_namedtuple(input_mapping)
    second_namedtuple = namedtuple_utils.to_namedtuple(first_namedtuple)

    # Assertions:
    # - The first result should be a namedtuple-like object: tuple-subclass with _fields
    # - It should expose the original key as an attribute with the original value
    # - Calling to_namedtuple again should return an equivalent object (idempotency)
    assert isinstance(first_namedtuple, tuple), "Expected a tuple-subclass (namedtuple) result"
    assert hasattr(first_namedtuple, "_fields") and KEY in first_namedtuple._fields, "Expected namedtuple to have the 'author' field"
    assert getattr(first_namedtuple, KEY) == VALUE

    # second conversion should produce an equivalent namedtuple (no change)
    assert isinstance(second_namedtuple, tuple)
    assert getattr(second_namedtuple, KEY) == VALUE
    assert second_namedtuple == first_namedtuple

def test_to_namedtuple_with_bytes_returns_original_bytes():
    # Purpose:
    # Ensure that to_namedtuple can accept raw bytes input and that it does not
    # attempt to convert bytes into a NamedTuple or Mapping — it should return
    # the original bytes (or an equivalent bytes-like object) unchanged.
    #
    # Setup: define a representative bytes object used as input.
    SAMPLE_BYTES = b"xs&,\x9b\xc2\xf1\x80\xb3y"
    input_bytes = SAMPLE_BYTES

    # Execution: call the conversion function under test.
    result = namedtuple_utils.to_namedtuple(input_bytes)

    # Assertions:
    # - The result should be a bytes-like object and equal to the original input.
    # - The result should not be treated as a Mapping/Mapping-like object.
    assert isinstance(result, (bytes, bytearray)), "Expected a bytes-like result"
    assert result == SAMPLE_BYTES, "Expected the bytes value to remain unchanged"
    assert not isinstance(result, collections_module.abc.Mapping), (
        "Bytes should not be converted into a Mapping/NamedTuple"
    )

def test_to_namedtuple_with_empty_tuple_returns_empty_tuple():
    """
    Verify that to_namedtuple returns an empty tuple unchanged when given an empty tuple.
    This ensures tuple inputs are preserved and that conversion recursion does not alter empty sequences.
    """
    # Setup
    EMPTY_TUPLE = ()

    # Execution
    result = namedtuple_utils.to_namedtuple(EMPTY_TUPLE)

    # Assertions
    assert isinstance(result, tuple), "Expected a tuple result for tuple input"
    assert result == EMPTY_TUPLE, "Expected the empty tuple to be returned unchanged"
    assert len(result) == 0, "Resulting tuple should be empty"

def test_to_namedtuple_multiple_conversions_empty_ordered_dict_and_tuple():
    # Purpose:
    # Verify that to_namedtuple correctly handles repeated conversions of an
    # empty OrderedDict, returns a namedtuple-like object (with no fields),
    # and that converting a tuple containing such a namedtuple and raw bytes
    # preserves the bytes and keeps the namedtuple-like object in the tuple.

    # Constants / Setup
    EMPTY_ORDERED_DICT = collections_module.OrderedDict()
    SAMPLE_BYTES = b"\xe2\xf8\xb9\x01\x8c\xa5\xed\xb1\x0e&rdHE"

    # Execution: perform several conversions to exercise idempotence and
    # repeated conversions on the same input type
    namedtuple_from_ordered = namedtuple_utils.to_namedtuple(EMPTY_ORDERED_DICT)
    namedtuple_from_namedtuple = namedtuple_utils.to_namedtuple(namedtuple_from_ordered)
    namedtuple_from_ordered_again = namedtuple_utils.to_namedtuple(EMPTY_ORDERED_DICT)
    namedtuple_from_ordered_twice = namedtuple_utils.to_namedtuple(namedtuple_from_ordered_again)
    namedtuple_from_ordered_thrice = namedtuple_utils.to_namedtuple(EMPTY_ORDERED_DICT)

    # Convert a tuple containing the previously obtained namedtuple-like object
    tuple_input = (namedtuple_from_namedtuple, SAMPLE_BYTES)
    converted_tuple = namedtuple_utils.to_namedtuple(tuple_input)

    # Final conversion of the ordered dict again to ensure repeated calls remain consistent
    final_namedtuple = namedtuple_utils.to_namedtuple(EMPTY_ORDERED_DICT)

    # Assertions:
    # The conversions of an empty OrderedDict should yield namedtuple-like objects.
    # Namedtuple-like objects are instances of tuple and expose the _fields attribute.
    for nt in (
        namedtuple_from_ordered,
        namedtuple_from_namedtuple,
        namedtuple_from_ordered_again,
        namedtuple_from_ordered_twice,
        namedtuple_from_ordered_thrice,
        final_namedtuple,
    ):
        assert isinstance(nt, tuple), "Expected a tuple-like namedtuple result"
        assert hasattr(nt, "_fields"), "Expected namedtuple-like object to have _fields attribute"
        # Empty OrderedDict -> no fields on the resulting namedtuple
        assert nt._fields == (), "Expected no fields for an empty OrderedDict conversion"

    # The tuple conversion should return a tuple where:
    # - the first element is the namedtuple-like object (with empty fields)
    # - the second element is the original bytes object (preserved)
    assert isinstance(converted_tuple, tuple)
    assert converted_tuple[0]._fields == ()
    assert converted_tuple[1] is SAMPLE_BYTES

def test_to_namedtuple_handles_ordered_dict_with_non_identifier_keys_and_constructor_errors():
    # Constants / setup data
    INVALID_KEY = "wm=-g\ry#\x0b#:*"
    INVALID_MAPPING = {INVALID_KEY: INVALID_KEY}

    # 1) Creating an OrderedDict via kwargs with a non-identifier key should raise
    #    a TypeError because keyword argument names must be valid identifiers.
    with pytest.raises(TypeError):
        collections_module.OrderedDict(**INVALID_MAPPING)

    # 2) Creating an OrderedDict from an iterable of pairs containing the same
    #    non-identifier key should succeed (use the iterable constructor).
    ordered_with_invalid_key = collections_module.OrderedDict([(INVALID_KEY, INVALID_KEY)])

    # Execution: convert the OrderedDict to a namedtuple-like structure
    namedtuple_result = namedtuple_utils.to_namedtuple(ordered_with_invalid_key)

    # Assertion: the conversion should return a tuple-like object (namedtuple is a tuple subclass)
    assert isinstance(namedtuple_result, tuple)

    # 3) Passing a non-iterable positional argument (None) to OrderedDict constructor
    #    should raise a TypeError because OrderedDict expects a mapping or iterable of pairs.
    with pytest.raises(TypeError):
        collections_module.OrderedDict(None)

def test_to_namedtuple_converts_list_containing_empty_list_and_handles_none():
    # Purpose:
    # - Verify that to_namedtuple returns a new list when given a list,
    #   and that inner lists are also converted (returned as new lists).
    # - Verify that passing None to to_namedtuple returns None unchanged.
    
    # Constants / setup
    ORIGINAL_INNER_LIST = []  # an empty list to be nested
    INPUT_LIST = [ORIGINAL_INNER_LIST]  # top-level list containing the empty list
    
    # Execution: convert the nested list and convert None
    converted_list = namedtuple_utils.to_namedtuple(INPUT_LIST)
    converted_none = namedtuple_utils.to_namedtuple(None)
    
    # Assertions:
    # - The top-level return should be a list equal in value to the input,
    #   but it must be a different object (a new list as documented).
    assert isinstance(converted_list, list)
    assert converted_list == INPUT_LIST
    assert converted_list is not INPUT_LIST
    
    # - The inner list should also be a new list (not the same object as the original inner list).
    assert isinstance(converted_list[0], list)
    assert converted_list[0] == ORIGINAL_INNER_LIST
    assert converted_list[0] is not ORIGINAL_INNER_LIST
    
    # - Passing None should return None (unchanged)
    assert converted_none is None

def test_to_namedtuple_with_mixed_keys_and_nested_structures():
    # Purpose:
    # Verify that to_namedtuple can be called on dictionaries, tuples and booleans
    # in various nested combinations without raising, that tuple conversion
    # preserves tuple semantics and that repeated conversions preserve type
    # / equality where reasonable.

    # Setup: prepare a complex string key and simple structures that will be reused
    DOCSTRING = (
        "Normalize a given path.\n\n"
        "    The given ``path`` will be normalized in the following process.\n\n"
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
        "        PosixPath('/home/test_user/tmp/bar')\n"
    )

    # A dictionary using the DOCSTRING as key and value (duplicate keys in a literal
    # will collapse to a single entry, but that models real input where keys may be
    # non-identifier strings).
    simple_dict = {DOCSTRING: DOCSTRING}

    # Execution: perform a series of conversions similar to the original test flow
    named_from_dict_first = namedtuple_utils.to_namedtuple(simple_dict)
    named_from_dict_second = namedtuple_utils.to_namedtuple(simple_dict)

    # Wrap the namedtuple result in a tuple and convert that tuple
    tuple_containing_named = (named_from_dict_second,)
    converted_tuple = namedtuple_utils.to_namedtuple(tuple_containing_named)

    # Use the converted tuple and a boolean key to build a new dict and convert it
    complex_dict = {converted_tuple: named_from_dict_second, False: named_from_dict_second}
    named_from_complex = namedtuple_utils.to_namedtuple(complex_dict)

    # Convert the result of a conversion again to ensure idempotence / stability
    named_from_named = namedtuple_utils.to_namedtuple(named_from_complex)
    another_named_from_complex = namedtuple_utils.to_namedtuple(named_from_complex)

    # Convert a plain boolean to verify simple, non-container values are handled
    bool_result = namedtuple_utils.to_namedtuple(False)

    # Assertions:
    # - Repeated conversion of the same dict yields the same type
    assert type(named_from_dict_first) == type(named_from_dict_second)

    # - Converting a tuple returns a tuple, and its first element matches the original namedtuple
    assert isinstance(converted_tuple, tuple)
    assert converted_tuple[0] == named_from_dict_second

    # - Converting the complex dict is stable across repeated conversions (type-stability)
    assert type(named_from_complex) == type(named_from_named) == type(another_named_from_complex)

    # - Converting a boolean returns the boolean unchanged
    assert bool_result is False

def test_to_namedtuple_idempotence_for_list_with_nested_mapping_and_int():
    # Purpose:
    # Verify that to_namedtuple can handle a list containing a tuple that itself
    # contains a string and a mapping with non-identifier keys, and that repeated
    # conversions are idempotent. Also verify that primitive types (int) are
    # returned unchanged.
    #
    # Setup: construct an input list with:
    #  - a control-character-containing string (not a valid identifier)
    #  - a dict whose keys are non-identifiers (a string with control char and an empty tuple)
    CONTROL_STRING = "\x0cMv"
    EMPTY_TUPLE = ()
    MIXED_DICT = {CONTROL_STRING: EMPTY_TUPLE, EMPTY_TUPLE: EMPTY_TUPLE}
    NESTED_TUPLE = (CONTROL_STRING, MIXED_DICT)
    INPUT_LIST = [NESTED_TUPLE]
    INTEGER_VALUE = 2

    # Execution: apply to_namedtuple multiple times to exercise recursive conversion
    first_conversion = namedtuple_utils.to_namedtuple(INPUT_LIST)
    second_conversion = namedtuple_utils.to_namedtuple(first_conversion)
    third_conversion = namedtuple_utils.to_namedtuple(second_conversion)
    int_conversion = namedtuple_utils.to_namedtuple(INTEGER_VALUE)

    # Assertions:
    # - Converting a list returns a list
    # - Re-applying to_namedtuple does not change the result (idempotence)
    # - Primitive types like int are returned unchanged
    assert isinstance(first_conversion, list)
    assert second_conversion == first_conversion
    assert third_conversion == first_conversion

    assert int_conversion == INTEGER_VALUE
    assert isinstance(int_conversion, int)

    # Sanity checks for nested structure: the outer list and inner tuple lengths are preserved
    assert len(first_conversion) == 1
    assert len(first_conversion[0]) == 2

def test_to_namedtuple_handles_non_identifier_bytes_keys_returns_sequence():
    # Purpose:
    # Verify that to_namedtuple can be called with a mapping that uses non-identifier
    # keys (bytes) and that the call completes without error and returns a sequence-like
    # result (either a list or a tuple / namedtuple).

    # Constants / test data
    BYTE_KEY = b"F\xdb\xfdf\x8a\xe4\n\xa2\x1d[\xdc*\xa3\xba\xf6s}"
    BYTE_VALUE = BYTE_KEY  # use the same bytes object for key and value (mirrors original test)

    # --- Setup ---
    # Create the input mapping. Repeating the same key in a literal would collapse to one entry,
    # so a single-entry dict represents the effective input from the original test.
    input_mapping = {BYTE_KEY: BYTE_VALUE}

    # Keep a copy to assert the function does not mutate the input mapping.
    original_mapping_copy = dict(input_mapping)

    # --- Execution ---
    result = namedtuple_utils.to_namedtuple(input_mapping)

    # --- Assertions ---
    # The call should return either a list or a tuple (namedtuple is a tuple subclass).
    assert isinstance(result, (list, tuple)), "to_namedtuple should return a list or tuple-like object"

    # Ensure the input mapping was not modified by the conversion.
    assert input_mapping == original_mapping_copy, "to_namedtuple should not mutate the input mapping"

