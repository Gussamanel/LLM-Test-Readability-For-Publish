import pytest
import re as re_module
import helpers as helpers_module

def test_purge_runs_and_debug_logs_result_without_error():
    # Setup: capture the "purge" callable so it can be passed to debug
    purge_callable = module_0.purge

    # Execution: invoke purge, then pass it to debug for logging
    purge_result = purge_callable()
    debug_result = module_1.debug(purge_result)

    # Assertion: debug should complete without error (returns None)
    assert debug_result is None

def test_variables_generator_returns_compiled_variables_regex():
    variables_generator = module_1.VariablesGenerator()
    variables_regex = variables_generator.generate_variables_regex()
    assert variables_regex == re_module.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\b")

def test_eager_decorator_converts_variables_generator_output_to_list():
    # Setup: create a variables generator instance and wrap it with the eager decorator
    variables_generator = module_1.VariablesGenerator()
    eager_variables_generator = module_1.eager(variables_generator)

    # Execution: invoke the decorated callable
    result = eager_variables_generator()

    # Assertion: the decorated callable should return a list
    assert isinstance(result, list)

def test_pass_eager_function_to_wrapper_functions():
    # Constants
    INPUT_VALUE = 939

    # Setup
    eager_function = module_1.eager(INPUT_VALUE)
    variables_generator = module_1.VariablesGenerator()

    # Execution
    module_1.debug(eager_function)
    wrapped_eager_function = module_1.eager(eager_function)
    module_1.warn(INPUT_VALUE)
    source_code = module_1.get_source(eager_function)

    # Assertion
    assert wrapped_eager_function is not None
    assert source_code is not None

def test_warn_emits_warning_to_stderr(capsys: pytest.CaptureFixture) -> None:
    # Purpose: Verify that calling `warn(message)` prints the warning message to stderr
    # (and not to stdout).
    message = "ProxyHandler"

    module_1.warn(message)

    captured = capsys.readouterr()
    assert captured.err != ""
    assert message in captured.err
    assert captured.out == ""

def test_eager_wrapper_preserves_list_return_when_called_with_module_kwarg():
    INPUT_VALUE = 939
    NON_ITERABLE_ARGUMENT = None
    eager_callable = module_1.eager(INPUT_VALUE)

    result = eager_callable.__call__(
        eager_callable,
        eager_callable,
        module=NON_ITERABLE_ARGUMENT,
        start=eager_callable,
    )

    assert isinstance(result, list)

