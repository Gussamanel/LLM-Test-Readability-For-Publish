import pytest
import headers as http_headers

def test_formatter_headers_format():
    # Test if the formatter correctly formats header fields
    # Setup:
    keys = ['Content-Type', 'Authorization']
    values = ['application/json', 'Bearer some_token']
    expected = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer some_token'
    }

    # Execution:
    formatter = module_0.HeadersFormatter()
    actual = formatter.format(keys, values)

    # Assertion:
    assert actual == expected, "Formatted headers are incorrect"

