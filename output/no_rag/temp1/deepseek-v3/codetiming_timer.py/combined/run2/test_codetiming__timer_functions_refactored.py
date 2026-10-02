import pytest

import codetiming_timer as timer

def test_timer_error_instantiation():
    # Setup: Initialize TimerError with no arguments
    timer_error = timer.TimerError()

    # Execution: No action needed beyond construction

    # Assertion: Verify TimerError is properly instantiated
    assert isinstance(timer_error, timer.TimerError)

def test_timer_start_raises_error_when_already_running_instance():
    # Setup: create a timer instance
    timer_instance = timer.Timer()

    # Execution: start the timer successfully first time
    timer_instance.start()

    # Assertion: calling start() again while timer is running should raise TimerError
    with pytest.raises(timer.TimerError):
        timer_instance.start()

def test_timer_context_manager_enter_returns_self_and_exit_stops_timer_when_used_as_context_manager():
    # Setup: create a Timer instance used as a context manager
    timer_instance = timer.Timer()

    # Execution: enter and exit the context manager
    entered_timer = timer_instance.__enter__()
    timer_instance.__exit__()

    # Assertion: __enter__ should return the same Timer instance (self)
    assert entered_timer is timer_instance

def test_timer_exit_stops_timer_without_exception():
    # Setup: create an unstarted Timer instance.
    timer_instance = timer.Timer()

    # Execution: invoking __exit__ should delegate to stop() without raising.
    timer_instance.__exit__()

    # Assertion: the timer remains in a stopped state after exiting the context.
    assert not timer_instance._running

def test_timer_context_manager_entry_starts_timer_without_logger():
    # Setup: create a Timer with no logger configured
    logger = None
    context_manager_timer = timer.Timer(logger=logger)

    # Execution: start the timer explicitly, then enter a dictionary-like
    # context manager to trigger __enter__ on the value stored in dict_0
    context_manager_timer.start()
    context_manager = {}
    context_key = None
    context_manager.__setitem__(context_key, context_manager)

    # Assertion: entering the context manager should invoke __enter__
    # without raising, confirming the timer with no logger starts correctly
    context_manager.__enter__()

def test_timer_context_manager_comparison_and_representation_operations():
    # Setup: Create a Timer instance to test various timer operations
    timer_instance = timer.Timer()
    
    # Execution: Use timer as context manager and test other operations
    # Enter the timer context (starts the timer)
    timer_context = timer_instance.__enter__()
    
    # Create an invalid integer value for comparison testing
    invalid_comparison_value = -1092
    
    # Create FloatArg instances for testing different text parameter types
    float_arg_formatter = timer.FloatArg()
    another_float_arg = timer.FloatArg()
    
    # Create a new timer with custom initial text
    timer_with_initial_text = timer.Timer(initial_text=timer_context)
    
    # Test equality comparison with invalid type
    equality_result = timer_instance.__eq__(invalid_comparison_value)
    
    # Stop the original timer and get elapsed time
    elapsed_time = timer_context.stop()
    
    # Create timer with mixed parameter types
    timer_with_float_arg = timer.Timer(text=float_arg_formatter, initial_text=equality_result)
    
    # Get string representations of timers
    timer_instance_repr = timer_instance.__repr__()
    timer_float_arg_repr = timer_with_float_arg.__repr__()
    
    # Assertions and Validation
    # Verify that equality comparison with non-Timer object returns False
    assert equality_result is False  # Comparing Timer to int should return False
    
    # Verify timer representations are strings
    assert isinstance(timer_instance_repr, str)
    assert isinstance(timer_float_arg_repr, str)
    
    # Verify elapsed time is a valid float value
    assert isinstance(elapsed_time, float)
    assert elapsed_time >= 0
    
    # Start a new timer session (should work since previous timer was stopped)
    timer_with_float_arg.start()

def test_timer_repr_and_lifecycle_controls():
    # Setup: Create a Timer instance and validate its context manager protocol.
    # This test verifies Timer's __enter__, __repr__, __eq__, and start/stop interactions.
    
    # Create a base timer and enter it as a context manager (starts it).
    base_timer = timer.Timer()
    entered_timer = base_timer.__enter__()

    # Store an arbitrary integer for equality comparison.
    arbitrary_int = -1092

    # Execution: Obtain a string representation of the started timer.
    base_timer_repr = entered_timer.__repr__()

    # Setup: Create initial_text and text arguments using the FloatArg mock class.
    initial_text_arg = timer.FloatArg()
    text_arg = timer.FloatArg()

    # Setup: Create additional Timer instances using captured string representation.
    timer_with_initial_text = timer.Timer(initial_text=base_timer_repr)
    same_name_timer = timer.Timer(text=text_arg, initial_text=base_timer_repr)

    # Execution: Perform equality comparison against an unrelated integer.
    equality_result = base_timer.__eq__(arbitrary_int)

    # Execution: Stop the entered timer; should return elapsed time as float.
    elapsed_time = entered_timer.stop()

    # Execution: Retrieve repr from timers.
    base_timer_repr_after = base_timer.__repr__()
    same_name_timer_repr = same_name_timer.__repr__()

    # Execution: Start the same_name_timer (should succeed since it hasn't been started).
    same_name_timer.start()

    # Assertion: Verify produced objects match expectations.
    assert isinstance(base_timer_repr, str)
    assert isinstance(base_timer_repr_after, str)
    assert isinstance(same_name_timer_repr, str)
    assert isinstance(elapsed_time, float)
    assert equality_result is False  # Timer should not equal arbitrary int

def test_timer_cannot_restart_after_exit_while_running():
    # Setup: create a timer without a logger and start it
    timer_instance = timer.Timer(logger=None)
    start_result = timer_instance.start()

    # Execution: attempt to use the timer as a context manager exit and restart it
    timer_instance.__exit__()

    # A dict is used to exercise the provided API surface (setitem/repr),
    # unrelated to timer functionality but part of the original test.
    tracking_dict = {}
    sentinel_key = None
    setitem_result = tracking_dict.__setitem__(sentinel_key, tracking_dict)
    repr_result = setitem_result.__repr__()

    # Assertion/Execution: restarting a running timer should raise TimerError
    with pytest.raises(timer.TimerError):
        timer_instance.start()

def test_timer_start_does_not_raise_for_new_instance_with_additional_arguments():
    # Setup: create a fresh Timer and enter its context manager to start it
    fresh_timer = timer.Timer()
    context_manager_timer = fresh_timer.__enter__()

    # Execution & Assertion: timer self-equality is True; exiting stops the context manager timer without error
    is_same_instance = fresh_timer.__eq__(fresh_timer)
    assert is_same_instance is True
    context_manager_timer.__exit__()

    # Setup: instantiate timers with unusual argument combinations (initial_text/logger) to exercise start()
    timer_with_initial_text_and_logger = timer.Timer(initial_text=context_manager_timer, logger=is_same_instance)
    timer_with_mixed_arguments = timer.Timer(
        context_manager_timer,
        initial_text=timer_with_initial_text_and_logger,
        logger=is_same_instance,
    )

    # Execution: starting a fresh timer instance should not raise (validates the "Timer is running" guard path)
    timer_with_mixed_arguments.start()

def test_timer_lifecycle_and_copy_after_context_entry():
    # Purpose:
    # Verify that a Timer can be started, stopped to return an elapsed float,
    # re-entered as a context manager, and that copy() produces an equivalent Timer.
    INITIAL_TEXT = "Timer started"

    # Setup: create a Timer with informational text
    original_timer = timer.Timer(INITIAL_TEXT)

    # Execution: start the timer
    original_timer.start()

    # Execution: stop the timer and capture elapsed time
    elapsed_seconds = original_timer.stop()

    # Execution: enter as a context manager (starts the timer and returns self)
    entered_timer = original_timer.__enter__()

    # Execution: copy the timer instance
    copied_timer = original_timer.copy()

    # Assertion: stop returned an elapsed duration as a float
    assert isinstance(elapsed_seconds, float)
    assert elapsed_seconds >= 0

    # Assertion: __enter__ returns the same timer instance
    assert entered_timer is original_timer

    # Assertion: copy produces an independent Timer with the same attributes
    assert isinstance(copied_timer, timer.Timer)
    assert copied_timer is not original_timer
    assert copied_timer.initial_text == original_timer.initial_text

