import pytest
import httpie.plugins.base as plugins_base

def test_formatter_plugin_instantiation_succeeds():
    # Setup: create an instance of the FormatterPlugin base class
    formatter_plugin = plugins_base.FormatterPlugin()

    # Assertion: verify the instance is created successfully
    assert formatter_plugin is not None

def test_auth_plugin_get_auth_with_special_characters_raises_not_implemented_error():
    # Setup: Create an AuthPlugin instance with a password containing special characters and newlines
    SPECIAL_CHARACTERS_PASSWORD = "xzOB\n\n.wP|P-l"
    auth_plugin = plugins_base.AuthPlugin()

    # Execution & Assertion: Verify that the base AuthPlugin's get_auth method raises NotImplementedError
    with pytest.raises(NotImplementedError):
        auth_plugin.get_auth(password=SPECIAL_CHARACTERS_PASSWORD)

def test_abstract_transport_plugin_get_adapter_raises_not_implemented_error():
    transport_plugin = plugins_base.TransportPlugin()

    with pytest.raises(NotImplementedError):
        transport_plugin.get_adapter()

def test_base_transport_plugin_get_adapter_raises_not_implemented_error():
    """
    Test that TransportPlugin.get_adapter raises NotImplementedError.

    The TransportPlugin base class is intended to be subclassed, and its
    get_adapter method must be overridden to return a requests.adapters.BaseAdapter
    instance. Calling the base implementation directly should raise NotImplementedError.
    """
    # Setup: instantiate plugins used in this test
    converter_plugin = plugins_base.ConverterPlugin(CONVERTER_BYTES)
    transport_plugin = plugins_base.TransportPlugin()

    # Execution & Assertion: base get_adapter must signal it is not implemented
    with pytest.raises(NotImplementedError):
        transport_plugin.get_adapter()

def test_abstract_converter_plugin_convert_raises_not_implemented_error():
    # ARRANGE
    # The ConverterPlugin base class is abstract; its convert method should not be
    # implemented, so any attempt to call it is expected to raise NotImplementedError.
    arbitrary_body = None

    # ACT
    converter_plugin = plugins_base.ConverterPlugin(arbitrary_body)
    with pytest.raises(NotImplementedError):
        converter_plugin.convert(arbitrary_body)

    # ASSERT
    # The pytest.raises context manager above asserts that NotImplementedError
    # was raised, confirming the base plugin contract is enforced.

