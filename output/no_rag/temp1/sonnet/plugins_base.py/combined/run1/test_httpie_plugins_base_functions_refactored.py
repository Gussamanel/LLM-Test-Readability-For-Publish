import pytest
import httpie.plugins.base as base_plugin

def test_formatter_plugin_default_instantiation():
    # Test that FormatterPlugin can be instantiated with default parameters
    # without raising any exceptions, verifying the basic constructor works
    
    # Setup & Execution: Create a FormatterPlugin instance with no arguments
    formatter_plugin_instance = base_plugin.FormatterPlugin()
    
    # Assert: Verify the instance was created successfully
    assert formatter_plugin_instance is not None

def test_auth_plugin_get_auth_raises_not_implemented():
    """
    Test that the base AuthPlugin's get_auth method raises NotImplementedError.
    This ensures that subclasses are required to implement the get_auth method,
    enforcing the abstract interface contract of the AuthPlugin base class.
    """
    # Setup
    MOCK_PASSWORD = "xzOB\n\n.wP|P-l"
    auth_plugin = base_plugin.AuthPlugin()

    # Execute & Assert
    with pytest.raises(NotImplementedError):
        auth_plugin.get_auth(password=MOCK_PASSWORD)

def test_transport_plugin_get_adapter_raises_not_implemented():
    # Verify that the base TransportPlugin class enforces implementation
    # of get_adapter() in subclasses by raising NotImplementedError

    # Setup: Create a base TransportPlugin instance
    transport_plugin = base_plugin.TransportPlugin()

    # Execution & Assertion: Calling get_adapter() on the base class
    # should raise NotImplementedError, as it must be implemented by subclasses
    with pytest.raises(NotImplementedError):
        transport_plugin.get_adapter()

def test_transport_plugin_get_adapter_raises_not_implemented():
    # Setup: Create a base TransportPlugin instance
    transport_plugin = base_plugin.TransportPlugin()

    # Execution & Assertion: Verify that calling get_adapter() on the base
    # TransportPlugin raises NotImplementedError, enforcing subclass implementation
    with pytest.raises(NotImplementedError):
        transport_plugin.get_adapter()

def test_converter_plugin_convert_raises_not_implemented():
    # Test that the base ConverterPlugin.convert() method raises NotImplementedError,
    # enforcing that subclasses must provide their own implementation of the convert method.

    # Setup
    NONE_MIME_TYPE = None
    NONE_BODY = None
    converter_plugin = base_plugin.ConverterPlugin(NONE_MIME_TYPE)

    # Execution & Assertion
    with pytest.raises(NotImplementedError):
        # Calling the base class convert() should raise NotImplementedError
        # as it is an abstract method that subclasses are required to implement
        converter_plugin.convert(NONE_BODY)

