import pytest
import headers as headers_module

def test_headers_formatter_object_creation():
    formatter = headers_module.HeadersFormatter()

    assert formatter is not None

