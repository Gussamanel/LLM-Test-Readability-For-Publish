import pytest
import headers as http_headers

def test_H001_send_headers_with_valid_data():
    """
    Test Case ID: H001

    Purpose: This test case aims to verify that the HeadersFormatter
    is correctly handling a valid data.
    
    Steps:
        1. Create an instance of HeadersFormatter.
        2. Call the format_headers function with valid data.
        3. Assert that the returned headers are correct.
    """

    # CONSTANTS
    VALID_DATA = {"Key1": "Value1", "Key2": "Value2"}
    EXPECTED_HEADERS = http_headers.header_formatter(VALID_DATA)
    
    # SETUP
    headers_formatter = module_0.HeadersFormatter()

    # EXECUTION
    result = headers_formatter.format_headers(VALID_DATA)

    # ASSERTION
    assert result == EXPECTED_HEADERS

