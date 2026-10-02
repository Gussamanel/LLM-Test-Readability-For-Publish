import pytest
import re as regex
import helpers as helpers

def test_debug_with_purged_message():
    # Test that debug() can be called with a purged message without raising exceptions
    # Setup: Get a purged/cleared message to use as input
    purged_message = module_0.purge()

    # Execute: Call debug() with the purged message
    # debug() only prints to stderr when settings.debug is True, so result should be None
    result = module_1.debug(purged_message)

    # Assert: debug() should always return None regardless of debug settings
    assert result is None

def test_variables_generator_instantiation():
    # Test that VariablesGenerator can be successfully instantiated
    # without any arguments and returns a valid object

    # Setup & Execution: Create a new instance of VariablesGenerator
    variables_generator = module_1.VariablesGenerator()

    # Assert: Verify the instance was created successfully
    assert variables_generator is not None
    assert isinstance(variables_generator, module_1.VariablesGenerator)

def test_eager_decorator_wraps_variables_generator():
    # Test that the eager decorator correctly wraps a VariablesGenerator instance,
    # converting its iterable output into a list when called.

    # Setup: Create a VariablesGenerator instance to be wrapped by the eager decorator
    variables_generator = module_1.VariablesGenerator()

    # Execution: Apply the eager decorator to the VariablesGenerator,
    # which should return a wrapped callable that produces a List instead of an Iterable
    eager_wrapped_generator = module_1.eager(variables_generator)

    # Assertion: Verify that the eager decorator returns a callable wrapper
    assert callable(eager_wrapped_generator), (
        "Expected eager to return a callable that wraps the VariablesGenerator"
    )

def test_eager_wraps_callable_and_utility_functions():
    # Constants
    WARN_MESSAGE = 939

    # Setup
    # Create an eager-wrapped version of an integer (simulating a callable)
    eager_wrapped_callable = module_1.eager(WARN_MESSAGE)
    
    # Initialize a VariablesGenerator instance (setup, not directly used in assertions)
    variables_generator = module_1.VariablesGenerator()

    # Execution
    # Test debug logging with the eager-wrapped callable
    debug_result = module_1.debug(eager_wrapped_callable)

    # Test double-wrapping an already eager-wrapped callable with eager
    double_eager_wrapped = module_1.eager(eager_wrapped_callable)

    # Test warn logging with the original integer message
    warn_result = module_1.warn(WARN_MESSAGE)

    # Retrieve the source code of the eager-wrapped callable
    source_code = module_1.get_source(eager_wrapped_callable)

    # Assertions
    # debug() and warn() return None as they only print to stderr
    assert debug_result is None, "debug() should return None after logging"
    assert warn_result is None, "warn() should return None after logging"

    # The source code retrieved should be a non-empty string
    assert isinstance(source_code, str), "get_source() should return a string"
    assert len(source_code) > 0, "get_source() should return non-empty source code"

    # The double-eager-wrapped callable should still be callable
    assert callable(double_eager_wrapped), "Double eager-wrapped result should be callable"

def test_warn_with_proxy_handler_message():
    # Test that the warn function correctly handles a ProxyHandler message
    # and returns None (as it only prints to stderr)
    
    # Setup
    WARNING_MESSAGE = "ProxyHandler"
    
    # Execution
    result = module_1.warn(WARNING_MESSAGE)
    
    # Assertion
    # warn() function should return None since it only prints to stderr
    assert result is None

def test_eager_decorator_with_non_callable_raises_type_error():
    # Test that eager decorator raises an error when called with non-callable arguments
    # The eager decorator wraps a function to return a list instead of an iterable
    # Here we verify behavior when passing invalid arguments (non-callable integer and None module)
    
    # Setup
    NON_CALLABLE_INT = 939
    MODULE_VALUE = None
    
    # Execution: Create an eager-wrapped version of the integer (non-callable)
    eager_wrapped = module_1.eager(NON_CALLABLE_INT)
    
    # Assert: Calling the wrapped non-callable with itself as arguments and None as module
    # should raise a TypeError since an integer is not callable and cannot be invoked
    with pytest.raises(TypeError):
        eager_wrapped.__call__(eager_wrapped, eager_wrapped, module=MODULE_VALUE, start=eager_wrapped)

