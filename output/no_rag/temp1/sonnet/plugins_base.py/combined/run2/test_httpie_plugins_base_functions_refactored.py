import pytest
import httpie.plugins.base as base_plugin

def test_formatter_plugin_default_instantiation():
    # Test that FormatterPlugin can be instantiated with default parameters
    # without raising any exceptions, verifying basic constructor functionality
    
    # Setup & Execution: Create a default instance of FormatterPlugin
    formatter_plugin_instance = base_plugin.FormatterPlugin()
    
    # Assertion: Verify that the instance was created successfully
    assert formatter_plugin_instance is not None

def test_auth_plugin_get_auth_raises_not_implemented():
    """
    Test that the base AuthPlugin's get_auth method raises NotImplementedError.
    This verifies that the base class enforces subclasses to implement
    the get_auth method, following the template method pattern.
    """
    # Setup
    SAMPLE_PASSWORD = "xzOB\n\n.wP|P-l"
    auth_plugin = base_plugin.AuthPlugin()

    # Execute & Assert
    with pytest.raises(NotImplementedError):
        auth_plugin.get_auth(password=SAMPLE_PASSWORD)

def test_transport_plugin_get_adapter_raises_not_implemented():
    """
    Test that calling get_adapter() on a base TransportPlugin instance
    raises NotImplementedError, as it is an abstract method that must
    be implemented by subclasses.
    """
    # Setup: Create a base TransportPlugin instance
    transport_plugin = base_plugin.TransportPlugin()

    # Execution & Assertion: Verify that get_adapter() raises NotImplementedError
    # since the base class requires subclasses to provide their own implementation
    with pytest.raises(NotImplementedError):
        transport_plugin.get_adapter()

def test_transport_plugin_get_adapter_raises_not_implemented():
    SAMPLE_BYTES = b"\xec\xdb\xe5\\V\xe1\xbb \xfd2\x80z\xf9\x96`-\xa1y"
    converter_plugin = base_plugin.ConverterPlugin(SAMPLE_BYTES)
    transport_plugin = base_plugin.TransportPlugin()

    with pytest.raises(NotImplementedError):
        transport_plugin.get_adapter()

def test_converter_plugin_convert_raises_not_implemented():
    # Test that the base ConverterPlugin raises NotImplementedError when convert() is called,
    # ensuring that subclasses must provide their own implementation of the convert method.

    # Setup
    MIME_TYPE = None
    converter_plugin = base_plugin.ConverterPlugin(MIME_TYPE)

    # Execution & Assertion
    with pytest.raises(NotImplementedError):
        # The base class convert() method should raise NotImplementedError,
        # as it is intended to be overridden by subclasses
        converter_plugin.convert(None)

