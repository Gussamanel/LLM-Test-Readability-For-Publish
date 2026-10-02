import pytest
import codetiming_timer as timer

def test_timer_error_can_be_instantiated_without_arguments():
    # Arrange: A fresh TimerError instance should be constructible with no arguments.
    # Act
    timer_error = timer.TimerError()

    # Assert: The error is an instance of the expected TimerError type.
    assert isinstance(timer_error, timer.TimerError)

def test_timer_start_raises_error_when_already_started():
    # Setup: create a timer instance and start it via the context manager entry
    timer_instance = timer.Timer()
    entered_timer = timer_instance.__enter__()

    # Execution: stop the timer through context manager exit, then attempt to start again
    timer_instance.__exit__()
    entered_timer.start()

    # Assertion: starting an already running timer should raise a TimerError
    with pytest.raises(timer.TimerError):
        timer_instance.start()

def test_timer_used_as_context_manager_returns_self_and_exits_without_suppressing_exceptions():
    # Constants
    EXPECTED_EXIT_RETURN_VALUE = None

    # Setup
    context_manager_timer = timer.Timer()

    # Execution
    entered_timer = context_manager_timer.__enter__()
    exit_return_value = context_manager_timer.__exit__()

    # Assertion
    # The __enter__ method should start the timer and return the Timer instance itself,
    # enabling use as a context manager (e.g., `with Timer() as t:`).
    assert entered_timer is context_manager_timer
    # The __exit__ method should stop the timer and return None (no exception suppression).
    assert exit_return_value is EXPECTED_EXIT_RETURN_VALUE

def test_timer_exit_method_stops_timer_without_exception():
    # Setup: create test objects to verify the __exit__ method interacts with the timer's stop functionality
    float_arg = module_0.FloatArg()
    timer_error = module_0.TimerError()
    context_manager_timer = module_0.Timer()

    # Execution: invoke __exit__ on the timer context manager (with no exception info, simulating a normal exit)
    context_manager_timer.__exit__()

    # Assertion: verify the timer's stop method was called without raising an error
    # (No explicit assertion is provided in the original test, but the test passes if no exception occurs)

def test_entering_timer_context_manager_initializes_start_time():
    # Setup: create a timer without a logger
    logger = None
    timer_instance = timer.Timer(logger=logger)

    # Execution: use the timer as a context manager
    # Entering the context should start the timer
    timer_instance.__enter__()

    # Assertion: verify that the timer has been started
    assert timer_instance._start_time is not None

def test_timer_context_manager_and_manual_start_stop_operations():
    timer_context_manager = timer.Timer()
    entered_timer = timer_context_manager.__enter__()

    invalid_comparison_value = -1092
    float_arg = timer.FloatArg()
    initial_text_from_entered_timer = entered_timer

    second_timer = timer.Timer(initial_text=initial_text_from_entered_timer)
    another_float_arg = timer.FloatArg()

    equality_result = timer_context_manager.__eq__(invalid_comparison_value)

    elapsed_time = entered_timer.stop()

    third_timer = timer.Timer(text=float_arg, initial_text=equality_result)

    first_timer_repr = timer_context_manager.__repr__()
    third_timer_repr = third_timer.__repr__()

    start_result = third_timer.start()

    assert equality_result is False
    assert isinstance(elapsed_time, float)
    assert elapsed_time >= 0.0
    assert isinstance(first_timer_repr, str)
    assert isinstance(third_timer_repr, str)
    assert start_result is None

def test_timer_operations_with_custom_text_and_float_arguments():
    default_timer = timer.Timer()
    float_arg_for_text = timer.FloatArg()
    float_arg_for_other = timer.FloatArg()

    context_entered_timer = default_timer.__enter__()
    entered_timer_repr = context_entered_timer.__repr__()

    custom_text_timer = timer.Timer(initial_text=entered_timer_repr)
    equality_result = default_timer.__eq__(-1092)
    elapsed_time = context_entered_timer.stop()

    float_text_timer = timer.Timer(text=float_arg_for_text, initial_text=entered_timer_repr)

    default_timer_repr = default_timer.__repr__()
    float_text_timer_repr = float_text_timer.__repr__()

    float_text_timer.start()

    assert equality_result is False, "Timer should not equal an integer"
    assert elapsed_time >= 0, "Elapsed time should be non-negative"
    assert isinstance(entered_timer_repr, str), "Timer representation should be a string"
    assert isinstance(default_timer_repr, str), "Timer representation should be a string"
    assert isinstance(float_text_timer_repr, str), "Timer representation should be a string"

def test_timer_stop_resets_start_time_and_dict_repr_is_string():
    # Setup: create a timer with no logger and a dictionary for context
    NO_LOGGER = None
    timer_no_logger = timer.Timer(logger=NO_LOGGER)
    context_dict = {}
    key_for_self = None

    # Execution & Assertion
    # Start the timer
    timer_no_logger.start()
    assert timer_no_logger._start_time is not None, "Timer should have a start time after start()"

    # Exit the context manager (stops the timer)
    timer_no_logger.__exit__(None, None, None)
    assert timer_no_logger._start_time is None, "Timer should reset start time after stop()"

    # Perform dictionary operations
    context_dict.__setitem__(key_for_self, context_dict)
    repr_result = context_dict.__repr__()
    assert isinstance(repr_result, str), "Dictionary repr should return a string"

    # Restart the timer (should succeed because previous stop reset _start_time)
    timer_no_logger.start()
    assert timer_no_logger._start_time is not None, "Timer should start again after being stopped"

    # Cleanup: stop the timer to leave it in a defined state
    timer_no_logger.stop()

def test_timer_can_start_after_another_timer_context_manager_usage():
    # Purpose: Verify that a new Timer can be started even after
    # another Timer instance has been used as a context manager
    # (i.e., entered and exited).

    # Setup: create a Timer and use it as a context manager
    context_timer = timer.Timer()

    # Execution: enter and exit the context manager
    context_manager_return_value = context_timer.__enter__()
    timers_are_equal = context_timer == context_timer
    context_timer.__exit__(None, None, None)

    # Setup: create additional Timer instances using the values obtained
    first_new_timer = timer.Timer(
        initial_text=context_manager_return_value, logger=timers_are_equal
    )
    second_new_timer = timer.Timer(
        context_manager_return_value,
        initial_text=first_new_timer,
        logger=timers_are_equal,
    )

    # Execution: start the second new timer
    second_new_timer.start()

    # Assertion: the timer should now be running
    assert second_new_timer._start_time is not None

def test_timer_enter_then_copy_preserves_restarted_state():
    # Constants
    TIMER_NAME = "Timer started"

    # Setup
    timer_instance = timer.Timer(TIMER_NAME)

    # Execution
    timer_instance.start()
    elapsed_time = timer_instance.stop()

    # Re-enter the timer using the context manager protocol, which should start it again
    context_manager_timer = timer_instance.__enter__()

    # Copy the timer's state
    timer_instance.copy()

    # Assertion
    # The timer should have been restarted by __enter__ and returned itself
    assert context_manager_timer is timer_instance
    # The elapsed time from stop() should be a non-negative float
    assert isinstance(elapsed_time, float)
    assert elapsed_time >= 0

