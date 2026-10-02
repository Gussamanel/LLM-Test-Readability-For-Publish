import pytest

import re as regex
import helpers as helpers_module

def test_debug_accepts_purge_callable_and_returns_none():
    """
    Verify that module_0.purge() returns a callable (a get_message provider)
    and that module_1.debug accepts that callable and returns None.
    """
    # Expected return value from module_1.debug
    EXPECTED_DEBUG_RETURN = None

    # Obtain the callable produced by purge()
    purge_result = module_0.purge()

    # Pre-condition: purge() should return a callable
    assert callable(purge_result), "module_0.purge() must return a callable that produces a message string"

    # Execute debug with the callable and verify it returns None
    debug_return = module_1.debug(purge_result)
    assert debug_return is EXPECTED_DEBUG_RETURN

def test_variables_generator_instantiation_creates_valid_instance():
    # Purpose:
    # Verify that the VariablesGenerator class can be instantiated and returns
    # a valid object of the expected type (sanity check of constructor).
    
    # Constants / Test data
    VARIABLES_GENERATOR_CLASS = module_1.VariablesGenerator

    # Setup
    # (No special preconditions required beyond the class being importable.)
    
    # Execution
    generator_instance = VARIABLES_GENERATOR_CLASS()

    # Assertion
    # Ensure an object was created and it's an instance of the expected class.
    assert generator_instance is not None, "VariablesGenerator() returned None instead of an instance"
    assert isinstance(generator_instance, VARIABLES_GENERATOR_CLASS), (
        "VariablesGenerator() did not return an instance of the expected class"
    )

def test_eager_wraps_callable_generator_and_returns_list():
    # Purpose:
    # Verify that module_1.eager wraps a callable that yields an iterable
    # and produces a new callable that returns a list when invoked.
    #
    # This test checks:
    # - the returned object is callable
    # - invoking the wrapped callable returns a list
    # - repeated invocations also return lists (i.e., wrapper is reusable)

    # --- Setup ---
    ORIGINAL_GENERATOR_CALLABLE = module_1.VariablesGenerator()
    WRAPPED_CALLABLE = module_1.eager(ORIGINAL_GENERATOR_CALLABLE)

    # Constants for assertions
    EXPECTED_RETURN_TYPE = list

    # --- Execution ---
    first_result = WRAPPED_CALLABLE()
    second_result = WRAPPED_CALLABLE()

    # --- Assertions ---
    # The wrapper should be a callable distinct from the original generator callable
    assert callable(WRAPPED_CALLABLE)
    assert WRAPPED_CALLABLE is not ORIGINAL_GENERATOR_CALLABLE

    # Each invocation of the wrapped callable should return a list
    assert isinstance(first_result, EXPECTED_RETURN_TYPE)
    assert isinstance(second_result, EXPECTED_RETURN_TYPE)

def test_eager_wrap_debug_warn_and_get_source_flow():
    # This test verifies a small integration flow:
    # - module_1.eager returns a callable when given a target (even if the target is not a function here),
    # - module_1.debug and module_1.warn return None (they are side-effecting functions),
    # - module_1.get_source can retrieve the textual source of the wrapped callable.
    # The test separates setup, execution and assertions for clarity.

    # --- Setup ---
    SAMPLE_INT = 939  # constant used as the input to eager/warn/debug
    eager_wrapper = module_1.eager  # function under test that wraps callables to eagerly return lists
    VariablesGeneratorClass = module_1.VariablesGenerator  # class used in setup to exercise module API

    # create an instance of VariablesGenerator to ensure module API constructs work
    variables_generator = VariablesGeneratorClass()

    # --- Execution ---
    # Wrap the integer with eager. eager returns a callable (the wrapped function).
    wrapped_fn = eager_wrapper(SAMPLE_INT)

    # Call debug with the wrapped function (debug prints only when settings.debug is True).
    debug_result = module_1.debug(wrapped_fn)

    # Wrap the already-wrapped function again with eager to ensure double-wrapping still yields a callable.
    double_wrapped_fn = eager_wrapper(wrapped_fn)

    # Call warn with the sample integer (warn prints a message and returns None).
    warn_result = module_1.warn(SAMPLE_INT)

    # Retrieve the source code of the first wrapped function to ensure get_source works on such callables.
    source_text = module_1.get_source(wrapped_fn)

    # --- Assertions ---
    # eager should produce callables (functions)
    assert callable(wrapped_fn), "eager(...) should return a callable"
    assert callable(double_wrapped_fn), "eager(...) called on a wrapped callable should still return a callable"

    # VariablesGenerator instance should be of the expected type
    assert isinstance(variables_generator, VariablesGeneratorClass), "VariablesGenerator constructor should return an instance"

    # debug and warn are side-effecting helpers that should return None
    assert debug_result is None, "debug(...) is expected to return None"
    assert warn_result is None, "warn(...) is expected to return None"

    # get_source should return a string representation of the function's source and contain the wrapper function name
    assert isinstance(source_text, str), "get_source(...) should return a string"
    assert ("def wrapped" in source_text) or ("def wrapped(" in source_text), "get_source(...) should return source containing the wrapped function definition"

def test_warn_logs_message_to_stderr_and_returns_none(capsys):
    # Purpose:
    # Verify that module_1.warn prints a warning message to stderr and returns None.

    # Constants / Setup
    TEST_MESSAGE = "ProxyHandler"
    EXPECTED_SUBSTRING = TEST_MESSAGE  # we expect the original message to appear in the logged output

    # Execution: call the function under test
    result = module_1.warn(TEST_MESSAGE)

    # Capture output written to stdout/stderr by the function
    captured = capsys.readouterr()
    stderr_output = captured.err
    stdout_output = captured.out

    # Assertions
    # - function should return None
    assert result is None, "warn should return None"
    # - nothing should be printed to stdout
    assert stdout_output == "", "warn should not print to stdout"
    # - the provided message (or containing substring) should appear in stderr output
    assert EXPECTED_SUBSTRING in stderr_output, f"stderr should contain the message substring: {EXPECTED_SUBSTRING}"

def test_eager_raises_typeerror_when_wrapped_object_is_not_callable():
    # Purpose:
    # Verify that module_1.eager raises a TypeError when the wrapped "fn" is not callable.
    # eager expects a callable that returns an iterable; wrapping a non-callable should fail at call time.

    # Constants / setup inputs
    NON_CALLABLE = 939
    POSITIONAL_ARGS = (object(), object())

    # Setup: create the wrapped callable using a non-callable value
    wrapped = module_1.eager(NON_CALLABLE)

    # Prepare keyword arguments similar to the original test (module=None, start=wrapped)
    keyword_args = {"module": None, "start": wrapped}

    # Exercise + Assert: calling the wrapped object should raise a TypeError because the underlying fn is not callable
    with pytest.raises(TypeError) as exc_info:
        # Use __call__ to mirror the original invocation style
        wrapped.__call__(*POSITIONAL_ARGS, **keyword_args)

    # Verify the error message indicates the object is not callable
    assert regex.search(r"not callable", str(exc_info.value), regex.IGNORECASE) is not None

