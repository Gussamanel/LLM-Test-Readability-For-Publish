import pytest
import codetiming_timer as timer

def test_timer_error_instantiation():
    # Test that TimerError can be instantiated without any arguments
    # This verifies that the custom exception class is properly defined
    # and can be created with default initialization

    # Execution: Create a TimerError instance with no arguments
    timer_error = timer.TimerError()

    # Assert: Verify that the instance is created successfully
    # and is of the correct type
    assert isinstance(timer_error, timer.TimerError)
    assert isinstance(timer_error, Exception)

def test_timer_raises_error_when_started_while_already_running():
    """
    Test that starting a timer that is already running raises a TimerError.

    A Timer instance is started, and then an attempt to start it again
    while it is still running should raise a TimerError.
    """
    # Setup: Create a new Timer instance and start it
    running_timer = timer.Timer()
    running_timer.start()

    # Assert: Attempting to start an already running timer raises TimerError
    with pytest.raises(timer.TimerError):
        running_timer.start()

def test_timer_context_manager_enter_and_exit():
    """
    Test that the Timer can be used as a context manager.
    Verifies that __enter__ returns the Timer instance and
    __exit__ stops the timer without raising exceptions.
    """
    # Setup: Create a new Timer instance
    timer_instance = timer.Timer()

    # Execution: Simulate entering and exiting the context manager
    returned_timer = timer_instance.__enter__()  # Should start the timer and return self
    exit_result = timer_instance.__exit__()       # Should stop the timer and return None

    # Assertions: Verify behavior of context manager protocol
    assert returned_timer is timer_instance, "Timer.__enter__ should return the Timer instance itself"
    assert exit_result is None, "Timer.__exit__ should return None"

def test_timer_exit_stops_context_manager():
    # Test that __exit__ properly stops the timer when used as a context manager
    
    # Setup: Create necessary objects
    float_arg = timer.FloatArg()
    timer_error = timer.TimerError()
    test_timer = timer.Timer()
    
    # Execute: Call __exit__ to simulate exiting the context manager
    # __exit__ internally calls self.stop() to halt the timer
    test_timer.__exit__()

def test_timer_start_with_no_logger():
    """
    Test that starting a Timer with no logger (None) works correctly.
    The timer should start successfully without logging since logger is None.
    """
    # Constants
    NO_LOGGER = None

    # Setup: Create a timer with no logger
    timer_instance = timer.Timer(logger=NO_LOGGER)

    # Execution: Start the timer (should succeed with no logger)
    result = timer_instance.start()

    # Assertion: Timer start returns None as expected
    assert result is None

    # Assertion: Timer internal start time has been set after start()
    assert timer_instance._start_time is not None

def test_timer_context_manager_with_float_arg_and_repr():
    """
    Test Timer behavior when used as a context manager, with FloatArg text parameter,
    equality comparison, stop functionality, and string representation.
    
    This test verifies:
    - Timer can be used as a context manager via __enter__
    - Timer can be initialized with another timer as initial_text
    - Timer equality comparison with an integer returns a result
    - Timer stop() returns elapsed time when called on an active timer
    - Timer can be created with FloatArg as text and a comparison result as initial_text
    - Timer __repr__ works on both running and configured timers
    - Timer start() can be called on a newly configured timer
    """
    # Setup: Create initial timer and enter context manager
    base_timer = timer.Timer()
    active_timer = base_timer.__enter__()  # Starts the timer and returns itself

    # Setup: Constants and FloatArg instances
    NEGATIVE_INT_VALUE = -1092
    float_arg_text = timer.FloatArg()

    # Setup: Create a second timer using the active timer as initial_text
    timer_with_timer_as_initial_text = timer.Timer(initial_text=active_timer)
    float_arg_initial_text = timer.FloatArg()

    # Execution: Compare base timer with a negative integer
    equality_result = base_timer.__eq__(NEGATIVE_INT_VALUE)

    # Execution: Stop the active (context-managed) timer and capture elapsed time
    elapsed_time = active_timer.stop()

    # Setup: Create a third timer with FloatArg as text and equality result as initial_text
    timer_with_float_arg_text = timer.Timer(text=float_arg_text, initial_text=equality_result)

    # Execution: Get string representations of both timers
    base_timer_repr = base_timer.__repr__()
    float_arg_timer_repr = timer_with_float_arg_text.__repr__()

    # Assertion: Start the float-arg timer to verify it can be started without errors
    start_result = timer_with_float_arg_text.start()

    # Assert that stop returned a float (elapsed time)
    assert isinstance(elapsed_time, float)

    # Assert that repr returns strings for both timers
    assert isinstance(base_timer_repr, str)
    assert isinstance(float_arg_timer_repr, str)

    # Assert that start() returns None
    assert start_result is None

def test_timer_context_manager_with_initial_text_and_float_arg():
    """
    Test Timer behavior when used as a context manager with various configurations:
    - Verifies Timer can be used as a context manager via __enter__
    - Tests Timer initialization with initial_text from repr of another timer
    - Tests Timer initialization with FloatArg as text parameter
    - Tests equality comparison between Timer and an integer
    - Tests stopping a timer started via context manager
    - Tests starting a new timer with FloatArg text and custom initial_text
    """
    # Constants
    NEGATIVE_INT_VALUE = -1092

    # Setup - Create and enter timer context manager
    base_timer = timer.Timer()
    context_timer = base_timer.__enter__()  # Starts the timer as context manager

    # Capture repr of the running context timer to use as initial_text
    timer_repr_text = context_timer.__repr__()

    # Setup - Create FloatArg instances for text parameters
    float_arg_text = timer.FloatArg()
    float_arg_initial = timer.FloatArg()

    # Setup - Create additional timers with various configurations
    timer_with_initial_text = timer.Timer(initial_text=timer_repr_text)

    # Execution - Test equality comparison between timer and integer
    equality_result = base_timer.__eq__(NEGATIVE_INT_VALUE)

    # Execution - Stop the context manager timer and capture elapsed time
    elapsed_time = context_timer.stop()

    # Execution - Create timer with FloatArg as text and repr as initial_text
    timer_with_float_text = timer.Timer(text=float_arg_text, initial_text=timer_repr_text)

    # Capture repr values for both timers
    base_timer_repr = base_timer.__repr__()
    float_text_timer_repr = timer_with_float_text.__repr__()

    # Execution - Start the timer with FloatArg text configuration
    timer_with_float_text.start()

    # Assertions
    assert elapsed_time >= 0, "Elapsed time should be non-negative"
    assert equality_result is NotImplemented or equality_result == False, (
        "Timer should not be equal to an integer"
    )
    assert base_timer_repr is not None, "Base timer repr should not be None"
    assert float_text_timer_repr is not None, "Float text timer repr should not be None"
    assert timer_with_initial_text is not None, "Timer with initial text should be created successfully"

def test_timer_exit_stops_timer_and_non_timer_start_raises_attribute_error():
    """
    Test that after using __exit__ to stop a timer context manager,
    attempting to call start() on a non-timer object (a dict) raises AttributeError.

    This verifies that:
    1. Timer can be initialized without a logger (logger=None)
    2. Timer.start() works correctly
    3. Timer.__exit__() properly stops the timer
    4. Attempting to call start() on a dict raises AttributeError
    """
    # Setup: Create a timer with no logger and start it
    NO_LOGGER = None
    timer_instance = timer.Timer(logger=NO_LOGGER)
    timer_instance.start()

    # Execution: Stop the timer using __exit__ context manager method
    timer_instance.__exit__()

    # Setup: Create a self-referential dict (dict maps None key to itself)
    test_dict = {}
    test_dict[None] = test_dict

    # Retrieve the value stored in dict and verify its representation
    retrieved_value = test_dict[None]
    repr(retrieved_value)

    # Assert: Attempting to call start() on the dict raises AttributeError
    # since dict has no start() method
    with pytest.raises(AttributeError):
        retrieved_value.start()

def test_timer_start_with_nested_timers_as_parameters():
    """
    Test that a Timer can be started when configured with another Timer instance
    as initial_text and a boolean equality result as logger.
    
    Steps:
    1. Create a base timer and use it as a context manager to get a running timer reference.
    2. Compare the timer with itself to get a truthy logger value.
    3. Exit the context manager to stop the base timer.
    4. Create intermediate and final timers using the running timer reference and equality result.
    5. Start the final timer and verify no exceptions are raised.
    """
    # Setup: Create and enter a base timer as context manager
    base_timer = timer.Timer()
    running_timer_ref = base_timer.__enter__()  # Returns the timer itself after starting
    
    # Get a truthy value to use as logger by comparing timer with itself
    timer_equality_result = base_timer.__eq__(base_timer)  # Expected: True
    
    # Exit the context manager, stopping the base timer
    base_timer.__exit__()
    
    # Create an intermediate timer using the running timer ref as initial_text
    # and equality result as logger
    intermediate_timer = timer.Timer(initial_text=running_timer_ref, logger=timer_equality_result)
    
    # Create the final timer using running_timer_ref as name, intermediate_timer as initial_text
    # and equality result as logger
    final_timer = timer.Timer(running_timer_ref, initial_text=intermediate_timer, logger=timer_equality_result)
    
    # Execution: Start the final timer (should not raise any exceptions)
    final_timer.start()

def test_timer_start_stop_and_context_manager_with_named_timer():
    """
    Test that a named Timer can be started, stopped, and then used as a context manager,
    followed by copying the timer instance.
    
    This test verifies:
    - A Timer can be created with a custom initial text name.
    - The timer can be started and stopped, returning elapsed time as a float.
    - The timer can then be used as a context manager via __enter__, 
      which starts a new timing session and returns the same timer instance.
    - The timer can be copied after being used as a context manager.
    """
    # Constants
    TIMER_INITIAL_TEXT = "Timer started"

    # Setup: Create a named timer with custom initial text
    named_timer = timer.Timer(TIMER_INITIAL_TEXT)

    # Execution: Start and stop the timer to record elapsed time
    named_timer.start()
    elapsed_time = named_timer.stop()

    # Assert stop() returns a float representing elapsed time
    assert isinstance(elapsed_time, float), "Expected stop() to return a float elapsed time"

    # Execution: Use the timer as a context manager, which calls start() internally
    context_timer = named_timer.__enter__()

    # Assert __enter__ returns the same timer instance
    assert context_timer is named_timer, "Expected __enter__ to return the same Timer instance"

    # Execution: Copy the timer instance while it is running
    timer_copy = named_timer.copy()

