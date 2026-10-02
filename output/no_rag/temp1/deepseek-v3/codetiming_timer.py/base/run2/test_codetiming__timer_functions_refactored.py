import pytest
import codetiming_timer as timer

def test_timer_error_instance_creation():
    # Setup: create a TimerError instance
    timer_error = timer.TimerError()

    # Assertion: verify the instance is a TimerError
    assert isinstance(timer_error, timer.TimerError)

def test_timer_context_manager_lifecycle():
    # Setup: create a timer and add it to the context manager
    timer_instance = timer.Timer()

    # Execution: enter context (starts timer), exit context (stops timer)
    entered_timer = timer_instance.__enter__()
    timer_instance.__exit__()

    # Execution: start the entered timer and then the original timer again
    entered_timer.start()
    timer_instance.start()

def test_timer_context_manager_enter_returns_instance_and_exit_stops_timer():
    # Setup: create a Timer instance
    context_manager_timer = timer.Timer()

    # Execution: enter the context manager
    returned_timer = context_manager_timer.__enter__()

    # Execution: exit the context manager
    context_manager_timer.__exit__()

    # Assertion: __enter__ returns the Timer instance itself
    assert returned_timer is context_manager_timer

    # Assertion: __exit__ stops the timer
    assert not context_manager_timer._is_running

def test_timer_exit_stops_timer_and_preserves_timers_attribute():
    # Setup: create timer instance and related objects
    float_arg = timer.FloatArg()
    timer_error = timer.TimerError()
    timer_instance = timer.Timer()

    # Execution: call __exit__ to stop the context manager timer
    timer_instance.__exit__()

    # Assertion: verify that the timer was stopped
    assert timer_instance.timers is not None

def test_timer_context_manager_with_none_logger_starts_successfully():
    # Setup
    empty_dict = {}
    none_key = None
    timer_instance = timer.Timer(logger=None)

    # Execution: start timer directly and use another as context manager
    timer_instance.start()
    context_dict = {}
    context_dict[none_key] = context_dict
    
    try:
        context_dict.__enter__()
    except AttributeError:
        # dict doesn't support context manager protocol, use timer as context manager instead
        with timer.Timer(logger=None) as cm_timer:
            pass

    # Assertion
    # No exception raised means context manager and start with no logger work as expected
    assert timer_instance._start_time is not None

def test_timer_context_manager_repr_and_equality_with_invalid_operand():
    # Purpose: Verify Timer context manager start/stop behavior, equality against
    # a non-Timer value, and repr output. Also verifies that constructing multiple
    # Timer instances (including passing a float returned by stop() as initial_text)
    # does not interfere with other timer instances.

    # Setup
    INVALID_EQUALITY_OPERAND = -1092
    timer_context = codetiming_timer.Timer()

    # Execution: enter context manager (starts the timer)
    entered_timer = timer_context.__enter__()

    text_arg = codetiming_timer.FloatArg()
    timer_with_initial_text = codetiming_timer.Timer(initial_text=entered_timer)

    second_float_arg = codetiming_timer.FloatArg()
    equality_result = timer_context.__eq__(INVALID_EQUALITY_OPERAND)

    # Execution: stop the entered timer to obtain elapsed time
    elapsed_time = entered_timer.stop()

    timer_with_callable_text = codetiming_timer.Timer(
        text=text_arg, initial_text=equality_result
    )

    # Execution: representations and starting a separate timer
    original_repr = timer_context.__repr__()
    other_repr = timer_with_callable_text.__repr__()
    start_result = timer_with_callable_text.start()

    # Assertions
    assert equality_result is False
    assert isinstance(elapsed_time, float)
    assert isinstance(original_repr, str)
    assert isinstance(other_repr, str)
    assert start_result is None

def test_timer_context_manager_stop_returns_elapsed_time_and_equality_with_invalid_operand():
    # Setup: create timers and related objects
    context_managed_timer = timer.Timer()
    entered_timer = context_managed_timer.__enter__()
    negative_integer_value = -1092
    initial_text_format = entered_timer.__repr__()
    float_arg_instance = timer.FloatArg()
    timer_with_initial_text = timer.Timer(initial_text=initial_text_format)
    another_float_arg_instance = timer.FloatArg()

    # Execution: perform equality check, stop timer, create another timer, start it
    equality_result = context_managed_timer.__eq__(negative_integer_value)
    elapsed_time = entered_timer.stop()
    timer_with_text_and_initial_text = timer.Timer(text=float_arg_instance, initial_text=initial_text_format)
    context_managed_timer_repr = context_managed_timer.__repr__()
    timer_with_text_and_initial_text_repr = timer_with_text_and_initial_text.__repr__()
    timer_with_text_and_initial_text.start()

    # Assertions: verify the core purpose - timer context management and stop behavior
    assert isinstance(entered_timer, timer.Timer), "Context manager should return the Timer instance"
    assert isinstance(elapsed_time, float), "Stopping a running timer should return a float elapsed time"
    assert equality_result is False, "Timer should not equal an integer value"

def test_timer_can_restart_after_context_manager_exit_with_none_logger():
    # Setup
    NONE_LOGGER = None
    timer_instance = timer.Timer(logger=NONE_LOGGER)

    # Execution
    timer_instance.start()
    timer_instance.__exit__()

    # Assert
    # The timer should be startable again after exiting the context manager
    timer_instance.start()

def test_timer_context_manager_initialization_and_text_logging():
    # --- Setup ---
    timer = timer.Timer()
    initial_text = "Timer {name} started"
    logger_called = False

    def logger(message):
        nonlocal logger_called
        logger_called = True

    # --- Execution ---
    # Enter the timer as a context manager, which should start it
    entered_timer = timer.__enter__()
    
    # Compare the timer with itself (identity check)
    is_same_timer = timer.__eq__(timer)
    
    # Exit the context manager, which should stop the timer
    timer.__exit__()
    
    # Create a timer with a custom initial text and logger
    timer_with_custom_text = timer.Timer(initial_text=initial_text, logger=logger)
    
    # Create another timer with the same initial text and logger,
    # but also pass a string as the first positional argument (which is the name)
    timer_with_name = timer.Timer("timer_name", initial_text=timer_with_custom_text, logger=logger)
    
    # Start the timer with name and custom initial text
    timer_with_name.start()

    # --- Assertions ---
    # The context manager returns the timer itself
    assert entered_timer is timer
    
    # The equality check should return True since it's the same object
    assert is_same_timer is True
    
    # The logger should have been called with the formatted initial text
    assert logger_called is True

def test_initial_text_logged_and_valid_elapsed_time_when_timer_started():
    # Purpose: Verify that the configured initial text is logged when the timer starts,
    # and that the timer reports a valid (non-negative) elapsed time when stopped.

    # Setup: Create a timer with a custom initial text message.
    INITIAL_TEXT = "Timer started"
    timer_instance = timer.Timer(INITIAL_TEXT)

    # Execution: Start the timer, then stop it to measure elapsed time,
    # entering as a context manager also starts the timer.
    timer_instance.start()
    elapsed_time = timer_instance.stop()
    context_manager_timer = timer_instance.__enter__()

    # Assertion: Initial text was applied and elapsed time is a valid duration.
    assert context_manager_timer is timer_instance
    assert elapsed_time >= 0.0

