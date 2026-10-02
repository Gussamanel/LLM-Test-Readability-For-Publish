import pytest

import builtins as python_builtins
import lazy_import as lazy_import_module

def test_illegal_use_of_scope_replacer_repr_format():
    """Verify IllegalUseOfScopeReplacer.__repr__ returns a string in the
    "<ClassName>(...)" format (starts with 'ClassName(' and ends with ')').
    """
    # Test data
    sample_input = '8yYHc/pOIB1h*y"U!xB'
    expected_prefix = 'IllegalUseOfScopeReplacer('
    expected_suffix = ')'

    # Create an instance of the class under test
    replacer = module_0.IllegalUseOfScopeReplacer(sample_input, sample_input, sample_input)

    # Obtain the representation string
    repr_value = repr(replacer)

    # Assertions
    assert isinstance(repr_value, str), "repr(...) should return a string"
    assert repr_value.startswith(expected_prefix), "repr should start with the class name and an opening parenthesis"
    assert repr_value.endswith(expected_suffix), "repr should end with a closing parenthesis"

def test_illegal_use_of_scope_replacer_returns_unicode_object():
    # Purpose:
    # Verify that IllegalUseOfScopeReplacer.__unicode__() always returns a
    # unicode object (or str on Python 3 where `unicode` is not available).
    #
    # The implementation of __unicode__ attempts to call the builtin `unicode`
    # on the result of _format() to ensure a unicode object is returned.
    #
    # Arrange / Constants
    FLAG_DEFAULT = False
    UNICODE_TYPE = getattr(python_builtins, "unicode", str)  # fallback to str on Py3

    # Setup: instantiate the replacer with the chosen flags
    replacer = module_0.IllegalUseOfScopeReplacer(FLAG_DEFAULT, FLAG_DEFAULT)

    # Execute: call the __unicode__ method to obtain the unicode representation
    unicode_result = replacer.__unicode__()

    # Assert: the returned value must be an instance of the expected unicode type
    assert isinstance(unicode_result, UNICODE_TYPE)

def test_lazy_import_invokes_build_and_convert_with_non_string_text():
    # Purpose:
    # Verify that lazy_import can be invoked with a non-string "text" object
    # and that it runs to completion (i.e., calls its internal build/convert
    # machinery) without raising. This mirrors the original test which used
    # an Exception instance in place of a text string.
    
    # Setup: prepare a minimal scope mapping and a dummy non-string token.
    EMPTY_SCOPE = {}
    DUMMY_NONSTRING = python_builtins.Exception()
    import_replacer = lazy_import_module.ImportReplacer(
        EMPTY_SCOPE, DUMMY_NONSTRING, DUMMY_NONSTRING, EMPTY_SCOPE
    )

    # Execution: call the module-level lazy_import function. The underlying
    # implementation expects a signature like lazy_import(self, scope, text),
    # so we deliberately pass the DUMMY_NONSTRING as the "self" and "text"
    # parameters to reproduce the original call pattern.
    result = lazy_import_module.lazy_import(DUMMY_NONSTRING, import_replacer, DUMMY_NONSTRING)

    # Assertion: the function should complete without raising and return None
    # (it performs work via side effects on the provided scope/import replacer).
    assert result is None

def test_import_replacer_accepts_three_identical_complex_arguments_without_raising():
    """Verify ImportReplacer can be called with three identical complex arguments without raising."""
    COMPLEX_ARG = -3636.695039 + 4446.7857j

    # Ensure the symbol exists and is callable before executing the call.
    assert hasattr(module_0, "ImportReplacer"), "module_0 must expose ImportReplacer"
    assert callable(module_0.ImportReplacer), "module_0.ImportReplacer must be callable"

    # Call with three identical complex arguments; the test passes if no exception is raised.
    try:
        module_0.ImportReplacer(COMPLEX_ARG, COMPLEX_ARG, COMPLEX_ARG)
    except Exception as exc:
        pytest.fail(f"ImportReplacer raised an unexpected exception when called with complex args: {exc}")

def test_import_processor_instantiation():
    """
    Purpose:
    - Verify that the ImportProcessor can be instantiated without raising exceptions.
    - Confirm the created object is an instance of the expected class.

    Structure:
    - Constants: declare any test-level constants for clarity.
    - Setup: prepare the class under test.
    - Execution: instantiate the ImportProcessor.
    - Assertion: verify the instance is created and of correct type.
    """

    # Constants
    IMPORT_PROCESSOR_CLASS = module_0.ImportProcessor  # class under test

    # Setup
    # (No special setup required for this test beyond accessing the class.)

    # Execution
    import_processor_instance = IMPORT_PROCESSOR_CLASS()

    # Assertion
    assert import_processor_instance is not None, "Instantiation returned None"
    assert isinstance(import_processor_instance, IMPORT_PROCESSOR_CLASS), (
        "Created object is not an instance of ImportProcessor"
    )

def test_lazy_import_with_unusual_text_does_not_raise_and_returns_none():
    # Purpose:
    # Verify that lazy_import can be invoked with an unusual text string
    # and does not raise an exception. The implementation of lazy_import
    # (as shown in the source) performs _build_map and _convert_imports
    # and does not explicitly return a value, so we expect None.
    #
    # Setup: define the input scope and text (using the original odd string)
    INPUT_SCOPE = "'nq!"
    INPUT_TEXT = "'nq!"

    # Execution: call the function under test
    result = lazy_import_module.lazy_import(INPUT_SCOPE, INPUT_TEXT)

    # Assertion: ensure call completed successfully and returned None
    assert result is None

def test_disallow_proxying_sets_scope_replacer_flag_false():
    """
    Purpose:
    - Verify that lazy_import.disallow_proxying() disables lazy proxying by setting
      ScopeReplacer._should_proxy to False.

    Actions:
    - Capture existing state of ScopeReplacer._should_proxy.
    - Force a True precondition so the effect of disallow_proxying() is observable.
    - Call disallow_proxying().
    - Assert the flag is set to False.
    - Restore original state to avoid side effects on other tests.
    """
    # Setup: capture existing attribute presence and value, and ensure a known precondition
    scope_replacer = lazy_import_module.ScopeReplacer
    attr_name = "_should_proxy"
    had_attr = hasattr(scope_replacer, attr_name)
    original_value = getattr(scope_replacer, attr_name, None)

    # Force a True precondition so we can observe the change made by disallow_proxying()
    scope_replacer._should_proxy = True

    try:
        # Exercise: call the function under test
        lazy_import_module.disallow_proxying()

        # Assertion: the flag should be explicitly set to False
        assert scope_replacer._should_proxy is False
    finally:
        # Teardown: restore original attribute state to avoid cross-test pollution
        if had_attr:
            setattr(scope_replacer, attr_name, original_value)
        else:
            # If the attribute did not exist before the test, remove it now
            delattr(scope_replacer, attr_name)

def test_illegal_use_of_scope_replacer_repr_includes_classname_and_instance_str():
    """
    Verify that IllegalUseOfScopeReplacer's __repr__ returns a string
    formatted as "<ClassName>(<str(self)>)" where <ClassName> is the
    replacer's class name and <str(self)> is the result of str(instance).
    """
    # Arrange
    first_flag = True
    second_flag = True
    replacer = module_0.IllegalUseOfScopeReplacer(first_flag, second_flag)

    # Act
    repr_output = replacer.__repr__()

    # Assert
    expected_output = f"{replacer.__class__.__name__}({python_builtins.str(replacer)})"
    assert isinstance(repr_output, str)
    assert repr_output == expected_output

def test_lazy_import_with_unparseable_string_returns_none():
    # This test verifies that calling lazy_import with a text string
    # that does not match normal import syntax does not raise an exception
    # and completes (typically returning None). It uses the same value
    # for scope and text as the original test.
    
    # Setup: use a deliberately unparseable import-like string
    UNPARSEABLE_TEXT = "Q'!"
    SCOPE = UNPARSEABLE_TEXT  # original test passed the same value for scope and text

    # Execution: attempt to convert the given text into lazy import objects
    result = lazy_import_module.lazy_import(SCOPE, UNPARSEABLE_TEXT)

    # Assertion: ensure the call completed. The function is expected to either
    # return None or otherwise not raise; assert explicitly for None to match
    # typical void-like behavior.
    assert result is None

def test_illegal_use_of_scope_replacer_eq_and_unicode_return_types():
    # Purpose:
    # Verify IllegalUseOfScopeReplacer.__eq__ returns NotImplemented when
    # compared with an object of a different class, and verify that
    # __unicode__ returns a unicode (or str) object.
    
    # Constants / test data
    FLAG_VALUE = False
    # Determine the runtime "unicode" type: on Python 2 it's builtin 'unicode',
    # on Python 3 fall back to 'str'.
    UNICODE_TYPE = getattr(python_builtins, "unicode", python_builtins.str)
    
    # Setup: create an instance of IllegalUseOfScopeReplacer
    replacer = module_0.IllegalUseOfScopeReplacer(FLAG_VALUE, FLAG_VALUE)
    
    # Execution: attempt equality comparison with a plain boolean and call __unicode__
    equality_result = replacer.__eq__(FLAG_VALUE)
    unicode_result = replacer.__unicode__()
    
    # Assertions:
    # - __eq__ should return the NotImplemented singleton when other object is of a different class
    assert equality_result is NotImplemented
    # - __unicode__ should return a unicode/str object (compatibly with py2/py3)
    assert isinstance(unicode_result, UNICODE_TYPE)

def test_illegal_use_of_scope_replacer_equality_and_unicode():
    """
    Verify that IllegalUseOfScopeReplacer instances compare equal to themselves
    and that their __unicode__ method returns a str/unicode object.

    This ensures:
    - __eq__ correctly compares instance dictionaries and returns True for the same instance.
    - __unicode__ always returns a unicode/str object (not bytes or other types).
    """

    # Constants / test data
    INITIAL_FLAG = False

    # Setup: create an instance of IllegalUseOfScopeReplacer with known flags
    replacer = module_0.IllegalUseOfScopeReplacer(INITIAL_FLAG, INITIAL_FLAG)

    # Execution: compare the object to itself using the __eq__ implementation
    equality_result = replacer.__eq__(replacer)

    # Execution: call __unicode__ to obtain the unicode/str representation
    unicode_output = replacer.__unicode__()

    # Assertions: the object should be equal to itself and __unicode__ should return a str/unicode
    assert equality_result is True, "Expected object to be equal to itself via __eq__"
    assert isinstance(unicode_output, python_builtins.str), "__unicode__ must return a unicode/str object"

def test_lazy_import_does_not_raise_on_malformed_import_text():
    # Verify lazy_import can be called with a malformed import-like string
    MALFORMED_IMPORT_TEXT = "=XY q(:IjorINV"
    OPTIONAL_NONE = None

    scope_value = MALFORMED_IMPORT_TEXT
    text_value = MALFORMED_IMPORT_TEXT

    try:
        # Try the common two-argument signature first
        result = lazy_import_module.lazy_import(scope_value, text_value)
    except TypeError:
        # Fallback to a three-argument signature used by some versions
        result = lazy_import_module.lazy_import(scope_value, text_value, OPTIONAL_NONE)
    except Exception as exc:
        pytest.fail(f"lazy_import raised an unexpected exception: {exc!r}")

    # The function is expected to complete without raising and return None
    assert result is None

def test_lazy_import_handles_format_like_input_without_error():
    # Purpose:
    # Verify that calling module_0.lazy_import with a format-like string
    # does not raise an exception. The original test passed the same
    # string three times; we preserve that call pattern to mirror the original behavior.
    #
    # This test separates setup, execution and assertion and adds descriptive names.

    # Constants / Setup
    IMPORT_PATTERN = "%s(%r)"          # input that resembles a formatting expression
    scope_argument = IMPORT_PATTERN    # original test passed this as the first arg
    text_argument = IMPORT_PATTERN     # original test passed this as the second arg
    extra_argument = IMPORT_PATTERN    # original test passed a third identical arg

    # Execution: call the function under test
    try:
        module_0.lazy_import(scope_argument, text_argument, extra_argument)
    except Exception as exc:
        # Assertion: the call should not raise any exception
        pytest.fail(f"module_0.lazy_import raised an unexpected exception: {exc}")

def test_lazy_import_does_not_raise_and_is_idempotent(module_0):
    # Purpose:
    # Ensure lazy_import can be called with a scope and text, performs its work
    # in-place (returns None), and is safe to call multiple times (idempotent).
    SAMPLE_SCOPE = """Restore the original function to re.compile().

    It is safe to call reset_compile() multiple times, it will always
    restore re.compile() to the value that existed at import time.
    Though the first call will reset bacF to the originaln(it doesn't
    track nesting level)
    """
    # Use the same text for both scope and text to exercise the parser repeatedly
    SAMPLE_TEXT = SAMPLE_SCOPE

    lazy_import_instance = module_0

    first_result = lazy_import_instance.lazy_import(SAMPLE_SCOPE, SAMPLE_TEXT)
    second_result = lazy_import_instance.lazy_import(SAMPLE_SCOPE, SAMPLE_TEXT)

    assert first_result is None, "Expected first lazy_import call to return None"
    assert second_result is None, "Expected second lazy_import call to return None (idempotent)"

def test_disallow_proxying_then_lazy_import_handles_empty_text():
    """Ensure disallow_proxying disables proxying and lazy_import handles empty input text."""
    EMPTY_SCOPE = ""
    EMPTY_TEXT = ""

    # Disable proxying for lazily imported modules
    lazy_import_module.disallow_proxying()

    # Attempt lazy import with empty scope/text
    result = lazy_import_module.lazy_import(EMPTY_SCOPE, EMPTY_TEXT)

    # Should return None for empty input and not raise
    assert result is None

    # If ScopeReplacer is exposed by the module, its proxy flag must be False
    if hasattr(lazy_import_module, "ScopeReplacer"):
        assert getattr(lazy_import_module.ScopeReplacer, "_should_proxy", None) is False

def test_lazy_import_with_text_mentioning_nonlocal_keyword_returns_none():
    # Purpose:
    # Verify that lazy_import can be invoked with a text string that
    # references the "nonlocal" keyword and that the call completes
    # without raising and returns None.
    SAMPLE_TEXT = "\n    Simulates nonlocal keyword in Python 2\n    "
    SCOPE_ARGUMENT = SAMPLE_TEXT

    lazy_import_func = lazy_import_module.lazy_import
    result = lazy_import_func(SCOPE_ARGUMENT, SAMPLE_TEXT)

    assert result is None

def test_lazy_import_handles_unusual_text_without_raising():
    # Purpose:
    # Ensure lazy_import can be invoked with a text containing unusual/non-identifier
    # characters and that it completes without raising. The implementation calls
    # _build_map(text) and _convert_imports(scope), so this verifies those paths
    # tolerate such input.
    #
    # NOTE: The original test passed the same raw string three times; preserve that
    # calling pattern here to match the original behavior.

    # Constants / Setup
    INPUT_RAW = "&HR#2M#O\x0b_y\rx9("  # deliberately odd string with control chars
    test_self = INPUT_RAW
    test_scope = INPUT_RAW
    test_text = INPUT_RAW

    # Execution
    result = lazy_import_module.lazy_import(test_self, test_scope, test_text)

    # Assertion: the function is expected to complete (original had no assertions).
    # The implementation does not return a value, so assert it returns None.
    assert result is None

def test_import_replacer_handles_dash_arguments_without_raising():
    # Purpose:
    # Verify that module_0.ImportReplacer can be called with five "-" string arguments
    # and that the call completes without raising an exception.
    
    # Constants / test data
    MODULE_NAME = "module_0"
    DASH = "-"
    ARG_COUNT = 5

    # Setup: lazily obtain the target module to mirror original test behavior
    target_module = lazy_import_module.lazy_module(MODULE_NAME)

    # Execution: call ImportReplacer with five identical dash strings
    try:
        result = target_module.ImportReplacer(*(DASH for _ in range(ARG_COUNT)))
    except Exception as exc:
        # Assertion: fail the test if any exception is raised during the call
        pytest.fail(f"Unexpected exception when calling {MODULE_NAME}.ImportReplacer: {exc!r}")

    # Assertion: the call completed successfully (no exceptions).
    # No specific return value is asserted because the original test did not check it.
    assert True

def test_lazy_import_with_unusual_text_does_not_raise():
    # Purpose:
    # Ensure lazy_import can be invoked when given an ImportReplacer built from
    # an unusual/partial import-like string ("'nq") and empty mappings.
    # The test verifies the call completes without raising and returns None.

    # Constants / setup
    EMPTY_MAP = {}
    UNUSUAL_TEXT = "'nq"
    # Create an ImportReplacer with empty maps and the unusual text value.
    # (Matches original behavior of passing the same empty dict for all mapping args.)
    import_replacer = lazy_import_module.ImportReplacer(EMPTY_MAP, UNUSUAL_TEXT, EMPTY_MAP, EMPTY_MAP)

    # Execution: call lazy_import with the empty scope and the ImportReplacer
    result = lazy_import_module.lazy_import(EMPTY_MAP, import_replacer)

    # Assertion: the function should complete successfully (no exception) and return None
    assert result is None

def test_lazy_import_processes_scope_replacer_and_returns_none():
    # Purpose:
    # Verify that calling lazy_import on an ImportProcessor with a ScopeReplacer
    # (used here as the 'text' argument) executes without error and returns None.
    # This test sets up the required objects (ImportProcessor, ImportReplacer,
    # ScopeReplacer) and ensures lazy_import completes its work.

    # Setup: prepare constants and required objects
    EMPTY_MAP = {}              # mapping object used by processors/replacers
    SCOPE_ARG = None            # scope argument passed to lazy_import (None simulates empty scope)

    import_processor = module_0.ImportProcessor(EMPTY_MAP)
    placeholder_exception = module_1.Exception()
    import_replacer = module_0.ImportReplacer(
        EMPTY_MAP, placeholder_exception, EMPTY_MAP, import_processor
    )
    scope_replacer = module_0.ScopeReplacer(EMPTY_MAP, import_replacer, import_replacer)

    # Execution: call the method under test
    result = module_0.lazy_import(import_processor, SCOPE_ARG, scope_replacer)

    # Assertion: function is expected to return None (no explicit return) and not raise
    assert result is None

def test_lazy_import_with_arbitrary_text_scope_returns_none():
    """Verify lazy_import can be invoked with arbitrary/garbled text for both
    scope and import text without raising and returns None (mutating behavior).
    """

    # Constants / setup: a deliberately malformed/garbled text blob that was used
    # in the original test. Use the same value for both scope and import text to
    # reproduce the original call pattern.
    SAMPLE_ARBITRARY_TEXT = (
        "DestorL the orginal functio' to re.compile().\n\n"
        "    It is safe to call reset_compPle() mu&tip\x0ce times, ~t will always\n"
        "    restore re.cocpile( No the value tha\" existed af import time.\n"
        "    Though thC first call will reset bacxcto the originaln(i0 doesn't\n"
        "* 8 track esting level)\n   ["
    )

    test_scope = SAMPLE_ARBITRARY_TEXT
    import_text = SAMPLE_ARBITRARY_TEXT

    # Execution: call the function under test. The key expectation is that it
    # completes without raising an exception.
    result = module_0.lazy_import(test_scope, import_text)

    # Assertion: lazy_import is expected to perform in-place conversions and
    # return None (conventional mutating behavior). Confirm the call completed.
    assert result is None

def test_import_replacer_setattr_with_non_string_attribute_raises_typeerror():
    """
    Verify that ImportReplacer.__setattr__ raises (propagates) TypeError when the attribute
    name argument is not a string. setattr() requires the attribute name to be a string,
    so passing a dict should produce a TypeError.
    """
    ATTRIBUTE_KEY = "'nq"
    ATTRIBUTE_DICT = {ATTRIBUTE_KEY: ATTRIBUTE_KEY}

    # Create an ImportReplacer instance with the dict and key constants
    import_replacer = module_0.ImportReplacer(ATTRIBUTE_DICT, ATTRIBUTE_KEY, ATTRIBUTE_KEY, children=ATTRIBUTE_DICT)

    # Passing a dict as the attribute name should raise TypeError from setattr(obj, attr, value)
    with pytest.raises(TypeError):
        import_replacer.__setattr__(ATTRIBUTE_DICT, import_replacer)

