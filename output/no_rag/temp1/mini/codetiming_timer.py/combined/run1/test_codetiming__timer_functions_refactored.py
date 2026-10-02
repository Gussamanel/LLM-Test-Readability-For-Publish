import pytest

import codetiming_timer as timer

def test_timer_error_instantiation_and_type():
    # Purpose:
    # Verify that the TimerError class can be instantiated and that it is an Exception subclass.

    # Constants / test fixtures
    TEST_ERROR_CLASS = timer.TimerError
    EXPECTED_BASE_EXCEPTION = Exception

    # Setup: create an instance of the TimerError
    error_instance = TEST_ERROR_CLASS()

    # Execution & Assertions:
    # - The created object should be an instance of the TimerError class.
    # - The TimerError class should inherit from the built-in Exception type.
    assert isinstance(error_instance, TEST_ERROR_CLASS)
    assert issubclass(TEST_ERROR_CLASS, EXPECTED_BASE_EXCEPTION)

def test_timer_start_raises_if_started_twice_after_context_exit():
    # Constants used in the test
    TEST_TIMER_NAME = "sample_timer"

    # Setup: create a Timer instance (not running yet)
    timer_instance = timer.Timer(name=TEST_TIMER_NAME)

    # Execution: enter the timer context -> __enter__ calls start() and returns the same Timer
    context_timer = timer_instance.__enter__()
    assert context_timer is timer_instance  # context manager should return the same instance

    # Execution: exit the context -> __exit__ should stop the timer and return None
    exit_result = timer_instance.__exit__(None, None, None)

    # Assertion: __exit__ returns None (stops the timer)
    assert exit_result is None

    # Execution: start the timer again after context exit -> should succeed and return None
    first_start_result = context_timer.start()

    # Assertion: start() returns None on successful start
    assert first_start_result is None

    # Execution & Assertion: starting the timer a second time without stopping should raise TimerError
    with pytest.raises(timer.TimerError):
        timer_instance.start()

def test_timer_context_manager_enter_and_exit_returns_expected():
    # Purpose:
    # Verify that Timer implements the context manager protocol:
    # - __enter__ starts the timer and returns the same Timer instance
    # - __exit__ stops the timer and returns None

    # Arrange (setup)
    TIMER_CLASS = timer.Timer
    EXPECTED_EXIT_RETURN = None
    timer_instance = TIMER_CLASS()

    # Act (execution)
    enter_result = timer_instance.__enter__()  # start via context manager enter
    exit_result = timer_instance.__exit__()    # stop via context manager exit

    # Assert (verification)
    # __enter__ should return the same Timer instance
    assert enter_result is timer_instance
    # __exit__ should return None (no exception suppression)
    assert exit_result is EXPECTED_EXIT_RETURN

def test_timer_exit_stops_timer_and_returns_none():
    # Purpose:
    # Verify that calling the context manager __exit__ method on Timer stops the timer
    # and returns None. Also ensure related helper objects can be instantiated.
    
    # Constants
    # No exception information provided to __exit__ (equivalent to normal exit)
    NO_EXCEPTION_INFO = ()
    
    # Setup: create required objects for the test
    float_arg_instance = timer.FloatArg()
    timer_error_instance = timer.TimerError()
    context_timer = timer.Timer()
    
    # Execution: call __exit__ without exception info (normal context manager exit)
    result = context_timer.__exit__()  # calls self.stop() internally
    
    # Assertions: __exit__ should return None and object types should be correct
    assert result is None
    assert isinstance(float_arg_instance, timer.FloatArg)
    assert isinstance(timer_error_instance, timer.TimerError)

def test_timer_start_and_calling_enter_on_non_context_object_raises():
    # Create a Timer with no logger and an empty dictionary
    timer_instance = timer.Timer(logger=None)
    sample_dict = {}

    # Start the timer and verify an internal start time was recorded
    timer_instance.start()
    assert timer_instance._start_time is not None

    # dict.__setitem__ returns None (not a context manager). Calling __enter__ on that should raise AttributeError.
    non_context_result = sample_dict.__setitem__(None, sample_dict)
    with pytest.raises(AttributeError):
        non_context_result.__enter__()

def test_timer_context_manager_start_stop_and_repr():
    # Purpose:
    # Verify Timer's context-manager start (via __enter__), stop, equality, repr,
    # construction with non-string initial_text, and starting a Timer that uses a callable text.
    # The test separates setup, execution, and assertions for clarity.

    # --- Constants / test data ---
    NEGATIVE_INT = -1092

    # --- Setup: create timers and callables used in the test ---
    primary_timer = timer.Timer()
    # Start the primary timer using the context-manager __enter__ method
    entered_timer = primary_timer.__enter__()

    # Construct a timer whose initial_text is another Timer object (non-string initial_text)
    timer_with_timer_initial = timer.Timer(initial_text=entered_timer)

    # Construct a callable used as the timer's text formatter
    float_text_callable = timer.FloatArg()
    # Will create another timer where initial_text is the result of an equality check (bool)
    timer_with_callable_text = None  # defined later after equality and stop

    # --- Execution: exercise methods under test ---
    # Compare the primary timer to an unrelated integer to exercise __eq__
    equality_result = primary_timer.__eq__(NEGATIVE_INT)

    # Stop the entered timer and capture elapsed time
    elapsed_time = entered_timer.stop()

    # Now create a timer that uses a callable for the text and the equality_result as initial_text
    timer_with_callable_text = timer.Timer(text=float_text_callable, initial_text=equality_result)

    # Capture string representations
    repr_primary = repr(primary_timer)
    repr_callable_timer = repr(timer_with_callable_text)

    # Start the timer that uses a callable text (start() should return None)
    start_return = timer_with_callable_text.start()

    # --- Assertions: verify expected state and return values ---
    # __enter__ should return the same Timer instance and have started it
    assert entered_timer is primary_timer

    # stop() should return a non-negative float and set the timer's last attribute
    assert isinstance(elapsed_time, float) and elapsed_time >= 0
    assert primary_timer.last == elapsed_time

    # After stopping, the timer's _start_time should have been cleared
    assert entered_timer._start_time is None

    # Equality with an unrelated integer should be False
    assert equality_result is False

    # The timer constructed with another Timer as initial_text should preserve that object
    assert timer_with_timer_initial.initial_text is entered_timer

    # Repr outputs should contain an identifier for the Timer type (basic sanity check)
    assert "Timer" in repr_primary
    assert "Timer" in repr_callable_timer

    # start() returns None and sets an internal start time
    assert start_return is None
    assert timer_with_callable_text._start_time is not None

    # The callable text was attached correctly
    assert timer_with_callable_text.text is float_text_callable

def test_timer_context_manager_start_stop_and_repr_behavior():
    # Constants / test data
    DUMMY_INT = -1092

    # Setup: create a Timer and start it using the context-manager entry method
    timer_a = timer.Timer()
    # __enter__ starts the timer and returns the Timer instance
    timer_a_ctx = timer_a.__enter__()

    # Capture a representation to use as initial_text for other timers
    captured_repr = timer_a_ctx.__repr__()

    # Create a callable formatter (FloatArg) and additional Timer instances to exercise repr/initial_text/text behavior
    float_formatter = timer.FloatArg()
    timer_b = timer.Timer(initial_text=captured_repr)
    timer_c = timer.Timer(text=float_formatter, initial_text=captured_repr)

    # Execution: exercise equality, stopping, repr again, and starting another timer
    eq_result = timer_a.__eq__(DUMMY_INT)    # compare Timer to an integer
    elapsed_seconds = timer_a_ctx.stop()     # stop the timer started via __enter__()

    repr_after_stop = timer_a.__repr__()     # representation after stopping
    repr_timer_c = timer_c.__repr__()        # representation of the timer created with text and initial_text
    timer_c.start()                          # start timer_c to ensure .start() path runs

    # Assertions: verify types and expected non-error behaviors
    # - repr values should be strings
    assert isinstance(captured_repr, str)
    assert isinstance(repr_after_stop, str)
    assert isinstance(repr_timer_c, str)

    # - equality with an unrelated int should not return True (either False or NotImplemented)
    assert eq_result in (False, NotImplemented)

    # - stopping a running timer returns a non-negative float elapsed time
    assert isinstance(elapsed_seconds, float)
    assert elapsed_seconds >= 0.0

    # - starting timer_c should set an internal start time (ensure start() executed)
    assert getattr(timer_c, "_start_time", None) is not None

    # Clean up: stop timer_c to avoid leaving a running timer
    timer_c.stop()

def test_timer_start_exit_and_none_method_call_behavior():
    """
    Purpose:
    - Verify Timer.start() sets an internal start time
    - Verify Timer.__exit__() (context-manager exit) stops the timer (clears start time)
    - Verify dict.__setitem__ returns None when setting a key to a self-referential value
    - Verify that attempting to call a method on the None returned by dict.__setitem__ raises AttributeError
    """
    # Constants / test data
    LOGGER = None
    SELF_KEY = None

    # Setup: create a Timer instance with no logger
    timer_instance = timer.Timer(logger=LOGGER)

    # Precondition: timer not started
    assert getattr(timer_instance, "_start_time", None) is None

    # Start the timer
    timer_instance.start()

    # start() should set an internal start time
    assert getattr(timer_instance, "_start_time", None) is not None

    # Call __exit__ to stop the timer (context-manager exit)
    timer_instance.__exit__()  # should internally call stop()

    # Timer should be stopped and internal start time cleared
    assert getattr(timer_instance, "_start_time", None) is None

    # Set a dictionary item where the value is the dict itself; __setitem__ returns None
    sample_dict = {}
    setitem_result = sample_dict.__setitem__(SELF_KEY, sample_dict)

    # The dict should contain a self-referential value and __setitem__ should return None
    assert sample_dict[SELF_KEY] is sample_dict
    assert setitem_result is None
    assert repr(setitem_result) == "None"

    # Calling a method on the None returned by __setitem__ should raise AttributeError
    with pytest.raises(AttributeError):
        setitem_result.start()

def test_context_enter_exit_and_start_with_non_callable_logger_raises():
    # Purpose:
    # - Verify context manager start/stop behavior via __enter__ and __exit__.
    # - Verify __eq__ behavior when comparing a Timer to itself.
    # - Attempt to start a Timer that was constructed with a non-callable logger and
    #   a non-string initial_text to confirm a TypeError is raised when the code
    #   tries to call the logger.

    # Constants / test inputs
    UNUSED_INITIAL_TEXT = None  # placeholder for clarity

    # --- Setup ---
    base_timer = timer.Timer()
    # Use the context-manager entry method to start the timer and return the instance
    entered_timer = base_timer.__enter__()
    # Equality check against itself (should be True)
    equality_result = base_timer.__eq__(base_timer)
    # Stop the timer via the context-manager exit method
    exit_result = base_timer.__exit__()

    # Construct timers using the previously created objects to reproduce the original scenario:
    # - Provide a Timer instance as initial_text (non-string)
    # - Provide the boolean equality result as logger (non-callable)
    timer_with_nonstring_initial = timer.Timer(initial_text=entered_timer, logger=equality_result)
    constructed_timer = timer.Timer(entered_timer, initial_text=timer_with_nonstring_initial, logger=equality_result)

    # --- Execution & Assertions ---
    # Verify __enter__ returned the same instance
    assert entered_timer is base_timer
    # __eq__ comparing the timer to itself should be True
    assert equality_result is True
    # __exit__ should return None (no exception propagation)
    assert exit_result is None

    # Starting constructed_timer should attempt to call a non-callable logger (the boolean True)
    # which is expected to raise a TypeError. Ensure the start failed and did not set a start time.
    with pytest.raises(TypeError):
        constructed_timer.start()
    assert getattr(constructed_timer, "_start_time", None) is None

def test_timer_start_stop_enter_and_copy_behaviour():
    # Purpose:
    # Verify Timer.start(), Timer.stop(), Timer.__enter__() and Timer.copy()
    # behave as expected: start returns None and sets an internal start time,
    # stop returns a float elapsed value and clears the start time, __enter__
    # returns the timer and starts it, and copy returns a distinct Timer
    # with the same configuration.

    # Constants / Setup
    INITIAL_TEXT = "Timer started"
    timer_obj = timer.Timer(INITIAL_TEXT)

    # Execution: start the timer
    start_result = timer_obj.start()

    # Assertions: start behavior
    assert start_result is None  # start() should not return a value
    assert getattr(timer_obj, "_start_time", None) is not None  # internal start time set

    # Execution: stop the timer and capture elapsed time
    elapsed = timer_obj.stop()

    # Assertions: stop behavior
    assert isinstance(elapsed, float)  # stop() should return a float elapsed time
    assert pytest.approx(timer_obj.last, rel=1e-12) == elapsed  # last should equal returned elapsed
    assert getattr(timer_obj, "_start_time", None) is None  # start time cleared after stop
    assert elapsed >= 0  # elapsed time should be non-negative

    # Execution: use __enter__() to start again (context-manager entry)
    entered = timer_obj.__enter__()

    # Assertions: __enter__ behavior
    assert entered is timer_obj  # __enter__ returns the timer instance
    assert getattr(timer_obj, "_start_time", None) is not None  # start time should be set

    # Clean up: stop the timer started by __enter__()
    elapsed2 = timer_obj.stop()
    assert isinstance(elapsed2, float) and elapsed2 >= 0

    # Execution: copy the timer
    copied = timer_obj.copy()

    # Assertions: copy behavior
    assert isinstance(copied, timer.Timer)  # copy returns a Timer instance
    assert copied is not timer_obj  # copy is a distinct object
    # The copy should preserve configuration attributes (compare common names if present)
    assert getattr(copied, "initial_text", None) == getattr(timer_obj, "initial_text", None)
    assert getattr(copied, "text", None) == getattr(timer_obj, "text", None)

