import pytest

import headers as headers_module

def test_headers_formatter_instantiation():
    """
    Ensure HeadersFormatter can be constructed and produces an instance of the class.
    """
    # Arrange: reference the class under test from the imported headers_module
    HeadersFormatter = headers_module.HeadersFormatter

    # Act: instantiate the formatter (will raise if construction fails)
    formatter = HeadersFormatter()

    # Assert: verify the created object is an instance of the expected class
    assert isinstance(formatter, HeadersFormatter)

