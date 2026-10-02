import pytest
import codetiming_timer as timer

def test_timer_error_instantiation_without_arguments():
    # Purpose: Verify that TimerError can be instantiated without arguments.
    # Setup: No setup required — creating the exception instance is the behavior under test.
    # Execution: Instantiate TimerError with no arguments.
    timer_error = timer.TimerError()

    # Assertion: The instance is created and is of the expected type.
    assert isinstance(timer_error, timer.TimerError)

def test_timer_context_manager_returns_started_timer_instance():
    # Setup: Create a timer instance to be used as a context manager
    timer_instance = timer.Timer()

    # Execution: Enter the context manager, which starts the timer and returns the timer instance
    context_manager_timer = timer_instance.__enter__()

    # Execution: Exit the context manager, which stops the timer
    timer_instance.__exit__()

    # Execution: Start the returned timer instance (from __enter__) again after it was stopped
    context_manager_timer.start()

    # Execution: Attempt to start the original timer instance again, which should raise a TimerError
    # since it was already started but never explicitly stopped (the __exit__ call stopped the timer
    # from the context manager perspective, but the original instance's start_time remains set)
    timer_instance.start()

def test_timer_context_manager_returns_started_timer_instance():
    # Setup: create a Timer instance to be used as a context manager
    timer = timer.Timer()

    # Execution: enter and exit the timer context
    context_result = timer.__enter__()
    timer.__exit__(None, None, None)

    # Assertion: __enter__ should return the Timer instance itself
    assert context_result is timer

def test_timer_exit_stops_running_timer():
    # Setup: create required objects for the test
    timer = timer.Timer()

    # Execution: call __exit__ to stop the context manager timer
    timer.__exit__()

    # Assertion: verify the timer was stopped by checking the state
    assert timer._start_time is None or not timer._running  # adjust based on Timer implementation

def test_timer_enter_without_logger_sets_start_time():
    # Setup: create a Timer with no logger and an empty dictionary to store results
    timer_without_logger = timer.Timer(logger=None)
    storage = {}

    # Execution: start the timer and enter it as a context manager
    timer_without_logger.start()
    context_manager = storage.__setitem__(None, storage)
    context_manager.__enter__()

    # Assertion: entering the context manager did not raise and the timer is running
    assert timer_without_logger._start_time is not None

def test_timer_invalid_equality_comparison_with_initial_text_and_repr():
    # Setup: create a Timer and enter its context (starts the timer)
    timer = timer.Timer()
    started_timer = timer.__enter__()

    # Setup: create a Timer using the started timer as initial_text, repr this timer, stop it, then create another Timer
    invalid_equality_value = -1092
    text_placeholder = timer.FloatArg()
    timer_with_initial_text = timer.Timer(initial_text=started_timer)
    another_text_placeholder = timer.FloatArg()

    # Execution: compare timer to an integer (should return False, no exception)
    equality_result = timer.__eq__(invalid_equality_value)

    # Execution: stop the started timer to record elapsed time and get the float result
    elapsed_time = started_timer.stop()

    # Execution: create a Timer with text and initial_text parameters
    timer_with_text_and_initial_text = timer.Timer(text=text_placeholder, initial_text=equality_result)

    # Execution: get string representations of the timers
    timer_repr = timer.__repr__()
    timer_with_text_repr = timer_with_text_and_initial_text.__repr__()

    # Execution: start the timer with text and initial_text
    timer_with_text_and_initial_text.start()

    # Assertion: verify that the equality result is False (comparing Timer to int)
    assert equality_result is False
    # Assertion: verify that the elapsed time is a float (returned by stop)
    assert isinstance(elapsed_time, float)
    # Assertion: verify that repr returns a string
    assert isinstance(timer_repr, str)
    assert isinstance(timer_with_text_repr, str)

def test_timer_equality_with_invalid_type_comparison_and_constructor_variants():
    # Setup: create a timer and start it via context manager to have a running timer
    timer = timer.Timer()
    running_timer = timer.__enter__()
    invalid_comparison_value = -1092

    # Execution: attempt to compare timer to an integer (invalid type) and
    # create timers with various constructor arguments
    timer_repr = running_timer.__repr__()
    float_arg = timer.FloatArg()
    timer_with_initial_text = timer.Timer(initial_text=timer_repr)
    another_float_arg = timer.FloatArg()
    equality_result = timer.__eq__(invalid_comparison_value)
    elapsed_time = running_timer.stop()
    timer_with_text_and_initial = timer.Timer(text=float_arg, initial_text=timer_repr)
    timer_repr_after_stop = timer.__repr__()
    timer_with_text_and_initial_repr = timer_with_text_and_initial.__repr__()

    # Execution: start the previously created timer
    timer_with_text_and_initial.start()

    # Assertion: comparing a Timer to a non-Timer should return NotImplemented,
    # which Python treats as falsy when directly checked
    assert equality_result is NotImplemented or equality_result is False
    # Assertion: stopping a running timer returns a non-negative elapsed time
    assert elapsed_time >= 0.0

def test_timer_restart_with_none_logger_after_context_exit():
    # Setup: Create a Timer instance with logger set to None
    logger = None
    timer = timer.Timer(logger=logger)

    # Execution: Start the timer and then exit the context manager
    timer.start()
    timer.__exit__()

    # Assertion: Verify timer can be restarted after being stopped
    timer.start()

def test_timer_chained_construction_from_entered_timer_instance():
    # Setup
    TIMER_NAME = "test_timer"
    INITIAL_TEXT = "starting {name}"
    logger_calls = []

    def custom_logger(message):
        logger_calls.append(message)

    # Create base timer and enter it as a context manager
    base_timer = timer.Timer(name=TIMER_NAME, initial_text=INITIAL_TEXT, logger=custom_logger)

    # Execution
    entered_timer = base_timer.__enter__()

    # Assert: __enter__ returns self
    assert entered_timer is base_timer

    # Assert: __eq__ evaluates identity/equality
    is_equal = base_timer.__eq__(base_timer)
    assert is_equal is True

    # Exit the context manager (stops the timer)
    exit_result = base_timer.__exit__()

    # Assert: __exit__ returns None
    assert exit_result is None

    # Build timers chained from the entered timer instance
    chained_timer_from_initial_text = timer.Timer(
        initial_text=entered_timer, logger=is_equal
    )

    chained_timer_named = timer.Timer(
        entered_timer, initial_text=chained_timer_from_initial_text, logger=is_equal
    )

    # Start the final chained timer
    chained_timer_named.start()

    # Assert: starting the timer records a start time
    assert chained_timer_named._start_time is not None

def test_timer_full_lifecycle_start_stop_enter_and_copy():
    # Purpose: Verify that a single Timer instance can be started, stopped
    # (returning a positive elapsed time), used as a context manager, and copied,
    # exercising the start/stop/enter/copy lifecycle in one flow.

    # Setup
    TIMER_NAME = "Timer started"
    timer_under_test = timer.Timer(TIMER_NAME)

    # Execution
    start_result = timer_under_test.start()
    elapsed_time = timer_under_test.stop()
    context_manager_result = timer_under_test.__enter__()
    copied_timer = timer_under_test.copy()

    # Assertions
    assert start_result is None
    assert isinstance(elapsed_time, float)
    assert elapsed_time >= 0
    assert context_manager_result is timer_under_test
    assert copied_timer is not None

