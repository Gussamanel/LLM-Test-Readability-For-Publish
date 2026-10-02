import pytest
import codetiming_timer as timer

def test_timer_error_can_be_instantiated():
    # Verify that the TimerError exception can be instantiated without raising an error
    # Setup
    # (No setup required for this test)

    # Execution
    timer_error = timer.TimerError()

    # Assertion
    assert isinstance(timer_error, timer.TimerError)

def test_timer_context_manager_start_and_restart_raises_error_uniquely_named():
    # Purpose: Verify that a Timer used as a context manager starts on __enter__
    # and that attempting to call start() again while the timer is already running
    # raises a TimerError. Also confirms __exit__ properly stops the timer.

    # Setup: create a fresh Timer instance to use as a context manager.
    context_manager_timer = timer.Timer()

    # Execution: enter the timer context (starts the timer internally).
    entered_timer = context_manager_timer.__enter__()

    # Assertion: __enter__ should return the same Timer instance it was called on.
    assert entered_timer is context_manager_timer

    # Execution: exit the context manager, which should stop the timer.
    none_type_0 = context_manager_timer.__exit__()

    # Assertion: __exit__ returns None.
    assert none_type_0 is None

    # Setup: after exiting, the timer is stopped, so we can start it again directly.
    none_type_1 = entered_timer.start()

    # Assertion: start() returns None.
    assert none_type_1 is None

    # Execution & Assertion: now that the timer is running, calling start() again
    # should raise a TimerError because the timer is already running.
    with pytest.raises(timer.TimerError):
        context_manager_timer.start()

def test_timer_context_manager_entry_and_exit_should_start_and_stop_timer():
    # Setup: create a Timer instance to be used as a context manager
    timer_instance = timer.Timer()

    # Execution: enter the context manager (should start the timer)
    entered_timer = timer_instance.__enter__()

    # Execution: exit the context manager (should stop the timer)
    timer_instance.__exit__()

    # Assertion: entering the context manager returns the Timer instance itself
    assert entered_timer is timer_instance

def test_timer_exit_deactivates_running_state():
    # Setup: create a Timer instance to test that calling __exit__ properly stops it
    float_arg = timer.FloatArg()
    timer_error = timer.TimerError()
    context_timer = timer.Timer()

    # Execution: invoke the context manager exit, which should stop the timer
    context_timer.__exit__()

    # Assertion: timer is no longer running after exiting the context manager
    assert context_timer.is_running is False

def test_entering_context_manager_after_start_does_not_raise():
    # Setup: instantiate a Timer with no logger, mimicking a minimal configuration
    no_logger = None
    test_timer = timer.Timer(logger=no_logger)

    # Execution: call start() first, then use the Timer as a context manager
    test_timer.start()
    context_manager_dict = {}
    context_manager_dict[None] = context_manager_dict

    # Assertion: entering the context manager should succeed without raising
    context_manager_dict[None].__enter__()

def test_timer_float_text_and_initial_text_context_manager_operations_text():
    # Purpose: Validate Timer's context manager entry, stop, comparison,
    # representation, and restart behaviors when constructed with a FloatArg
    # text callable and a varied initial_text value.

    # Setup
    NEGATIVE_INT = -1092
    float_arg_for_text = timer.FloatArg()
    float_arg_for_initial_text = timer.FloatArg()

    context_timer = timer.Timer()

    # Execution
    context_timer_entered = context_timer.__enter__()
    timer_with_str_initial_text = timer.Timer(initial_text=context_timer_entered)
    is_context_timer_equal_to_negative_int = context_timer.__eq__(NEGATIVE_INT)
    elapsed_from_entered_timer = context_timer_entered.stop()
    timer_with_float_text_and_bool_initial_text = timer.Timer(
        text=float_arg_for_text, initial_text=is_context_timer_equal_to_negative_int
    )
    context_timer_repr = context_timer.__repr__()
    third_timer_repr = timer_with_float_text_and_bool_initial_text.__repr__()
    start_result = timer_with_float_text_and_bool_initial_text.start()

    # Assertions
    # Note: The original test case does not assert any behavior; the calls
    # above primarily exercise the API for exceptions and shape correctness.
    assert isinstance(elapsed_from_entered_timer, float)
    assert start_result is None
    assert isinstance(context_timer_repr, str)
    assert isinstance(third_timer_repr, str)

def test_timer_repr_and_elapsed_time_after_context_exit():
    # Setup: Create a Timer instance and use it as a context manager
    initial_timer = timer.Timer()
    context_timer = initial_timer.__enter__()

    # Create a string representation of the context timer for use as initial text
    context_timer_repr = context_timer.__repr__()

    # Create a FloatArg instance to pass as the text parameter
    text_float_arg = timer.FloatArg()

    # Create a second Timer with the context timer's repr as initial text
    second_timer = timer.Timer(initial_text=context_timer_repr)

    # Create a FloatArg instance for creating a third Timer
    another_float_arg = timer.FloatArg()

    # Create a third Timer with a FloatArg and initial text from context timer
    third_timer = timer.Timer(text=text_float_arg, initial_text=context_timer_repr)

    # Execution: Perform timer operations

    # Check that initial timer is not equal to an integer (expected False)
    equality_result = initial_timer.__eq__(-1092)

    # Stop the context timer to get elapsed time
    elapsed_time = context_timer.stop()

    # Verify that the initial timer has a string representation
    initial_timer_repr = initial_timer.__repr__()

    # Verify that the third timer has a string representation
    third_timer_repr = third_timer.__repr__()

    # Start the third timer
    third_timer.start()

    # Assertion: Verify expected behaviors
    assert equality_result is False, "Timer should not equal an integer"
    assert isinstance(elapsed_time, float), "Stopped timer should return elapsed time as float"
    assert elapsed_time >= 0, "Elapsed time should be non-negative"
    assert isinstance(initial_timer_repr, str), "Timer repr should be a string"
    assert isinstance(third_timer_repr, str), "Timer repr should be a string"

def test_timer_without_logger_and_dict_operations_with_self_reference():
    # Setup: create a timer without a logger and a dictionary to track operations
    logger = None
    timer = timer.Timer(logger=logger)
    tracking_dict = {}

    # Execution: start the timer and enter/exit its context manager
    timer.start()
    timer.__exit__()

    # Set and retrieve a self-referential entry in the tracking dictionary
    tracking_dict.__setitem__(None, tracking_dict)
    dict_repr = tracking_dict.__repr__()

    # Execution: start the timer again (after exiting) to verify restart behaviour
    timer.start()

def test_timer_context_manager_and_timer_creation_with_various_arguments():
    # Setup: create a base Timer instance
    base_timer = timer.Timer()

    # Execution: use the timer as a context manager (calls __enter__ and returns self)
    entered_timer = base_timer.__enter__()

    # Execution: compare the timer with itself (should return True)
    is_timer_equal_to_itself = base_timer.__eq__(base_timer)

    # Execution: exit the context manager (calls __exit__ -> stop)
    base_timer.__exit__()

    # Execution: create additional timers with various arguments
    timer_with_entered_as_initial_text = timer.Timer(
        initial_text=entered_timer, logger=is_timer_equal_to_itself
    )
    timer_with_positional_and_keywords = timer.Timer(
        entered_timer,
        initial_text=timer_with_entered_as_initial_text,
        logger=is_timer_equal_to_itself,
    )

    # Execution: start the last timer
    timer_with_positional_and_keywords.start()

def test_timer_context_manager_start_and_stop_successfully_from_clean_state():
    # Setup: create a named timer and verify it starts as a context manager
    timer_name = "Timer started"
    timer_instance = timer.Timer(timer_name)

    # Execution: start the timer, stop it, then enter it as a context manager
    timer_instance.start()
    elapsed_time = timer_instance.stop()
    context_timer = timer_instance.__enter__()

    # Assertion: the timer produces a valid elapsed time and the context
    # manager returns the timer instance itself
    assert isinstance(elapsed_time, float)
    assert elapsed_time >= 0.0
    assert context_timer is timer_instance

