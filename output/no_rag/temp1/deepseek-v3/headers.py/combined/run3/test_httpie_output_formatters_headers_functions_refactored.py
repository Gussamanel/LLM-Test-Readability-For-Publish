import pytest
import headers as headers_module

def test_headers_formatter_default_constructor_initializes_instance():
    # Purpose: Verify that the HeadersFormatter class can be instantiated
    # without raising any errors, confirming the class is available and
    # its constructor works with default arguments.

    # Act
    formatter = headers_module.HeadersFormatter()

    # Assert
    assert formatter is not None
    assert isinstance(formatter, headers_module.HeadersFormatter)

