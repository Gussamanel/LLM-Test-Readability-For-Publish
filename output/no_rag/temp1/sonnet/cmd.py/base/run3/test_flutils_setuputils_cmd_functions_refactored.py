import pytest
import cmd as cmd_module

def test_build_setup_cfg_command_class_with_none_config():
    # Test that build_setup_cfg_command_class raises an error when
    # passed None instead of a valid SetupCfgCommandConfig object.
    # Since None has no attributes (name, description, commands, camel),
    # accessing them should raise an AttributeError.
    
    # Setup
    invalid_config = None
    
    # Execution & Assertion
    with pytest.raises(AttributeError):
        module_0.build_setup_cfg_command_class(invalid_config)

