import pytest
import cmd as cmd_module

def test_build_setup_cfg_command_class_with_none_config():
    # Test that build_setup_cfg_command_class raises an error
    # when provided with None instead of a valid SetupCfgCommandConfig object.
    # This verifies the function's behavior with invalid input.

    # Setup
    invalid_config = None

    # Execution & Assertion
    with pytest.raises((AttributeError, TypeError)):
        # Attempting to access attributes like .name, .description, .commands, .camel
        # on None should raise an AttributeError or TypeError
        module_0.build_setup_cfg_command_class(invalid_config)

