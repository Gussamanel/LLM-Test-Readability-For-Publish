import pytest

import httpie.plugins.base as plugins_base

def test_formatter_plugin_instantiation_succeeds():
    formatter_plugin = plugins_base.FormatterPlugin()

    assert isinstance(formatter_plugin, plugins_base.FormatterPlugin)

def test_auth_plugin_get_auth_raises_not_implemented_error():
    # This test verifies that the base AuthPlugin's get_auth method,
    # being abstract, raises a NotImplementedError when invoked directly.
    # Setup: instantiate the base plugin and provide a sample password.
    SAMPLE_PASSWORD = "xzOB\n\n.wP|P-l"
    auth_plugin = plugins_base.AuthPlugin()

    # Execution & Assertion: calling get_auth should raise NotImplementedError.
    with pytest.raises(NotImplementedError):
        auth_plugin.get_auth(password=SAMPLE_PASSWORD)

def test_transport_plugin_get_adapter_not_implemented():
    transport_plugin = plugins_base.TransportPlugin()

    with pytest.raises(NotImplementedError):
        transport_plugin.get_adapter()

def test_transport_plugin_get_adapter_unimplemented_error():
    # Setup: create a ConverterPlugin instance with arbitrary bytes and a TransportPlugin instance
    arbitrary_bytes = b"\xec\xdb\xe5\\V\xe1\xbb \xfd2\x80z\xf9\x96`-\xa1y"
    converter_plugin = module_0.ConverterPlugin(arbitrary_bytes)
    transport_plugin = module_0.TransportPlugin()

    # Execution & Assertion: the base TransportPlugin.get_adapter should raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport_plugin.get_adapter()

def test_converter_plugin_convert_with_none_raises_not_implemented_error_base_class():
    # Setup: create a converter plugin with a None argument
    plugin_input = None
    converter_plugin = plugins_base.ConverterPlugin(plugin_input)

    # Execution & Assertion: base ConverterPlugin.convert is abstract and should raise NotImplementedError
    with pytest.raises(NotImplementedError):
        converter_plugin.convert(plugin_input)

