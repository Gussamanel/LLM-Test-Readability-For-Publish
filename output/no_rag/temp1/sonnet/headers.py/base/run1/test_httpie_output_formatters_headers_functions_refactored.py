import pytest
import headers as headers

def test_headers_formatter_instantiation():
    # Test that HeadersFormatter can be successfully instantiated
    # without any arguments and without raising any exceptions

    # Setup & Execution: Create a new instance of HeadersFormatter
    formatter_instance = headers.HeadersFormatter()

    # Assertion: Verify that the instance was created successfully
    assert formatter_instance is not None

