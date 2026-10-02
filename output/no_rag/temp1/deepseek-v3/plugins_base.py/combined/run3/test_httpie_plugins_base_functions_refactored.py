import pytest
import httpie.plugins.base as plugins_base

def test_formatter_plugin_instantiation_succeeds():
    formatter_plugin = plugins_base.FormatterPlugin()
    assert formatter_plugin is not None, "FormatterPlugin instance should not be None"

def test_auth_plugin_get_auth_raises_notimplementederror():
    # Purpose: Verify that the base AuthPlugin's get_auth method raises
    # NotImplementedError, ensuring subclasses must override it.

    # Setup
    arbitrary_password = "xzOB\n\n.wP|P-l"
    auth_plugin = plugins_base.AuthPlugin()

    # Execution & Assertion
    with pytest.raises(NotImplementedError):
        auth_plugin.get_auth(password=arbitrary_password)

def test_transport_plugin_get_adapter_raises_not_implemented_error():
    # Setup: instantiate the base TransportPlugin
    transport_plugin = plugins_base.TransportPlugin()

    # Execution and Assertion: calling get_adapter should raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport_plugin.get_adapter()

def test_transport_plugin_get_adapter_raises_error():
    SAMPLE_BYTES = b"\xec\xdb\xe5\\V\xe1\xbb \xfd2\x80z\xf9\x96`-\xa1y"
    converter_plugin = plugins_base.ConverterPlugin(SAMPLE_BYTES)
    transport_plugin = plugins_base.TransportPlugin()

    with pytest.raises(NotImplementedError):
        transport_plugin.get_adapter()

def test_converter_plugin_convert_none_body_raises_not_implemented_error():
    # Setup: create a ConverterPlugin instance with a None argument
    none_body = None
    converter_plugin = plugins_base.ConverterPlugin(none_body)

    # Execution & Assertion: converting a None body should raise NotImplementedError
    # because the base ConverterPlugin.convert method is abstract and not implemented
    with pytest.raises(NotImplementedError):
        converter_plugin.convert(none_body)

