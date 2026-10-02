import pytest

import collections as collections_module
import namedtupleutils as namedtuple_utils

def test_to_namedtuple_returns_same_float_when_input_is_float():
    """Verify a primitive float is returned unchanged (not converted to a tuple/namedtuple)."""
    FLOAT_INPUT = -476.66

    result = namedtuple_utils.to_namedtuple(FLOAT_INPUT)

    assert result == FLOAT_INPUT
    assert isinstance(result, float)
    assert not isinstance(result, tuple)

def test_to_namedtuple_preserves_values_in_tuple_with_set():
    # Purpose:
    # Ensure to_namedtuple can handle a tuple that contains a set and that
    # values are preserved after conversion (no data loss).
    #
    # Setup (Arrange)
    TEST_FLOAT = -67.0
    # Create a set with repeated references to the same float to ensure duplicate
    # entries are collapsed by the set itself.
    TEST_SET = {TEST_FLOAT, TEST_FLOAT, TEST_FLOAT}
    TEST_TUPLE = (TEST_FLOAT, TEST_SET)

    # Execution (Act)
    # Convert the tuple (which contains the set) and convert the set alone.
    converted_tuple = namedtuple_utils.to_namedtuple(TEST_TUPLE)
    converted_set_like = namedtuple_utils.to_namedtuple(TEST_SET)

    # Assertions (Assert)
    # The top-level tuple should remain a tuple and the first element preserved.
    assert isinstance(converted_tuple, tuple)
    assert converted_tuple[0] == TEST_FLOAT

    # The second element corresponds to the original set. It may be converted
    # to some sequence-like or tuple-like structure; verify the float value
    # exists among its contents.
    second_element = converted_tuple[1]
    assert any(item == TEST_FLOAT for item in second_element)

    # Converting the set by itself should also produce a collection-like object
    # that contains the original float value.
    assert any(item == TEST_FLOAT for item in converted_set_like)

def test_to_namedtuple_idempotent_for_simple_dict():
    # Purpose:
    # Verify that a simple mapping is converted to a namedtuple with the
    # expected attribute and that calling to_namedtuple on an already-converted
    # namedtuple is idempotent (returns an equal object).

    # Constants
    KEY = "author"
    VALUE = "author"

    # Setup: create a source dictionary and perform the first conversion
    source_dict = {KEY: VALUE}
    first_conversion = namedtuple_utils.to_namedtuple(source_dict)

    # Execution: perform the conversion again on the result
    second_conversion = namedtuple_utils.to_namedtuple(first_conversion)

    # Assertions:
    # - The converted object exposes the original key as an attribute with the expected value.
    assert hasattr(first_conversion, KEY)
    assert getattr(first_conversion, KEY) == VALUE

    # - Namedtuple instances are tuple subclasses.
    assert isinstance(first_conversion, tuple)

    # - Converting an already-converted object is idempotent: the results are equal.
    assert first_conversion == second_conversion

def test_to_namedtuple_returns_same_bytes_when_input_is_bytes():
    # Purpose:
    #   Ensure that non-container types (bytes) are not converted and are returned
    #   unchanged by namedtuple_utils.to_namedtuple.
    SAMPLE_BYTES = b"xs&,\x9b\xc2\xf1\x80\xb3y"

    # Setup: prepare the input bytes value
    input_bytes = SAMPLE_BYTES

    # Execution: call the function under test
    result = namedtuple_utils.to_namedtuple(input_bytes)

    # Assertion: the result should remain a bytes object and equal the original value
    assert isinstance(result, bytes)
    assert result == SAMPLE_BYTES

def test_to_namedtuple_with_empty_tuple_returns_empty_tuple():
    # Purpose:
    # Verify that converting an empty tuple with to_namedtuple returns an empty
    # tuple (no items added/removed) and that the returned value is a tuple.

    # Constants / Setup
    EMPTY_TUPLE = ()
    original_tuple = EMPTY_TUPLE

    # Execution: convert the empty tuple
    converted = namedtuple_utils.to_namedtuple(original_tuple)

    # Assertions: result should be an empty tuple and preserve tuple type
    assert isinstance(converted, tuple), "Expected result to be a tuple"
    assert converted == EMPTY_TUPLE, "Expected converted empty tuple to equal the original empty tuple"
    assert len(converted) == 0, "Expected converted tuple to have length 0"

def test_to_namedtuple_idempotence_and_tuple_handling():
    # Purpose:
    # - Verify that converting an OrderedDict to a namedtuple is stable/idempotent
    #   (converting the result again yields the same structure).
    # - Verify that a tuple containing a namedtuple and raw bytes is converted
    #   into a tuple where the namedtuple is preserved/converted and the bytes
    #   remain unchanged.

    # Constants / setup
    SAMPLE_BYTES = b"\xe2\xf8\xb9\x01\x8c\xa5\xed\xb1\x0e&rdHE"
    empty_ordered = collections_module.OrderedDict()

    # Execution: convert the empty OrderedDict multiple times to test idempotence
    first_namedtuple = namedtuple_utils.to_namedtuple(empty_ordered)
    second_namedtuple = namedtuple_utils.to_namedtuple(first_namedtuple)
    third_namedtuple_from_ordered = namedtuple_utils.to_namedtuple(empty_ordered)
    fourth_namedtuple = namedtuple_utils.to_namedtuple(third_namedtuple_from_ordered)

    # Execution: convert a tuple that contains a namedtuple and raw bytes
    mixed_tuple = (second_namedtuple, SAMPLE_BYTES)
    converted_mixed_tuple = namedtuple_utils.to_namedtuple(mixed_tuple)

    # Assertions: idempotence / stability checks
    # Expect the converted objects to expose namedtuple-like _fields attribute.
    first_fields = getattr(first_namedtuple, "_fields", None)
    second_fields = getattr(second_namedtuple, "_fields", None)
    third_fields = getattr(third_namedtuple_from_ordered, "_fields", None)
    fourth_fields = getattr(fourth_namedtuple, "_fields", None)

    assert first_fields is not None, "Expected first conversion to produce a namedtuple-like object"
    assert second_fields is not None, "Expected second conversion to produce a namedtuple-like object"
    assert third_fields is not None and fourth_fields is not None

    # The field definitions should remain the same across repeated conversions.
    assert first_fields == second_fields == third_fields == fourth_fields

    # Assertions: tuple handling
    assert isinstance(converted_mixed_tuple, tuple), "Expected conversion of a tuple to return a tuple"
    # The first element should be a namedtuple-like object; second element should be the original bytes
    assert getattr(converted_mixed_tuple[0], "_fields", None) is not None
    assert converted_mixed_tuple[1] == SAMPLE_BYTES

def test_to_namedtuple_handles_non_identifier_keys_and_ordered_dict_init_error():
    # This test verifies two behaviors:
    # 1. namedtuple_utils.to_namedtuple can accept an OrderedDict whose key
    #    is not a valid Python identifier and will return a NamedTuple-like
    #    object (tuple subclass) preserving the OrderedDict value order.
    # 2. collections.OrderedDict initialization with None is invalid and should
    #    raise a TypeError.
    
    # Constants / Setup
    INVALID_KEY = "wm=-g\ry#\x0b#:*"
    TEST_VALUE = INVALID_KEY  # value is the same string for clarity
    # Create a mapping with duplicate key entries to simulate typical dict input.
    # Duplicate keys collapse to a single entry, so the OrderedDict will have one item.
    mapping_with_duplicate_key = {INVALID_KEY: TEST_VALUE, INVALID_KEY: TEST_VALUE}
    # Construct OrderedDict from the mapping (do not use **kwargs, since the key is not a valid identifier)
    ordered_mapping = collections_module.OrderedDict(mapping_with_duplicate_key)
    
    # Execution: convert the OrderedDict to a namedtuple-like object
    namedtuple_result = namedtuple_utils.to_namedtuple(ordered_mapping)
    
    # Assertions for to_namedtuple:
    # - The result should be a tuple subclass (namedtuple) and expose _fields.
    # - The values (when viewed as a tuple) should preserve the OrderedDict order.
    assert isinstance(namedtuple_result, tuple)
    assert hasattr(namedtuple_result, "_fields")
    assert tuple(namedtuple_result) == (TEST_VALUE,)
    
    # Execution + Assertion: constructing an OrderedDict from None should raise TypeError
    with pytest.raises(TypeError):
        collections_module.OrderedDict(None)

def test_to_namedtuple_converts_nested_empty_list_and_handles_none():
    # Purpose:
    # Verify that to_namedtuple:
    #  - returns a new outer list when given a list,
    #  - recursively converts inner lists to new lists (even if empty),
    #  - and returns None unchanged when given None.
    #
    # Setup
    ORIGINAL_INNER_LIST = []
    INPUT_LIST = [ORIGINAL_INNER_LIST]

    # Execution
    result = namedtuple_utils.to_namedtuple(INPUT_LIST)
    result_none = namedtuple_utils.to_namedtuple(None)

    # Assertions
    # Outer structure: result should be a different list object than the input
    assert isinstance(result, list)
    assert result is not INPUT_LIST

    # Inner structure: there should be one element which is itself a list,
    # that is empty and not the same object as the original inner list.
    assert len(result) == 1
    assert isinstance(result[0], list)
    assert result[0] == []
    assert result[0] is not ORIGINAL_INNER_LIST

    # None handling: converting None should return None (no exception, unchanged)
    assert result_none is None

def test_to_namedtuple_handles_various_inputs():
    # Purpose:
    # Verify that namedtuple_utils.to_namedtuple can be called with various
    # input types (mapping, tuple containing a namedtuple, complex dict keys,
    # already-converted namedtuple and a non-convertible value) without error
    # and that the return types/values match expectations.
    
    # Constants / setup
    LONG_DOC = (
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
        "        PosixPath('/home/test_user/tmp/bar')\n\n"
    )
    
    # Create a dict where the (invalid-as-identifier) key is the long docstring.
    mapping_with_nonidentifier_key = {LONG_DOC: LONG_DOC}
    
    # Execution: convert mapping to a namedtuple (NamedTuple is a subclass of tuple)
    namedtuple_from_mapping = namedtuple_utils.to_namedtuple(mapping_with_nonidentifier_key)
    
    # Assertion: mapping conversion yields a tuple-like namedtuple object
    assert isinstance(namedtuple_from_mapping, tuple), (
        "Expected mapping to be converted to a namedtuple (tuple subclass)."
    )
    
    # Execution: place the namedtuple inside a tuple and convert that tuple
    tuple_wrapping_namedtuple = (namedtuple_from_mapping,)
    converted_tuple = namedtuple_utils.to_namedtuple(tuple_wrapping_namedtuple)
    
    # Assertion: tuple conversion should produce a tuple containing the original namedtuple
    assert isinstance(converted_tuple, tuple), "Expected tuple input to produce a tuple."
    assert len(converted_tuple) == 1 and converted_tuple[0] is namedtuple_from_mapping, (
        "Converted tuple should preserve the contained namedtuple as the single element."
    )
    
    # Setup: create a dictionary with complex (hashable) keys:
    # - a tuple (converted_tuple) as a key
    # - a boolean as another key
    complex_key_dict = {converted_tuple: namedtuple_from_mapping, False: namedtuple_from_mapping}
    
    # Execution: convert the complex-key dictionary to a namedtuple
    namedtuple_from_complex_dict = namedtuple_utils.to_namedtuple(complex_key_dict)
    
    # Assertion: conversion of a mapping with complex keys should succeed and return a tuple-like object
    assert isinstance(namedtuple_from_complex_dict, tuple), (
        "Expected complex-key mapping to be converted to a namedtuple (tuple subclass)."
    )
    
    # Execution & Assertion: converting an already-converted namedtuple should return an equivalent tuple-like object
    reconverted = namedtuple_utils.to_namedtuple(namedtuple_from_complex_dict)
    assert isinstance(reconverted, tuple), "Re-converting a namedtuple should still return a tuple-like object."
    assert reconverted == namedtuple_from_complex_dict, "Re-converting a namedtuple should preserve its value/equality."
    
    # Finally, verify that passing a non-convertible scalar (False) returns it unchanged
    result_for_false = namedtuple_utils.to_namedtuple(False)
    assert result_for_false is False, "Non-convertible scalar values should be returned unchanged."

def test_to_namedtuple_idempotent_on_nested_structures_and_primitives():
    # Purpose:
    # Verify that to_namedtuple can process a nested structure (list -> tuple -> dict)
    # without raising, that repeated conversions are idempotent, and that primitive
    # values (int) are returned unchanged.

    # Constants / Setup
    SAMPLE_STR = "\x0cMv"
    EMPTY_TUPLE = ()
    # Note: duplicate dict keys in the original test collapse; emulate resulting mapping.
    MIXED_DICT = {SAMPLE_STR: EMPTY_TUPLE, EMPTY_TUPLE: EMPTY_TUPLE}
    NESTED_TUPLE = (SAMPLE_STR, MIXED_DICT)
    NESTED_LIST = [NESTED_TUPLE]

    # Execution: perform the conversion multiple times to check idempotency
    first_conversion = namedtuple_utils.to_namedtuple(NESTED_LIST)
    second_conversion = namedtuple_utils.to_namedtuple(first_conversion)
    third_conversion = namedtuple_utils.to_namedtuple(second_conversion)

    # Also ensure primitive conversion does not raise and returns the original value
    PRIMITIVE_INT = 2
    primitive_conversion = namedtuple_utils.to_namedtuple(PRIMITIVE_INT)

    # Assertions
    # The conversion of a list should produce a list-like result
    assert isinstance(first_conversion, list), "Expected top-level conversion of list to produce a list"

    # Repeated conversions should not change the resulting structure (idempotent)
    assert first_conversion == second_conversion == third_conversion, "to_namedtuple should be idempotent on its own output"

    # Primitive values should be returned unchanged
    assert primitive_conversion == PRIMITIVE_INT and isinstance(primitive_conversion, int), "Primitive int should be returned unchanged by to_namedtuple"

def test_to_namedtuple_handles_bytes_keys_without_error():
    # Purpose:
    # Verify that to_namedtuple can be called with a mapping that uses non-string
    # keys (bytes) without raising an exception and that it returns a container-like
    # value (list, tuple, or namedtuple-like object).

    # Constants / Setup
    TEST_BYTES_KEY = b"F\xdb\xfdf\x8a\xe4\n\xa2\x1d[\xdc*\xa3\xba\xf6s}"
    test_mapping_with_bytes_keys = {TEST_BYTES_KEY: TEST_BYTES_KEY}
    # Note: byte keys are not valid Python identifiers and therefore cannot become
    # namedtuple attribute names; the purpose here is to ensure the function
    # handles such keys gracefully.

    # Execution
    result = namedtuple_utils.to_namedtuple(test_mapping_with_bytes_keys)

    # Assertion: function should return some container-like object (not raise).
    assert result is not None
    assert isinstance(result, (list, tuple)) or getattr(result, "_fields", None) is not None

