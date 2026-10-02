import pytest
import httpie.plugins.base as base_plugin

def test_formatter_plugin_instantiation():
    """
    Test that FormatterPlugin can be successfully instantiated.
    
    This test verifies that the FormatterPlugin base class can be created
    without any arguments and without raising any exceptions.
    """
    # Act: Instantiate the FormatterPlugin base class
    formatter_plugin_instance = base_plugin.FormatterPlugin()

    # Assert: Verify the instance was created successfully
    assert formatter_plugin_instance is not None

def test_auth_plugin_get_auth_raises_not_implemented():
    # Test that the base AuthPlugin's get_auth method raises NotImplementedError
    # This ensures that subclasses are required to implement their own authentication logic
    
    # Setup
    SAMPLE_PASSWORD = "xzOB\n\n.wP|P-l"
    auth_plugin = base_plugin.AuthPlugin()
    
    # Execution & Assertion
    # Verify that calling get_auth on the base class raises NotImplementedError,
    # enforcing that subclasses must provide their own implementation
    with pytest.raises(NotImplementedError):
        auth_plugin.get_auth(password=SAMPLE_PASSWORD)

def test_transport_plugin_get_adapter_raises_not_implemented():
    # Test that the base TransportPlugin's get_adapter method raises NotImplementedError
    # This ensures that subclasses are required to implement their own get_adapter method

    # Setup: Create a base TransportPlugin instance
    transport_plugin = base_plugin.TransportPlugin()

    # Execution & Assertion: Verify that calling get_adapter raises NotImplementedError
    # since it is an abstract method that must be overridden by subclasses
    with pytest.raises(NotImplementedError):
        transport_plugin.get_adapter()

def test_transport_plugin_get_adapter_raises_not_implemented():
    # Test that TransportPlugin.get_adapter() raises NotImplementedError
    # as it is an abstract method that must be implemented by subclasses

    # Setup: Create a TransportPlugin instance
    transport_plugin = base_plugin.TransportPlugin()

    # Execution & Assertion: Verify that calling get_adapter() raises NotImplementedError
    # since TransportPlugin is a base class and get_adapter() must be overridden by subclasses
    with pytest.raises(NotImplementedError):
        transport_plugin.get_adapter()

def test_converter_plugin_convert_raises_not_implemented():
    # Test that the base ConverterPlugin's convert method raises NotImplementedError
    # as it is an abstract method meant to be overridden by subclasses
    
    # Setup
    NONE_MIME_TYPE = None
    NONE_BODY = None
    converter_plugin = base_plugin.ConverterPlugin(NONE_MIME_TYPE)
    
    # Execution & Assertion
    with pytest.raises(NotImplementedError):
        # Calling the base convert method should raise NotImplementedError
        # since it serves as an abstract interface requiring subclass implementation
        converter_plugin.convert(NONE_BODY)

