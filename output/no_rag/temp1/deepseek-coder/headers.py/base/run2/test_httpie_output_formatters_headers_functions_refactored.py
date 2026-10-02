import headers as headers

def test_header_formatter_valid_input():
    """
    Test that the HeadersFormatter returns the correct format when given valid input
    """
    ### Setup
    input_headers = ['first_field', 'second_field', 'third_field']  # Define input headers
    expected_result = {'FirstField': 'first_field',  # Define expected result
                       'SecondField': 'second_field', 
                       'ThirdField': 'third_field'}
    
    ### Execution
    result = HeadersFormatter(input_headers)  # Execute the function
    
    ### Assertion
    assert result == expected_result  # Check if the result matches the expected result

