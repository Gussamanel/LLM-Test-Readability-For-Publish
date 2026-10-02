import pytest

import headers as headers_module

def test_headers_formatter_can_be_instantiated_without_arguments():
    # Purpose:
    # - Sanity test to ensure HeadersFormatter can be constructed with its default parameters
    # - Verifies that construction does not raise and returns an object of the expected type

    # Constants / test configuration
    FORMATTER_CLASS = headers_module.HeadersFormatter

    # --- Setup ---
    # Prepare the class under test (no inputs required for default construction)
    formatter_cls = FORMATTER_CLASS

    # --- Exercise ---
    # Instantiate the formatter to ensure construction succeeds
    formatter_instance = formatter_cls()

    # --- Verify / Assert ---
    # The returned object should be an instance of the HeadersFormatter class
    assert isinstance(formatter_instance, FORMATTER_CLASS), (
        "HeadersFormatter() should return an instance of HeadersFormatter"
    )

