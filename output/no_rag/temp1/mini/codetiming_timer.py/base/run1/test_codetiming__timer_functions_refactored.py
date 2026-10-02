import pytest

import codetiming_timer as timer

def test_timer_error_instantiation_is_exception():
    # Purpose:
    # Verify that the TimerError class can be instantiated and that it behaves like an Exception.
    # This ensures consumers can raise/catch TimerError as a normal exception type.

    # Constants
    EXPECTED_CLASS_NAME = "TimerError"

    # Setup: instantiate the TimerError without arguments (matches original test behavior)
    timer_error_instance = timer.TimerError()

    # Execution: inspect the created instance
    is_exception_subclass = isinstance(timer_error_instance, Exception)
    actual_class_name = timer_error_instance.__class__.__name__

    # Assertions: ensure it's an Exception subclass and has the expected class name
    assert is_exception_subclass, "TimerError should be an Exception subclass"
    assert actual_class_name == EXPECTED_CLASS_NAME, (
        f"Expected class name '{EXPECTED_CLASS_NAME}', got '{actual_class_name}'"
    )

def test_start_raises_TimerError_when_starting_timer_twice_after_context():
    # Constants
    TEST_TIMER_NAME = "unit-test-timer"

    # Purpose:
    # Verify that starting a Timer twice (without stopping in between) raises a TimerError.
    # This exercises the context-manager start/stop behavior and then a manual start conflict.

    # Setup: create a Timer instance and enter/exit the context manager to exercise __enter__/__exit__.
    timer_instance = timer.Timer(name=TEST_TIMER_NAME)
    # __enter__ should start the timer and return the same Timer instance
    returned_instance = timer_instance.__enter__()
    assert returned_instance is timer_instance  # ensure __enter__ returns self

    # __exit__ should stop the timer, leaving it in a stopped state
    timer_instance.__exit__()

    # Execution: start the timer once (valid)
    returned_instance.start()

    # Assertion: starting the same timer a second time without stopping should raise TimerError
    with pytest.raises(timer.TimerError):
        timer_instance.start()

def test_timer_context_manager_enter_returns_self_and_exit_returns_none():
    """Ensure Timer can be used as a context manager:
    - __enter__ starts the timer and returns the same Timer instance
    - __exit__ stops the timer and returns None
    """
    # Constants
    EMPTY_EXC_INFO = ()

    # Setup: create a Timer instance
    timer_instance = timer.Timer()

    # Execution: enter the context (starts timer) and then exit (stops timer)
    entered_instance = timer_instance.__enter__()
    exit_result = timer_instance.__exit__(*EMPTY_EXC_INFO)

    # Assertions: __enter__ returns self, __exit__ returns None
    assert entered_instance is timer_instance, "__enter__ should return the same Timer instance"
    assert exit_result is None, "__exit__ should return None"

def test_timer_exit_invokes_stop_and_returns_none(monkeypatch):
    # Verify that Timer.__exit__ calls stop() and returns None when no exception info is provided.
    DESCRIPTION = "Ensure Timer.__exit__ triggers stop() and returns None"

    # Supporting objects (kept for parity with original test)
    float_arg = timer.FloatArg()
    timer_error = timer.TimerError()

    # Timer instance under test
    t = timer.Timer()

    # Replace the instance stop() with a recorder so we can verify it was called.
    called = {"value": False}
    def _record_stop():
        called["value"] = True
    monkeypatch.setattr(t, "stop", _record_stop)

    # Execute __exit__ with no exception info
    result = t.__exit__()

    # Assertions
    assert called["value"] is True, "Timer.__exit__ should call stop()"
    assert result is None, "Timer.__exit__ should return None"

def test_timer_start_then_call_enter_on_none_from_setitem_raises_attribute_error():
    """Starting a Timer without a logger and calling dict.__setitem__
    (which returns None) should raise AttributeError when __enter__ is invoked
    on that None result.
    """
    # Setup: create and start a Timer without a logger
    t = timer.Timer(logger=None)
    t.start()
    assert t._start_time is not None

    # Execution: dict.__setitem__ returns None
    d = {}
    result = d.__setitem__(None, d)

    # Assertion: calling __enter__ on None should raise AttributeError
    with pytest.raises(AttributeError):
        result.__enter__()

def test_timer_enter_stop_equality_repr_and_initial_text_behavior():
    # Purpose:
    # - Verify that __enter__ starts the timer and stop() returns a non-negative float.
    # - Verify that Timer.__eq__ with an unrelated integer returns False.
    # - Verify that Timer accepts another Timer instance as initial_text.
    # - Verify that repr() returns a string for Timer instances.
    # - Verify that start() returns None and actually starts the timer (internal start time set).

    # Constants / test data
    NEGATIVE_INT = -1092

    # --- Setup: create timers and helpers ---
    base_timer = timer.Timer()

    # Calling __enter__ should start the timer and return the same Timer instance
    started_timer = base_timer.__enter__()

    # Create a FloatArg helper (used as callable text) for later Timer construction
    float_arg_callable = timer.FloatArg()

    # --- Execution: perform operations under test ---
    # Compare timer to an integer (should not be equal)
    equality_result = base_timer == NEGATIVE_INT

    # Stop the timer started via __enter__ and capture elapsed time
    elapsed = started_timer.stop()

    # Create a new Timer using an existing Timer instance as initial_text
    timer_with_timer_initial = timer.Timer(initial_text=started_timer)

    # Create a Timer that uses a callable text and a boolean initial_text (from equality_result)
    timer_with_callable_text = timer.Timer(text=float_arg_callable, initial_text=equality_result)

    # Obtain repr strings for both timers
    repr_base = repr(base_timer)
    repr_callable = repr(timer_with_callable_text)

    # Start the timer that was constructed with callable text; start() should return None and set internal state
    start_return = timer_with_callable_text.start()

    # --- Assertions ---
    # __eq__ with an unrelated integer should be False
    assert equality_result is False

    # stop() returns a float representing elapsed time (should be non-negative)
    assert isinstance(elapsed, float)
    assert elapsed >= 0.0

    # initial_text was stored as the Timer instance passed in
    assert timer_with_timer_initial.initial_text is started_timer

    # repr() should return string representations
    assert isinstance(repr_base, str)
    assert isinstance(repr_callable, str)

    # start() returns None and sets the internal _start_time (indicating timer is running)
    assert start_return is None
    assert getattr(timer_with_callable_text, "_start_time") is not None

def test_timer_context_start_stop_and_repr_and_equality():
    # This test verifies several basic behaviors of Timer:
    # - starting via the context-manager entry (__enter__) sets the start time
    # - stopping returns a non-negative float and clears the start time
    # - __repr__ returns a stable string representation
    # - comparing a Timer to an unrelated type yields False or NotImplemented
    # - a separately constructed Timer can be started after construction

    # Constants / test data
    UNRELATED_INT = -1092

    # Setup: create timers and start one via context-manager entry
    main_timer = timer.Timer()
    started_timer = main_timer.__enter__()  # starts the timer

    # Capture representation while running
    repr_while_running = started_timer.__repr__()

    # Create additional timers using the captured repr as initial_text
    timer_with_initial = timer.Timer(initial_text=repr_while_running)
    float_arg_callable = timer.FloatArg()
    timer_with_callable_text = timer.Timer(text=float_arg_callable, initial_text=repr_while_running)

    # Execution: compare timer to an unrelated type and stop the running timer
    equality_result = main_timer.__eq__(UNRELATED_INT)
    elapsed_seconds = started_timer.stop()

    # Capture representations after stopping and from the other timer
    repr_after_stop = main_timer.__repr__()
    repr_other_timer = timer_with_callable_text.__repr__()

    # Start the other timer to ensure it can transition to running state
    timer_with_callable_text.start()

    # Assertions: representations are strings and stable for the main timer
    assert isinstance(repr_while_running, str)
    assert isinstance(repr_after_stop, str)
    assert repr_while_running == repr_after_stop

    # Comparing to an unrelated type should not produce True; accept False or NotImplemented
    assert equality_result in (False, NotImplemented)

    # Stopping returns a non-negative float, clears the start time, and sets last
    assert isinstance(elapsed_seconds, float)
    assert elapsed_seconds >= 0
    assert main_timer._start_time is None
    assert main_timer.last == elapsed_seconds

    # The other timer's repr is a string and starting it sets its start time
    assert isinstance(repr_other_timer, str)
    assert timer_with_callable_text._start_time is not None

def test_timer_start_stop_and_setitem_return_value_behaviour():
    # Purpose:
    # - Verify Timer.start() initializes the timer state and returns None.
    # - Verify Timer.__exit__() (context manager stop) clears the start time and returns None.
    # - Demonstrate that dict.__setitem__ returns None, that the dict was updated,
    #   and that calling an attribute on that None raises AttributeError.
    
    # Constants
    NO_LOGGER = None
    DICT_KEY = None

    # --- Setup: create Timer with no logger
    timer_obj = timer.Timer(logger=NO_LOGGER)

    # --- Execution: start the timer
    start_return = timer_obj.start()

    # --- Assertions after start
    # start() returns None and the internal start time should be set
    assert start_return is None
    assert timer_obj._start_time is not None

    # --- Execution: stop the timer via context manager exit
    exit_return = timer_obj.__exit__()  # __exit__ delegates to stop()

    # --- Assertions after exit/stop
    # __exit__ returns None and the internal start time should be cleared
    assert exit_return is None
    assert timer_obj._start_time is None

    # --- Setup: prepare a dict and use __setitem__ directly
    test_dict = {}
    setitem_return = test_dict.__setitem__(DICT_KEY, test_dict)

    # --- Assertions for dict setitem behavior
    # __setitem__ returns None, and the dict should contain the key mapping to itself
    assert setitem_return is None
    assert DICT_KEY in test_dict and test_dict[DICT_KEY] is test_dict

    # The repr of the None return is the string "None"
    assert setitem_return.__repr__() == "None"

    # Attempting to call a method on the None return value should raise AttributeError
    import pytest
    with pytest.raises(AttributeError):
        setitem_return.start()

def test_start_raises_typeerror_when_logger_is_not_callable():
    # Start a base timer via its context manager and verify basic behavior.
    base_timer = timer.Timer()
    entered_timer = base_timer.__enter__()            # starts base_timer and returns it
    assert entered_timer is base_timer

    equality_result = base_timer.__eq__(base_timer)   # should be True (timer equals itself)
    assert equality_result is True

    exit_result = base_timer.__exit__()               # stops the timer
    assert exit_result is None

    # Build timers that reproduce the original scenario:
    # - initial_text is a Timer instance (entered_timer)
    # - logger is a non-callable boolean (equality_result)
    timer_with_initial_text = timer.Timer(initial_text=entered_timer, logger=equality_result)
    timer_with_bad_logger = timer.Timer(entered_timer, initial_text=timer_with_initial_text, logger=equality_result)

    # Starting timer_with_bad_logger should attempt to call the non-callable logger and raise TypeError.
    with pytest.raises(TypeError):
        timer_with_bad_logger.start()

def test_timer_start_stop_enter_and_copy_behavior():
    # Purpose:
    # Verify basic Timer lifecycle:
    # - start() returns None
    # - stop() returns a non-negative float
    # - __enter__() returns the same Timer instance and starts the timer again
    # - copy() does not raise and returns either None or another Timer-like object

    # Setup
    INITIAL_TEXT = "Timer started"
    timer_obj = timer.Timer(INITIAL_TEXT)

    # Execution: start the timer, stop it, re-enter as context manager, and call copy()
    start_result = timer_obj.start()
    elapsed = timer_obj.stop()
    entered = timer_obj.__enter__()  # should call start() and return self
    copy_result = timer_obj.copy()    # ensure this does not raise

    # Assertions
    # start() should return None (it only starts the timer)
    assert start_result is None

    # stop() should return a non-negative float representing elapsed seconds
    assert isinstance(elapsed, float)
    assert elapsed >= 0.0

    # __enter__() should return the same timer instance and leave the timer running
    assert entered is timer_obj
    assert timer_obj._start_time is not None

    # copy() may return None or a Timer-like object; if it returns something, it should be a Timer
    if copy_result is not None:
        assert isinstance(copy_result, timer.Timer)

