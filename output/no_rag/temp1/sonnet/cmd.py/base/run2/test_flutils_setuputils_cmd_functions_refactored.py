import pytest
import cmd as cmd_module

def test_build_setup_cfg_command_class_with_none_config():
    # Test that build_setup_cfg_command_class raises an error when passed None
    # as the setup_command_cfg argument, since it tries to access attributes
    # like .name, .description, .commands, and .camel on the config object
    
    # Setup
    invalid_config = None
    
    # Execution & Assertion
    with pytest.raises((AttributeError, TypeError)):
        # Passing None should fail when the function tries to access
        # attributes on the config object (e.g., setup_command_cfg.name)
        module_0.build_setup_cfg_command_class(invalid_config)

