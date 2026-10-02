import pytest

import re as regex
import helpers as test_helpers

def test_debug_prints_formatted_purge_message_to_stderr(monkeypatch, capsys):
    # Purpose:
    # Verify that module_1.debug calls the messages.debug formatter on the string
    # returned by the callable produced by module_0.purge and prints the result to stderr
    # when settings.debug is enabled. Also ensure debug() returns None.

    # Constants / expected values
    TEST_MESSAGE = "purge invoked"
    FORMATTED_MESSAGE = f"[DEBUG] {TEST_MESSAGE}"
    DEBUG_ENABLED = True

    # Setup: replace module_0.purge with a controlled implementation that returns a callable
    def fake_purge():
        return lambda: TEST_MESSAGE
    monkeypatch.setattr(module_0, "purge", fake_purge, raising=False)

    # Ensure settings.debug is enabled for this test
    monkeypatch.setattr(module_1.settings, "debug", DEBUG_ENABLED, raising=False)

    # Replace the messages.debug formatter to produce a predictable formatted string
    def fake_messages_debug(message: str) -> str:
        return FORMATTED_MESSAGE
    monkeypatch.setattr(module_1, "messages", module_1.messages, raising=False)
    monkeypatch.setattr(module_1.messages, "debug", fake_messages_debug, raising=False)

    # Execution
    purge_callable = module_0.purge()            # obtain the callable under test
    result = module_1.debug(purge_callable)      # exercise debug with the callable

    # Assertion: debug should return None and write the formatted message to stderr
    assert result is None
    captured = capsys.readouterr()
    assert FORMATTED_MESSAGE in captured.err

def test_variables_generator_instantiation_creates_valid_instance():
    """
    Verify VariablesGenerator can be instantiated and produces an object of the expected class
    with the correct runtime class name.
    """
    # Expectations
    CLASS_UNDER_TEST = module_1.VariablesGenerator
    EXPECTED_CLASS_NAME = "VariablesGenerator"

    # Instantiate
    variables_generator_class = CLASS_UNDER_TEST
    variables_generator_instance = variables_generator_class()

    # Assertions
    assert variables_generator_instance is not None, "Instantiation returned None"
    assert isinstance(variables_generator_instance, variables_generator_class), (
        "Created object is not an instance of VariablesGenerator"
    )
    assert variables_generator_instance.__class__.__name__ == EXPECTED_CLASS_NAME, (
        f"Expected class name '{EXPECTED_CLASS_NAME}', "
        f"got '{variables_generator_instance.__class__.__name__}'"
    )

def test_eager_decorator_converts_generator_callable_to_list_and_preserves_wrapped_reference():
    """
    Purpose:
    - Verify that module_1.eager wraps a generator-like callable and returns a new callable
      that, when invoked, produces a list (materialized sequence) instead of an iterator.
    - Ensure the decorator preserves a reference to the original callable via __wrapped__.
    """

    # Constants for the test
    EXPECTED_RESULT_TYPE = list

    # ---------------------------
    # Setup
    # ---------------------------
    # Create the generator-like callable instance (the object to be wrapped).
    generator_callable = module_1.VariablesGenerator()

    # Wrap the generator-like callable with the eager decorator which should produce a callable
    # that returns a list when invoked.
    eager_wrapper = module_1.eager(generator_callable)

    # Basic sanity: the wrapper should be callable and should expose the original via __wrapped__
    assert callable(eager_wrapper), "The result of eager(...) must be callable"
    assert getattr(eager_wrapper, "__wrapped__", None) is generator_callable, (
        "The eager wrapper should preserve the original callable via __wrapped__"
    )

    # ---------------------------
    # Execution
    # ---------------------------
    # Call the wrapped callable to get the "eager" result (should be a list).
    eager_result = eager_wrapper()

    # For comparison, obtain the expected result by explicitly materializing the original callable's iterable.
    # Using list(...) ensures we compare materialized sequences rather than generator objects.
    expected_result = list(generator_callable())

    # ---------------------------
    # Assertions
    # ---------------------------
    # The eager wrapper must return a list and match the explicitly materialized sequence.
    assert isinstance(eager_result, EXPECTED_RESULT_TYPE), "Eager wrapper must return a list"
    assert eager_result == expected_result, "Eager wrapper result must equal list(...) of the original iterable"

def test_eager_wraps_generator_and_supporting_debug_warn_and_get_source():
    # Purpose:
    # - Verify that module_1.eager converts a generator function into a callable that
    #   returns a list of yielded items.
    # - Exercise module_1.debug and module_1.warn to ensure they run without raising.
    # - Ensure module_1.get_source can retrieve the source code of the wrapped function.
    #
    # This test separates setup, execution and assertions and uses descriptive names.

    # --- Constants / expected values ---
    SAMPLE_WARNING_MESSAGE = "939"
    EXPECTED_LIST_FROM_GENERATOR = [1, 2]
    DEBUG_MESSAGE = "debug-message"

    # --- Setup ---
    # A simple generator function to be wrapped by eager
    def simple_generator():
        yield 1
        yield 2

    # Create an eager-wrapped callable from the generator
    eager_wrapped_callable = module_1.eager(simple_generator)

    # Instantiate supporting object used by other tests / code paths
    variables_generator_instance = module_1.VariablesGenerator()

    # --- Execution ---
    # Call debug with a callable that returns a string (should be a no-op when settings.debug is False)
    debug_result = module_1.debug(lambda: DEBUG_MESSAGE)

    # Call warn with a string message (prints to stderr) and ensure it doesn't raise
    warn_result = module_1.warn(SAMPLE_WARNING_MESSAGE)

    # Execute the eager-wrapped callable to obtain the list version of the generator's output
    result_list = eager_wrapped_callable()

    # Retrieve the source code for the wrapped callable to assert it looks like the eager wrapper
    wrapped_source = module_1.get_source(eager_wrapped_callable)

    # --- Assertions ---
    # The VariablesGenerator instance should be of the correct type
    assert isinstance(variables_generator_instance, module_1.VariablesGenerator)

    # The eager wrapper should have converted the generator output to a list with expected contents
    assert result_list == EXPECTED_LIST_FROM_GENERATOR

    # debug and warn are logging helpers that return None (they print to stderr). Ensure they did not return values.
    assert debug_result is None
    assert warn_result is None

    # The source of the wrapped callable should contain the eager wrapper behavior (calls list on the inner fn)
    assert regex.search(r"return\s+list\s*\(", wrapped_source) is not None

def test_warn_writes_formatted_message_to_stderr(monkeypatch, capsys):
    """
    Purpose:
    - Verify that module_1.warn formats the provided message via module_1.messages.warn
      and writes the result to stderr.
    - Ensure the function returns None (its documented behavior).
    """

    # Constants / test data
    TEST_MESSAGE = "ProxyHandler"
    # Define a deterministic formatted string so the test does not rely on the real formatting implementation
    EXPECTED_FORMATTED_MESSAGE = f"[TEST-WARN] {TEST_MESSAGE}"

    # Setup: make messages.warn return a predictable formatted string
    # This isolates the test to only exercise module_1.warn's printing behavior.
    monkeypatch.setattr(module_1.messages, "warn", lambda msg: EXPECTED_FORMATTED_MESSAGE)

    # Execution: call the function under test
    result = module_1.warn(TEST_MESSAGE)

    # Assertion: capture stderr and verify output and return value
    stderr_output = capsys.readouterr().err
    assert result is None  # warn should not return a value
    # The formatted message produced by messages.warn should have been printed to stderr
    assert EXPECTED_FORMATTED_MESSAGE in stderr_output

def test_eager_raises_type_error_when_wrapped_object_is_not_callable():
    """
    Verify that module_1.eager returns a callable wrapper even when given a non-callable object,
    and that invoking that wrapper raises a TypeError because the original object is not callable.
    """
    # Arrange: a non-callable value (an int)
    NON_CALLABLE_OBJECT = 939

    # Act: create the eager wrapper around the non-callable value.
    # module_1.eager should return a callable wrapper object, but the wrapped value itself is not callable.
    wrapped_callable = module_1.eager(NON_CALLABLE_OBJECT)

    # Assert: attempting to call the wrapper in the same shape as the original test should raise TypeError.
    # Use the explicit __call__ invocation and pass arguments to reproduce the failure mode.
    with pytest.raises(TypeError):
        wrapped_callable.__call__(wrapped_callable, wrapped_callable, module=None, start=wrapped_callable)

