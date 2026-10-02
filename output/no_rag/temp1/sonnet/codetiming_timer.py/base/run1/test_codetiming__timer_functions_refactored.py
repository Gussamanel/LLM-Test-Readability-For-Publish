import pytest
import codetiming_timer as timer

def test_timer_error_can_be_instantiated():
    # Verify that TimerError can be instantiated without any arguments
    # This tests the basic constructor of the TimerError exception class

    # Execution: Create a TimerError instance with no arguments
    timer_error = timer.TimerError()

    # Assert: Verify the instance was created successfully and is of the correct type
    assert isinstance(timer_error, timer.TimerError)

def test_timer_error_on_start_while_already_running():
    """
    Test that starting a timer that is already running raises a TimerError.
    
    The Timer context manager automatically starts the timer on __enter__ and stops it 
    on __exit__. While inside the context manager, the timer is running. Attempting to 
    call start() on a running timer should raise a TimerError.
    After exiting the context manager, the timer is stopped, and calling start() again 
    should succeed without errors.
    """
    # Setup: Create a new timer instance
    t = Timer()
    
    # Execution: Use the timer as a context manager
    # __enter__ starts the timer and returns itself
    timer_in_context = t.__enter__()
    
    # Attempting to start the timer again while it's already running
    # This should raise a TimerError since the timer is already running
    with pytest.raises(Exception):
        timer_in_context.start()
    
    # Exit the context manager, which stops the timer internally
    t.__exit__(None, None, None)
    
    # Starting the original timer after it has been stopped via __exit__ should succeed
    t.start()

def test_timer_context_manager_enter_and_exit():
    # Test that the Timer can be used as a context manager
    # verifying that __enter__ returns the timer instance and __exit__ stops it

    # Setup: Create a new Timer instance
    timer_instance = timer.Timer()

    # Execution: Simulate entering the context manager, which starts the timer
    # and returns the Timer instance itself
    returned_timer = timer_instance.__enter__()

    # Assert: The returned value from __enter__ should be the same Timer instance
    assert returned_timer is timer_instance

    # Execution: Simulate exiting the context manager, which stops the timer
    # __exit__ accepts optional exception info arguments and returns None
    result = timer_instance.__exit__()

    # Assert: __exit__ should return None as it only stops the timer
    assert result is None

def test_timer_exit_stops_context_manager():
    # Test that __exit__ properly stops the timer when used as a context manager
    
    # Setup: Create timer-related objects
    float_arg = timer.FloatArg()
    timer_error = timer.TimerError()
    test_timer = timer.Timer()
    
    # Execute: Call __exit__ to simulate exiting the context manager
    # __exit__ internally calls self.stop() to halt the timer
    test_timer.__exit__()
    
    # Assertion: No exception raised means __exit__ successfully called stop()
    # The timer should have been stopped without errors

def test_timer_enter_raises_error_when_called_on_none():
    """
    Test that a Timer can be started without a logger, and that calling __enter__
    on None raises an AttributeError, since None does not implement the context
    manager protocol.
    """
    NO_LOGGER = None

    # Setup: Create and start a timer with no logger
    timer_instance = timer.Timer(logger=NO_LOGGER)
    timer_instance.start()

    # Execution & Assertion: Attempting to call __enter__ on None should raise
    # an AttributeError since None does not have a __enter__ method
    none_value = None
    with pytest.raises(AttributeError):
        none_value.__enter__()

def test_timer_context_manager_with_float_arg_and_repr():
    """
    Test Timer behavior when used as a context manager, with FloatArg as text parameter,
    and verifying repr output and start functionality.
    
    This test verifies:
    1. Timer can be used as a context manager via __enter__
    2. A stopped timer can be compared with an integer using __eq__
    3. Timer can be initialized with another timer instance as initial_text
    4. Timer repr works correctly for different timer configurations
    5. Timer with FloatArg text and non-boolean initial_text can be started
    """
    NEGATIVE_INT_VALUE = -1092

    # Setup: Create initial timer and use it as context manager
    base_timer = timer.Timer()
    context_timer = base_timer.__enter__()  # Starts the timer and returns it

    # Setup: Create FloatArg instances and additional timers
    float_arg_text = timer.FloatArg()
    timer_with_timer_as_initial_text = timer.Timer(initial_text=context_timer)
    float_arg_initial = timer.FloatArg()

    # Execution: Compare base timer with a negative integer
    eq_result = base_timer.__eq__(NEGATIVE_INT_VALUE)

    # Execution: Stop the context manager timer and capture elapsed time
    elapsed_time = context_timer.stop()

    # Setup: Create a timer using FloatArg as text and eq_result as initial_text
    timer_with_float_arg = timer.Timer(text=float_arg_text, initial_text=eq_result)

    # Execution: Get string representations of both timers
    base_timer_repr = base_timer.__repr__()
    float_arg_timer_repr = timer_with_float_arg.__repr__()

    # Execution: Start the timer configured with FloatArg
    start_result = timer_with_float_arg.start()

    # Assertion: start() should return None
    assert start_result is None

def test_timer_context_manager_with_repr_and_custom_text():
    """
    Test that verifies Timer behavior when used as a context manager,
    including repr output, equality comparison, stop functionality,
    and initialization with custom text parameters.
    """
    # Constants
    NEGATIVE_INT_VALUE = -1092

    # Setup: Create a timer and enter context manager
    base_timer = timer.Timer()
    context_timer = base_timer.__enter__()

    # Get repr of the running context timer to use as initial text
    timer_repr_text = context_timer.__repr__()

    # Create additional timers with custom text configurations
    float_arg_text = timer.FloatArg()
    timer_with_initial_text = timer.Timer(initial_text=timer_repr_text)
    float_arg_initial = timer.FloatArg()

    # Execution: Test equality comparison with negative integer
    equality_result = base_timer.__eq__(NEGATIVE_INT_VALUE)

    # Stop the context timer and capture elapsed time
    elapsed_time = context_timer.stop()

    # Create a timer with both custom text and initial text
    timer_with_custom_texts = timer.Timer(text=float_arg_text, initial_text=timer_repr_text)

    # Get repr of both timers after stop
    base_timer_repr = base_timer.__repr__()
    custom_text_timer_repr = timer_with_custom_texts.__repr__()

    # Start the timer with custom text configurations
    timer_with_custom_texts.start()

    # Assertions: Verify elapsed time was recorded and equality check returned a result
    assert elapsed_time >= 0, "Elapsed time should be non-negative"
    assert equality_result is not None, "Equality comparison should return a result"
    assert base_timer_repr is not None, "Base timer repr should not be None"
    assert custom_text_timer_repr is not None, "Custom text timer repr should not be None"

def test_timer_start_and_exit_then_none_start_raises_attribute_error():
    # Setup: Create a Timer with no logger
    NO_LOGGER = None
    timer_instance = timer.Timer(logger=NO_LOGGER)

    # Execution: Start the timer and then stop it via __exit__
    timer_instance.start()
    timer_instance.__exit__()

    # Setup: Simulate a non-Timer object by using None
    plain_dict = {}
    NONE_KEY = None

    # Set a dict entry with None as key and the dict itself as value
    result = plain_dict.__setitem__(NONE_KEY, plain_dict)

    # Verify that the result of __setitem__ has a repr (returns None, repr is 'None')
    repr_result = result.__repr__()
    assert repr_result == 'None'

    # Assert: Calling start() on None raises an AttributeError
    with pytest.raises(AttributeError):
        result.start()

def test_timer_with_context_manager_as_initial_text_and_equality_as_logger():
    """
    Test that a Timer can be created with another Timer instance as initial_text
    and a boolean equality result as logger.
    
    This test verifies:
    1. A Timer can be used as a context manager, which starts and stops the timer.
    2. Timer equality comparison returns a boolean value.
    3. A new Timer can be configured with a Timer instance as initial_text and boolean as logger.
    4. A third Timer can be configured with a name, Timer as initial_text, and boolean as logger,
       and successfully started.
    """
    # Setup: Create and use a timer as context manager to get a timer reference
    base_timer = timer.Timer()
    
    # Execution: Enter context manager, which starts the timer and returns itself
    context_timer = base_timer.__enter__()
    
    # Get a boolean result from equality comparison (used as logger)
    timer_equality_result = base_timer.__eq__(base_timer)
    
    # Exit context manager, which stops the timer
    base_timer.__exit__()
    
    # Create a timer using the context_timer instance as initial_text and bool as logger
    timer_with_timer_as_initial_text = timer.Timer(
        initial_text=context_timer,
        logger=timer_equality_result
    )
    
    # Create a timer with context_timer as name, timer_with_timer_as_initial_text as initial_text,
    # and bool as logger, then start it
    timer_with_name_and_timer_initial_text = timer.Timer(
        context_timer,
        initial_text=timer_with_timer_as_initial_text,
        logger=timer_equality_result
    )
    
    # Assert: Starting the timer should work without raising an error
    timer_with_name_and_timer_initial_text.start()

def test_timer_start_stop_then_context_manager():
    """
    Test that a Timer can be started and stopped normally,
    and then reused as a context manager, which internally
    calls start() again after the timer has been stopped.
    """
    # Constants
    TIMER_NAME = "Timer started"

    # Setup: Create a timer with a specific name
    named_timer = timer.Timer(TIMER_NAME)

    # Execution: Start and stop the timer in normal mode
    named_timer.start()
    elapsed_time = named_timer.stop()

    # Assert: Verify the elapsed time is a valid float after stopping
    assert isinstance(elapsed_time, float)
    assert elapsed_time >= 0

    # Execution: Reuse the same timer as a context manager
    # __enter__ calls start() internally, returning the timer instance
    context_timer = named_timer.__enter__()

    # Assert: The context manager returns the same timer instance
    assert context_timer is named_timer

    # Execution: Create a copy of the timer to verify copy functionality
    timer_copy = named_timer.copy()

    # Assert: The copied timer is a separate instance but equivalent
    assert timer_copy is not named_timer
    assert timer_copy.name == named_timer.name

