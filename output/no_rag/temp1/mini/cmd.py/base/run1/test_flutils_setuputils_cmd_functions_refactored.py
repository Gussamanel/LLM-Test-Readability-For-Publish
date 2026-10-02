import pytest
import cmd as cmd_module

def test_build_setup_cfg_command_class_raises_with_none_input():
    # Purpose:
    # Verify that build_setup_cfg_command_class raises an AttributeError
    # when given None instead of a valid SetupCfgCommandConfig object.
    # This ensures the function fails fast when required attributes are missing.
    
    # Constant input used for the test
    INVALID_SETUP_CFG = None

    # Setup: prepare the invalid configuration (None)
    setup_cfg = INVALID_SETUP_CFG

    # Execute + Assert: calling the function with None should raise AttributeError
    # because the implementation accesses attributes like `.name` on the input.
    with pytest.raises(AttributeError):
        cmd_module.build_setup_cfg_command_class(setup_cfg)

