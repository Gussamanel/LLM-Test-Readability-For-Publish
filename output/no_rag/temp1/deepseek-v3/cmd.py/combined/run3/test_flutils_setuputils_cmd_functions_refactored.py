import pytest
import cmd as cmd_module

def test_build_setup_cfg_command_class_with_none_config_raises_attribute_error():
    # Arrange: provide None as the SetupCfgCommandConfig (invalid input)
    setup_cfg_command_config = None

    # Act & Assert: building the class with None should raise an AttributeError
    # since the function accesses attributes like .name and .description on the config
    with pytest.raises(AttributeError):
        cmd_module.build_setup_cfg_command_class(setup_cfg_command_config)

