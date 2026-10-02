import pytest
import cmd as cmd_module

def test_build_setup_cfg_command_class_rejects_none_config():
    # Arrange: passing None where a SetupCfgCommandConfig is expected
    invalid_setup_command_cfg = None

    # Act & Assert: verify that passing None raises an error rather than
    # silently producing an invalid command class
    with pytest.raises(AttributeError):
        cmd_module.build_setup_cfg_command_class(invalid_setup_command_cfg)

