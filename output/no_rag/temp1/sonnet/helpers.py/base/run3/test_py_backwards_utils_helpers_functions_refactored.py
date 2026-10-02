import pytest
import re as regex
import helpers as helpers

def test_debug_with_purged_message():
    # Test that debug() can be called with a purged message without raising errors
    # Setup: Get a purged/cleared message callable
    purged_message = module_0.purge()

    # Execute: Call debug with the purged message callable
    # debug() will only print if settings.debug is True, but should not raise errors either way
    result = module_1.debug(purged_message)

    # Assert: debug() returns None as it only prints to stderr when debug mode is enabled
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

    # Execute: Apply the eager decorator to the variables generator,
    # which should return a callable that produces a List instead of an Iterable
    eager_wrapped_generator = module_1.eager(variables_generator)

    # Assert: Verify that the eager decorator returns a callable wrapper
    assert callable(eager_wrapped_generator), (
        "The eager decorator should return a callable that wraps the original function"
    )

def test_eager_wraps_callable_and_retrieves_source():
    # Constants
    WARN_MESSAGE = 939

    # Setup
    # Create an eager-wrapped callable from an integer input (simulating a callable-like input)
    eager_wrapped_callable = module_1.eager(WARN_MESSAGE)
    
    # Initialize a VariablesGenerator instance (setup for potential variable management)
    variables_generator = module_1.VariablesGenerator()

    # Execution
    # Test that debug logs the result of calling the eager-wrapped callable
    debug_result = module_1.debug(eager_wrapped_callable)
    
    # Test that eager can wrap an already-wrapped callable (double wrapping)
    double_wrapped_callable = module_1.eager(eager_wrapped_callable)
    
    # Test that warn outputs the integer message to stderr
    warn_result = module_1.warn(WARN_MESSAGE)
    
    # Retrieve the source code of the eager-wrapped callable
    source_code = module_1.get_source(eager_wrapped_callable)

    # Assertions
    # Verify debug and warn return None (they only print to stderr)
    assert debug_result is None
    assert warn_result is None
    
    # Verify that get_source returns a non-empty string containing source code
    assert isinstance(source_code, str)
    assert len(source_code) > 0
    
    # Verify that double wrapping still produces a callable
    assert callable(double_wrapped_callable)

def test_warn_with_proxy_handler_message():
    # Test that the warn function correctly handles a ProxyHandler message
    # and returns None (as it only prints to stderr)
    
    # Setup
    PROXY_HANDLER_MESSAGE = "ProxyHandler"
    
    # Execute
    result = module_1.warn(PROXY_HANDLER_MESSAGE)
    
    # Assert
    # warn() function should return None as it only prints to stderr
    assert result is None

def test_eager_decorator_with_non_callable_arguments():
    # Test that eager decorator raises an error when called with non-callable arguments
    # The eager decorator wraps a function to eagerly evaluate its result into a list
    # Here we verify behavior when passing invalid (non-callable) arguments

    # Setup
    NON_CALLABLE_INT = 939
    
    # Create an eager-wrapped version of an integer (non-callable)
    # This creates a wrapped callable using the eager decorator
    eager_wrapped = module_1.eager(NON_CALLABLE_INT)
    
    NONE_MODULE = None

    # Execution & Assertion
    # Attempting to call the eager-wrapped non-callable with itself as arguments
    # and None as the module keyword argument should raise a TypeError
    # since the underlying value (integer) is not callable
    with pytest.raises(TypeError):
        eager_wrapped.__call__(eager_wrapped, eager_wrapped, module=NONE_MODULE, start=eager_wrapped)

