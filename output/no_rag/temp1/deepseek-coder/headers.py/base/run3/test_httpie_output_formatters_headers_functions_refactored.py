import headers as module_0

def test_case_default_inputs():
    # Setup
    default_formatter = HeadersFormatter()

    # Execution
    response = default_formatter.execute()

    # Assertion
    assert response == 'default settings'

