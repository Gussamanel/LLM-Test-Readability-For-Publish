import pytest
import codetiming_timer as timer

def test_timer_error_can_be_instantiated():
    # Verify that TimerError can be instantiated without any arguments
    # This tests the basic construction of the custom exception class

    # Execution: Create a TimerError instance
    timer_error = timer.TimerError()

    # Assert: Verify the instance was created successfully and is of correct type
    assert isinstance(timer_error, timer.TimerError)

def test_timer_raises_error_when_started_while_already_running():
    """
    Test that a TimerError is raised when attempting to start a timer
    that is already running.
    
    The Timer is first used as a context manager (which calls start internally),
    then explicitly stopped via __exit__. After that, the inner timer reference
    is started, and starting the outer timer again should raise a TimerError
    since it is already running.
    """
    # Setup: Create a new Timer instance and use it as a context manager
    # which internally calls start()
    running_timer = timer.Timer()
    inner_timer_ref = running_timer.__enter__()  # Starts the timer and returns self

    # Execution: Stop the timer via __exit__ and then start the inner reference
    running_timer.__exit__()  # Stops the timer
    inner_timer_ref.start()   # Starts the timer again via the inner reference

    # Assert: Starting the timer while it's already running raises a TimerError
    with pytest.raises(timer.TimerError):
        running_timer.start()  # Should raise TimerError since timer is already running

def test_timer_context_manager_enter_and_exit():
    """
    Test that Timer works correctly as a context manager.
    The __enter__ method should start the timer and return the Timer instance,
    while __exit__ should stop the timer without errors.
    """
    # Setup: Create a new Timer instance
    timer_instance = timer.Timer()

    # Execution: Simulate entering and exiting the context manager
    returned_timer = timer_instance.__enter__()  # Should start the timer and return self
    exit_result = timer_instance.__exit__()       # Should stop the timer and return None

    # Assertion: Verify __enter__ returns the Timer instance and __exit__ returns None
    assert returned_timer is timer_instance, "Timer.__enter__ should return the Timer instance itself"
    assert exit_result is None, "Timer.__exit__ should return None after stopping the timer"

def test_timer_exit_stops_context_manager():
    # Test that __exit__ properly stops the timer when used as a context manager
    
    # Setup: Create timer-related objects
    float_arg = timer.FloatArg()
    timer_error = timer.TimerError()
    test_timer = timer.Timer()
    
    # Execute: Call __exit__ to simulate exiting the context manager
    # __exit__ internally calls self.stop() to halt the timer
    test_timer.__exit__()
    
    # Assertion: No exception should be raised when exiting the context manager
    # The test verifies that __exit__ executes without errors

def test_timer_dict_lacks_context_manager_protocol():
    """
    Test that calling __enter__ on a dict raises an AttributeError,
    since dicts don't have a 'start' method or context manager support.
    This verifies that the context manager protocol requires a proper Timer instance.
    """
    # Setup: Create a Timer with no logger to suppress output
    NO_LOGGER = None
    timer_instance = timer.Timer(logger=NO_LOGGER)

    # Start the timer normally
    timer_instance.start()

    # Setup: Create a dict with a None key mapping to itself,
    # simulating an invalid context manager usage
    invalid_context = {}
    NONE_KEY = None
    invalid_context[NONE_KEY] = invalid_context

    # Execution & Assertion: Attempting to use __enter__ on a dict
    # should raise an AttributeError since dicts don't support 'start()'
    with pytest.raises(AttributeError):
        invalid_context.__enter__()

def test_timer_context_manager_with_float_arg_and_repr():
    """
    Test Timer behavior when used as a context manager, with FloatArg configurations,
    equality comparison, stop functionality, and repr output.
    
    This test verifies:
    - Timer can be used as a context manager via __enter__
    - Timer can be initialized with another timer instance as initial_text
    - Timer equality comparison with an integer returns a result
    - A running timer (entered via context manager) can be stopped
    - Timer can be created with FloatArg as text and a comparison result as initial_text
    - repr() works on both basic and configured Timer instances
    - A Timer with FloatArg text can be started successfully
    """
    # Setup: Create and enter a timer as context manager
    base_timer = timer.Timer()
    running_timer = base_timer.__enter__()  # Starts the timer and returns itself

    NEGATIVE_INT_VALUE = -1092

    # Setup: Create FloatArg instances for timer text configuration
    float_arg_text = timer.FloatArg()
    
    # Create a timer using the running timer instance as initial_text
    timer_with_timer_initial_text = timer.Timer(initial_text=running_timer)
    float_arg_initial = timer.FloatArg()

    # Execution: Compare base timer with a negative integer
    equality_result = base_timer.__eq__(NEGATIVE_INT_VALUE)

    # Execution: Stop the running timer (entered via context manager)
    elapsed_time = running_timer.stop()

    # Setup: Create a timer with FloatArg as text and equality result as initial_text
    timer_with_float_arg = timer.Timer(text=float_arg_text, initial_text=equality_result)

    # Execution: Get repr of both timers
    base_timer_repr = base_timer.__repr__()
    float_arg_timer_repr = timer_with_float_arg.__repr__()

    # Execution: Start the timer configured with FloatArg
    start_result = timer_with_float_arg.start()

    # Assertions
    assert isinstance(elapsed_time, float), "Stopped timer should return elapsed time as float"
    assert isinstance(base_timer_repr, str), "Timer repr should return a string"
    assert isinstance(float_arg_timer_repr, str), "FloatArg timer repr should return a string"
    assert start_result is None, "Timer.start() should return None"

def test_timer_context_manager_equality_and_float_arg_initial_text():
    """
    Test Timer behavior when used as a context manager, verifying:
    - Timer can be started via context manager (__enter__)
    - Timer repr can be used as initial_text for other timers
    - Timer equality comparison with non-timer values returns NotImplemented/False
    - Timer can be stopped after being started via context manager
    - A new Timer with FloatArg text and custom initial_text can be created and started
    """
    INVALID_INT_VALUE = -1092

    # Setup: Create and start a timer using context manager
    base_timer = timer.Timer()
    context_timer = base_timer.__enter__()  # Starts the timer and returns it

    # Get string representation of running timer to use as initial_text
    timer_repr_text = context_timer.__repr__()

    # Create a FloatArg instance for use as timer text
    float_arg_for_text = timer.FloatArg()

    # Create additional timers using the repr string as initial_text
    timer_with_initial_text = timer.Timer(initial_text=timer_repr_text)
    float_arg_for_second_timer = timer.FloatArg()

    # Execute: Compare timer with non-timer integer value (should return NotImplemented/False)
    equality_result = base_timer.__eq__(INVALID_INT_VALUE)

    # Stop the context manager timer and capture elapsed time
    elapsed_time = context_timer.stop()

    # Create a timer with FloatArg as text formatter and repr string as initial_text
    timer_with_float_arg = timer.Timer(text=float_arg_for_text, initial_text=timer_repr_text)

    # Get repr of both timers after stop
    base_timer_repr = base_timer.__repr__()
    float_arg_timer_repr = timer_with_float_arg.__repr__()

    # Start the timer configured with FloatArg text
    timer_with_float_arg.start()

    # Assertions
    assert elapsed_time >= 0, "Elapsed time should be non-negative"
    assert equality_result is NotImplemented or equality_result is False, \
        "Timer equality with non-timer value should return NotImplemented or False"
    assert isinstance(timer_repr_text, str), "Timer repr should return a string"
    assert isinstance(base_timer_repr, str), "Base timer repr should return a string"
    assert isinstance(float_arg_timer_repr, str), "Float arg timer repr should return a string"

def test_timer_with_no_logger_exit_and_dict_start_raises_attribute_error():
    """
    Test that:
    1. A Timer can be started with logger=None without errors.
    2. Using __exit__ properly stops the timer.
    3. Calling start() on a plain dict (which lacks Timer's start logic) raises an AttributeError.
    """
    NO_LOGGER = None

    # Setup: Create a Timer with no logger and start it
    test_timer = timer.Timer(logger=NO_LOGGER)
    test_timer.start()

    # Execution: Use __exit__ to stop the timer (simulating context manager exit)
    test_timer.__exit__()

    # Setup: Create a plain dict and set a None key mapping to itself (non-Timer object)
    plain_dict = {}
    none_key = None
    plain_dict[none_key] = plain_dict

    # Get the value stored at the None key (which is the dict itself)
    retrieved_value = plain_dict[none_key]

    # Verify repr works on retrieved value
    retrieved_value.__repr__()

    # Assert: Calling start() on a dict (not a Timer) raises AttributeError
    with pytest.raises(AttributeError):
        retrieved_value.start()

def test_timer_start_with_complex_initial_text_and_logger():
    """
    Test that a Timer can be started when configured with another Timer instance
    as initial_text and a boolean equality check as logger.
    
    Steps:
    1. Create a base timer and use it as a context manager to get a Timer instance.
    2. Use the equality check result (True) as a logger substitute.
    3. Create nested timers using the context manager timer as initial_text.
    4. Verify that starting the final timer does not raise an error.
    """
    # Setup: Create a base timer and enter context manager
    base_timer = timer.Timer()
    context_timer = base_timer.__enter__()  # Starts the timer and returns self
    
    # Get a truthy value to use as logger (True from equality check)
    is_equal = base_timer.__eq__(base_timer)  # Evaluates to True
    
    # Stop the base timer by exiting the context manager
    base_timer.__exit__()  # Stops the base timer

    # Create a timer with the context_timer instance as initial_text and is_equal as logger
    timer_with_timer_as_text = timer.Timer(initial_text=context_timer, logger=is_equal)
    
    # Create another timer using context_timer as name, timer_with_timer_as_text as initial_text
    timer_with_complex_config = timer.Timer(
        context_timer, 
        initial_text=timer_with_timer_as_text, 
        logger=is_equal
    )

    # Execution: Start the timer with complex configuration
    # This should not raise a TimerError since the timer hasn't been started yet
    timer_with_complex_config.start()

    # Assertion: Implicitly verified by no exception being raised during start()
    assert timer_with_complex_config._start_time is not None

def test_timer_start_stop_and_context_manager():
    """
    Test that a Timer can be started, stopped, and re-entered as a context manager.
    Verifies the full lifecycle of a Timer:
    1. Creating a Timer with a custom name
    2. Starting and stopping the timer to get elapsed time
    3. Using the timer as a context manager (re-entering after stop)
    4. Copying the timer state
    """
    # Constants
    TIMER_NAME = "Timer started"

    # Setup: Create a timer with a custom name
    named_timer = timer.Timer(TIMER_NAME)

    # Execution: Start and stop the timer to measure elapsed time
    named_timer.start()
    elapsed_time = named_timer.stop()

    # Assert: Verify that stop() returns a valid elapsed time (float)
    assert isinstance(elapsed_time, float)
    assert elapsed_time >= 0

    # Execution: Re-use the timer as a context manager after stopping
    # __enter__ calls start() internally and returns the timer instance
    context_timer = named_timer.__enter__()

    # Assert: Verify that __enter__ returns the same timer instance
    assert context_timer is named_timer

    # Execution: Copy the timer state while it is running
    timer_copy = named_timer.copy()

    # Assert: Verify a copy was successfully created
    assert timer_copy is not None

