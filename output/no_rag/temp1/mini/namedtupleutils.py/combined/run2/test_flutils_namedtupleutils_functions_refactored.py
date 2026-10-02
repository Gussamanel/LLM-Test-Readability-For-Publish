import pytest

import namedtupleutils as namedtuple_utils
import collections as std_collections

def test_to_namedtuple_leaves_float_unchanged():
    """Verify that to_namedtuple returns float values unchanged and preserves their type."""
    # Arrange
    sample_float = -476.66
    input_value = sample_float

    # Act
    result = namedtuple_utils.to_namedtuple(input_value)

    # Assert
    assert result == sample_float
    assert isinstance(result, float)

def test_to_namedtuple_handles_tuple_with_set_and_duplicates():
    # Purpose:
    # Ensure to_namedtuple can process a tuple that contains a float and a set
    # (with duplicate entries), and that converting the set on its own preserves
    # the underlying values (no loss or unexpected transformation).
    #
    # The test is structured into: constants, setup, execution, assertion.

    # Constants
    TEST_FLOAT = -67.0
    EXPECTED_SET = {TEST_FLOAT}

    # Setup: create inputs (note duplicate entries in the set literal are harmless)
    set_with_duplicates = {TEST_FLOAT, TEST_FLOAT, TEST_FLOAT}
    input_tuple = (TEST_FLOAT, set_with_duplicates)

    # Execution: convert the tuple and the set using the module under test
    converted_tuple = namedtuple_utils.to_namedtuple(input_tuple)
    converted_set_result = namedtuple_utils.to_namedtuple(set_with_duplicates)

    # Assertions:
    # - The converted tuple should still be a tuple-like sequence and preserve the float
    assert isinstance(converted_tuple, tuple), "Converted tuple should be a tuple"
    assert converted_tuple[0] == TEST_FLOAT

    # - The second element (converted set) should contain the same values as the original set
    #   Use set(...) to allow for different iterable/sequence types returned by the conversion.
    assert set(converted_tuple[1]) == EXPECTED_SET

    # - Converting the set on its own should also yield an iterable with the same values
    assert set(converted_set_result) == EXPECTED_SET

def test_to_namedtuple_converts_dict_and_is_idempotent():
    # Purpose:
    # - Verify that a simple dict with a valid identifier key is converted to a namedtuple
    # - Verify that passing the resulting namedtuple back into to_namedtuple is idempotent
    #   (i.e., returns an equivalent namedtuple instance/value)

    # Constants / Setup
    KEY = "author"
    VALUE = "author"
    INPUT_DICT = {KEY: VALUE}

    # Execution
    first_namedtuple = namedtuple_utils.to_namedtuple(INPUT_DICT)
    second_namedtuple = namedtuple_utils.to_namedtuple(first_namedtuple)

    # Assertions
    # The converted object should behave like a namedtuple: tuple subclass with named fields
    assert isinstance(first_namedtuple, tuple), "Expected the result to be a tuple-like namedtuple"
    assert hasattr(first_namedtuple, KEY), f"Expected namedtuple to have attribute '{KEY}'"
    assert getattr(first_namedtuple, KEY) == VALUE, f"Expected attribute '{KEY}' to equal '{VALUE}'"

    # Converting an already converted namedtuple should be idempotent (produce an equal result)
    assert second_namedtuple == first_namedtuple, "Expected second conversion to produce an equivalent namedtuple"
    assert isinstance(second_namedtuple, tuple), "Expected the second result to still be a tuple-like namedtuple"

def test_to_namedtuple_leaves_bytes_unchanged():
    # Purpose:
    # Verify that to_namedtuple does not attempt to convert a bytes object
    # into a namedtuple and returns the original value (or an equal value)
    # with the same type preserved.

    # Setup: a sample bytes value (not a mapping, list or tuple)
    SAMPLE_BYTES = b"xs&,\x9b\xc2\xf1\x80\xb3y"

    # Execution: call the function under test
    result = namedtuple_utils.to_namedtuple(SAMPLE_BYTES)

    # Assertion: the result should be equal to the original bytes and remain of bytes type
    assert result == SAMPLE_BYTES
    assert isinstance(result, bytes)

def test_to_namedtuple_with_empty_tuple_returns_empty_tuple():
    # Ensure that to_namedtuple returns an empty tuple unchanged when given an empty tuple.
    EMPTY_TUPLE = ()
    converted = namedtuple_utils.to_namedtuple(EMPTY_TUPLE)
    assert isinstance(converted, tuple)
    assert converted == EMPTY_TUPLE

def test_to_namedtuple_empty_ordereddict_and_tuple_conversion():
    # Purpose:
    # - Verify that to_namedtuple converts an empty OrderedDict into a namedtuple
    #   with no fields.
    # - Verify calling to_namedtuple on an already-converted namedtuple is stable
    #   (preserves field structure).
    # - Verify that converting a tuple preserves non-convertible items (bytes)
    #   and converts nested namedtuple elements.

    # Constants / setup
    EMPTY_ORDERED_DICT = std_collections.OrderedDict()
    SAMPLE_BYTES = b"\xe2\xf8\xb9\x01\x8c\xa5\xed\xb1\x0e&rdHE"

    # Convert an empty OrderedDict to a namedtuple
    namedtuple_from_empty = namedtuple_utils.to_namedtuple(EMPTY_ORDERED_DICT)

    # Execution: perform additional conversions to exercise idempotency and tuple handling
    namedtuple_converted_again = namedtuple_utils.to_namedtuple(namedtuple_from_empty)
    namedtuple_from_empty_again = namedtuple_utils.to_namedtuple(EMPTY_ORDERED_DICT)
    converted_tuple = namedtuple_utils.to_namedtuple((namedtuple_converted_again, SAMPLE_BYTES))

    # Assertions: check the structure and behavior
    # The result of converting an empty OrderedDict should be a tuple-like namedtuple
    assert isinstance(namedtuple_from_empty, tuple)
    assert hasattr(namedtuple_from_empty, "_fields")
    assert namedtuple_from_empty._fields == ()  # no fields for an empty OrderedDict

    # Re-converting the namedtuple should preserve the same fields (idempotent behavior)
    assert hasattr(namedtuple_converted_again, "_fields")
    assert namedtuple_converted_again._fields == namedtuple_from_empty._fields

    # Converting the empty OrderedDict again should produce the same field structure
    assert hasattr(namedtuple_from_empty_again, "_fields")
    assert namedtuple_from_empty_again._fields == namedtuple_from_empty._fields

    # When converting a tuple containing a namedtuple and bytes:
    # - the namedtuple element should remain a namedtuple-like object
    # - the bytes element should be preserved unchanged
    assert isinstance(converted_tuple, tuple)
    assert converted_tuple[1] == SAMPLE_BYTES
    assert hasattr(converted_tuple[0], "_fields")
    assert converted_tuple[0]._fields == namedtuple_from_empty._fields

def test_to_namedtuple_from_ordereddict_and_ordereddict_init_with_none_raises():
    # This test checks two things:
    # 1) namedtuple_utils.to_namedtuple can consume an OrderedDict and returns a tuple-like object.
    # 2) std_collections.OrderedDict initialized with a single None positional argument raises TypeError.

    # Constants / Setup
    KEY_STR = "wm=-g\ry#\x0b#:*"
    VALUE_STR = KEY_STR
    INPUT_MAPPING = {KEY_STR: VALUE_STR}

    # Create an OrderedDict from the mapping and convert it to a namedtuple-like object.
    ordered_input = std_collections.OrderedDict(INPUT_MAPPING)

    # Execution: convert OrderedDict to namedtuple (or tuple-like) structure
    converted = namedtuple_utils.to_namedtuple(ordered_input)

    # Assertions for conversion:
    # - The result should be a tuple or namedtuple (namedtuples are instances of tuple).
    # - The original value should be present in the converted structure.
    assert isinstance(converted, tuple)
    assert VALUE_STR in converted

    # Execution + Assertion: constructing an OrderedDict with a single None positional argument should raise TypeError
    with pytest.raises(TypeError):
        std_collections.OrderedDict(*[None])

def test_to_namedtuple_converts_nested_lists_and_handles_none():
    # Purpose:
    # - Verify that to_namedtuple converts a list containing another list
    #   into a new list structure with its contents converted (recursively).
    # - Verify that passing None is handled gracefully (returned as-is).
    #
    # Setup: create a nested empty list structure to be converted.
    ORIGINAL_INNER = []
    ORIGINAL_OUTER = [ORIGINAL_INNER]

    # Execution: convert the outer list
    converted_outer = namedtuple_utils.to_namedtuple(ORIGINAL_OUTER)

    # Assertions: structure and identity checks for list conversion
    assert isinstance(converted_outer, list)
    assert len(converted_outer) == 1

    # The inner element should be an empty list after conversion
    assert converted_outer[0] == []

    # to_namedtuple should produce new list objects (no in-place mutation)
    assert converted_outer is not ORIGINAL_OUTER
    assert converted_outer[0] is not ORIGINAL_INNER

    # Original inputs must remain unchanged
    assert ORIGINAL_OUTER == [ORIGINAL_INNER]
    assert ORIGINAL_OUTER[0] is ORIGINAL_INNER

    # Execution & Assertion: None input should be returned as-is (no conversion)
    assert namedtuple_utils.to_namedtuple(None) is None

def test_to_namedtuple_handles_nested_structures_and_primitives():
    # Verify to_namedtuple handles nested structures, non-string keys, idempotency,
    # and leaves primitive booleans unchanged.

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
        "        PosixPath('/home/test_user/tmp/bar')\n\n"
    )

    # Dict where the long string is both key and value.
    simple_dict_input = {LONG_DOCSTRING: LONG_DOCSTRING}

    # Convert dict to namedtuple-like object.
    first_namedtuple = namedtuple_utils.to_namedtuple(simple_dict_input)

    # Conversion should produce a tuple-like object and be deterministic.
    assert isinstance(first_namedtuple, tuple)
    second_namedtuple = namedtuple_utils.to_namedtuple(simple_dict_input)
    assert first_namedtuple == second_namedtuple

    # A tuple that contains the previously created namedtuple.
    tuple_wrapping_namedtuple = (first_namedtuple,)

    # Converting a tuple should recursively convert its contents.
    converted_tuple = namedtuple_utils.to_namedtuple(tuple_wrapping_namedtuple)
    assert isinstance(converted_tuple, tuple)
    assert len(converted_tuple) == 1
    assert converted_tuple[0] == first_namedtuple

    # Dict that uses the converted tuple as a key and a boolean key, both mapping
    # to the same namedtuple value.
    mixed_key_dict = {converted_tuple: first_namedtuple, False: first_namedtuple}

    # Convert mixed-key dict and assert idempotency.
    mixed_namedtuple = namedtuple_utils.to_namedtuple(mixed_key_dict)
    assert isinstance(mixed_namedtuple, tuple)
    mixed_namedtuple_again = namedtuple_utils.to_namedtuple(mixed_namedtuple)
    assert mixed_namedtuple == mixed_namedtuple_again

    # Primitive booleans should be returned unchanged.
    bool_conversion_result = namedtuple_utils.to_namedtuple(False)
    assert bool_conversion_result is False

def test_to_namedtuple_recursive_idempotent_and_handles_non_identifier_keys():
    # Purpose:
    # - Verify that to_namedtuple can be applied to a nested structure (list -> tuple -> dict)
    #   and that repeated conversions are idempotent (further conversions don't change the result).
    # - Ensure primitive values are returned unchanged (e.g. an int).
    #
    # Setup: build a list containing a tuple whose second element is a mapping with
    # keys that are not valid Python identifiers (a control-character-starting string
    # and an empty tuple). The mapping values are empty tuples.
    SPECIAL_KEY = "\x0cMv"
    EMPTY_TUPLE = ()
    nested_mapping = {SPECIAL_KEY: EMPTY_TUPLE, EMPTY_TUPLE: EMPTY_TUPLE}
    nested_tuple = (SPECIAL_KEY, nested_mapping)
    input_list = [nested_tuple]

    # Execution: perform conversion once and then repeatedly (to test idempotency).
    converted_once = namedtuple_utils.to_namedtuple(input_list)
    converted_twice = namedtuple_utils.to_namedtuple(converted_once)
    converted_thrice = namedtuple_utils.to_namedtuple(converted_twice)

    # Also verify a primitive value is returned unchanged.
    primitive_input = 2
    primitive_result = namedtuple_utils.to_namedtuple(primitive_input)

    # Assertions:
    # - The top-level result of converting a list should be a list with the same length.
    assert isinstance(converted_once, list)
    assert len(converted_once) == 1

    # - The first (and only) item should be a tuple with two elements (the string and the converted mapping).
    first_item = converted_once[0]
    assert isinstance(first_item, tuple)
    assert len(first_item) == 2

    # - The first element of that tuple should still be the original string.
    assert first_item[0] == SPECIAL_KEY
    assert isinstance(first_item[0], str)

    # - The second element (result of converting the dict) should be a tuple-like object
    #   (namedtuple instances are subclasses of tuple). We don't assert on specific fields
    #   because the original mapping keys are not valid identifiers and the implementation
    #   may produce an empty-namedtuple or another tuple-like representation.
    converted_mapping = first_item[1]
    assert isinstance(converted_mapping, tuple)

    # - Repeated conversions should be idempotent (no changes after the first conversion).
    assert converted_twice == converted_once
    assert converted_thrice == converted_once

    # - Converting a primitive should return it unchanged.
    assert primitive_result == primitive_input

def test_to_namedtuple_ignores_non_identifier_byte_keys_returns_empty_namedtuple():
    # Purpose:
    # Verify that to_namedtuple can handle dicts with non-identifier keys (bytes)
    # without raising and that such keys do not become attributes on the returned
    # namedtuple (i.e., no fields are created).
    #
    # Setup: define a bytes key and a dict that uses that bytes value as a key
    SAMPLE_BYTES = b"F\xdb\xfdf\x8a\xe4\n\xa2\x1d[\xdc*\xa3\xba\xf6s}"
    SAMPLE_DICT = {
        SAMPLE_BYTES: SAMPLE_BYTES,
        SAMPLE_BYTES: SAMPLE_BYTES,  # repeated keys collapse in a dict; kept to mirror original test
        SAMPLE_BYTES: SAMPLE_BYTES,
    }

    # Execution: convert the mapping to a namedtuple-like object
    result = namedtuple_utils.to_namedtuple(SAMPLE_DICT)

    # Assertion: result is a namedtuple instance (tuple with _fields) and, because
    # the keys are not valid Python identifiers (they are bytes), no attributes
    # should be created — _fields should be empty and the tuple length zero.
    assert isinstance(result, tuple)
    assert hasattr(result, "_fields")
    assert result._fields == ()
    assert len(result) == 0

