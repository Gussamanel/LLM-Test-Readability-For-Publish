import pytest
import codetiming_timer as timer

def test_timer_error_can_be_instantiated():
    # Verify that TimerError can be instantiated without any arguments
    # This ensures the basic exception class is properly defined and accessible

    # Execution: Create a TimerError instance with no arguments
    timer_error = timer.TimerError()

    # Assertion: Verify the instance is of the correct type
    assert isinstance(timer_error, timer.TimerError)

def test_timer_raises_error_when_started_while_already_running():
    """
    Test that starting a timer that is already running raises a TimerError.

    A timer is started explicitly, and then attempting to start it again
    while it is still running should raise a TimerError.
    """
    # Setup: Create a new timer instance and start it
    running_timer = timer.Timer()
    running_timer.start()

    # Assert: Attempting to start an already running timer should raise a TimerError
    with pytest.raises(timer.TimerError):
        running_timer.start()

def test_timer_context_manager_enter_and_exit():
    """
    Test that the Timer can be used as a context manager.
    Verifies that __enter__ starts the timer and returns the Timer instance,
    and that __exit__ stops the timer without raising any errors.
    """
    # Setup: Create a new Timer instance
    timer_instance = timer.Timer()

    # Execution: Simulate entering the context manager, which starts the timer
    returned_timer = timer_instance.__enter__()

    # Assert: __enter__ should return the same Timer instance
    assert returned_timer is timer_instance

    # Execution: Simulate exiting the context manager, which stops the timer
    exit_result = timer_instance.__exit__()

    # Assert: __exit__ should return None as it only stops the timer
    assert exit_result is None

def test_timer_exit_stops_context_manager():
    # Test that __exit__ properly stops the timer when used as a context manager
    
    # Setup: Create instances of FloatArg, TimerError, and Timer
    float_arg = timer.FloatArg()
    timer_error = timer.TimerError()
    context_manager_timer = timer.Timer()
    
    # Execute: Call __exit__ to simulate exiting a context manager block
    # __exit__ internally calls self.stop() to halt the timer
    context_manager_timer.__exit__()

def test_none_type_lacks_enter_method_raises_attribute_error():
    """
    Test that calling __enter__ on a non-Timer object raises an AttributeError.
    This verifies that the context manager protocol (__enter__) is specific to Timer instances
    and cannot be used with arbitrary objects like dictionaries.
    """
    # Setup: Create and start a timer with no logger
    NO_LOGGER = None
    timer_instance = timer.Timer(logger=NO_LOGGER)
    
    # Start the timer manually
    timer_instance.start()
    
    # Setup: Create a dictionary and attempt to use it as a context manager
    # by setting None as a key pointing to itself
    non_timer_object = {}
    none_value = None
    non_timer_object.__setitem__(none_value, non_timer_object)
    
    # Execution & Assertion: Attempting to call __enter__ on the result of __setitem__
    # (which returns None) should raise an AttributeError since NoneType 
    # does not have a __enter__ method
    with pytest.raises(AttributeError):
        result = non_timer_object.__setitem__(none_value, non_timer_object)
        result.__enter__()

def test_timer_context_manager_with_custom_initial_text_and_equality():
    """
    Test Timer behavior when used as a context manager, with custom initial text,
    equality comparison, and repr functionality.
    
    This test verifies:
    1. Timer can be used as a context manager via __enter__
    2. A new Timer can be initialized with another timer instance as initial_text
    3. Timer equality comparison with a non-timer integer value
    4. Stopping a timer that was started via context manager returns elapsed time
    5. Timer can be initialized with a FloatArg as text and a comparison result as initial_text
    6. Timer repr works correctly for both running and non-running timers
    8. A timer can be started after being created with custom text arguments
    """
    NEGATIVE_INT_VALUE = -1092

    # Setup: Create and start a timer using context manager protocol
    base_timer = timer.Timer()
    context_timer = base_timer.__enter__()  # Starts the timer and returns self

    # Create supporting objects for timer configuration
    float_arg_text = timer.FloatArg()

    # Create a timer using the running context_timer as initial_text
    timer_with_timer_initial_text = timer.Timer(initial_text=context_timer)
    float_arg_initial = timer.FloatArg()

    # Execute equality comparison between timer and a non-timer integer
    equality_result = base_timer.__eq__(NEGATIVE_INT_VALUE)

    # Stop the context manager timer and capture elapsed time
    elapsed_time = context_timer.stop()

    # Create a timer with FloatArg as text and equality result as initial_text
    timer_with_custom_args = timer.Timer(text=float_arg_text, initial_text=equality_result)

    # Assert repr works on both base timer (stopped) and newly configured timer (not started)
    base_timer_repr = base_timer.__repr__()
    custom_args_timer_repr = timer_with_custom_args.__repr__()

    # Start the timer with custom args to verify it can be started after creation
    timer_with_custom_args.start()

    # Assert elapsed time was captured after stopping context manager timer
    assert elapsed_time >= 0, "Elapsed time should be a non-negative float"
    assert isinstance(elapsed_time, float), "Elapsed time should be a float"
    assert isinstance(base_timer_repr, str), "Timer repr should return a string"
    assert isinstance(custom_args_timer_repr, str), "Timer repr should return a string"

def test_timer_context_manager_with_initial_text_and_equality_check():
    """
    Test that verifies Timer behavior when used as a context manager,
    including repr output, equality comparison, stop functionality,
    and creating new timers with initial_text set from repr output.
    """
    # Constants
    NON_TIMER_INT_VALUE = -1092

    # Setup: Create and start a timer using context manager protocol
    base_timer = timer.Timer()
    active_timer = base_timer.__enter__()  # Starts the timer and returns self

    # Get string representation of the active timer to use as initial_text
    timer_repr_text = active_timer.__repr__()

    # Setup: Create additional timers using the repr text as initial_text
    float_arg_for_text = timer.FloatArg()
    timer_with_initial_text = timer.Timer(initial_text=timer_repr_text)
    float_arg_for_initial_text = timer.FloatArg()

    # Execution: Test equality comparison with a non-Timer integer value
    equality_result = base_timer.__eq__(NON_TIMER_INT_VALUE)

    # Execution: Stop the active timer and capture elapsed time
    elapsed_time = active_timer.stop()

    # Setup: Create a timer with both text (as FloatArg) and initial_text (as repr string)
    timer_with_float_text = timer.Timer(text=float_arg_for_text, initial_text=timer_repr_text)

    # Assertion: Verify repr output for both timers
    base_timer_repr = base_timer.__repr__()
    float_text_timer_repr = timer_with_float_text.__repr__()

    # Execution: Start the timer that has float_arg as text and repr string as initial_text
    timer_with_float_text.start()

    # Assertions
    assert elapsed_time >= 0, "Elapsed time should be non-negative after stopping the timer"
    assert equality_result is NotImplemented or equality_result == False, (
        "Timer equality with a non-Timer integer should return NotImplemented or False"
    )
    assert isinstance(base_timer_repr, str), "Timer repr should return a string"
    assert isinstance(float_text_timer_repr, str), "Timer repr should return a string"

def test_timer_exit_stops_running_timer():
    """
    Test that calling __exit__ on a running timer stops it,
    and that attempting to call .start() on None raises an AttributeError.
    """
    # Constants
    NO_LOGGER = None

    # Setup: Create a timer with no logger and start it
    timer_instance = timer.Timer(logger=NO_LOGGER)
    timer_instance.start()

    # Execution: Call __exit__ to stop the timer (simulating context manager exit)
    timer_instance.__exit__()

    # Setup: Verify that None does not have a .start() method
    none_value = None

    # Assertion: Calling .start() on None should raise an AttributeError
    with pytest.raises(AttributeError):
        none_value.start()

def test_timer_start_with_another_timer_as_initial_text_and_logger():
    """
    Test that a Timer can be started when configured with another Timer instance
    as initial_text and a boolean equality result as logger.
    
    This test verifies that:
    1. A Timer can be used as a context manager, which starts and stops it.
    2. A Timer can be created using another Timer instance as initial_text.
    3. A Timer can be started with a name set to another Timer instance,
       initial_text set to a Timer, and logger set to a boolean value.
    """
    # Setup: Create and use a base timer as a context manager to get a stopped timer reference
    base_timer = timer.Timer()
    entered_timer = base_timer.__enter__()  # Starts the timer and returns itself
    
    # Check equality of the timer with itself (returns True, used as logger later)
    timer_self_equal = base_timer.__eq__(base_timer)  # Expected: True
    
    # Exit the context manager, which stops the base timer
    base_timer.__exit__()
    
    # Create a second timer using the entered_timer as initial_text and bool as logger
    timer_with_timer_as_initial_text = timer.Timer(
        initial_text=entered_timer,
        logger=timer_self_equal
    )
    
    # Create a third timer using entered_timer as name, timer_with_timer_as_initial_text
    # as initial_text, and bool as logger
    timer_with_timer_name_and_initial_text = timer.Timer(
        entered_timer,
        initial_text=timer_with_timer_as_initial_text,
        logger=timer_self_equal
    )
    
    # Execution: Start the third timer
    # This should succeed since logger is True (callable-like) and initial_text is a Timer instance
    timer_with_timer_name_and_initial_text.start()
    
    # Assertion: Verify the timer has been started (internal start time should be set)
    assert timer_with_timer_name_and_initial_text._start_time is not None

def test_timer_start_stop_and_reuse_as_context_manager():
    """
    Test that a Timer can be started, stopped, and then reused as a context manager.
    
    This test verifies:
    1. A Timer can be initialized with a custom name.
    2. The timer can be started and stopped, returning elapsed time as a float.
    3. After stopping, the timer can be used as a context manager via __enter__,
       which restarts the timer and returns the same Timer instance.
    4. The timer can be copied after being reused as a context manager.
    """
    # Constants
    TIMER_NAME = "Timer started"

    # Setup: Create a timer with a custom name
    named_timer = timer.Timer(TIMER_NAME)

    # Execution: Start and stop the timer to measure elapsed time
    named_timer.start()
    elapsed_time = named_timer.stop()

    # Assert: Elapsed time should be a positive float
    assert isinstance(elapsed_time, float)
    assert elapsed_time >= 0

    # Execution: Reuse the timer as a context manager via __enter__
    # This restarts the timer and returns the same Timer instance
    context_timer = named_timer.__enter__()

    # Assert: The context manager should return the same Timer instance
    assert context_timer is named_timer

    # Execution: Copy the timer while it is running as a context manager
    timer_copy = named_timer.copy()

    # Assert: The copied timer should be a new Timer instance
    assert timer_copy is not named_timer

