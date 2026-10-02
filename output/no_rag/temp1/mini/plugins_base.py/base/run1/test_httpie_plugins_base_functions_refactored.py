import pytest

import httpie.plugins.base as plugins_base

def test_formatter_plugin_can_be_instantiated():
    """
    Ensure that the FormatterPlugin class from httpie.plugins.base can be
    constructed using its default constructor without raising an exception.
    """
    # Plugin class under test
    PLUGIN_CLASS = plugins_base.FormatterPlugin

    # --- Execution ---
    plugin_instance = PLUGIN_CLASS()

    # --- Assertion ---
    assert isinstance(plugin_instance, plugins_base.FormatterPlugin)

def test_authplugin_get_auth_with_password_only_returns_auth_object():
    """Ensure AuthPlugin accepts password-only input and returns an auth object."""
    TEST_PASSWORD = "xzOB\n\n.wP|P-l"

    # Instantiate the plugin under test
    auth_plugin = module_0.AuthPlugin()

    # Call get_auth with only a password provided
    auth_result = auth_plugin.get_auth(password=TEST_PASSWORD)

    # The call should not raise and should return a non-None auth object
    assert auth_result is not None

def test_transport_plugin_get_adapter_raises_not_implemented():
    """Base TransportPlugin should require subclasses to override get_adapter."""
    # Arrange
    plugin_cls = module_0.TransportPlugin
    transport_plugin = plugin_cls()

    # Act / Assert: calling the base implementation must raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport_plugin.get_adapter()

def test_transport_plugin_get_adapter_raises_not_implemented_by_default():
    # Purpose:
    # Verify that TransportPlugin.get_adapter() raises NotImplementedError by default.
    # This ensures subclasses are required to implement this method.

    # --- Setup ---
    # Sample bytes used to instantiate a ConverterPlugin (kept to mirror original setup).
    BYTES_PAYLOAD = b"\xec\xdb\xe5\\V\xe1\xbb \xfd2\x80z\xf9\x96`-\xa1y"
    converter_plugin = module_0.ConverterPlugin(BYTES_PAYLOAD)
    transport_plugin = module_0.TransportPlugin()

    # The converter_plugin is intentionally created to ensure that creating other plugin
    # instances does not affect the TransportPlugin behavior.

    # --- Execution & Assertion ---
    # Calling get_adapter on the base TransportPlugin should raise NotImplementedError.
    with pytest.raises(NotImplementedError):
        transport_plugin.get_adapter()

def test_converter_plugin_convert_raises_not_implemented_by_default():
    """Ensure the base ConverterPlugin.convert raises NotImplementedError.

    The base ConverterPlugin is intended to be extended by subclasses. Calling
    convert() on the base implementation should raise NotImplementedError.
    """
    # Arrange
    SAMPLE_BODY = None
    converter_plugin = plugins_base.ConverterPlugin(None)

    # Act & Assert
    with pytest.raises(NotImplementedError):
        converter_plugin.convert(SAMPLE_BODY)

