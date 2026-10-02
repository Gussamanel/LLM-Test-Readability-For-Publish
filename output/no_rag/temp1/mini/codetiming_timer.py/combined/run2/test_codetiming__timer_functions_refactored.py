import pytest

import codetiming_timer as timer

def test_timer_error_is_instantiable_and_behaves_like_exception():
    """Verify TimerError can be instantiated and behaves like a normal Exception."""
    TIMER_ERROR = timer.TimerError

    # Instantiate the custom error
    err = TIMER_ERROR()

    # Basic behavior checks
    assert isinstance(err, TIMER_ERROR)
    assert isinstance(err, Exception)

    # Ensure converting to string does not raise and returns a string
    assert isinstance(str(err), str)

def test_start_raises_if_already_running_after_context_restart():
    """
    Verify that starting a Timer that's already running raises TimerError.
    Use the context-manager entry/exit to start and stop the timer, then
    restart it and attempt to start it again to confirm the error is raised.
    """
    TIMER_CLASS = timer.Timer
    EXPECTED_EXCEPTION = timer.TimerError

    # Create and enter the context to start the timer
    timer_instance = TIMER_CLASS()
    entered = timer_instance.__enter__()  # starts the timer

    # Exit the context to stop the timer so it can be restarted
    timer_instance.__exit__()  # stops the timer

    # Restart the timer (should succeed)
    entered.start()

    # Attempting to start the already-running timer should raise TimerError
    with pytest.raises(EXPECTED_EXCEPTION):
        timer_instance.start()

def test_timer_context_manager_enter_returns_self_and_exit_returns_none():
    # Purpose:
    # Verify that Timer used as a context manager returns itself on __enter__
    # and that __exit__ returns None (stops the timer).
    
    # Constants
    EXPECTED_EXIT_RETURN = None

    # Setup: create a Timer instance
    timer_instance = timer.Timer()

    # Execution: enter the context manager (should start and return self)
    entered_timer = timer_instance.__enter__()

    # Execution: exit the context manager (should stop and return None)
    exit_result = timer_instance.__exit__()

    # Assertions: ensure __enter__ returned the same Timer and __exit__ returned None
    assert entered_timer is timer_instance
    assert exit_result is EXPECTED_EXIT_RETURN

def test_timer_exit_stops_timer_and_handles_exception_info_correctly():
    # Purpose:
    # Verify that Timer.__exit__ stops the context-manager timer and
    # returns None both when called without exception info and when
    # called with exception information.

    # Constants
    EXPECTED_RETURN = None  # __exit__ should return None per context manager protocol

    # Setup: create placeholder argument and exception objects and a Timer instance
    float_placeholder = module_0.FloatArg()
    timer_exception = module_0.TimerError()
    timer_instance = module_0.Timer()

    # Execution: call __exit__ without any exception information
    result_no_exc = timer_instance.__exit__()

    # Assertion: __exit__ returns None and does not raise when no exception info provided
    assert result_no_exc is EXPECTED_RETURN

    # Execution: call __exit__ with typical exception info tuple
    exc_info = (type(timer_exception), timer_exception, None)
    result_with_exc = timer_instance.__exit__(*exc_info)

    # Assertion: __exit__ returns None and handles provided exception info gracefully
    assert result_with_exc is EXPECTED_RETURN

def test_timer_start_with_no_logger_and_setitem_returns_non_context_raises():
    # Purpose:
    # - Verify Timer.start() works when no logger is provided (logger=None).
    # - Verify that dict.__setitem__ returns None (not a context manager),
    #   and attempting to call __enter__ on that return value raises AttributeError.

    # Constants / Setup
    LOGGER = None
    KEY_FOR_DICT = None

    timer_instance = timer.Timer(logger=LOGGER)

    # Execution: start the timer (should set internal start time without logging)
    timer_instance.start()

    # Assert timer was started (internal state changed)
    assert timer_instance._start_time is not None

    # Setup: create a dictionary and call __setitem__ which returns None
    sample_dict = {}
    result_of_setitem = sample_dict.__setitem__(KEY_FOR_DICT, sample_dict)

    # Execution & Assertion: result_of_setitem is None and is not a context manager;
    # calling __enter__ on it should raise AttributeError
    with pytest.raises(AttributeError):
        result_of_setitem.__enter__()

def test_timer_context_manager_equality_and_start_behavior():
    # Purpose:
    # - Verify the Timer context manager starts a timer and stop() returns a non-negative float.
    # - Ensure __eq__ can be called with an integer and returns a boolean.
    # - Ensure __repr__ returns strings for Timer instances.
    # - Ensure start() can be called after creating a Timer with unusual initial_text and that it sets an internal start time.
    #
    # This test keeps setup, execution and assertions separated and uses descriptive names.

    # -----------------------
    # Setup
    # -----------------------
    ROOT_TIMER = timer.Timer()                     # base Timer instance
    ctx_timer = ROOT_TIMER.__enter__()             # start via context manager entry

    NEGATIVE_INT = -1092                           # value used to exercise __eq__
    float_arg_0 = timer.FloatArg()                 # object used as 'text' argument
    float_arg_1 = timer.FloatArg()                 # additional FloatArg (unused but mirrors original flow)

    timer_with_ctx_initial = timer.Timer(initial_text=ctx_timer)  # Timer created with a Timer object as initial_text

    # -----------------------
    # Execution
    # -----------------------
    eq_result = ROOT_TIMER.__eq__(NEGATIVE_INT)    # call equality with an integer
    elapsed = ctx_timer.stop()                     # stop the timer started by __enter__()

    custom_timer = timer.Timer(text=float_arg_0, initial_text=eq_result)  # create timer using boolean initial_text
    repr_root = ROOT_TIMER.__repr__()              # string representation of the root timer
    repr_custom = custom_timer.__repr__()          # string representation of the custom timer

    start_result = custom_timer.start()            # start the custom timer

    # -----------------------
    # Assertions
    # -----------------------
    assert isinstance(eq_result, bool), "Expected __eq__ to return a boolean"
    assert isinstance(elapsed, float), "Expected stop() to return a float elapsed time"
    assert elapsed >= 0.0, "Elapsed time should be non-negative"

    assert isinstance(repr_root, str), "Expected __repr__() to return a string for the root timer"
    assert isinstance(repr_custom, str), "Expected __repr__() to return a string for the custom timer"

    # start() returns None on success and should set an internal start time
    assert start_result is None, "Expected start() to return None"
    assert getattr(custom_timer, "_start_time", None) is not None, "Expected start() to set _start_time on the timer"

    # Clean up: stop the custom timer to avoid leaving a running timer
    custom_timer.stop()

def test_timer_context_start_stop_and_text_callable_behaviour():
    # Purpose:
    # - Using the Timer as a context manager should start the timer
    # - repr(timer) should return a non-empty string usable as initial_text
    # - stop() should return a non-negative float
    # - Timer.__eq__ with a non-timer (int) should return False
    # - A Timer configured with a callable text and an initial_text can be started and stopped normally

    # Test data
    NEG_INT = -1092

    # Setup
    main_timer = timer.Timer()
    float_formatter_1 = timer.FloatArg()
    float_formatter_2 = timer.FloatArg()

    # Start via context manager __enter__ (expected to call start() and return self)
    cm_timer = main_timer.__enter__()

    # __enter__ should return the same instance and set a start time
    assert cm_timer is main_timer, "Timer.__enter__ should return the same Timer instance"
    assert getattr(main_timer, "_start_time") is not None, "Timer should have a start time after __enter__()"

    # Use repr of the running timer as initial_text for other timers
    initial_text_from_repr = repr(cm_timer)
    assert isinstance(initial_text_from_repr, str) and initial_text_from_repr != ""

    # Equality with an unrelated type should be False
    assert main_timer.__eq__(NEG_INT) is False, "Timer.__eq__ with an int should return False"

    # Stop the context-managed timer and assert elapsed value
    elapsed_main = cm_timer.stop()
    assert isinstance(elapsed_main, float), "stop() should return a float"
    assert elapsed_main >= 0.0, "Elapsed time should be non-negative"

    # Create another timer using the repr string as initial_text and a callable text formatter
    timer_with_callable_text = timer.Timer(text=float_formatter_1, initial_text=initial_text_from_repr)

    # Ensure reprs are valid strings for both timers
    assert isinstance(repr(main_timer), str)
    assert isinstance(repr(timer_with_callable_text), str)

    # Start and stop the timer configured with a callable text to ensure it runs without error
    timer_with_callable_text.start()
    assert getattr(timer_with_callable_text, "_start_time") is not None, "Timer should have started"
    elapsed_callable = timer_with_callable_text.stop()
    assert isinstance(elapsed_callable, float) and elapsed_callable >= 0.0

    # Sanity: additional FloatArg instance exists and is independent (no functional assertion needed)
    _ = float_formatter_2

def test_timer_start_stop_and_self_referential_dict_insertion():
    # Purpose:
    # - Verify Timer.start() sets an internal start time (when logger is None).
    # - Verify Timer.__exit__() (context-manager exit) stops the timer.
    # - Demonstrate inserting a None key that references the dict itself and validate the self-reference.
    # - Verify the timer can be started again after being stopped.

    # Constants / configuration
    LOGGER = None
    DICT_SELF_KEY = None

    # Setup: create Timer with no logger
    timer_instance = timer.Timer(logger=LOGGER)

    # Execution: start the timer and record the start time
    timer_instance.start()

    # Assertion: start() should set a numeric start time
    assert isinstance(timer_instance._start_time, float), "Timer._start_time should be a float after start()"

    # Execution: stop the timer via the context-manager exit method
    timer_instance.__exit__()  # calls .stop()

    # Assertion: after stopping, the internal start time should be cleared (None)
    assert timer_instance._start_time is None, "Timer._start_time should be None after __exit__()/stop()"

    # Setup/Execution: create a dictionary and insert a self-reference under the None key
    my_dict = {}
    my_dict[DICT_SELF_KEY] = my_dict

    # Assertion: the dictionary value for the None key should be the dictionary itself (self-reference)
    assert my_dict[DICT_SELF_KEY] is my_dict, "Dictionary should contain a self-reference under the None key"

    # The repr of a self-referential dict typically shows recursion, e.g. '{None: {...}}'
    repr_text = repr(my_dict)
    assert "{None: {...}}" in repr_text or "{None: {...}}" == repr_text, "repr should indicate a self-reference"

    # Execution: ensure the timer can be started again after being stopped
    timer_instance.start()

    # Assertion: start() should set a numeric start time again
    assert isinstance(timer_instance._start_time, float), "Timer._start_time should be a float after restarting"

def test_timer_start_raises_when_logger_is_not_callable_and_initial_text_is_truthy():
    """Verify Timer.start() raises TypeError when logger is truthy but not callable and initial_text is truthy."""
    # Alias to the Timer class under test
    TIMER_CLASS = timer.Timer

    # --------------------
    # Setup: exercise context-manager and equality behavior
    # --------------------
    base_timer = TIMER_CLASS()
    entered_timer = base_timer.__enter__()            # start via context-manager entry
    assert entered_timer is base_timer                 # __enter__ should return self

    equality_result = base_timer.__eq__(base_timer)    # compare timer to itself
    assert equality_result is True                     # __eq__ with itself should be True

    exit_result = base_timer.__exit__()                # stop via context-manager exit
    assert exit_result is None                         # __exit__ should return None

    # --------------------
    # Construct edge-case timers
    # --------------------
    # - initial_text is a Timer instance (truthy)
    # - logger is a boolean True (truthy but not callable)
    timer_with_timer_initial_text = TIMER_CLASS(initial_text=entered_timer, logger=equality_result)
    target_timer = TIMER_CLASS(entered_timer, initial_text=timer_with_timer_initial_text, logger=equality_result)

    # --------------------
    # Execution & Assertion
    # --------------------
    # Timer.start() will attempt to call logger when both logger and initial_text are truthy.
    # Since logger is True (not callable), starting should raise a TypeError.
    with pytest.raises(TypeError):
        target_timer.start()

def test_timer_start_stop_enter_and_copy():
    # Purpose:
    # Verify basic Timer lifecycle methods work together:
    # - start() begins timing
    # - stop() returns a non-negative float elapsed time
    # - __enter__() starts the timer and returns the same Timer instance
    # - copy() returns a Timer-like object (a distinct Timer instance with the same name)
    
    # Constants / Setup
    TIMER_NAME = "Timer started"
    original_timer = timer.Timer(TIMER_NAME)
    
    # Execution: start the timer and then stop it to obtain an elapsed time
    original_timer.start()
    elapsed_seconds = original_timer.stop()
    
    # Execution: use context-enter helper to start the timer again and call copy()
    entered_timer = original_timer.__enter__()  # should call start() and return self
    copied_timer = original_timer.copy()  # should produce a Timer-like copy
    
    # Assertions: validate outcomes and side-effects
    assert isinstance(elapsed_seconds, float), "stop() should return a float elapsed time"
    assert elapsed_seconds >= 0, "Elapsed time should be non-negative"
    
    # __enter__ should return the same instance and leave it running (start called)
    assert entered_timer is original_timer, "__enter__ should return self"
    assert getattr(original_timer, "_start_time", None) is not None, "Timer should be running after __enter__"
    
    # copy() should produce a Timer object distinct from the original, preserving the name
    assert isinstance(copied_timer, timer.Timer), "copy() should return a Timer instance"
    assert copied_timer is not original_timer, "copy() should return a distinct instance"
    assert getattr(copied_timer, "name", None) == original_timer.name, "Copied timer should preserve the name"

