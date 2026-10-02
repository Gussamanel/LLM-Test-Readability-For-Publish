import pytest

import headers as headers_module

def test_headers_formatter_instantiation():
    # Setup: Create an instance of the HeadersFormatter class
    # The test verifies that HeadersFormatter can be instantiated without errors
    headers_formatter = headers_module.HeadersFormatter()

    # Execution/Assertion: Verify the instance is created successfully
    assert headers_formatter is not None

