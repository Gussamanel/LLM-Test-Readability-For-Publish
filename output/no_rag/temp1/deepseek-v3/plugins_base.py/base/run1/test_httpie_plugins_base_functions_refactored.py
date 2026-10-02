import pytest
import httpie.plugins.base as base_plugin

def test_formatter_plugin_can_be_instantiated_without_arguments():
    """
    Test that FormatterPlugin can be instantiated without arguments.

    Purpose: Verifies that the base FormatterPlugin class is instantiable
    directly, ensuring its constructor does not require any parameters.
    """
    # Setup & Execution: instantiate the FormatterPlugin
    plugin = base_plugin.FormatterPlugin()

    # Assertion: verify the plugin was created successfully
    assert plugin is not None

def test_auth_plugin_get_auth_raises_not_implemented_error_when_not_overridden():
    # Setup
    TEST_PASSWORD = "xzOB\n\n.wP|P-l"
    auth_plugin = base_plugin.AuthPlugin()
    
    # Execution and Assertion
    # The base AuthPlugin.get_auth method is abstract and should raise
    # NotImplementedError when called, ensuring subclasses override it.
    with pytest.raises(NotImplementedError):
        auth_plugin.get_auth(password=TEST_PASSWORD)

def test_transport_plugin_get_adapter_raises_not_implemented_error_when_not_overridden():
    # Setup: Create an instance of the abstract base TransportPlugin class.
    # This plugin serves as a base for all transport plugins and its
    # get_adapter method is expected to be overridden by subclasses.
    transport_plugin = base_plugin.TransportPlugin()

    # Execution + Assertion: The base implementation of get_adapter must
    # raise NotImplementedError, signaling that subclasses are required
    # to provide their own adapter implementation.
    with pytest.raises(NotImplementedError):
        transport_plugin.get_adapter()

def test_transport_plugin_get_adapter_raises_not_implemented_error_when_not_overridden():
    # ARRANGE: create a ConverterPlugin with some arbitrary bytes
    # (used only to exercise the constructor, not related to the assertion)
    arbitrary_bytes = b"\xec\xdb\xe5\\V\xe1\xbb \xfd2\x80z\xf9\x96`-\xa1y"
    converter_plugin = module_0.ConverterPlugin(arbitrary_bytes)

    # ARRANGE: create a TransportPlugin whose get_adapter is under test
    transport_plugin = module_0.TransportPlugin()

    # ACT + ASSERT: the base TransportPlugin.get_adapter must not be
    # implemented directly and should raise NotImplementedError, signaling
    # that concrete subclasses are required to provide an adapter.
    with pytest.raises(NotImplementedError):
        transport_plugin.get_adapter()

def test_converter_plugin_handles_none_body_without_error():
    # Constants
    none_body = None

    # Setup
    converter_plugin = base_plugin.ConverterPlugin(none_body)

    # Execution & Assertion
    # Verify that passing None as the body does not raise an unexpected error
    # The base ConverterPlugin is expected to handle/ignore this input gracefully
    converter_plugin.convert(none_body)

