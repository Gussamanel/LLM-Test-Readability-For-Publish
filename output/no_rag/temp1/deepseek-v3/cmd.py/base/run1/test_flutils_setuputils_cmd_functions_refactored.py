import pytest
import cmd as cmd_module

def test_build_setup_cfg_command_class_rejects_none_config():
    # Setup: Passing None as the configuration should be invalid input.
    invalid_setup_command_cfg = None

    # Execution & Assertion: The builder should reject a None config.
    with pytest.raises(AttributeError):
        cmd_module.build_setup_cfg_command_class(invalid_setup_command_cfg)

