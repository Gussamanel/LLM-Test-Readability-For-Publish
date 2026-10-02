import pytest

import httpie.plugins.base as plugins_base

def test_formatter_plugin_can_be_instantiated():
    """Verify that FormatterPlugin can be instantiated and is the expected type."""
    # Arrange: define the class under test for clarity
    PLUGIN_CLASS = plugins_base.FormatterPlugin

    # Act: instantiate the plugin
    plugin_instance = PLUGIN_CLASS()

    # Assert: ensure an object of the expected type was created
    assert isinstance(plugin_instance, plugins_base.FormatterPlugin)

def test_get_auth_raises_not_implemented_for_base_auth_plugin():
    """Ensure the base AuthPlugin requires subclasses to implement get_auth by raising NotImplementedError."""
    sample_password = "xzOB\n\n.wP|P-l"
    sample_username = None

    auth_plugin = plugins_base.AuthPlugin()

    with pytest.raises(NotImplementedError):
        auth_plugin.get_auth(username=sample_username, password=sample_password)

def test_transport_plugin_get_adapter_raises_not_implemented():
    # Purpose:
    # Verify that the TransportPlugin base class requires subclasses to implement
    # get_adapter() by raising NotImplementedError when called on the base class.
    #
    # This enforces that concrete transport plugins must provide their own adapter
    # implementation.

    TRANSPORT_PLUGIN_CLASS = module_0.TransportPlugin
    EXPECTED_EXCEPTION = NotImplementedError
    METHOD_NAME = "get_adapter"

    transport_plugin = TRANSPORT_PLUGIN_CLASS()

    assert hasattr(transport_plugin, METHOD_NAME) and callable(getattr(transport_plugin, METHOD_NAME))

    with pytest.raises(EXPECTED_EXCEPTION):
        transport_plugin.get_adapter()

def test_base_transport_plugin_get_adapter_raises_not_implemented():
    # Purpose:
    # Verify that TransportPlugin.get_adapter is an abstract method that
    # raises NotImplementedError when not implemented by a subclass.
    #
    # Setup:
    # Create a ConverterPlugin instance to simulate a realistic plugin environment.
    SAMPLE_PAYLOAD = b"\xec\xdb\xe5\\V\xe1\xbb \xfd2\x80z\xf9\x96`-\xa1y"
    converter_plugin = module_0.ConverterPlugin(SAMPLE_PAYLOAD)
    transport_plugin = module_0.TransportPlugin()

    # Execution & Assertion:
    # Calling get_adapter on the base TransportPlugin should raise NotImplementedError.
    with pytest.raises(NotImplementedError):
        transport_plugin.get_adapter()

def test_converter_plugin_convert_raises_not_implemented_for_none_input():
    # Purpose:
    # Verify that the base ConverterPlugin raises NotImplementedError when its
    # convert method is called (it's intended to be implemented by subclasses).

    # Constants / test data
    PLUGIN_INIT_ARG = None
    INPUT_BODY = None

    # Setup: instantiate the base plugin with a None argument (as in the original test)
    converter_plugin = plugins_base.ConverterPlugin(PLUGIN_INIT_ARG)

    # Execution & Assertion: calling the abstract convert method should raise NotImplementedError
    with pytest.raises(NotImplementedError):
        converter_plugin.convert(INPUT_BODY)

