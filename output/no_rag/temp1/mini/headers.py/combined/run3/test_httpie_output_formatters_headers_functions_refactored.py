import pytest

import headers as headers_module

def test_headers_formatter_instantiation_creates_formatter_instance():
    """
    Verify HeadersFormatter can be instantiated and returns an object
    of the expected type.
    """
    # Arrange
    FORMATTER_CLASS = headers_module.HeadersFormatter

    # Act
    formatter_instance = FORMATTER_CLASS()

    # Assert
    assert formatter_instance is not None
    assert isinstance(formatter_instance, FORMATTER_CLASS)

