import pytest

import collections as collections_module
import namedtupleutils as namedtuple_utils

def test_to_namedtuple_returns_primitive_float_unchanged():
    """Verify that to_namedtuple does not convert a primitive float into a NamedTuple."""
    # Arrange
    float_input = -476.66  # a primitive numeric value

    # Act
    result = namedtuple_utils.to_namedtuple(float_input)

    # Assert
    assert result == float_input
    assert isinstance(result, float)

def test_to_namedtuple_preserves_tuple_and_set_contents(module_0):
    """
    Verify that to_namedtuple preserves scalar values inside tuples and
    converts iterable containers (like sets) into an iterable result
    whose contents match the original container.
    """
    # Setup
    FLOAT_VALUE = -67.0
    original_set = {FLOAT_VALUE}
    original_tuple = (FLOAT_VALUE, original_set)
    nt = module_0

    # Execution
    converted_tuple = nt.to_namedtuple(original_tuple)
    converted_from_set = nt.to_namedtuple(original_set)

    # Assertions
    assert isinstance(converted_tuple, tuple), "Expected tuple input to produce a tuple"
    assert converted_tuple[0] == FLOAT_VALUE, "Scalar value inside tuple was not preserved"

    second_element = converted_tuple[1]
    assert isinstance(second_element, (list, tuple)), "Expected converted set inside tuple to be a list/tuple"
    assert set(second_element) == original_set, "Contents of converted iterable do not match original set"

    assert isinstance(converted_from_set, (list, tuple)), "Expected direct set conversion to return list/tuple"
    assert set(converted_from_set) == original_set, "Converted set contents do not match original set"

def test_to_namedtuple_is_idempotent_for_simple_dict():
    # Verify a simple dict with a valid identifier key converts to a namedtuple
    # and that converting the resulting namedtuple again is idempotent.
    key = "author"
    value = "author"
    simple_dict = {key: value}

    # First conversion: dict -> namedtuple
    first_converted = namedtuple_utils.to_namedtuple(simple_dict)

    # Second conversion: apply to_namedtuple to the already converted namedtuple
    second_converted = namedtuple_utils.to_namedtuple(first_converted)

    # The first conversion should produce a namedtuple-like object
    assert isinstance(first_converted, tuple), "Expected a tuple subclass (namedtuple) from conversion"
    assert hasattr(first_converted, "_fields"), "Expected the converted object to have _fields (namedtuple)"
    assert first_converted._fields == (key,), "Expected a single field named as the dict key"

    # The namedtuple should expose the original value as an attribute
    assert getattr(first_converted, key) == value

    # Re-converting an already converted namedtuple should yield an equivalent namedtuple
    assert second_converted == first_converted, "Expected second conversion to be equal to the first"
    assert type(second_converted) is type(first_converted), "Expected the same namedtuple type after re-conversion"

def test_to_namedtuple_returns_bytes_unchanged():
    # Verify that to_namedtuple does not alter plain bytes input and returns
    # a bytes object equal to the original (ensures no exception and no conversion).
    SAMPLE_BYTES = b"xs&,\x9b\xc2\xf1\x80\xb3y"

    input_value = SAMPLE_BYTES
    result = namedtuple_utils.to_namedtuple(input_value)

    assert isinstance(result, bytes)
    assert result == SAMPLE_BYTES

def test_to_namedtuple_with_empty_tuple_returns_empty_tuple():
    # Purpose: Ensure passing an empty tuple returns an empty tuple and type is tuple
    EMPTY_TUPLE = ()
    input_tuple = EMPTY_TUPLE

    result = namedtuple_utils.to_namedtuple(input_tuple)

    assert result == EMPTY_TUPLE
    assert isinstance(result, tuple)

def test_to_namedtuple_nested_empty_ordereddict_and_bytes_conversion():
    # Purpose:
    # Verify that to_namedtuple correctly converts an empty OrderedDict into
    # a namedtuple-like object (empty fields), that repeated conversions are
    # idempotent, and that nested structures (tuple containing a namedtuple and
    # raw bytes) are converted appropriately (preserving bytes and converting
    # nested namedtuple elements).

    # Constants / setup
    EMPTY_ORDERED_DICT = collections_module.OrderedDict()
    SAMPLE_BYTES = b"\xe2\xf8\xb9\x01\x8c\xa5\xed\xb1\x0e&rdHE"

    # Execution: perform several conversions to check idempotency and nested conversion
    converted_empty_once = namedtuple_utils.to_namedtuple(EMPTY_ORDERED_DICT)
    converted_empty_twice = namedtuple_utils.to_namedtuple(converted_empty_once)
    converted_empty_again = namedtuple_utils.to_namedtuple(EMPTY_ORDERED_DICT)

    nested_input = (converted_empty_twice, SAMPLE_BYTES)
    converted_nested = namedtuple_utils.to_namedtuple(nested_input)

    converted_empty_thrice = namedtuple_utils.to_namedtuple(EMPTY_ORDERED_DICT)

    # Assertions

    # The conversion of an empty OrderedDict should produce a namedtuple-like object:
    # - It should be a tuple (namedtuple instances subclass tuple)
    # - It should expose _fields (empty tuple for no keys)
    assert isinstance(converted_empty_once, tuple)
    assert getattr(converted_empty_once, "_fields", None) == ()

    # Repeated conversions of the same object or source should be idempotent (value-equal)
    assert converted_empty_once == converted_empty_twice
    assert converted_empty_once == converted_empty_again
    assert converted_empty_once == converted_empty_thrice

    # The nested conversion should return a tuple of length 2:
    # - First element should be the converted namedtuple (same as converted_empty_twice)
    # - Second element should remain the original bytes object
    assert isinstance(converted_nested, tuple)
    assert len(converted_nested) == 2
    assert getattr(converted_nested[0], "_fields", None) == ()
    assert converted_nested[0] == converted_empty_twice
    assert converted_nested[1] == SAMPLE_BYTES

def test_to_namedtuple_from_ordereddict_and_ordereddict_positional_none_raises():
    """
    Verify that:
    - namedtuple_utils.to_namedtuple converts an OrderedDict into a namedtuple-like object
      (a tuple subclass exposing _fields) and preserves the number of items and values.
    - Constructing an OrderedDict with a single positional None argument raises TypeError.
    """
    SAMPLE_KEY = "wm=-g\ry#\x0b#:*"
    SAMPLE_VALUE = SAMPLE_KEY
    SAMPLE_MAPPING = {SAMPLE_KEY: SAMPLE_VALUE}

    # Create an OrderedDict from a mapping (use positional mapping constructor).
    ordered = collections_module.OrderedDict(SAMPLE_MAPPING)

    # Convert the OrderedDict to a namedtuple-like object.
    namedtuple_result = namedtuple_utils.to_namedtuple(ordered)

    # The result should be a tuple-like namedtuple with _fields matching the OrderedDict keys.
    assert isinstance(namedtuple_result, tuple), "to_namedtuple should return a tuple-like object"
    assert hasattr(namedtuple_result, "_fields"), "returned object should expose _fields like a namedtuple"
    assert len(namedtuple_result._fields) == len(ordered), "number of namedtuple fields should match OrderedDict keys"

    # Ensure the value was preserved for the single field that was created.
    first_field_name = namedtuple_result._fields[0]
    assert getattr(namedtuple_result, first_field_name) == SAMPLE_VALUE

    # Constructing an OrderedDict with a positional None should raise TypeError.
    with pytest.raises(TypeError):
        collections_module.OrderedDict(None)

def test_to_namedtuple_creates_new_list_and_preserves_unconvertible_items_and_none_returns_none():
    # Purpose:
    # Verify that to_namedtuple returns a new list when given a list input,
    # preserves items that cannot be converted (by identity), and returns
    # None unchanged when given None.
    
    # --- Setup ---
    EMPTY_INNER_LIST = []                       # an item that cannot be converted to a namedtuple
    input_list = [EMPTY_INNER_LIST]             # list containing the unconvertible item
    NONE_INPUT = None
    
    # --- Execution ---
    result_list = namedtuple_utils.to_namedtuple(input_list)
    result_for_none = namedtuple_utils.to_namedtuple(NONE_INPUT)
    
    # --- Assertions ---
    # The returned list must be a new list object (original list is not mutated)
    assert result_list is not input_list
    # The inner unconvertible item should be preserved (same identity)
    assert result_list[0] is EMPTY_INNER_LIST
    # Passing None should return None (no conversion / no exception)
    assert result_for_none is None

def test_to_namedtuple_handles_various_nested_inputs_without_raising():
    # Purpose:
    # Verify that namedtuple_utils.to_namedtuple can be called on a variety of
    # nested and mixed inputs (mapping with complex string keys, tuples
    # containing namedtuples, mappings with non-string/hashable keys and
    # boolean values) and returns expected Python container/NamedTuple types
    # (i.e. does not raise and preserves convertible structure).

    # Constants / Setup data
    LONG_DOCSTRING = (
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
        "\n"
    )

    # Create a dict using the long (non-identifier) string as the key.
    # Note: duplicate keys in a literal dict collapse to one entry; this still
    # tests behavior with a complex key.
    mapping_with_long_string_key = {LONG_DOCSTRING: LONG_DOCSTRING}

    # Execution: convert mapping to a namedtuple-like object
    namedtuple_from_long_key = namedtuple_utils.to_namedtuple(mapping_with_long_string_key)

    # Assertion: mapping input should produce a NamedTuple-like object (has _fields)
    assert hasattr(namedtuple_from_long_key, "_fields"), (
        "Expected a NamedTuple-like result (mapping inputs should become NamedTuple)."
    )

    # Execution: convert a tuple that contains the previously produced namedtuple
    tuple_with_namedtuple = (namedtuple_from_long_key,)
    converted_tuple = namedtuple_utils.to_namedtuple(tuple_with_namedtuple)

    # Assertion: tuple input should return a tuple and its element should still
    # be a NamedTuple-like object after conversion
    assert isinstance(converted_tuple, tuple), "Expected tuple input to return a tuple."
    assert hasattr(converted_tuple[0], "_fields"), "Element inside converted tuple should be NamedTuple-like."

    # Setup: build a mapping that uses a tuple (hashable) as a key and a boolean as another key
    bool_key = False
    mapping_with_mixed_keys = {converted_tuple: namedtuple_from_long_key, bool_key: namedtuple_from_long_key}

    # Execution: convert the mixed-key mapping
    namedtuple_from_mixed = namedtuple_utils.to_namedtuple(mapping_with_mixed_keys)

    # Assertion: mapping input should again produce a NamedTuple-like object
    assert hasattr(namedtuple_from_mixed, "_fields"), (
        "Expected NamedTuple-like result from mapping with mixed keys."
    )

    # Execution: convert an already-converted NamedTuple-like object (idempotency / safe conversion)
    namedtuple_double_converted = namedtuple_utils.to_namedtuple(namedtuple_from_mixed)

    # Assertion: converting a NamedTuple-like object should yield a NamedTuple-like result (or preserve)
    assert hasattr(namedtuple_double_converted, "_fields"), (
        "Converting an already-NamedTuple-like object should still yield a NamedTuple-like result."
    )

    # Execution + Assertion: converting a plain boolean should return it unchanged
    returned_bool = namedtuple_utils.to_namedtuple(bool_key)
    assert returned_bool is False, "Expected boolean input to be returned unchanged by to_namedtuple."

def test_to_namedtuple_handles_nested_structures_and_is_idempotent():
    # Purpose:
    # - Ensure to_namedtuple can handle a list containing a tuple with a string and a dict.
    # - Ensure the dict inside the tuple is converted into a namedtuple-like object
    #   (i.e., a tuple subclass with a `_fields` attribute).
    # - Ensure repeated conversions are idempotent (calling to_namedtuple on an already
    #   converted object does not change it).
    # - Ensure non-container scalar types (int) are returned as-is.

    # --- Setup ---
    CONTROL_STRING = "\x0cMv"            # a string that is unlikely to be a valid identifier
    EMPTY_TUPLE = ()                      # used as a value and as a key in the dict
    # Create a dict with keys that are not valid identifier names (so they should not
    # become namedtuple fields); also demonstrate a non-string key (tuple).
    sample_dict = {CONTROL_STRING: EMPTY_TUPLE, EMPTY_TUPLE: EMPTY_TUPLE}
    # A list containing a tuple (string, dict) to exercise recursive conversion
    nested_input = [(CONTROL_STRING, sample_dict)]

    # --- Execution ---
    first_conversion = namedtuple_utils.to_namedtuple(nested_input)
    second_conversion = namedtuple_utils.to_namedtuple(first_conversion)
    third_conversion = namedtuple_utils.to_namedtuple(second_conversion)
    int_conversion = namedtuple_utils.to_namedtuple(2)

    # --- Assertions ---
    # The outer structure for a list input should still be a list
    assert isinstance(first_conversion, list)
    assert len(first_conversion) == 1

    # The first (and only) element should be a tuple (original tuple preserved, but with
    # its dict element converted)
    first_element = first_conversion[0]
    assert isinstance(first_element, tuple)
    assert len(first_element) == 2

    # The second item of the tuple was a dict and should be converted to a namedtuple-like
    # object: a tuple subclass with a `_fields` attribute.
    converted_inner = first_element[1]
    assert isinstance(converted_inner, tuple)
    assert hasattr(converted_inner, "_fields")
    # `_fields` should be a tuple (possibly empty if no dict keys were valid identifiers)
    assert isinstance(converted_inner._fields, tuple)

    # Repeated conversions should be idempotent (structure and contents remain equal)
    assert second_conversion == first_conversion
    assert third_conversion == second_conversion

    # Scalars (like ints) should be returned unchanged
    assert int_conversion == 2

def test_to_namedtuple_accepts_dict_with_bytes_keys_without_raising():
    # Purpose:
    # Ensure namedtuple_utils.to_namedtuple can be invoked on a dictionary
    # that uses bytes objects as keys/values and that the call does not raise.
    #
    # Notes:
    # - The original test used duplicate identical keys; Python dict literals
    #   collapse duplicate keys into a single entry, so we intentionally create
    #   a single-entry mapping here to match runtime behavior.
    # - We don't make assumptions about the exact return shape (namedtuple,
    #   tuple, list, etc.), only that conversion completes and returns a value.

    # Setup: define a sample bytes value and a dict using that bytes as key/value
    SAMPLE_BYTES_KEY = b"F\xdb\xfdf\x8a\xe4\n\xa2\x1d[\xdc*\xa3\xba\xf6s}"
    mapping_with_bytes_keys = {SAMPLE_BYTES_KEY: SAMPLE_BYTES_KEY}

    # Execution: perform the conversion
    result = namedtuple_utils.to_namedtuple(mapping_with_bytes_keys)

    # Assertion: conversion completed successfully and returned a non-None object
    assert result is not None

