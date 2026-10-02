import pytest
import httpie.plugins.base as base_plugin

def test_formatter_plugin_instantiation():
    formatter_plugin_instance = base_plugin.FormatterPlugin()
    assert formatter_plugin_instance is not None

def test_auth_plugin_get_auth_raises_not_implemented():
    # Test that the base AuthPlugin raises NotImplementedError when get_auth is called,
    # ensuring subclasses are required to implement this method.
    
    # Setup
    PASSWORD_WITH_SPECIAL_CHARS = "xzOB\n\n.wP|P-l"
    auth_plugin = base_plugin.AuthPlugin()
    
    # Execution & Assertion
    with pytest.raises(NotImplementedError):
        # Calling get_auth on the base AuthPlugin should raise NotImplementedError
        # as it is an abstract method that must be implemented by subclasses
        auth_plugin.get_auth(password=PASSWORD_WITH_SPECIAL_CHARS)

def test_transport_plugin_get_adapter_raises_not_implemented_error():
    # Core purpose: Verify that the base TransportPlugin class raises NotImplementedError
    # when get_adapter() is called, enforcing that subclasses must implement this method

    # Setup: Create an instance of the base TransportPlugin
    transport_plugin = base_plugin.TransportPlugin()

    # Execution & Assertion: Verify that calling get_adapter() raises NotImplementedError
    # as it is an abstract method that must be implemented by subclasses
    with pytest.raises(NotImplementedError):
        transport_plugin.get_adapter()

def test_transport_plugin_base_class_get_adapter_not_implemented():
    # Constants representing test data
    SAMPLE_BYTES = b"\xec\xdb\xe5\\V\xe1\xbb \xfd2\x80z\xf9\x96`-\xa1y"

    # Setup: Create a ConverterPlugin instance with sample bytes
    # and a TransportPlugin instance
    converter_plugin = base_plugin.ConverterPlugin(SAMPLE_BYTES)
    transport_plugin = base_plugin.TransportPlugin()

    # Execution & Assertion: Verify that calling get_adapter() on a base
    # TransportPlugin raises NotImplementedError, as subclasses must implement
    # this method to return a requests.adapters.BaseAdapter instance
    with pytest.raises(NotImplementedError):
        transport_plugin.get_adapter()

def test_converter_plugin_convert_raises_not_implemented():
    """
    Test that the ConverterPlugin's convert method raises NotImplementedError
    when called, as it is an abstract method that must be implemented by subclasses.
    """
    # Setup
    NONE_BODY = None

    # Execution & Assertion
    converter_plugin = base_plugin.ConverterPlugin(NONE_BODY)
    with pytest.raises(NotImplementedError):
        # The base ConverterPlugin.convert() method should raise NotImplementedError
        # since it is meant to be overridden by concrete subclasses
        converter_plugin.convert(NONE_BODY)

