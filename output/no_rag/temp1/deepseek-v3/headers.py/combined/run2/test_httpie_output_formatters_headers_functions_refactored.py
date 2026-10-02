import pytest
import headers as headers_module

def test_create_headers_formatter_instance():
    formatter = headers_module.HeadersFormatter()
    assert isinstance(formatter, headers_module.HeadersFormatter)

