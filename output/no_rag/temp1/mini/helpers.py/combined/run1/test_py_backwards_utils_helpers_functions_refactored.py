import pytest

import re as regex
import helpers as test_helpers

def test_debug_uses_message_callable_and_prints_to_stderr_when_debug_enabled(monkeypatch, capsys):
    """
    Purpose:
    - Verify that module_1.debug accepts a callable (produced by module_0.purge()),
      invokes the callable via messages.debug, prints the formatted message to stderr
      when settings.debug is True, and returns None.
    """

    # Constants and expected formatting
    DEBUG_ENABLED = True
    FORMATTED_PREFIX = "DEBUG: "

    # -------- Setup --------
    # Obtain the message-producing callable from module_0.purge()
    message_callable = module_0.purge()

    # Ensure settings.debug is enabled for this test
    monkeypatch.setattr(module_1.settings, "debug", DEBUG_ENABLED)

    # Replace messages.debug with a deterministic formatter that calls the provided callable
    def fake_messages_debug(get_message_callable):
        # Call the provided callable to obtain the underlying message string
        return FORMATTED_PREFIX + get_message_callable()

    monkeypatch.setattr(module_1.messages, "debug", fake_messages_debug)

    # -------- Execution --------
    # Call the debug function under test and capture its return value
    result = module_1.debug(message_callable)

    # Capture stderr output produced by module_1.debug
    captured = capsys.readouterr()

    # -------- Assertions --------
    # debug has no return value (should be None)
    assert result is None

    # The stderr output should contain the formatted message produced by fake_messages_debug
    expected_message = FORMATTED_PREFIX + message_callable()
    assert expected_message in captured.err

def test_variables_generator_initialization_and_repr_contains_class_name():
    # Purpose:
    # - Verify that VariablesGenerator can be instantiated.
    # - Verify its string representation includes the class name.

    # Arrange
    CLASS_UNDER_TEST = module_1.VariablesGenerator
    REPR_NAME_PATTERN = regex.compile(r"VariablesGenerator")

    # Act
    variables_generator = CLASS_UNDER_TEST()
    repr_text = repr(variables_generator)

    # Assert
    assert variables_generator is not None, "Expected VariablesGenerator() to return a non-None instance"
    assert isinstance(variables_generator, CLASS_UNDER_TEST), "Instance is not of type VariablesGenerator"
    assert REPR_NAME_PATTERN.search(repr_text), (
        "Expected the string representation of VariablesGenerator to include the class name; got: "
        f"{repr_text}"
    )

def test_eager_converts_generator_callable_to_list_and_returns_fresh_lists():
    # Purpose:
    # Verify that module_1.eager wraps a generator-producing callable so that:
    #  - the wrapped callable returns a list (materialized iterable) instead of an iterator
    #  - each call to the wrapped callable produces a fresh list object with the same contents

    # Constants
    EXPECTED_RETURN_TYPE = list

    # Setup: create the generator-producing callable and wrap it with eager
    variables_generator_factory = module_1.VariablesGenerator  # callable that yields values when called
    eager_wrapped_callable = module_1.eager(variables_generator_factory)

    # Execution: call the eager-wrapped callable multiple times and also materialize the original generator
    first_result = eager_wrapped_callable()
    second_result = eager_wrapped_callable()
    direct_materialized_from_factory = list(variables_generator_factory())

    # Assertions:
    # - Wrapped callable returns a list
    assert isinstance(first_result, EXPECTED_RETURN_TYPE)
    assert isinstance(second_result, EXPECTED_RETURN_TYPE)

    # - Contents match what the original generator would produce when materialized
    assert first_result == direct_materialized_from_factory
    assert second_result == direct_materialized_from_factory

    # - Each call returns a new list object (not the same identity), ensuring no shared mutable state
    assert first_result is not second_result

def test_wrap_generator_with_eager_and_inspect_source():
    """
    Verify that:
    - module_1.eager converts a generator function into a callable that returns a list
    - module_1.debug and module_1.warn accept simple callables/values without error
    - module_1.get_source returns the original generator source containing 'yield'
    """
    SAMPLE_NUMBER = 939
    EXPECTED_STRINGS = [str(SAMPLE_NUMBER), "end"]

    def simple_generator():
        # simple generator that yields two values (one derived from SAMPLE_NUMBER)
        yield str(SAMPLE_NUMBER)
        yield "end"

    variables_generator = module_1.VariablesGenerator()

    # Wrap the generator eagerly (should produce a callable that returns a list)
    eager_wrapper = module_1.eager(simple_generator)
    # Exercise debug and warn APIs with simple inputs
    module_1.debug(lambda: f"debug: wrapping generator for {SAMPLE_NUMBER}")
    module_1.warn(str(SAMPLE_NUMBER))

    # Execute the wrapped generator and inspect the original source
    result_list = eager_wrapper()
    source_text = module_1.get_source(simple_generator)

    # Assertions
    assert isinstance(result_list, list), "eager wrapped function should return a list"
    assert result_list == EXPECTED_STRINGS, "wrapped generator should produce the expected list contents"
    assert isinstance(source_text, str) and "yield" in source_text, "get_source should return generator source containing 'yield'"
    assert variables_generator is not None, "VariablesGenerator instance should be created successfully"

def test_warn_prints_message_to_stderr(capsys):
    """
    Verify that module_1.warn writes a representation of the provided message to stderr
    and returns None.
    """
    # Arrange
    TEST_MESSAGE = "ProxyHandler"

    # Act: call the function and capture stderr output
    result = module_1.warn(TEST_MESSAGE)
    captured = capsys.readouterr()

    # Assert: function returns None and the message appears in stderr
    assert result is None
    assert regex.search(regex.escape(TEST_MESSAGE), captured.err) is not None, (
        "Expected the provided message to be printed to stderr"
    )

def test_eager_wrapped_with_non_callable_raises_type_error():
    # Purpose:
    # Verify that wrapping a non-callable with `eager` still produces a callable wrapper,
    # but invoking that wrapper will fail because the original object is not callable.
    #
    # Setup:
    # Use a non-callable (an int) as the "function" passed to eager.
    NON_CALLABLE_FUNCTION = 939
    wrapped_callable = module_1.eager(NON_CALLABLE_FUNCTION)

    # Execution & Assertion:
    # Calling the wrapper (here invoked via its __call__ method) should attempt to call
    # the original non-callable and raise a TypeError. Pass the wrapper itself as both
    # positional and keyword arguments to mirror the original test's argument structure.
    with pytest.raises(TypeError):
        wrapped_callable.__call__(wrapped_callable, wrapped_callable, module=None, start=wrapped_callable)

