import pytest

import headers as headers_module

def test_headers_formatter_instantiation_creates_instance():
    # Purpose: Verify HeadersFormatter can be instantiated and is of the correct type
    TARGET_CLASS = headers_module.HeadersFormatter

    # Execution
    formatter_instance = TARGET_CLASS()

    # Assertion
    assert isinstance(formatter_instance, TARGET_CLASS), "HeadersFormatter() should return an instance of HeadersFormatter"

