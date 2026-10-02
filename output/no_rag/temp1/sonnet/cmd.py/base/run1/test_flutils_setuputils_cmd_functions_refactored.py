import pytest
import cmd as cmd_module

def test_build_setup_cfg_command_class_with_none_config():
    # Test that build_setup_cfg_command_class raises an error when
    # provided with None as the setup command configuration,
    # since it attempts to access attributes (name, description, commands, camel)
    # on the None value which should result in an AttributeError.

    # Setup
    invalid_config = None

    # Execution & Assertion
    with pytest.raises(AttributeError):
        module_0.build_setup_cfg_command_class(invalid_config)

