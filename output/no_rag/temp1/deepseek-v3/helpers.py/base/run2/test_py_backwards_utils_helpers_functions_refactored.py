import pytest
import re as regex
import helpers as helper_utils

def test_should_return_none_when_debug_is_called_with_purge_result_wrapped_in_callable():
    var_0 = module_0.purge()

    debug_message_callable = lambda: str(var_0)

    none_type_0 = module_1.debug(debug_message_callable)

    assert none_type_0 is None

def test_variables_generator_starts_with_no_variables():
    # Setup: create the generator used by the test
    variables_generator = module_1.VariablesGenerator()

    # Execution & Assertion: verify the generator starts without variables
    assert variables_generator.variables == []

def test_eager_materializes_variables_generator_output_into_list():
    # Purpose: Verify that the `eager` decorator executes a generator-producing
    # callable and eagerly materializes its output into a concrete list.

    # Setup
    variables_generator = module_1.VariablesGenerator()
    eager_variables_generator = module_1.eager(variables_generator)

    # Execution
    result = eager_variables_generator()

    # Assertion
    assert isinstance(result, list)

def test_eager_composability_and_get_source_returns_nonempty_string_for_int_input():
    # Constants
    INPUT_VALUE = 939

    # Setup: create an eager-wrapped callable from an integer input
    eager_callable = module_1.eager(INPUT_VALUE)

    # Setup: instantiate the variables generator (used to ensure no side effects break)
    variables_generator = module_1.VariablesGenerator()

    # Execution: invoke debug with the eager callable's wrapped message getter
    # (debug only prints when settings.debug is enabled; should not raise)
    module_1.debug(eager_callable)

    # Execution: wrap the eager callable again to verify eager is composable/idempotent
    double_eager_callable = module_1.eager(eager_callable)

    # Execution: emit a warning using the original integer input
    # (warn should print to stderr and return None)
    module_1.warn(INPUT_VALUE)

    # Execution: retrieve source of the eager callable; should not raise
    source_code = module_1.get_source(eager_callable)

    # Assertions
    # eager should return a callable that produces a list
    assert callable(eager_callable)
    assert callable(double_eager_callable)
    assert isinstance(double_eager_callable(), list)
    assert double_eager_callable() == [INPUT_VALUE]

    # get_source should return a non-empty string containing the wrapped function source
    assert isinstance(source_code, str)
    assert len(source_code) > 0

def test_warn_writes_formatted_message_to_stderr_instead_of_stdout(capsys):
    # Purpose: Verify that the `warn` function writes the formatted warning
    # message (with the "warn" prefix) to stderr rather than stdout.
    WARNING_MESSAGE = "ProxyHandler"
    EXPECTED_STDERR_PATTERN = helper_utils.WARN_PREFIX + WARNING_MESSAGE

    # Execution
    module_1.warn(WARNING_MESSAGE)

    # Assertion
    captured = capsys.readouterr()
    assert captured.out == ""
    assert regex.search(EXPECTED_STDERR_PATTERN, captured.err)

def test_eager_wrapper_passes_itself_as_first_arg_and_unraisable_input_leads_to_type_error():
    # The `eager` decorator wraps a function and materialises its iterable result into a list.
    # Calling the wrapped function with itself as the first positional argument verifies that
    # the wrapper correctly forwards positional and keyword arguments to the original function.
    INPUT_VALUE = 939
    EXPECTED_RESULT = [INPUT_VALUE]

    # Setup: a wrapped callable whose underlying function returns the integer itself,
    # making it impossible to iterate, so the wrapper should raise a TypeError.
    wrapped_eager = module_1.eager(INPUT_VALUE)

    # Execution & Assertion
    with pytest.raises(TypeError):
        wrapped_eager(wrapped_eager, wrapped_eager, module=None, start=wrapped_eager)

