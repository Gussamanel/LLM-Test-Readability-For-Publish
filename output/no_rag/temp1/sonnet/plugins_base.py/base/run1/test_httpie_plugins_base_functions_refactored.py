import pytest
import httpie.plugins.base as base_plugin

def test_formatter_plugin_instantiation():
    # Test that FormatterPlugin can be instantiated without any arguments
    # This verifies the basic initialization of the FormatterPlugin class
    
    # Setup & Execution: Create an instance of FormatterPlugin
    formatter_plugin_instance = base_plugin.FormatterPlugin()
    
    # Assertion: Verify the instance was created successfully
    assert formatter_plugin_instance is not None

def test_auth_plugin_get_auth_raises_not_implemented():
    # Test that the base AuthPlugin class raises NotImplementedError
    # when get_auth() is called, enforcing that subclasses must implement this method

    # Setup: Define a password with special characters and create a base AuthPlugin instance
    SPECIAL_CHAR_PASSWORD = "xzOB\n\n.wP|P-l"
    auth_plugin = base_plugin.AuthPlugin()

    # Execution & Assertion: Verify that calling get_auth() on the base class
    # raises NotImplementedError, as it is an abstract method meant to be overridden
    with pytest.raises(NotImplementedError):
        auth_plugin.get_auth(password=SPECIAL_CHAR_PASSWORD)

def test_transport_plugin_get_adapter_raises_not_implemented():
    # Test that the base TransportPlugin's get_adapter method raises NotImplementedError
    # as it is an abstract method that must be implemented by subclasses

    # Setup: Create a base TransportPlugin instance
    transport_plugin = base_plugin.TransportPlugin()

    # Execution & Assertion: Verify that calling get_adapter raises NotImplementedError
    # since the base class does not provide a concrete implementation
    with pytest.raises(NotImplementedError):
        transport_plugin.get_adapter()

def test_transport_plugin_get_adapter_raises_not_implemented():
    # Test that TransportPlugin.get_adapter() raises NotImplementedError,
    # as it is an abstract method that must be implemented by subclasses.

    # Create a TransportPlugin instance to test the abstract method behavior
    transport_plugin = base_plugin.TransportPlugin()

    # Execution & Assertion
    # Verify that calling get_adapter() on the base TransportPlugin raises NotImplementedError,
    # enforcing that subclasses must provide their own implementation.
    with pytest.raises(NotImplementedError):
        transport_plugin.get_adapter()

def test_converter_plugin_convert_raises_not_implemented():
    # Test that the base ConverterPlugin's convert method raises NotImplementedError
    # as it is meant to be overridden by subclasses (abstract method behavior)
    
    # Setup
    NONE_MIME_TYPE = None
    NONE_BODY = None
    converter_plugin = base_plugin.ConverterPlugin(NONE_MIME_TYPE)
    
    # Execution & Assertion
    with pytest.raises(NotImplementedError):
        # The base class convert() should raise NotImplementedError
        # to enforce subclasses to provide their own implementation
        converter_plugin.convert(NONE_BODY)

