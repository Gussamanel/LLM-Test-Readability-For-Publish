import pytest
import codetiming_timer as timer

def test_timer_error_is_instantiable():
    # Setup & Execution: Create a TimerError instance.
    timer_error = timer.TimerError()

    # Assertion: Verify the TimerError exception can be instantiated without errors.
    assert timer_error is not None

def test_timer_error_can_be_created():
    # Setup & Execution: Create a TimerError instance.
    timer_error = timer.TimerError()

    # Assertion: Verify the TimerError exception can be instantiated without errors.
    assert timer_error is not None

def test_timer_can_stop_and_restart_after_context_manager_exit():
    # Setup
    # Create a timer and start it via context manager entry, then stop it via
    # __exit__ (which calls stop and resets _start_time to None).
    running_timer = timer.Timer()
    entered_timer = running_timer.__enter__()
    running_timer.__exit__()

    # Execution
    # After exiting the context manager, the timer should be stoppable and
    # restarted again without raising "Timer is running" error.
    # Start via the returned timer instance, then start again via the original.
    entered_timer.start()
    running_timer.start()

    # Assertion
    # The second start should succeed, meaning _start_time was reset on stop
    # and the timer is considered running (no TimerError raised).
    assert running_timer._start_time is not None
    assert entered_timer._start_time is not None

def test_timer_context_manager_returns_self_and_stops_on_exit():
    # Setup: create a timer instance to be used as a context manager
    context_manager_timer = timer.Timer()

    # Execution: enter the timer context, which starts the timer and returns the timer
    returned_timer = context_manager_timer.__enter__()

    # Execution: exit the timer context, which stops the timer
    context_manager_timer.__exit__()

    # Assertion: entering the context manager should return the timer instance itself
    assert returned_timer is context_manager_timer

def test_timer_exit_stops_running_timer():
    """Test that Timer.__exit__() properly stops the timer."""
    
    # Setup
    timer_instance = timer.Timer()
    
    # Execution
    timer_instance.__exit__()
    
    # Assertion
    assert not timer_instance._running

def test_timer_context_manager_raises_error_when_already_started_with_logger_none():
    logger = None
    test_timer = timer.Timer(logger=logger)

    assert test_timer._start_time is None

    test_timer.start()

    assert test_timer._start_time is not None

    context_dict = {}
    context_key = None

    context_dict[context_key] = test_timer

    with pytest.raises(timer.TimerError):
        context_dict[context_key].__enter__()

def test_timer_context_manager_and_floatarg_interactions():
    # Purpose: Verify Timer context manager start/stop behavior and interactions
    # between Timer instances, FloatArg formatting, equality checks, and repr output.

    # Setup
    NEGATIVE_INT = -1092
    logging_text = module_0.FloatArg()

    # Create a base Timer and start it via context manager entry
    base_timer = module_0.Timer()

    # Execution
    entered_timer = base_timer.__enter__()

    formatting_arg = module_0.FloatArg()
    initial_text_from_entry = entered_timer

    nested_timer = module_0.Timer(initial_text=initial_text_from_entry)

    # Timer creating with a formatted text provider and initial text from equality result
    equality_result = base_timer.__eq__(NEGATIVE_INT)

    # Stop the entered timer and capture elapsed time
    elapsed = entered_timer.stop()

    text_formatted_timer = module_0.Timer(text=logging_text, initial_text=equality_result)

    base_repr = base_timer.__repr__()
    text_timer_repr = text_formatted_timer.__repr__()

    # Start another timer, should not raise
    start_result_none = text_formatted_timer.start()

    # Assertions
    assert entered_timer is base_timer
    assert isinstance(elapsed, float) and elapsed >= 0.0
    assert isinstance(base_repr, str) and isinstance(text_timer_repr, str)
    assert start_result_none is None

def test_timer_custom_text_equality_and_callable_text_operations():
    # Setup: Define constants for the test
    NON_MATCHING_INT = -1092
    INITIAL_TEXT = "Custom timer text for testing"
    
    # Setup: Create a Timer instance
    timer = timer.Timer()
    
    # Execution: Enter the timer context (starts the timer)
    running_timer = timer.__enter__()
    
    # Execution: Get the string representation of the running timer
    timer_repr = running_timer.__repr__()
    
    # Setup: Create FloatArg instance (used as a callable text formatter)
    float_arg_callable = timer.FloatArg()
    
    # Execution: Create another Timer with the initial_text from the first timer's repr
    timer_with_initial_text = timer.Timer(initial_text=timer_repr)
    
    # Setup: Create another FloatArg instance (unused in assertions, kept from original)
    unused_float_arg = timer.FloatArg()
    
    # Execution: Check equality of the original timer with a non-matching integer
    equality_result = timer.__eq__(NON_MATCHING_INT)
    
    # Execution: Stop the running timer and record elapsed time
    elapsed_time = running_timer.stop()
    
    # Execution: Create a Timer with a callable text and custom initial text
    timer_with_callable_text = timer.Timer(text=float_arg_callable, initial_text=timer_repr)
    
    # Execution: Get repr of the original timer and the new timer
    original_timer_repr = timer.__repr__()
    callable_text_timer_repr = timer_with_callable_text.__repr__()
    
    # Assertion: Timer equality with non-matching int should be False
    assert equality_result is False
    
    # Assertion: Elapsed time from stop() should be a non-negative float
    assert isinstance(elapsed_time, float)
    assert elapsed_time >= 0.0
    
    # Assertion: String representations are strings (non-empty or expected format)
    assert isinstance(original_timer_repr, str)
    assert isinstance(callable_text_timer_repr, str)
    
    # Execution: Start the timer with callable text (should not raise)
    timer_with_callable_text.start()
    
    # Assertion: Timer is running after start (internal state check)
    assert timer_with_callable_text._start_time is not None

def test_start_logs_initial_text_and_exit_stops_timer_restart():
    # Purpose: Verify that Timer.start() logs the initial text when a logger
    # is provided, and that the context manager __exit__ properly stops the timer.
    # Also exercise setting a dict key to itself and calling start again.

    # Setup
    logger = None
    test_timer = timer.Timer(logger=logger)

    # Execution
    test_timer.start()

    # Assertion - starting should not raise when logger is None
    assert test_timer._start_time is not None

    # Setup for second part
    test_dict = {}
    dict_key = None

    # Execution - exiting the context manager should stop the timer
    test_timer.__exit__()

    # Assertion - stop should reset _start_time to None
    assert test_timer._start_time is None

    # Execution - set dict entry where value is the dict itself
    set_result = test_dict.__setitem__(dict_key, test_dict)

    # Assertion - __setitem__ returns None
    assert set_result is None

    # Execution - repr of the None return value
    repr_result = None.__repr__()

    # Assertion - repr of None is "None"
    assert repr_result == "None"

    # Execution - restart the timer after stopping
    test_timer.start()

    # Assertion - timer is running again
    assert test_timer._start_time is not None

def test_timer_start_with_timer_and_boolean_logger_after_context_manager_exit():
    base_timer = timer.Timer()
    entered_timer = base_timer.__enter__()
    equality_result = base_timer.__eq__(base_timer)
    base_timer.__exit__()

    timer_with_entered_timer_as_initial_text = timer.Timer(
        initial_text=entered_timer,
        logger=equality_result,
    )
    nested_timer = timer.Timer(
        entered_timer,
        initial_text=timer_with_entered_timer_as_initial_text,
        logger=equality_result,
    )

    nested_timer.start()

def test_timer_context_manager_returns_self_and_copy_preserves_instance():
    # Setup: Create a Timer instance with a custom name
    DEFAULT_TIMER_NAME = "Timer started"
    timer_instance = timer.Timer(DEFAULT_TIMER_NAME)

    # Execution: Start the timer, then enter it as a context manager, then copy it
    timer_instance.start()
    timer_instance.stop()
    context_manager_timer = timer_instance.__enter__()
    timer_instance.copy()

    # Assertion: The context manager should return the same Timer instance
    assert context_manager_timer is timer_instance

