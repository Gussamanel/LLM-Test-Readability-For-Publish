import pytest
import cmd as cmd_module

def test_build_setup_cfg_command_class_rejects_none_config():
    # Setup: prepare input for the function under test
    invalid_setup_cfg_command_config = None  # Intentionally invalid input to verify error handling

    # Execution and Assertion: ensure the function rejects a None configuration
    with pytest.raises(AttributeError):
        cmd_module.build_setup_cfg_command_class(invalid_setup_cfg_command_config)

