import pytest
import headers

def test_headers_formatter_can_be_instantiated_without_error():
    # Purpose: Verify that the HeadersFormatter class can be instantiated
    # without raising any errors.

    # Setup / Execution: Create an instance of the HeadersFormatter class.
    formatter = headers.HeadersFormatter()

    # Assertion: Confirm the instance was created successfully.
    assert formatter is not None

