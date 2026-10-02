import pytest

import cmd as cmd_module

def test_build_setup_cfg_command_class_raises_attribute_error_for_none_input():
    # Arrange: invalid/missing SetupCfgCommandConfig input
    invalid_setup_cfg = None

    # Act & Assert: calling the builder with None should raise AttributeError
    with pytest.raises(AttributeError):
        cmd_module.build_setup_cfg_command_class(invalid_setup_cfg)

