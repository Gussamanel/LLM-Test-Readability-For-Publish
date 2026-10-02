import pytest

import headers as headers_module

def test_headers_formatter_instantiation_creates_instance():
    """Verify HeadersFormatter can be constructed and yields the correct type."""
    # Arrange
    EXPECTED_CLASS = headers_module.HeadersFormatter

    # Act
    formatter_instance = EXPECTED_CLASS()

    # Assert
    assert formatter_instance is not None, "HeadersFormatter() returned None instead of an instance"
    assert isinstance(formatter_instance, EXPECTED_CLASS), "Created object is not an instance of HeadersFormatter"

