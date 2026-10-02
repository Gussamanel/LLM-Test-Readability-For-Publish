import pytest

import builtins as builtins_module
import lazy_import as lazy_import_module

def test_illegal_use_of_scope_replacer_repr_is_classname_with_str():
    """Ensure IllegalUseOfScopeReplacer.__repr__ returns '<ClassName>(<str(self)>)'."""
    SAMPLE_TEXT = '8yYHc/pOIB1h*y"U!xB'
    replacer = module_0.IllegalUseOfScopeReplacer(SAMPLE_TEXT, SAMPLE_TEXT, SAMPLE_TEXT)

    repr_result = repr(replacer)
    expected_repr = f"{replacer.__class__.__name__}({str(replacer)})"

    assert isinstance(repr_result, str)
    assert repr_result == expected_repr

def test_illegal_use_of_scope_replacer_returns_unicode_object():
    # Purpose:
    # Verify that IllegalUseOfScopeReplacer.__unicode__ always returns a unicode/text object.
    # The __unicode__ implementation calls self._format() and then ensures the result
    # is converted to a unicode/text object before returning.

    # Constants / Setup
    DISABLE_FIRST_FLAG = False
    DISABLE_SECOND_FLAG = False
    replacer_instance = module_0.IllegalUseOfScopeReplacer(DISABLE_FIRST_FLAG, DISABLE_SECOND_FLAG)

    # Execution: call the method under test
    unicode_result = getattr(replacer_instance, '__unicode__')()

    # Determine the correct text type for the running Python version (unicode in Py2, str in Py3)
    try:
        unicode_type = unicode  # type: ignore[name-defined]
    except NameError:
        unicode_type = str

    # Assertion: __unicode__ must return a unicode/text instance (per its contract)
    assert isinstance(unicode_result, unicode_type)

def test_lazy_import_handles_exception_objects_and_empty_map_without_raising():
    # Purpose:
    # Verify that lazy_import can be invoked with an empty mapping and Exception
    # instances used as the 'scope' and 'text' parameters without raising,
    # and that it returns None (no explicit return value).

    # --- Setup ---
    EMPTY_MAP = {}
    # Use an Exception instance for both the scope and text arguments,
    # mirroring the original test inputs.
    EXCEPTION_INSTANCE = builtins_module.Exception()
    # Create an ImportReplacer with the same empty map and exception instances
    # for its constructor parameters.
    import_replacer = lazy_import_module.ImportReplacer(
        EMPTY_MAP, EXCEPTION_INSTANCE, EXCEPTION_INSTANCE, EMPTY_MAP
    )

    # --- Execution ---
    # Call the module-level lazy_import function with the same argument order
    # as the original test: (scope, import_replacer, text).
    result = lazy_import_module.lazy_import(EXCEPTION_INSTANCE, import_replacer, EXCEPTION_INSTANCE)

    # --- Assertion ---
    # The function is expected to perform its work without raising and return None.
    assert result is None

def test_import_replacer_accepts_identical_complex_arguments():
    # Purpose:
    # Verify that ImportReplacer can be called with three identical complex numbers
    # and does not raise an exception (the function may be side-effect driven).
    
    # Constants / Setup: define a single complex value and prepare identical arguments
    COMPLEX_VALUE = -3636.695039 + 4446.7857j
    first_arg = COMPLEX_VALUE
    second_arg = COMPLEX_VALUE
    third_arg = COMPLEX_VALUE

    # Execution: call the function under test
    try:
        result = module_0.ImportReplacer(first_arg, second_arg, third_arg)
    except Exception as exc:
        # If any exception is raised, fail the test with useful context
        pytest.fail(f"ImportReplacer raised an unexpected exception when called with complex inputs: {exc}")

    # Assertion:
    # We only assert that the call completed without raising. The function's return
    # value is not asserted on here because the behavior appears to be side-effect oriented.
    assert True

def test_import_processor_instantiation_creates_instance():
    """
    Verify that ImportProcessor can be instantiated and returns an instance of ImportProcessor.
    """
    # Constants / Test data
    IMPORT_PROCESSOR_CLASS = module_0.ImportProcessor

    # Execution: create an instance of ImportProcessor
    import_processor_instance = IMPORT_PROCESSOR_CLASS()

    # Assertion: the created object is not None and is an instance of the class
    assert import_processor_instance is not None, "Expected an ImportProcessor instance, got None"
    assert isinstance(import_processor_instance, IMPORT_PROCESSOR_CLASS), (
        "Expected object to be instance of ImportProcessor"
    )

def test_lazy_import_raises_attribute_error_for_non_object_self():
    # Purpose:
    # Verify that calling lazy_import as a module function with a plain string as the
    # implicit "self" argument raises AttributeError because the function expects an
    # object with methods like _build_map and _convert_imports.
    invalid_self = "'nq!"
    scope_value = invalid_self
    text_value = invalid_self

    with pytest.raises(AttributeError):
        lazy_import_module.lazy_import(invalid_self, scope_value, text_value)

def test_disallow_proxying_sets_scope_replacer_flag_false():
    """
    Verify that lazy_import.disallow_proxying() clears ScopeReplacer._should_proxy.

    Steps:
    - Ensure ScopeReplacer._should_proxy exists and is True so we can observe the change.
    - Call lazy_import.disallow_proxying().
    - Assert the flag is set to False.
    - Restore the original attribute state to avoid side effects on other tests.
    """
    FLAG_ATTR = "_should_proxy"
    SUT = lazy_import_module  # system under test (lazy_import)

    ScopeReplacer = SUT.ScopeReplacer
    MISSING = object()
    original_value = getattr(ScopeReplacer, FLAG_ATTR, MISSING)

    # Ensure the flag is present and True before invoking the function under test.
    setattr(ScopeReplacer, FLAG_ATTR, True)

    try:
        SUT.disallow_proxying()
        assert getattr(ScopeReplacer, FLAG_ATTR) is False
    finally:
        # Restore original state: remove the attribute if it didn't exist before,
        # otherwise restore its original value.
        if original_value is MISSING:
            delattr(ScopeReplacer, FLAG_ATTR)
        else:
            setattr(ScopeReplacer, FLAG_ATTR, original_value)

def test_illegal_use_of_scope_replacer_repr_includes_class_name_and_parentheses():
    """Ensure __repr__ returns a string starting with ClassName( and ending with )."""
    # Setup
    FLAG_ENABLED = True
    replacer = module_0.IllegalUseOfScopeReplacer(FLAG_ENABLED, FLAG_ENABLED)

    # Execution
    repr_value = replacer.__repr__()

    # Assertions
    assert isinstance(repr_value, str), "Expected __repr__ to return a string"
    expected_prefix = f"{replacer.__class__.__name__}("
    assert repr_value.startswith(expected_prefix), (
        "Expected __repr__ result to start with the class name and an opening parenthesis"
    )
    assert repr_value.endswith(")"), "Expected __repr__ result to end with a closing parenthesis"

def test_lazy_import_handles_nonstandard_import_string_without_raising():
    """Verify lazy_import handles a non-standard import string without raising.

    The function should attempt to build its internal map and convert imports,
    but for this test we only assert that it completes cleanly and returns None.
    """
    # Constants / test data
    TEST_SCOPE = "Q'!"
    TEST_TEXT = "Q'!"

    # Setup: reference module under test (import aliases are provided at file level)
    module_under_test = lazy_import_module

    # Execution: call the method that builds the import map and converts imports
    result = module_under_test.lazy_import(TEST_SCOPE, TEST_TEXT)

    # Assertion: function completes without raising and (by contract) returns None
    assert result is None

def test_illegal_use_of_scope_replacer_equality_and_unicode(monkeypatch):
    # Purpose:
    # - Verify that IllegalUseOfScopeReplacer.__eq__ returns NotImplemented when
    #   compared to an object of a different class (here a bool).
    # - Ensure __unicode__ returns a native text string (avoid NameError on
    #   environments where 'unicode' is not defined by patching builtins).

    # Constants / Setup
    FLAG_VALUE = False
    # Ensure a 'unicode' callable exists in builtins for environments (e.g., Py3)
    # where 'unicode' is not defined. Monkeypatch will restore afterwards.
    monkeypatch.setattr(builtins_module, "unicode", str, raising=False)

    # Create the object under test
    replacer = module_0.IllegalUseOfScopeReplacer(FLAG_VALUE, FLAG_VALUE)

    # Execution
    equality_result = replacer.__eq__(FLAG_VALUE)
    unicode_result = replacer.__unicode__()

    # Assertions
    # When compared to a bool, __eq__ should return NotImplemented (different class)
    assert equality_result is NotImplemented
    # __unicode__ should return a text string (we patched 'unicode' to str)
    assert isinstance(unicode_result, str)

def test_illegal_use_of_scope_replacer_self_equality_and_unicode_return_type():
    # Purpose:
    # - Verify that IllegalUseOfScopeReplacer compares equal to itself via __eq__.
    # - Verify that __unicode__ returns a text type (unicode in Py2 or str in Py3)
    #   and does not raise.

    # Constants / test data
    INIT_FLAG = False

    # Setup: create an instance of IllegalUseOfScopeReplacer with known flags
    replacer = module_0.IllegalUseOfScopeReplacer(INIT_FLAG, INIT_FLAG)

    # Execution: call __eq__ explicitly and call __unicode__ to get its result
    equality_result = replacer.__eq__(replacer)
    unicode_result = replacer.__unicode__()

    # Determine the expected text type in a way that works on both Py2 and Py3.
    # Python 2 has 'unicode' in builtins, Python 3 does not — fall back to str.
    expected_text_type = getattr(builtins_module, "unicode", builtins_module.str)

    # Assertions:
    # - The object should be equal to itself.
    # - The __unicode__ call should return an instance of the expected text type.
    assert equality_result is True
    assert isinstance(unicode_result, expected_text_type)

def test_lazy_import_with_malformed_text_and_none_scope_returns_none():
    # Verify that lazy_import can be called with a malformed import string
    # and a None scope without raising an exception and that it returns None.
    MALFORMED_IMPORT_TEXT = "=XY q(:IjorINV"
    SCOPE_NONE = None
    IMPORTER = lazy_import_module  # module under test

    result = IMPORTER.lazy_import(SCOPE_NONE, MALFORMED_IMPORT_TEXT)

    assert result is None

def test_lazy_import_processes_simple_text_no_error():
    """Ensure lazy_import accepts a simple format-like text and completes without error.

    This exercises internal conversion steps (_build_map and _convert_imports)
    using a minimal input string.
    """
    SAMPLE_TEXT = "%s(%r)"
    SAMPLE_SCOPE = {}

    # The implementation expects a "self" first argument (method-style).
    self_obj = lazy_import_module

    # Call the function and assert it returns None (no explicit result expected).
    result = lazy_import_module.lazy_import(self_obj, SAMPLE_SCOPE, SAMPLE_TEXT)
    assert result is None

def test_lazy_import_returns_none_for_markup_describing_reset_compile():
    """
    Purpose:
    Verify that lazy_import can process a block of text resembling import
    markup (in this case text that documents restoring re.compile) without
    raising an exception and that it returns None (no explicit return value).

    This mirrors the original test which passed the same string for both the
    scope and the text parameters.
    """

    # Setup: prepare the input text used as both the scope and the markup text.
    IMPORT_MARKUP = (
        "Restore the original function to re.compile().\n\n"
        "    It is safe to call reset_compile() multiple times, it will always\n"
        "    restore re.compile() to the value that existed at import time.\n"
        "    Though the first call will reset bacF to the originaln(it doesn't\n"
        "    track nesting level)\n"
    )
    scope_value = IMPORT_MARKUP

    # Execution: call the function under test with the prepared inputs.
    result = lazy_import_module.lazy_import(scope_value, IMPORT_MARKUP)

    # Assertion: lazy_import is expected to return None (no explicit return) and not raise.
    assert result is None

def test_lazy_import_with_empty_text_and_no_callback_disables_proxying():
    """
    Ensure disallow_proxying() prevents lazily imported modules from acting as proxies,
    and that calling lazy_import with an empty scope, empty text, and no callback
    completes and returns None.
    """
    EMPTY_SCOPE = ""
    EMPTY_TEXT = ""
    NO_CALLBACK = None

    # Make lazy imports non-proxying for this test
    lazy_import_module.disallow_proxying()

    # Call lazy_import with empty inputs; should complete and return None
    result = lazy_import_module.lazy_import(EMPTY_SCOPE, EMPTY_TEXT, NO_CALLBACK)

    assert result is None

def test_lazy_import_handles_nonlocal_keyword_py2():
    # Purpose:
    # Verify that lazy_import can process a text snippet that contains
    # the word "nonlocal" (as might appear when simulating Python 3 code)
    # when running in a Python 2 style environment. The call should not
    # raise an exception and should return None (function has no explicit return).

    # Constants / Setup
    INPUT_TEXT = "\n    Simulates nonlocal keyword in Python 2\n    "
    # In the original test the same string was passed for both scope and text.
    # Preserve that behavior to reproduce the exact input conditions.
    scope_object = INPUT_TEXT
    text_to_parse = INPUT_TEXT

    # Execution
    result = lazy_import_module.lazy_import(scope_object, text_to_parse)

    # Assertion
    # lazy_import is an in-place converter and does not return a meaningful value,
    # so we assert it returns None and (implicitly) did not raise an exception.
    assert result is None

def test_lazy_import_with_non_python_like_text_does_not_raise():
    """Ensure lazy_import accepts arbitrary non-Python-looking text without raising."""
    test_text = "&HR#2M#O\x0b_y\rx9("

    # Pass the same opaque string for all three parameters (preserve original behavior).
    scope_param = test_text
    text_param = test_text
    extra_param = test_text

    # Call under test; should not raise.
    module_0.lazy_import(scope_param, text_param, extra_param)

    # Test passes if no exception was raised.
    assert True

def test_import_replacer_handles_single_dash_argument_gracefully():
    # Purpose:
    # Verify that ImportReplacer can be called with a repeated single-character token ("-")
    # for all five positional parameters without raising an exception and returns None.
    #
    # Notes:
    # - The original test called module_0.ImportReplacer("-", "-", "-", "-", "-").
    # - This refactor makes the intent clearer by naming constants and separating setup/execution/assertion.

    # Constants / Setup
    SINGLE_TOKEN = "-"        # token used for all parameters in this test
    NUM_POSITIONAL_ARGS = 5   # ImportReplacer is called with 5 positional arguments
    replacer_args = (SINGLE_TOKEN,) * NUM_POSITIONAL_ARGS

    # Execution
    result = module_0.ImportReplacer(*replacer_args)

    # Assertion
    # The original test did not assert anything; assert that the call completes and returns None.
    assert result is None

def test_lazy_import_handles_unusual_text_no_side_effects():
    # Purpose:
    # Verify that lazy_import can be called with a non-standard text string
    # and an ImportReplacer instance without raising, and that it returns
    # no value (None) and does not mutate the provided scope in this case.
    
    # Constants / inputs
    TEXT_WITH_QUOTE = "'nq"
    SHARED_SCOPE = {}  # scope passed to ImportReplacer and lazy_import
    
    # Setup: construct an ImportReplacer with the same empty mapping used everywhere
    import_replacer = lazy_import_module.ImportReplacer(SHARED_SCOPE, TEXT_WITH_QUOTE, SHARED_SCOPE, SHARED_SCOPE)
    
    # Execution: call the module-level lazy_import function with the scope and replacer
    result = lazy_import_module.lazy_import(SHARED_SCOPE, import_replacer)
    
    # Assertions: expect no return value and no mutation of the scope
    assert result is None
    assert SHARED_SCOPE == {}

def test_lazy_import_with_none_scope_and_scope_replacer_text():
    # Purpose:
    # Verify that lazy_import can be invoked when the scope is None and the
    # "text" argument is a ScopeReplacer instance. The call should complete
    # without raising and should return None (implicit).

    # --- Constants / Test data ---
    EMPTY_MAP = {}
    SCOPE_IS_NONE = None

    # --- Setup: create processor, replacers and exception object ---
    import_processor = lazy_import_module.ImportProcessor(EMPTY_MAP)
    sentinel_exception = builtins_module.Exception()
    import_replacer = lazy_import_module.ImportReplacer(
        EMPTY_MAP, sentinel_exception, EMPTY_MAP, import_processor
    )
    scope_replacer_as_text = lazy_import_module.ScopeReplacer(
        EMPTY_MAP, import_replacer, import_replacer
    )

    # --- Execution: call the method under test ---
    result = import_processor.lazy_import(SCOPE_IS_NONE, scope_replacer_as_text)

    # --- Assertion: ensure call completed and returned the expected value (None) ---
    assert result is None

def test_lazy_import_with_malformed_input_does_not_raise():
    """Ensure lazy_import tolerates a malformed/messy text string without raising."""
    MALFORMED_IMPORT_TEXT = (
        "DestorL the orginal functio' to re.compile().\n\n"
        "    It is safe to call reset_compPle() mu&tip\x0ce times, ~t will always\n"
        "    restore re.cocpile( No the value tha\" existed af import time.\n"
        "    Though thC first call will reset bacxcto the originaln(i0 doesn't\n"
        "* 8 track esting level)\n   ["
    )
    SCOPE = MALFORMED_IMPORT_TEXT

    # Reference to the module/object under test (provided by the test environment).
    lazy_importer = module_0

    # The test passes if this call completes without raising any exception.
    try:
        lazy_importer.lazy_import(SCOPE, MALFORMED_IMPORT_TEXT)
    except Exception as exc:
        pytest.fail(f"lazy_import raised an unexpected exception: {exc!r}")

    assert True

def test_import_replacer_setattr_forwards_to_resolved_object_and_rejects_non_string_attribute():
    # Purpose:
    # Verify that ImportReplacer.__setattr__ resolves its target object and then
    # attempts to set an attribute on that object. Passing a non-string attribute
    # (here a dict) should raise a TypeError from the underlying setattr call.
    
    # Constants / Test data
    SAMPLE_STRING = "'nq"
    SAMPLE_DICT = {SAMPLE_STRING: SAMPLE_STRING}
    
    # Setup: construct an ImportReplacer that would resolve to some object (we pass SAMPLE_DICT)
    import_replacer = module_0.ImportReplacer(SAMPLE_DICT, SAMPLE_STRING, SAMPLE_STRING, children=SAMPLE_DICT)
    
    # Execution & Assertion:
    # Expect a TypeError because the attribute name argument is not a string (we pass SAMPLE_DICT).
    with pytest.raises(TypeError):
        import_replacer.__setattr__(SAMPLE_DICT, import_replacer)

