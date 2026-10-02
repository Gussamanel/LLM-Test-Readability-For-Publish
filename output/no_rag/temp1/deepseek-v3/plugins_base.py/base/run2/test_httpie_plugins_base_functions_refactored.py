import pytest
import httpie.plugins.base as plugins_base

def test_formatter_plugin_instantiation_succeeds():
    formatter_plugin = plugins_base.FormatterPlugin()
    assert isinstance(formatter_plugin, plugins_base.FormatterPlugin)

def test_auth_plugin_get_auth_not_implemented_raises_error():
    # Setup: provide credentials passed to the base plugin's get_auth method
    password_with_special_characters = "xzOB\n\n.wP|P-l"
    auth_plugin = plugins_base.AuthPlugin()

    # Execution: call the base AuthPlugin.get_auth, which is expected to be
    # overridden by subclasses and therefore must raise NotImplementedError
    with pytest.raises(NotImplementedError):
        auth_plugin.get_auth(password=password_with_special_characters)

def test_transport_plugin_get_adapter_not_implemented_raises_error():
    # The base TransportPlugin's get_adapter method is abstract and must be
    # implemented by subclasses; calling it on the base class should raise
    # NotImplementedError.

    # Setup: instantiate the base TransportPlugin.
    transport_plugin = plugins_base.TransportPlugin()

    # Execution and Assertion: calling get_adapter() on the abstract base
    # class must raise NotImplementedError.
    with pytest.raises(NotImplementedError):
        transport_plugin.get_adapter()

def test_get_adapter_raises_not_implemented_error_with_bytes_data():
    # Constants
    SAMPLE_BYTES_DATA = b"\xec\xdb\xe5\\V\xe1\xbb \xfd2\x80z\xf9\x96`-\xa1y"
    
    # Setup
    transport_plugin_instance = plugins_base.TransportPlugin()
    
    # Execution and Assertion
    # Verify that the base TransportPlugin's get_adapter method raises
    # NotImplementedError when called with bytes data, as it is meant to be
    # overridden by subclasses.
    with pytest.raises(NotImplementedError):
        transport_plugin_instance.get_adapter(SAMPLE_BYTES_DATA)

def test_converter_plugin_convert_not_implemented_raises_error():
    # Setup: Instantiate ConverterPlugin with a None argument (base plugin's convert method is not implemented).
    plugin = plugins_base.ConverterPlugin(None)

    # Execution & Assertion: convert() on the base ConverterPlugin should raise NotImplementedError.
    with pytest.raises(NotImplementedError):
        plugin.convert(None)

