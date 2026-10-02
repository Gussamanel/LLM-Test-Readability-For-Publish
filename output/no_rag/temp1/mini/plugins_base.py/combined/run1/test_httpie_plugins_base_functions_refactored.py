import pytest

import httpie.plugins.base as plugins_base

def test_formatter_plugin_can_be_instantiated():
    """Ensure FormatterPlugin from httpie.plugins.base can be constructed and is of the expected type."""
    PLUGIN_CLASS = plugins_base.FormatterPlugin

    plugin_instance = PLUGIN_CLASS()

    assert isinstance(plugin_instance, PLUGIN_CLASS)

def test_authplugin_get_auth_raises_when_called_with_password():
    """Ensure the base AuthPlugin.get_auth() raises NotImplementedError when invoked."""
    PASSWORD = "xzOB\n\n.wP|P-l"

    # instantiate the base plugin
    auth_plugin = plugins_base.AuthPlugin()

    # calling the base implementation must raise NotImplementedError
    with pytest.raises(NotImplementedError):
        auth_plugin.get_auth(password=PASSWORD)

def test_transport_plugin_get_adapter_raises_not_implemented():
    """
    Verify that calling the base TransportPlugin.get_adapter() raises
    NotImplementedError.

    Purpose:
    - The base TransportPlugin defines get_adapter() as an abstract method
      that must be implemented by subclasses. This test ensures the base
      implementation enforces that contract by raising NotImplementedError.
    """
    # Constants
    EXPECTED_EXCEPTION = NotImplementedError

    # Setup: instantiate the base TransportPlugin (the unimplemented base class)
    transport_plugin = plugins_base.TransportPlugin()

    # Execution & Assertion: calling the base implementation should raise
    # NotImplementedError to force subclasses to provide their own adapter.
    with pytest.raises(EXPECTED_EXCEPTION):
        transport_plugin.get_adapter()

def test_transport_plugin_get_adapter_raises_not_implemented_in_base_class():
    """
    Verify that TransportPlugin.get_adapter() is abstract and raises NotImplementedError.

    Setup:
    - Create a ConverterPlugin with sample binary data to reflect typical plugin initialization.
    - Instantiate a TransportPlugin which should provide an abstract get_adapter method.

    Execution & Assertion:
    - Calling TransportPlugin.get_adapter() must raise NotImplementedError, indicating subclasses
      are expected to implement this method.
    """
    # Constants / test data
    SAMPLE_BYTES = b"\xec\xdb\xe5\\V\xe1\xbb \xfd2\x80z\xf9\x96`-\xa1y"
    EXPECTED_EXCEPTION = NotImplementedError

    # Setup
    converter_plugin = module_0.ConverterPlugin(SAMPLE_BYTES)
    transport_plugin = module_0.TransportPlugin()

    # Basic sanity check that the converter was constructed (not the focus of this test)
    assert isinstance(converter_plugin, module_0.ConverterPlugin)

    # Execution & Assertion: get_adapter is not implemented on the base TransportPlugin
    with pytest.raises(EXPECTED_EXCEPTION):
        transport_plugin.get_adapter()

def test_converter_plugin_convert_raises_not_implemented_for_base_class():
    # Purpose:
    # Ensure the abstract base ConverterPlugin.convert method raises NotImplementedError
    # when called on the base class. Subclasses are expected to override this method.
    
    # Constants / test data
    DUMMY_CONSTRUCTOR_ARG = None
    DUMMY_BODY = None

    # Setup: instantiate the base ConverterPlugin with a placeholder argument
    converter_plugin = plugins_base.ConverterPlugin(DUMMY_CONSTRUCTOR_ARG)

    # Execution & Assertion: calling the base implementation should raise NotImplementedError
    with pytest.raises(NotImplementedError):
        converter_plugin.convert(DUMMY_BODY)

