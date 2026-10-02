import pytest

import headers as headers_module

def test_headers_formatter_instantiation_without_arguments_returns_instance():
    """
    Ensure HeadersFormatter from headers_module can be instantiated without arguments
    and returns an object of the expected type.
    """
    CLASS_UNDER_TEST = headers_module.HeadersFormatter

    # Instantiate the formatter with no arguments
    formatter_instance = CLASS_UNDER_TEST()

    # Verify the created object is an instance of the expected class
    assert isinstance(formatter_instance, CLASS_UNDER_TEST)

