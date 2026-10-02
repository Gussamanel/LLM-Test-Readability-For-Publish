import pytest

import cmd as cmd_module

def test_build_setup_cfg_command_class_raises_attribute_error_on_none_input():
    """Verify build_setup_cfg_command_class raises AttributeError when given None."""
    invalid_setup_cfg = None
    target_module = module_0  # module under test

    with pytest.raises(AttributeError):
        target_module.build_setup_cfg_command_class(invalid_setup_cfg)

