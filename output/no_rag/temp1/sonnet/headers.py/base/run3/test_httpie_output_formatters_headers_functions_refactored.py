import pytest
import headers as headers

def test_headers_formatter_instantiation():
    # Test that HeadersFormatter can be successfully instantiated
    # without raising any exceptions
    
    # Setup & Execution: Create a new instance of HeadersFormatter
    formatter = headers.HeadersFormatter()
    
    # Assertion: Verify the instance was created successfully
    assert formatter is not None

