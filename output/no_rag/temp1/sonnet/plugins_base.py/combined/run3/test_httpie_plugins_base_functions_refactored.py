import pytest
import httpie.plugins.base as base_plugin

def test_formatter_plugin_default_instantiation():
    # Test that FormatterPlugin can be instantiated with default parameters
    # without raising any exceptions, verifying the basic constructor works
    
    # Setup & Execution: Instantiate FormatterPlugin with no arguments
    formatter_plugin_instance = base_plugin.FormatterPlugin()
    
    # Assert: Verify the instance was created successfully
    assert formatter_plugin_instance is not None

def test_auth_plugin_get_auth_raises_not_implemented():
    # Test that the base AuthPlugin's get_auth method raises NotImplementedError,
    # enforcing that subclasses must provide their own implementation.

    # Setup
    DUMMY_PASSWORD = "xzOB\n\n.wP|P-l"
    auth_plugin = base_plugin.AuthPlugin()

    # Execution & Assertion
    # Verify that calling get_auth on the base class raises NotImplementedError,
    # as it is an abstract method meant to be overridden by subclasses.
    with pytest.raises(NotImplementedError):
        auth_plugin.get_auth(password=DUMMY_PASSWORD)

def test_transport_plugin_get_adapter_raises_not_implemented_error():
    # Test that the base TransportPlugin's get_adapter method raises NotImplementedError,
    # enforcing that subclasses must provide their own implementation of this method.

    # Setup: Create a base TransportPlugin instance
    transport_plugin = base_plugin.TransportPlugin()

    # Execution & Assertion: Verify that calling get_adapter raises NotImplementedError,
    # as the base class does not provide a concrete implementation
    with pytest.raises(NotImplementedError):
        transport_plugin.get_adapter()

def test_transport_plugin_get_adapter_raises_not_implemented():
    # Test that TransportPlugin's get_adapter() raises NotImplementedError
    # as it is an abstract method that must be implemented by subclasses

    # Setup: Create a ConverterPlugin instance with some bytes data (not directly used
    # in the assertion but demonstrates plugin initialization context)
    SAMPLE_BYTES = b"\xec\xdb\xe5\\V\xe1\xbb \xfd2\x80z\xf9\x96`-\xa1y"
    converter_plugin = base_plugin.ConverterPlugin(SAMPLE_BYTES)

    # Setup: Create a base TransportPlugin instance
    transport_plugin = base_plugin.TransportPlugin()

    # Execution & Assertion: Verify that calling get_adapter() on the base
    # TransportPlugin raises NotImplementedError, enforcing subclass implementation
    with pytest.raises(NotImplementedError):
        transport_plugin.get_adapter()

def test_converter_plugin_convert_raises_not_implemented():
    # Test that the abstract convert method in ConverterPlugin raises NotImplementedError
    # when called, enforcing that subclasses must provide their own implementation

    # Setup: Create a ConverterPlugin instance with None as the mime type
    MIME_TYPE = None
    BINARY_BODY = None
    converter_plugin = base_plugin.ConverterPlugin(MIME_TYPE)

    # Execution & Assertion: Verify that calling convert raises NotImplementedError
    # as it is an abstract method that must be implemented by subclasses
    with pytest.raises(NotImplementedError):
        converter_plugin.convert(BINARY_BODY)

