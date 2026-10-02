import pytest
import codetiming_timer as timer

# Import the module
import module_0

# Setup
timer_error = module_0.TimerError()

# Assertion
# There are no explicit assertions in this test case. 
# However, if the import and object creation are successful, that means the test case passes.

def test_timer_0_start():
    with timer_0() as timer_0:
        timer_0.start()

def test_timer_starts_and_stops_as_context_manager():
    """
    Test the functionality of timer as a context manager.
    """

    # SETUP
    # create the timer instance
    my_timer = Timer()

    # START TIMER
    with Timer(text='Timer: {:.4f} seconds'):
        # EXECUTION
        my_timer.start()  # start the timer
        # here should be put the code you want to measure the timing for
        # here I'll suppose that the execution takes place here

    # ASSERTION
    # check if the timer has been stopped
    assert not my_timer.is_running(), "Timer was supposed to stop upon exiting the context manager"

def test_timer_stop_context_manager_exits():
    # Arrange
    float_arg_0 = FloatArg()  
    timer_error_0 = TimerError()  
    timer_0 = Timer()  

    # Act
    timer_0.__exit__()  

    # Assert
    assert not timer_0.is_running(), "Timer should stop when __exit__ is invoked"

def test_start_timer_inside_context_manager():
    """
    Test the start function of the Timer class inside the context manager.
    The timer should start when the context manager is entered and stop when exited.
    This test also checks if the logger prints the expected text when the timer starts.
    """
    # Constants
    NONE_TYPE = None
    TIMER_INITIAL_TEXT = "Initial text"
    TIMER_NAME = "Timer1"
    
    # Setup
    timer = Timer(logger=NONE_TYPE, initial_text=TIMER_INITIAL_TEXT, name=TIMER_NAME)
    
    # Execution
    with timer: # start the timer
        pass # within this context, the timer should be running
    
    # Assertion
    assert timer._start_time is not None, "Timer did not start"
    assert timer._end_time is not None, "Timer did not stop"
    assert timer._duration is not None, "Timer duration is None"
    
    # Check if logger prints the expected text when the timer starts
    if timer.logger:
        assert timer.logger.call_count == 2, "Logger was not called twice"
        logger_args, _ = timer.logger.call_args_list[0]
        initial_text = "Timer {name} started".format(name=TIMER_NAME)
        assert logger_args == initial_text, "Initial text logged is not as expected"

def test_timer_start_with_initial_text():
    # Start a timer as a context manager
    with module_0.Timer() as timer_0:
        timer_1 = timer_0.__enter__()

    # Start a new timer with initial text
    timer_2 = module_0.Timer(initial_text="-1092")
    timer_2.start()
    
    # Check if the timer is equal to a given value
    is_timer_equal = timer_0.__eq__(-1092)

    # Stop the timer and report the elapsed time
    elapsed_time = timer_1.stop()

    # Start a new timer with starting text and an initial text
    TIMER_STARTED_TEXT = "Timer started"
    timer_3 = module_0.Timer(text=TIMER_STARTED_TEXT, initial_text=is_timer_equal)
    
    # Start the timer with a predefined text
    timer_3.start()

def test_timer_0_start():
    # Constants
    TIME_TO_WAIT = 1  # 1 second

    # Setup: creating a timer with initial text
    with Timer(initial_text='Timer started.') as timer:
        initial_time = timer.__enter__()

        # Execution: Start the timer
        timer.start()

        # Wait for a time TIME_TO_WAIT to elapse for the timer
        time.sleep(TIME_TO_WAIT)

        # Execution: Stop the timer
        elapsed_time = timer.stop()

        # Assertion: check the time elapsed is within the accepted error range of 10 milliseconds
        assert abs(elapsed_time - TIME_TO_WAIT) < 0.01

        # Assertion: check the method __repr__ returns a string
        assert isinstance(timer.__repr__(), str)

        # Assertion: check the timers are not equal
        assert not timer.__eq__(initial_time)

        # Repeating Execution: stop the timer again
        stopped_time = timer.stop()

        # Assertion: check the stop method doesn't throw an error, and returns a float number
        assert isinstance(stopped_time, float)

@pytest.mark.test_timer_start_stop_context_manager
def test_timer_start_stop_context_manager():
    # Create a timer with None logger
    timer = module_0.Timer(logger=None)

    # Start the timer
    timer.start()

    # Create an empty dictionary to store duration values
    duration_dict = {}

    # Stop the timer, this will set the duration in the dictionary
    timer.__exit__(None, None, None)

    # Get the duration from the dictionary
    duration = duration_dict.get(None)

    # Check that the duration retrieved from the dictionary was in fact a duration
    assert isinstance(duration, dict), 'The duration from the dictionary is not a dict'

    # Reset the timer for reuse
    timer.start()

def test_start_timer_as_context_manager():
    with module_0.Timer() as timer_0:
        timer_0_start_time = timer_0._start_time 

    with module_0.Timer(initial_text="Timer {name} started", logger=None) as timer_1:
        timer_1_start_time = timer_1._start_time

    timer_2 = module_0.Timer(timer_1, initial_text="Timer {name} started", logger=None)
    timer_2.start()
    timer_2_start_time = timer_2._start_time

    assert timer_0_start_time is not None and timer_0._end_time is not None
    assert timer_1_start_time is not None and timer_1._end_time is not None
    assert timer_2_start_time is not None
    assert timer_1.initial_text == "Timer {name} started"
    assert timer_2.initial_text == "Timer {name} started"
    assert timer_1.logger is None
    assert timer_2.logger is None

def test_start_timer_inside_context_manager():
    with module_0.Timer() as timer_0:
        timer_0_start_time = timer_0._start_time
        with module_0.Timer() as timer_1:
            timer_1_start_time = timer_1._start_time 
            assert timer_1_start_time is not None

    assert timer_0_start_time is not None and timer_0._end_time is not None

def test_timer_start_with_initial_text():
    with module_0.Timer(initial_text="Timer {name} started") as timer_0:
        assert timer_0.initial_text == "Timer {name} started"

def test_start_stop_timer_with_unique_name():
    """
    Test to ensure that start and stop of a timer works as expected.
    """
    # Constants
    TEST_TIMER_NAME = "Unique Timer"
    TEST_INITIAL_TEXT = "{name} started"

    # Setup: Create a timer with a name and initial text
    timer = codetiming.Timer(TEST_TIMER_NAME, TEST_INITIAL_TEXT)

    # Execution: Start and stop the timer
    timer.start()
    time.sleep(1)  # simulate some processing work
    elapsed_time = timer.stop()

    # Assertion: Check that the elapsed time is accurate
    assert abs(elapsed_time - 1) < 0.1  # give some margin of error due to processing time

    # Additional assertion to check if timer is in a certain state
    assert timer._start_time is None  # checks if the timer has stopped

