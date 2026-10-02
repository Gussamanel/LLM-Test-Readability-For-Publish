import pytest
import re as regex
import helpers as helpers

def test_debug_with_purged_message():
    # Test that debug() can accept and process a callable returned by purge()
    # without raising any exceptions when debug mode may or may not be enabled

    # Setup: Get a callable message getter by purging the module's state
    get_message_callable = module_0.purge()

    # Execute: Pass the callable to debug(), which will invoke it only if debug mode is enabled
    # debug() returns None regardless of whether the message is printed
    result = module_1.debug(get_message_callable)

    # Assert: debug() should always return None
    assert result is None

def test_variables_generator_instantiation():
    # Test that VariablesGenerator can be successfully instantiated
    # without any arguments and creates a valid object instance
    
    # Setup & Execution: Create a new VariablesGenerator instance
    variables_generator = module_1.VariablesGenerator()
    
    # Assert: Verify the instance was created successfully
    assert variables_generator is not None
    assert isinstance(variables_generator, module_1.VariablesGenerator)

def test_eager_decorator_with_variables_generator():
    # Test that the eager decorator correctly wraps a VariablesGenerator instance
    # and returns a callable that produces a list instead of an iterable

    # Setup: Create a VariablesGenerator instance to be wrapped by eager
    variables_generator = module_1.VariablesGenerator()

    # Execution: Apply the eager decorator to the VariablesGenerator instance
    # eager should wrap the generator function to return a List instead of an Iterable
    eager_wrapped_callable = module_1.eager(variables_generator)

    # Assertion: Verify that eager returns a callable (wrapped function)
    assert callable(eager_wrapped_callable), (
        "eager() should return a callable that wraps the given function"
    )

def test_eager_wraps_function_and_debug_warn_get_source():
    # Constants
    WARN_MESSAGE = 939

    # Setup
    # Create an eager-wrapped callable from an integer value (used as a mock callable argument)
    eager_wrapped_callable = module_1.eager(WARN_MESSAGE)
    
    # Initialize a VariablesGenerator instance (used for setup, not directly asserted)
    variables_generator = module_1.VariablesGenerator()

    # Execution
    # Debug the eager-wrapped callable by passing it as a message provider
    debug_result = module_1.debug(eager_wrapped_callable)
    
    # Wrap the already-eager callable with another layer of eager
    double_eager_wrapped_callable = module_1.eager(eager_wrapped_callable)
    
    # Emit a warning using the integer message
    warn_result = module_1.warn(WARN_MESSAGE)
    
    # Retrieve the source code of the eager-wrapped callable
    source_code = module_1.get_source(eager_wrapped_callable)

    # Assertions
    # debug and warn return None as they only print to stderr
    assert debug_result is None
    assert warn_result is None
    
    # get_source should return a non-empty string containing the source code
    assert isinstance(source_code, str)
    assert len(source_code) > 0
    
    # The double-eager wrapped callable should still be callable
    assert callable(double_eager_wrapped_callable)

def test_warn_with_proxy_handler_message():
    # Test that the warn function correctly handles a ProxyHandler message
    # and returns None (as it only prints to stderr)
    
    # Setup
    PROXY_HANDLER_MESSAGE = "ProxyHandler"
    
    # Execute
    result = module_1.warn(PROXY_HANDLER_MESSAGE)
    
    # Assert
    # The warn function should return None since it only prints to stderr
    assert result is None

def test_eager_decorator_with_non_callable_argument():
    # Test that eager decorator raises an error when the wrapped function
    # receives a non-callable (integer) as its function argument and attempts
    # to call it with invalid arguments including None as module parameter

    # Setup
    NON_CALLABLE_INT = 939
    
    # Create an eager-wrapped version of an integer (non-callable)
    # eager() wraps the given argument in a function that converts the result to a list
    eager_wrapped_int = module_1.eager(NON_CALLABLE_INT)
    
    none_module = None

    # Execution & Assertion
    # Calling the eager-wrapped non-callable with itself as arguments should raise an error
    # since the underlying value (939) is not callable and cannot be invoked
    with pytest.raises((TypeError, Exception)):
        eager_wrapped_int.__call__(
            eager_wrapped_int,
            eager_wrapped_int,
            module=none_module,
            start=eager_wrapped_int
        )

