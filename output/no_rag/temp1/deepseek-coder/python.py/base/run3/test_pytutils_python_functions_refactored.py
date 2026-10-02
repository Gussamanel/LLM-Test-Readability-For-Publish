import python as py

def test_check_returned_type_info_from_PyInfo_001():
    # Constant definitions
    TYPE_OF_INFO_EXPECTED = "info"

    # Setup
    mock_py_info_0 = Mock()
    mock_py_info_0.get_info.return_value = "info"

    # Execution
    received_info = module_0.PyInfo()

    # Assertion
    assert received_info == TYPE_OF_INFO_EXPECTED, f"Received incorrect type information. Expected {TYPE_OF_INFO_EXPECTED}, but got {received_info}"

