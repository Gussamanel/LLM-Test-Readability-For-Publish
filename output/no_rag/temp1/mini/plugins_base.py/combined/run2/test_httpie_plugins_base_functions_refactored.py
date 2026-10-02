import pytest

import httpie.plugins.base as plugins_base

def test_formatter_plugin_can_be_instantiated():
    """
    Purpose:
    - Ensure that FormatterPlugin can be constructed without raising an exception
      and that the created object is an instance of the expected class.

    Actions:
    - Setup: capture the plugin class to construct.
    - Execution: instantiate the plugin.
    - Assertion: verify the instance is not None and is of the correct type.
    """
    # Setup
    PLUGIN_CLASS = plugins_base.FormatterPlugin

    # Execution
    plugin_instance = PLUGIN_CLASS()

    # Assertion
    assert plugin_instance is not None
    assert isinstance(plugin_instance, plugins_base.FormatterPlugin)

def test_auth_plugin_get_auth_raises_not_implemented():
    # Purpose:
    # Ensure the base AuthPlugin.get_auth() method raises NotImplementedError
    # when it has not been overridden by a subclass.

    # Constants
    PASSWORD = "xzOB\n\n.wP|P-l"

    # Setup: instantiate the base AuthPlugin implementation from httpie.plugins.base
    auth_plugin = plugins_base.AuthPlugin()

    # Execution & Assertion:
    # Calling get_auth on the base class (without overriding) should raise NotImplementedError.
    with pytest.raises(NotImplementedError):
        auth_plugin.get_auth(password=PASSWORD)

def test_transport_plugin_get_adapter_raises_not_implemented():
    """Verify that the base TransportPlugin enforces implementation of get_adapter
    by raising NotImplementedError; subclasses must override this method.
    """
    # Expected exception and method under test
    EXPECTED_EXCEPTION = NotImplementedError
    METHOD_NAME = "get_adapter"

    # Setup: create an instance of the base TransportPlugin
    transport_plugin = plugins_base.TransportPlugin()

    # Execution & Assertion: invoking the abstract method should raise the expected exception
    with pytest.raises(EXPECTED_EXCEPTION):
        getattr(transport_plugin, METHOD_NAME)()

def test_converter_instantiation_and_transport_get_adapter_raises_not_implemented():
    # Constant input used to initialize the ConverterPlugin
    SAMPLE_BYTES = b"\xec\xdb\xe5\\V\xe1\xbb \xfd2\x80z\xf9\x96`-\xa1y"

    # Setup: create plugin instances
    converter_plugin = plugins_base.ConverterPlugin(SAMPLE_BYTES)
    transport_plugin = plugins_base.TransportPlugin()

    # Assertion: converter plugin was instantiated correctly
    assert isinstance(converter_plugin, plugins_base.ConverterPlugin)

    # Execution & Assertion: TransportPlugin.get_adapter is abstract and should raise
    # NotImplementedError (it must be implemented by concrete subclasses).
    with pytest.raises(NotImplementedError):
        transport_plugin.get_adapter()

def test_converter_plugin_convert_raises_not_implemented():
    # Purpose:
    # Ensure the base ConverterPlugin.convert method raises NotImplementedError
    # when it has not been overridden by a subclass.
    # Setup: instantiate the base plugin with no application context.
    APP_NONE = None
    BODY_NONE = None

    converter_plugin = plugins_base.ConverterPlugin(APP_NONE)

    # Execution & Assertion: invoking convert on the base class must raise
    # NotImplementedError because it's an abstract method placeholder.
    with pytest.raises(NotImplementedError):
        converter_plugin.convert(BODY_NONE)

