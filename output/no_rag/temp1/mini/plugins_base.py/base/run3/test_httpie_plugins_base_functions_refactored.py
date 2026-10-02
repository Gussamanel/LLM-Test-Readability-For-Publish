import pytest

import httpie.plugins.base as plugins_base

def test_formatter_plugin_can_be_instantiated():
    """Confirm FormatterPlugin from httpie.plugins.base can be constructed and is the correct type."""
    PLUGIN_CLASS = plugins_base.FormatterPlugin

    plugin_instance = PLUGIN_CLASS()

    assert plugin_instance is not None
    assert isinstance(plugin_instance, PLUGIN_CLASS)

def test_base_auth_plugin_get_auth_raises_not_implemented():
    """Verify AuthPlugin base class enforces implementation by raising NotImplementedError."""
    PASSWORD = "xzOB\n\n.wP|P-l"

    base_auth_plugin = plugins_base.AuthPlugin()

    with pytest.raises(NotImplementedError):
        base_auth_plugin.get_auth(password=PASSWORD)

def test_transport_plugin_get_adapter_raises_not_implemented():
    # Purpose:
    # Verify that the base TransportPlugin implementation does not provide a default
    # adapter and therefore calling get_adapter() raises NotImplementedError.
    # This enforces that concrete transport plugins must implement get_adapter().

    # Constants
    EXPECTED_EXCEPTION = NotImplementedError
    TRANSPORT_PLUGIN_CLASS = plugins_base.TransportPlugin

    # Setup: instantiate the base transport plugin
    transport_plugin_instance = TRANSPORT_PLUGIN_CLASS()

    # Execution & Assertion: calling the abstract method should raise the expected exception
    with pytest.raises(EXPECTED_EXCEPTION):
        transport_plugin_instance.get_adapter()

def test_transport_plugin_get_adapter_is_abstract_raises_not_implemented():
    """
    Verify that TransportPlugin.get_adapter raises NotImplementedError.

    Setup:
    - Create a ConverterPlugin initialized with some binary data to simulate
      plugin state initialization.
    - Instantiate a TransportPlugin.

    Execution & Assertion:
    - Calling get_adapter() on the TransportPlugin should raise
      NotImplementedError, since this method is abstract/not implemented.
    """
    # Constants / test data
    SAMPLE_BYTES = b"\xec\xdb\xe5\\V\xe1\xbb \xfd2\x80z\xf9\x96`-\xa1y"
    EXPECTED_EXCEPTION = NotImplementedError

    # Setup: initialize plugins
    converter_plugin = module_0.ConverterPlugin(SAMPLE_BYTES)
    transport_plugin = module_0.TransportPlugin()

    # Execution & Assertion: get_adapter is expected to be unimplemented
    with pytest.raises(EXPECTED_EXCEPTION):
        transport_plugin.get_adapter()

def test_converter_plugin_convert_raises_not_implemented():
    """Verify that calling convert on the base ConverterPlugin raises NotImplementedError."""
    # Arrange
    init_arg = None
    converter_plugin = plugins_base.ConverterPlugin(init_arg)

    # Act & Assert: using None for the body to mirror the original test intent
    binary_body = None
    with pytest.raises(NotImplementedError):
        converter_plugin.convert(binary_body)

