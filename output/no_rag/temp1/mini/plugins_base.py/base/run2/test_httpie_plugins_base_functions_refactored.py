import pytest

import httpie.plugins.base as plugins_base

def test_formatter_plugin_instantiates_successfully():
    """Verify FormatterPlugin can be instantiated and yields the expected type."""
    # Arrange
    PLUGIN_CLASS = plugins_base.FormatterPlugin

    # Act
    plugin_instance = PLUGIN_CLASS()

    # Assert
    assert isinstance(plugin_instance, PLUGIN_CLASS)
    assert plugin_instance is not None

def test_get_auth_raises_not_implemented_for_base_plugin_with_password():
    # Purpose:
    # Verify that calling the base AuthPlugin.get_auth() method
    # raises NotImplementedError when provided with a password.
    # This ensures subclasses must implement get_auth.

    # Constants / Setup
    TEST_PASSWORD = "xzOB\n\n.wP|P-l"
    auth_plugin = plugins_base.AuthPlugin()

    # Execution & Assertion:
    # Calling the base implementation should raise NotImplementedError.
    with pytest.raises(NotImplementedError):
        auth_plugin.get_auth(password=TEST_PASSWORD)

def test_transport_plugin_get_adapter_raises_not_implemented():
    # Purpose:
    # Verify that the abstract TransportPlugin.get_adapter() method
    # raises NotImplementedError by default, signaling that subclasses
    # must implement this method.
    EXPECTED_EXCEPTION = NotImplementedError

    # Setup: instantiate the TransportPlugin from the test module
    transport_plugin_instance = module_0.TransportPlugin()

    # Execution & Assertion: calling get_adapter() should raise NotImplementedError
    with pytest.raises(EXPECTED_EXCEPTION):
        transport_plugin_instance.get_adapter()

def test_base_transport_plugin_get_adapter_raises_not_implemented():
    # Purpose:
    # - Verify that the base TransportPlugin.get_adapter method raises NotImplementedError
    #   (it's intended to be implemented by subclasses).
    # - Also ensure a ConverterPlugin can be instantiated with a bytes input.
    
    # Constants / Setup
    SAMPLE_BYTES = b"\xec\xdb\xe5\\V\xe1\xbb \xfd2\x80z\xf9\x96`-\xa1y"
    converter_plugin = plugins_base.ConverterPlugin(SAMPLE_BYTES)
    transport_plugin = plugins_base.TransportPlugin()
    
    # Sanity check: converter plugin was constructed successfully
    assert isinstance(converter_plugin, plugins_base.ConverterPlugin)
    
    # Execution & Assertion: calling the base implementation should raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport_plugin.get_adapter()

def test_converter_plugin_convert_raises_not_implemented():
    """Verify the base ConverterPlugin.convert method raises NotImplementedError."""
    # Setup
    DUMMY_CONFIG = None  # No configuration needed for the base plugin
    DUMMY_BODY = None    # convert typically expects bytes; base method should raise regardless
    converter_plugin = plugins_base.ConverterPlugin(DUMMY_CONFIG)

    # Execution & Assertion
    with pytest.raises(NotImplementedError):
        converter_plugin.convert(DUMMY_BODY)

