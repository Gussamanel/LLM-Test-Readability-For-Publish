import pytest

import re as regex
import helpers as test_helpers

def test_debug_with_purge_callable_returns_none():
    """
    Purpose:
    Verify that module_1.debug accepts a callable returned by module_0.purge and returns None.
    This ensures the debug wrapper handles message providers (callables) without raising and
    does not return any value.
    """

    # Expected return value from module_1.debug when given a message-provider callable.
    EXPECTED_RETURN = None

    # --- Setup ---
    # Obtain a message-provider callable from module_0.purge().
    # The purge function is expected to return a zero-argument Callable that supplies the debug message.
    purge_message_provider = module_0.purge()

    # Sanity check: the returned object should be callable.
    assert callable(purge_message_provider), "module_0.purge() should return a callable that provides a message"

    # --- Execution ---
    # Call the debug wrapper with the message provider. It might print to stderr when enabled,
    # but its return value is expected to be None regardless of settings.debug.
    debug_return_value = module_1.debug(purge_message_provider)

    # --- Assertion ---
    # Ensure debug returned the expected None value and did not produce a different result.
    assert debug_return_value is EXPECTED_RETURN

def test_variables_generator_instantiation_creates_object():
    """
    Purpose:
    - Verify that the VariablesGenerator class in module_1 can be instantiated.
    - Ensure the returned object is not None and is an instance of the expected class.

    Structure:
    - Setup: define the class under test as a constant for readability.
    - Execution: construct an instance of the class.
    - Assertion: check that the instance was created and has the expected type/structure.
    """
    # Constants / setup
    CLASS_UNDER_TEST = module_1.VariablesGenerator

    # Execution: create an instance of the VariablesGenerator
    variables_generator_instance = CLASS_UNDER_TEST()

    # Assertions: validate the instance was created and is of the expected type
    assert variables_generator_instance is not None, "Constructor returned None instead of an instance"
    assert isinstance(variables_generator_instance, CLASS_UNDER_TEST), (
        f"Expected instance of {CLASS_UNDER_TEST.__name__}, got {type(variables_generator_instance).__name__}"
    )

    # Sanity check: instance should expose a class attribute and basic introspection info
    # (keeps the test resilient even if the public API is minimal)
    assert hasattr(variables_generator_instance, "__class__"), "Instance must have a __class__ attribute"
    assert len(dir(variables_generator_instance)) > 0, "Instance should expose at least some attributes or methods"

def test_eager_wraps_callable_generator_and_returns_list():
    """Verify module_1.eager wraps a generator-like callable and the wrapper returns a list."""
    # Constants
    EXPECTED_RETURN_TYPE = list

    # Arrange: create a generator-like instance and wrap it with eager
    variables_generator = module_1.VariablesGenerator()
    wrapped_callable = module_1.eager(variables_generator)

    # Sanity: eager should return a callable
    assert callable(wrapped_callable), "module_1.eager(...) should return a callable"

    # Act: call the wrapped callable to eagerly consume the iterable
    result = wrapped_callable()

    # Assert: result must be present and be a list (eager consumption)
    assert result is not None, "Wrapped callable should return a value"
    assert isinstance(result, EXPECTED_RETURN_TYPE), "Wrapped callable must return a list"

def test_eager_wrapper_and_source_and_logging(monkeypatch, capsys):
    # Purpose:
    # - Verify module_1.eager wraps a generator to return a list.
    # - Verify wrapping an already-eager function still returns a list.
    # - Verify module_1.get_source returns the wrapper source (contains def wrapped and return list).
    # - Verify module_1.debug prints when settings.debug is True and module_1.warn prints to stderr.
    # - Instantiate VariablesGenerator to ensure it can be constructed without error.

    # --- Constants / Test data ---
    COUNT_A = 3
    COUNT_B = 2
    DEBUG_MESSAGE = "debug-message"
    WARN_MESSAGE = "warn-message"

    # --- Setup: create a simple generator function and replace side-effecting collaborators ---
    def simple_counter(n):
        for i in range(n):
            yield i

    # Replace module_1.messages and module_1.settings so debug/warn produce deterministic output
    class DummyMessages:
        def warn(self, msg):
            return msg

        def debug(self, msg):
            return msg

    class DummySettings:
        debug = True

    monkeypatch.setattr(module_1, "messages", DummyMessages())
    monkeypatch.setattr(module_1, "settings", DummySettings())

    # --- Execution: create eager wrappers and call them ---
    eager_wrapper = module_1.eager(simple_counter)            # wrap generator -> should return lists
    eager_of_eager = module_1.eager(eager_wrapper)            # wrap an already-wrapped callable

    result_a = eager_wrapper(COUNT_A)
    result_b = eager_of_eager(COUNT_B)

    # Call logging helpers that write to stderr
    module_1.debug(lambda: DEBUG_MESSAGE)
    module_1.warn(WARN_MESSAGE)

    # Also get the source for the eager wrapper
    wrapper_source = module_1.get_source(eager_wrapper)

    # Instantiate VariablesGenerator to ensure no construction errors
    variables_generator_instance = module_1.VariablesGenerator()

    # --- Assertions: verify behavior and side-effects ---
    # eager should convert generator output to list with expected contents
    assert isinstance(result_a, list), "eager wrapper must return a list"
    assert result_a == list(range(COUNT_A))

    assert isinstance(result_b, list), "eager(eager(...)) must still return a list"
    assert result_b == list(range(COUNT_B))

    # get_source of the wrapper should include the wrapper function definition and list conversion
    assert regex.search(r"def\s+wrapped\s*\(", wrapper_source), "source should contain the wrapper function definition"
    assert "return list" in wrapper_source, "source should contain the list conversion"

    # stderr should contain both debug and warn messages
    captured = capsys.readouterr()
    assert DEBUG_MESSAGE in captured.err, "debug should write the debug message to stderr when settings.debug is True"
    assert WARN_MESSAGE in captured.err, "warn should write the warn message to stderr"

    # VariablesGenerator instance should have been created
    assert variables_generator_instance is not None

def test_warn_prints_input_message_to_stderr_and_returns_none(capsys):
    """Verify that module_1.warn writes a formatted warning to stderr and returns None."""
    # Arrange
    input_message = "ProxyHandler"

    # Act
    returned_value = module_1.warn(input_message)
    captured = capsys.readouterr()

    # Assert: function returns None
    assert returned_value is None, "warn() should return None"

    # Assert: stderr contains the original input message (use regex for flexible matching)
    assert regex.search(regex.escape(input_message), captured.err), (
        f"Expected stderr to include the message {input_message!r}, but stderr was: {captured.err!r}"
    )

def test_eager_wrap_with_non_callable_raises_type_error_on_invocation():
    # Purpose:
    # Verify that applying the `eager` decorator to a non-callable value produces a wrapper
    # which raises a TypeError when invoked (because the original object is not callable).

    # Constants / fixtures
    NON_CALLABLE = 939
    NO_MODULE = None

    # Setup: create the eager-wrapped "callable" from a non-callable input
    wrapped_callable = module_1.eager(NON_CALLABLE)

    # Execution & Assertion:
    # Invoking the wrapper (using __call__ as in the original test) should raise TypeError
    # since the underlying `fn` (an int) cannot be called.
    with pytest.raises(TypeError):
        wrapped_callable.__call__(wrapped_callable, wrapped_callable, module=NO_MODULE, start=wrapped_callable)

