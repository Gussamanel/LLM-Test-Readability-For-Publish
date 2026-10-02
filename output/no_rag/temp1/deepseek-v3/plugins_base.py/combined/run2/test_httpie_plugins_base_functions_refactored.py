import pytest
import httpie.plugins.base as base_plugin

def test_formatter_plugin_instantiation_creates_valid_instance():
    # Setup
    # Instantiate the FormatterPlugin class from the module under test
    plugin_instance = base_plugin.FormatterPlugin()

    # Execution & Assertion
    # Verify that the plugin instance is created successfully
    assert plugin_instance is not None

def test_get_auth_with_password_raises_not_implemented_error():
    # Constant setup: password string to be used for test
    password_input = "xzOB\n\n.wP|P-l"
    
    # Setup: instantiate the base AuthPlugin class
    auth_plugin = base_plugin.AuthPlugin()
    
    # Execution and assertion: calling the abstract get_auth method should raise NotImplementedError
    # This verifies that the base AuthPlugin class enforces its abstract method contract.
    with pytest.raises(NotImplementedError):
        auth_plugin.get_auth(password=password_input)

def test_transport_plugin_get_adapter_raises_not_implemented_error():
    # Setup: instantiate the base TransportPlugin implementation
    transport_plugin = base_plugin.TransportPlugin()

    # Execution & Assertion: calling get_adapter() on the base class
    # should raise NotImplementedError since it must be implemented
    # by concrete subclasses.
    with pytest.raises(NotImplementedError):
        transport_plugin.get_adapter()

def test_transport_plugin_get_adapter_not_implemented_when_invoked():
    # Setup: instantiate the transport plugin that should raise an error
    # when get_adapter is called, since it's an abstract base implementation.
    transport_plugin = base_plugin.TransportPlugin()

    # Execution + Assertion: the base TransportPlugin.get_adapter should
    # raise NotImplementedError, signaling subclasses must override it.
    with pytest.raises(NotImplementedError):
        transport_plugin.get_adapter()

def test_converter_plugin_convert_raises_not_implemented_error_on_base_class():
    # Setup: create a ConverterPlugin instance with a None body
    body = None
    converter_plugin = base_plugin.ConverterPlugin(body)

    # Execution and Assertion: calling convert on the base plugin should raise NotImplementedError
    with pytest.raises(NotImplementedError):
        converter_plugin.convert(body)

