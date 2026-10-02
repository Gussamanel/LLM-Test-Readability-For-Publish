import pytest
import cmd as cmd_module

def test_build_setup_cfg_command_class_with_none_config_raises_attribute_error():
    # Setup: pass None as the setup command config, which lacks required attributes
    setup_command_cfg = None

    # Execution: attempting to build the command class should fail because
    # build_setup_cfg_command_class tries to access attributes on the config
    with pytest.raises(AttributeError):
        cmd_module.build_setup_cfg_command_class(setup_command_cfg)

