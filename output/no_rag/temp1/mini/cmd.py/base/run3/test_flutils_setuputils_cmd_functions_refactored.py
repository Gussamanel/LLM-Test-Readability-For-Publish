import pytest
import cmd as cmd_module

def test_build_setup_cfg_command_class_raises_attribute_error_for_none_config():
    """
    Verifies build_setup_cfg_command_class expects a valid SetupCfgCommandConfig.
    Passing None should raise AttributeError because the implementation accesses
    attributes like `.name` immediately.
    """
    invalid_setup_cfg = None

    with pytest.raises(AttributeError) as excinfo:
        module_0.build_setup_cfg_command_class(invalid_setup_cfg)

    assert "name" in str(excinfo.value)

