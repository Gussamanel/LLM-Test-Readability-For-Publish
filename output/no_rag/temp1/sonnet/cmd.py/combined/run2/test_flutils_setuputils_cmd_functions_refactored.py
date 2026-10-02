import pytest
import cmd as command_interpreter

def test_build_setup_cfg_command_class_raises_error_when_config_is_none():
    # Test that build_setup_cfg_command_class raises an AttributeError
    # when None is passed as the setup_command_cfg argument,
    # since the function attempts to access attributes (name, description, commands, camel)
    # on the provided config object, which will fail for None.

    # Setup
    invalid_config = None

    # Execution & Assertion
    with pytest.raises(AttributeError):
        module_0.build_setup_cfg_command_class(invalid_config)

