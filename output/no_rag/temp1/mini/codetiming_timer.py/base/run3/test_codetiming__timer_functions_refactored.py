import pytest

import codetiming_timer as codetiming_timer_module

def test_timer_error_instantiation_and_type():
    """Verify that TimerError can be instantiated and is an Exception."""
    # Expected exception class from the module under test
    EXPECTED_EXCEPTION_CLASS = codetiming_timer_module.TimerError

    # Instantiate the exception
    timer_error_instance = EXPECTED_EXCEPTION_CLASS()

    # The created object should be an instance of the declared TimerError class
    assert isinstance(timer_error_instance, EXPECTED_EXCEPTION_CLASS)
    # And it should also be an instance of the built-in Exception type
    assert isinstance(timer_error_instance, Exception)

def test_start_raises_when_starting_twice_after_manual_context_usage():
    # Purpose:
    # Verify that starting a Timer twice without stopping in between raises TimerError.
    # This simulates a common misuse pattern where a context-managed timer is
    # entered and exited, then started twice without an intervening stop.

    # Constants for readability
    TIMER_NAME = "sample_timer"

    # Setup: create a Timer and simulate entering/exiting the context manager
    timer = codetiming_timer_module.Timer(name=TIMER_NAME)
    context_timer = timer.__enter__()   # starts the timer as context manager
    exit_result = timer.__exit__()      # stops the timer as context manager (returns None)

    # Execution: start the timer once (valid) then attempt to start it again (invalid)
    # First start after the manual exit should succeed and set internal start time.
    context_timer.start()

    # Assertion: attempting to start again without stopping must raise TimerError
    with pytest.raises(codetiming_timer_module.TimerError):
        timer.start()

def test_timer_context_manager_enter_returns_self_and_exit_returns_none():
    # Purpose:
    # Verify that Timer can be used as a context manager:
    #  - __enter__ starts the timer and returns the same Timer instance
    #  - __exit__ stops the timer and returns None
    EXPECTED_EXIT_RETURN = None

    # Setup: create a Timer instance from the module under test
    timer = codetiming_timer_module.Timer()

    # Execution: enter the context manager and then exit it
    entered_timer = timer.__enter__()
    exit_result = timer.__exit__()  # no exception info passed

    # Assertions: __enter__ should return the same object, __exit__ should return None
    assert entered_timer is timer, "Timer.__enter__ should return the Timer instance itself"
    assert exit_result is EXPECTED_EXIT_RETURN, "Timer.__exit__ should return None"

def test_timer_exit_stops_context_manager_without_exception():
    """
    Verify that calling the Timer context-manager __exit__ stops the timer
    and returns None when no exception information is provided.

    This test also instantiates FloatArg and TimerError to mirror typical usage
    setup (they are not used directly here) and to ensure their construction
    does not interfere with calling Timer.__exit__.
    """
    # Simulate no exception information passed to __exit__
    NO_EXCEPTION_ARGS = (None, None, None)

    # Instantiate supporting objects to mirror typical usage
    float_arg_instance = codetiming_timer_module.FloatArg()
    timer_error_instance = codetiming_timer_module.TimerError()
    timer = codetiming_timer_module.Timer()

    # Call __exit__ as if exiting the context manager with no exception
    result = timer.__exit__(*NO_EXCEPTION_ARGS)

    # __exit__ should return None (and not raise), indicating stop() was called
    assert result is None

def test_timer_enter_starts_timer_and_prevents_restarting():
    # Purpose:
    # Verify that using Timer.__enter__ starts the timer (sets _start_time),
    # returns the same Timer instance, and that calling start() again raises TimerError.
    
    # Constants / configuration for the test
    NO_LOGGER = None

    # Setup: create a Timer with no logger
    timer = codetiming_timer_module.Timer(logger=NO_LOGGER)

    # Execution: enter the timer context (this should call start())
    returned_timer = timer.__enter__()

    # Assertions: __enter__ returns the same instance and _start_time is set to a float
    assert returned_timer is timer
    assert getattr(timer, "_start_time", None) is not None
    assert isinstance(timer._start_time, float)

    # Further assertion: calling start() while timer is running should raise TimerError
    with pytest.raises(codetiming_timer_module.TimerError):
        timer.start()

def test_timer_context_enter_stop_and_start_changes_state_and_returns_expected_types():
    # Purpose:
    # - Verify that using the Timer as a context manager starts the timer and returns the same object.
    # - Verify stop() returns a non-negative float elapsed time.
    # - Verify __eq__ with an unrelated type returns a boolean (False for an int).
    # - Verify __repr__ returns strings for both timers.
    # - Verify start() sets the internal start time on a timer configured with a callable text and a boolean initial_text.

    # Constants
    NEGATIVE_INT = -1092

    # Setup: create timers and helper callables
    primary_timer = codetiming_timer_module.Timer()
    # Using __enter__() to simulate context manager start()
    primary_ctx_timer = primary_timer.__enter__()
    float_arg_callable = codetiming_timer_module.FloatArg()
    # Create another Timer passing a non-string initial_text (the timer object returned above)
    timer_with_obj_initial = codetiming_timer_module.Timer(initial_text=primary_ctx_timer)
    another_float_arg = codetiming_timer_module.FloatArg()

    # Exercise: perform operations used in the original test
    eq_result = primary_timer.__eq__(NEGATIVE_INT)  # compare timer to an int
    elapsed_time = primary_ctx_timer.stop()  # stop the context-started timer
    # Create a timer that uses a callable for text and a boolean initial_text (from eq_result)
    timer_with_callable_text = codetiming_timer_module.Timer(text=float_arg_callable, initial_text=eq_result)
    repr_primary = primary_timer.__repr__()
    repr_callable_timer = timer_with_callable_text.__repr__()
    # Start the timer configured with a callable text and non-string initial_text
    timer_with_callable_text.start()

    # Assertions: separate checks for state and return types
    # __enter__ should return the same object (context manager started the same timer)
    assert primary_ctx_timer is primary_timer

    # __eq__ with an unrelated type (int) should produce a boolean (expected False)
    assert isinstance(eq_result, bool)
    assert eq_result is False

    # stop() returns an elapsed time as a float and should be non-negative
    assert isinstance(elapsed_time, float)
    assert elapsed_time >= 0

    # __repr__ should return string representations
    assert isinstance(repr_primary, str)
    assert isinstance(repr_callable_timer, str)

    # start() should set an internal start time on the timer instance
    assert getattr(timer_with_callable_text, "_start_time", None) is not None

def test_timer_context_manager_start_stop_and_repr_and_equality():
    """
    Verify Timer context-manager behavior and related functionality:
    - __enter__ starts the timer and returns the same object.
    - stop() returns a non-negative float elapsed time.
    - __repr__ returns a string both while running and after stopping.
    - Equality comparison with an unrelated type (int) returns False.
    - A separately created Timer can be started and stopped successfully when given `text` and `initial_text`.
    """

    # Setup
    timer_default = codetiming_timer_module.Timer()
    REFERENCE_INT = -1092

    # Enter context manager form (should start the timer and return same object)
    timer_running = timer_default.__enter__()

    # Capture repr while timer is running
    repr_after_start = timer_running.__repr__()

    # Create FloatArg instances as in original API usage
    float_arg_0 = codetiming_timer_module.FloatArg()
    float_arg_1 = codetiming_timer_module.FloatArg()

    # Create another Timer that uses the captured repr as its initial_text
    timer_with_initial = codetiming_timer_module.Timer(initial_text=repr_after_start)

    # Compare the timer to an unrelated int (should be False)
    equality_result = timer_default.__eq__(REFERENCE_INT)

    # Stop the running timer and record elapsed time
    elapsed_default = timer_running.stop()

    # Create a timer that has both text and initial_text and start it
    timer_with_text_and_initial = codetiming_timer_module.Timer(
        text=float_arg_0, initial_text=repr_after_start
    )
    repr_after_stop_default = timer_default.__repr__()
    repr_timer_with_text = timer_with_text_and_initial.__repr__()

    # Start the second timer so we can stop it and assert elapsed time as well
    timer_with_text_and_initial.start()
    elapsed_with_text = timer_with_text_and_initial.stop()

    # Assertions
    # __enter__ should return the same object
    assert timer_running is timer_default

    # repr values should be strings
    assert isinstance(repr_after_start, str)
    assert isinstance(repr_after_stop_default, str)
    assert isinstance(repr_timer_with_text, str)

    # Equality with unrelated type should be False
    assert equality_result is False

    # stop() should return a non-negative float elapsed time
    assert isinstance(elapsed_default, float) and elapsed_default >= 0
    assert isinstance(elapsed_with_text, float) and elapsed_with_text >= 0

def test_timer_start_and_exit_resets_start_time_and_supports_self_referential_dict():
    """Verify Timer.start() sets an internal start timestamp and __exit__ clears it.
    Also exercise that a dict can store a self-reference under the None key.
    """
    # No logger provided so Timer.start() won't attempt to log
    LOGGER = None
    timer = codetiming_timer_module.Timer(logger=LOGGER)

    # Start the timer and ensure a start timestamp was recorded
    timer.start()
    assert getattr(timer, "_start_time") is not None, "Timer did not set _start_time on start()"

    # Stop the timer via the context-manager exit and ensure the start timestamp is cleared
    timer.__exit__()
    assert getattr(timer, "_start_time") is None, "Timer did not clear _start_time on __exit__()"

    # Ensure a dict can hold a self-reference under the None key
    data = {}
    data[None] = data
    assert None in data
    assert data[None] is data

def test_start_raises_type_error_when_logger_is_not_callable():
    # Purpose:
    # Verify that Timer.start() will attempt to call the provided logger when both
    # `logger` and `initial_text` are truthy, and that a non-callable logger
    # therefore raises a TypeError.

    # Alias to the class under test
    Timer = codetiming_timer_module.Timer

    # --- Setup ---
    # Use a Timer as a context manager to obtain a running Timer instance
    context_timer = Timer()
    entered_timer = context_timer.__enter__()   # starts the timer and returns self

    # Create a non-callable logger value (boolean True)
    non_callable_logger = context_timer.__eq__(context_timer)  # True

    # Stop the context-managed timer
    context_timer.__exit__(None, None, None)

    # Construct timers so that calling start() on target_timer will attempt
    # to call the non-callable logger (boolean), triggering a TypeError.
    timer_with_non_callable_logger = Timer(initial_text=entered_timer, logger=non_callable_logger)
    target_timer = Timer(entered_timer, initial_text=timer_with_non_callable_logger, logger=non_callable_logger)

    # --- Execution & Assertion ---
    with pytest.raises(TypeError):
        target_timer.start()

def test_timer_start_stop_enter_and_copy_behavior():
    """
    Verify Timer lifecycle methods:
    - start() returns None
    - stop() returns a non-negative float (elapsed time)
    - __enter__() restarts the timer and returns self
    - copy() returns a distinct Timer instance and preserves the name if present
    """
    # Setup
    INITIAL_TEXT = "Timer started"
    TimerClass = codetiming_timer_module.Timer
    timer = TimerClass(INITIAL_TEXT)

    # Exercise
    start_result = timer.start()         # start the timer normally
    stop_result = timer.stop()           # stop and capture elapsed time
    enter_result = timer.__enter__()     # use __enter__ to start timer again (as context manager would)
    copy_result = timer.copy()           # create a copy of the timer while it is running

    # Assertions
    # start() should not return any value (None)
    assert start_result is None

    # stop() should return an elapsed time as a float (non-negative)
    assert isinstance(stop_result, float)
    assert stop_result >= 0.0

    # __enter__ should return the same Timer instance and have started it (private attr _start_time set)
    assert enter_result is timer
    assert getattr(timer, "_start_time") is not None

    # copy() should produce a distinct Timer object (not the same identity) and preserve the name if present
    assert copy_result is not timer
    assert isinstance(copy_result, TimerClass)
    if hasattr(timer, "name") and hasattr(copy_result, "name"):
        assert copy_result.name == timer.name

