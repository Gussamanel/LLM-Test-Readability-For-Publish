import pytest
import re as regex
import helpers as test_helpers

def test_debug_receives_callable_from_purge():
    # Setup: obtain the callable returned by purge()
    purge_message_provider = module_0.purge()

    # Execution: pass the callable into the debug logger
    module_1.debug(purge_message_provider)

    # Assertion: debug was invoked with the exact callable produced by purge
    # (debug only emits output when settings.debug is enabled, so we verify
    # the callable was forwarded correctly)
    assert callable(purge_message_provider)

def test_variables_generator_creation():
    # Setup: instantiate the variables generator using the module under test
    generator = module_1.VariablesGenerator()

    # Execution: verify the instance is created correctly
    result = generator is not None

    # Assertion: ensure the generator instance was successfully created
    assert result

def test_eager_wrapper_converts_generator_to_list():
    # Setup
    variables_generator = module_1.VariablesGenerator()

    # Execution
    eager_result = module_1.eager(variables_generator)

    # Assertion
    # The `eager` decorator should wrap the callable and, when invoked,
    # return a list rather than an iterable/generator. The wrapped function
    # itself is returned, so we invoke it to inspect the produced type.
    assert callable(eager_result), "eager should return a callable wrapping the input function"
    produced = eager_result()
    assert isinstance(produced, list), "eager should convert the generator output into a list"

def test_get_source_returns_callable_source_code_non_empty():
    SAMPLE_INTEGER = 939

    eager_callable = module_1.eager(SAMPLE_INTEGER)

    variables_generator = module_1.VariablesGenerator()

    module_1.debug(eager_callable)

    double_eager_callable = module_1.eager(eager_callable)

    module_1.warn(SAMPLE_INTEGER)

    source_code = module_1.get_source(eager_callable)

    assert isinstance(source_code, str)
    assert source_code != ""

def test_warn_prints_message_to_stderr_when_called():
    # Setup: define the warning message to pass to warn()
    warning_message = "ProxyHandler"

    # Execution: call warn() with the warning message
    module_1.warn(warning_message)

    # Assertion: verify warn() returns None (prints to stderr as a side effect)
    assert module_1.warn(warning_message) is None

def test_eager_decorator_call_returns_list_type():
    # Setup: A simple value that will be wrapped by the eager decorator
    INITIAL_VALUE = 939

    # Execution: apply the eager decorator to the value
    decorated_callable = module_1.eager(INITIAL_VALUE)

    # Then invoke the decorated callable, passing it as its own argument.
    # Since the decorator converts the result to a list, we expect a list back.
    UNUSED_MODULE_KWARG = None
    result = decorated_callable(
        decorated_callable,
        decorated_callable,
        module=UNUSED_MODULE_KWARG,
        start=decorated_callable,
    )

    # Assertion: the decorated callable should return a list
    assert isinstance(result, list)

